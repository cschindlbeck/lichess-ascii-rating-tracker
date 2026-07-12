# Auto-merge Pre-commit Hook Update PRs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a GitHub Actions workflow that automatically squash-merges the `pre-commit-autoupdate.yml`-generated PR once all of this repo's CI workflows report success, without any human review step.

**Architecture:** One new workflow file, `.github/workflows/auto-merge-precommit.yml`, triggered by `workflow_run` completion of the five existing pull-request-triggered CI workflows. A single job resolves the associated PR, checks it's from the trusted bot/branch/file-scope, confirms every non-self workflow run against that commit succeeded, then runs `gh pr merge --squash`. No new application code or dependencies — this is pure CI/CD configuration (YAML + embedded bash + `gh`/`jq`).

**Tech Stack:** GitHub Actions (`workflow_run` trigger), GitHub CLI (`gh`), `jq`, bash. No branch protection changes.

## Global Constraints

- Workflow name field values it depends on (must match exactly): `pre-commit`, `Pylint`, `Build and test docker`, `Dependency review`, `Build README` (from `.github/workflows/pre-commit.yml`, `pylint.yml`, `docker-image.yml`, `dependency-review.yml`, `build-readme.yml`).
- Trusted PR author login: `app/github-actions` (verified against real merged PR #67).
- Trusted head branch: `update/pre-commit-autoupdate` (hardcoded in `pre-commit-autoupdate.yml`).
- Allowed changed-file scope: `.pre-commit-config.yaml`, `README.md` only.
- Merge method: squash, `--delete-branch=false` (matches repo settings: `allow_squash_merge=true`, `allow_merge_commit=false`, `delete_branch_on_merge=false`).
- Must not wait on the default CodeQL code-scanning dynamic workflow (explicitly out of scope per design).
- No test framework exists for this repo's GitHub Actions workflows (only `test/test_lichess_ascii_tracker.py` for the Python app) — validation for this plan is: YAML lint, shellcheck on embedded scripts, and a local dry-run of the jq/bash decision logic against real, previously captured API response shapes. Do not invent a new workflow-testing framework for this one file (YAGNI).

---

### Task 1: Create the auto-merge workflow file

**Files:**
- Create: `.github/workflows/auto-merge-precommit.yml`

**Interfaces:**
- Produces: the complete workflow (trigger + guard + CI-check + merge steps) described below. No other task depends on intermediate exports — this is a single self-contained file.

- [ ] **Step 1: Write the workflow file**

```yaml
---
name: "Auto-merge pre-commit hook updates"

on:
  workflow_run:
    workflows:
      ["pre-commit", "Pylint", "Build and test docker", "Dependency review", "Build README"]
    types: [completed]

permissions:
  contents: write
  pull-requests: write
  actions: read

jobs:
  auto-merge:
    runs-on: ubuntu-latest
    if: >
      github.event.workflow_run.event == 'pull_request' &&
      github.event.workflow_run.conclusion == 'success'
    steps:
      - name: "Resolve pull request for this workflow run"
        id: pr
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          PR_NUMBER=$(gh api "repos/${{ github.repository }}/actions/runs/${{ github.event.workflow_run.id }}" \
            --jq '.pull_requests[0].number // empty')

          if [ -z "$PR_NUMBER" ]; then
            echo "No associated pull request for this workflow run. Skipping."
            echo "proceed=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          echo "Resolved pull request #$PR_NUMBER"
          echo "number=$PR_NUMBER" >> "$GITHUB_OUTPUT"
          echo "proceed=true" >> "$GITHUB_OUTPUT"

      - name: "Verify trusted actor, branch, and file scope"
        id: guard
        if: steps.pr.outputs.proceed == 'true'
        env:
          GH_TOKEN: ${{ github.token }}
          PR: ${{ steps.pr.outputs.number }}
        run: |
          set -euo pipefail

          AUTHOR_LOGIN=$(gh pr view "$PR" --json author --jq '.author.login')
          HEAD_REF=$(gh pr view "$PR" --json headRefName --jq '.headRefName')

          if [ "$AUTHOR_LOGIN" != "app/github-actions" ]; then
            echo "PR #$PR author '$AUTHOR_LOGIN' is not the trusted autoupdate bot. Skipping."
            echo "proceed=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          if [ "$HEAD_REF" != "update/pre-commit-autoupdate" ]; then
            echo "PR #$PR branch '$HEAD_REF' does not match the expected autoupdate branch. Skipping."
            echo "proceed=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          ALLOWED_FILES=".pre-commit-config.yaml
          README.md"
          OUT_OF_SCOPE=false
          while IFS= read -r f; do
            [ -z "$f" ] && continue
            if ! grep -qxF "$f" <<< "$ALLOWED_FILES"; then
              echo "PR #$PR changes file '$f', which is outside the allowed scope. Skipping."
              OUT_OF_SCOPE=true
            fi
          done < <(gh pr view "$PR" --json files --jq '.files[].path')

          if [ "$OUT_OF_SCOPE" = true ]; then
            echo "proceed=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          echo "PR #$PR passed actor/branch/file-scope checks."
          echo "proceed=true" >> "$GITHUB_OUTPUT"

      - name: "Confirm every other CI check for this commit succeeded"
        id: checks
        if: steps.guard.outputs.proceed == 'true'
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail

          SHA="${{ github.event.workflow_run.head_sha }}"
          SELF_PATH=".github/workflows/auto-merge-precommit.yml"

          RUNS=$(gh api "repos/${{ github.repository }}/actions/runs?head_sha=$SHA&per_page=100" \
            --jq "[.workflow_runs[] | select(.path != \"$SELF_PATH\")]")

          INCOMPLETE=$(echo "$RUNS" | jq '[.[] | select(.status != "completed")] | length')
          FAILED=$(echo "$RUNS" | jq '[.[] | select(.conclusion != "success" and .conclusion != "skipped" and .conclusion != null)] | length')

          if [ "$INCOMPLETE" != "0" ]; then
            echo "$INCOMPLETE other check(s) for commit $SHA still in progress. Skipping for now."
            echo "ready=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          if [ "$FAILED" != "0" ]; then
            echo "$FAILED check(s) for commit $SHA did not succeed. Will not merge."
            echo "ready=false" >> "$GITHUB_OUTPUT"
            exit 0
          fi

          echo "All CI checks for commit $SHA succeeded."
          echo "ready=true" >> "$GITHUB_OUTPUT"

      - name: "Merge pull request"
        if: steps.checks.outputs.ready == 'true'
        env:
          GH_TOKEN: ${{ github.token }}
          PR: ${{ steps.pr.outputs.number }}
        run: |
          set -euo pipefail
          echo "All checks green for PR #$PR — squash-merging."
          gh pr merge "$PR" --squash --delete-branch=false
```

- [ ] **Step 2: Commit**

```bash
git add .github/workflows/auto-merge-precommit.yml
git commit -m "Add workflow to auto-merge pre-commit hook update PRs"
```

---

### Task 2: Lint the workflow (YAML + embedded shell)

**Files:**
- Read only: `.github/workflows/auto-merge-precommit.yml`

**Interfaces:**
- Consumes: the file created in Task 1.
- Produces: nothing new — this task only verifies Task 1's output. No later task depends on artifacts from this task.

- [ ] **Step 1: Run yamllint against the new file**

Run: `yamllint .github/workflows/auto-merge-precommit.yml`
Expected: no output (clean), OR only pre-existing style warnings consistent with this repo's other workflow files (check by comparing against `yamllint .github/workflows/pre-commit.yml` output for the same warning types). Fix any real errors (bad indentation, duplicate keys, etc.) before proceeding.

- [ ] **Step 2: Extract and shellcheck each embedded `run:` block**

There's no existing extraction tooling in this repo, so do it manually for the 4 `run:` blocks in the new file:

```bash
mkdir -p /private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/shellcheck
```

For each of the 4 `run:` blocks (resolve-pr, guard, checks, merge), copy its shell body into its own file under that directory (e.g. `resolve-pr.sh`, `guard.sh`, `checks.sh`, `merge.sh`), prefixed with `#!/usr/bin/env bash` and using `PR`, `GH_TOKEN`, `SHA` etc. as already-exported env vars (add `export PR=1` style stubs at the top only for the shellcheck pass, so shellcheck doesn't flag "undefined variable" — remove those stub lines before shellcheck, or use `# shellcheck disable=SC2154` if simpler). Then run:

```bash
shellcheck /private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/shellcheck/*.sh
```

Expected: no warnings above `info` level. Fix any real issues (unquoted variables, etc.) directly in `.github/workflows/auto-merge-precommit.yml`, then re-run Step 1 and this step until both are clean.

- [ ] **Step 3: Commit any lint fixes (skip if nothing changed)**

```bash
git add .github/workflows/auto-merge-precommit.yml
git commit -m "Fix lint issues in auto-merge workflow"
```

If Step 1 and Step 2 produced no fixes, skip this step entirely (no empty commits).

---

### Task 3: Dry-run the guard and CI-check logic against real API shapes

**Files:**
- Create (scratch only, not committed): `/private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/dry-run.sh`

**Interfaces:**
- Consumes: the exact jq filters and comparisons written in Task 1's `guard` and `checks` steps — copy them verbatim so a passing dry run means the real workflow step will behave the same way.
- Produces: confidence that the logic's happy path and each rejection path behave as intended, using real data already gathered during design (PR #67's author/branch/files, and a live `actions/runs?head_sha=` response shape). Nothing here is consumed by later tasks.

This workflow can't be executed end-to-end locally (it depends on live `workflow_run` events), so this task validates the decision logic itself against real captured JSON instead of trusting it un-tested.

- [ ] **Step 1: Capture real fixture JSON**

```bash
mkdir -p /private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/fixtures
cd /private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/fixtures

gh pr view 67 --repo cschindlbeck/lichess-ascii-rating-tracker \
  --json author,headRefName,files > pr-good.json

gh api "repos/cschindlbeck/lichess-ascii-rating-tracker/actions/runs?per_page=15" \
  --jq '[.workflow_runs[] | select(.head_branch == "issue-65" and .event == "pull_request")]' \
  > runs-all-success.json
```

Expected: `pr-good.json` contains `author.login == "app/github-actions"`, `headRefName == "update/pre-commit-autoupdate"`... **wait, this is PR #67 (already merged, real autoupdate PR)** — its `headRefName` really is `update/pre-commit-autoupdate` and its single file really is `.pre-commit-config.yaml`. `runs-all-success.json` contains the 4 CI runs captured for the `issue-65` branch (all `conclusion: "success"`), used as a stand-in "all green" fixture — rename its `.path` values won't matter since the dry-run script filters generically.

- [ ] **Step 2: Write the dry-run harness**

```bash
cat > /private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/dry-run.sh <<'SCRIPT'
#!/usr/bin/env bash
set -euo pipefail
FIXTURES="$(dirname "$0")/fixtures"

echo "=== Case 1: trusted PR, in-scope files (expect proceed=true) ==="
AUTHOR_LOGIN=$(jq -r '.author.login' "$FIXTURES/pr-good.json")
HEAD_REF=$(jq -r '.headRefName' "$FIXTURES/pr-good.json")
[ "$AUTHOR_LOGIN" = "app/github-actions" ] && echo "author OK" || echo "author FAIL: $AUTHOR_LOGIN"
[ "$HEAD_REF" = "update/pre-commit-autoupdate" ] && echo "branch OK" || echo "branch FAIL: $HEAD_REF"

ALLOWED_FILES=".pre-commit-config.yaml
README.md"
OUT_OF_SCOPE=false
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if ! grep -qxF "$f" <<< "$ALLOWED_FILES"; then
    echo "file '$f' out of scope"
    OUT_OF_SCOPE=true
  fi
done < <(jq -r '.files[].path' "$FIXTURES/pr-good.json")
[ "$OUT_OF_SCOPE" = false ] && echo "file scope OK"

echo
echo "=== Case 2: wrong author (expect author FAIL) ==="
echo '{"author":{"login":"someone-else"}}' | jq -r '.author.login' | \
  { read -r a; [ "$a" != "app/github-actions" ] && echo "correctly rejected: $a"; }

echo
echo "=== Case 3: disallowed file present (expect out-of-scope detection) ==="
echo '{"files":[{"path":".pre-commit-config.yaml"},{"path":"lichess_ascii_tracker.py"}]}' > /tmp/pr-bad-files.json
OUT_OF_SCOPE=false
while IFS= read -r f; do
  [ -z "$f" ] && continue
  if ! grep -qxF "$f" <<< "$ALLOWED_FILES"; then
    echo "correctly flagged out-of-scope file: '$f'"
    OUT_OF_SCOPE=true
  fi
done < <(jq -r '.files[].path' /tmp/pr-bad-files.json)
[ "$OUT_OF_SCOPE" = true ] && echo "file scope rejection OK"
rm -f /tmp/pr-bad-files.json

echo
echo "=== Case 4: all CI runs succeeded (expect ready=true) ==="
SELF_PATH=".github/workflows/auto-merge-precommit.yml"
RUNS=$(jq "[.[] | select(.path != \"$SELF_PATH\")]" "$FIXTURES/runs-all-success.json")
INCOMPLETE=$(echo "$RUNS" | jq '[.[] | select(.status != "completed")] | length')
FAILED=$(echo "$RUNS" | jq '[.[] | select(.conclusion != "success" and .conclusion != "skipped" and .conclusion != null)] | length')
echo "incomplete=$INCOMPLETE failed=$FAILED"
[ "$INCOMPLETE" = "0" ] && [ "$FAILED" = "0" ] && echo "ready=true (correct)"

echo
echo "=== Case 5: one CI run still in progress (expect ready=false) ==="
RUNS_PENDING=$(echo "$RUNS" | jq '.[0].status = "in_progress"')
INCOMPLETE2=$(echo "$RUNS_PENDING" | jq '[.[] | select(.status != "completed")] | length')
[ "$INCOMPLETE2" != "0" ] && echo "correctly detected incomplete: $INCOMPLETE2 (ready=false, correct)"

echo
echo "=== Case 6: one CI run failed (expect ready=false) ==="
RUNS_FAILED=$(echo "$RUNS" | jq '.[0].conclusion = "failure"')
FAILED2=$(echo "$RUNS_FAILED" | jq '[.[] | select(.conclusion != "success" and .conclusion != "skipped" and .conclusion != null)] | length')
[ "$FAILED2" != "0" ] && echo "correctly detected failure: $FAILED2 (ready=false, correct)"
SCRIPT
chmod +x /private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/dry-run.sh
```

- [ ] **Step 3: Run the dry-run harness**

Run: `/private/tmp/claude-502/-Users-chris-schindlbeck-repos-lichess-ascii-rating-tracker/e7eae8f3-c6e5-4cdb-9c7d-fb73b32e18ce/scratchpad/dry-run.sh`

Expected output includes, in order: `author OK`, `branch OK`, `file scope OK`, a line showing the wrong-author case was correctly rejected, a line showing the disallowed-file case was correctly flagged, `ready=true (correct)`, a line showing the in-progress case was correctly detected, and a line showing the failure case was correctly detected. If any expected line is missing, the corresponding logic in `.github/workflows/auto-merge-precommit.yml` has a bug — fix it there (not just in the scratch script) and re-run.

- [ ] **Step 4: No commit needed**

This task only produces scratch validation artifacts outside the repo. If Step 3 required a fix to `.github/workflows/auto-merge-precommit.yml`, commit that fix:

```bash
git add .github/workflows/auto-merge-precommit.yml
git commit -m "Fix auto-merge guard logic found during dry-run validation"
```

Skip this step if no fix was needed.

---

### Task 4: Open the pull request for this change

**Files:**
- None (git/GitHub operations only)

**Interfaces:**
- Consumes: the committed workflow file from Tasks 1-3.
- Produces: an open PR against `master` for human/automated review — this workflow file itself is exempt from its own automation (its author will be a human/this session, not `app/github-actions`, and its branch won't be `update/pre-commit-autoupdate`), so it requires normal manual review and merge.

- [ ] **Step 1: Push the current branch**

Run: `git push -u origin HEAD`
Expected: branch pushed successfully.

- [ ] **Step 2: Open the PR**

```bash
gh pr create --repo cschindlbeck/lichess-ascii-rating-tracker \
  --base master \
  --title "Automate approval and merge of pre-commit hook update PRs" \
  --body "Resolves #65

Adds \`.github/workflows/auto-merge-precommit.yml\`, which squash-merges the \`pre-commit-autoupdate.yml\`-generated PR automatically once all CI checks for its commit succeed. Skips the formal approval step (GitHub blocks self-approval for the bot identity that opens the PR) and merges directly via \`gh pr merge\` instead. Guards: PR author must be \`app/github-actions\`, head branch must be \`update/pre-commit-autoupdate\`, and changed files must be limited to \`.pre-commit-config.yaml\`/\`README.md\`.

See \`docs/superpowers/specs/2026-07-12-auto-merge-precommit-updates-design.md\` for the full design."
```

Expected: PR created; report the URL back.
