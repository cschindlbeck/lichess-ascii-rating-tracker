# Auto-approve/merge pre-commit hook update PRs

Resolves: https://github.com/cschindlbeck/lichess-ascii-rating-tracker/issues/65

## Problem

`pre-commit-autoupdate.yml` opens a PR (branch `update/pre-commit-autoupdate`) whenever
`pre-commit autoupdate` finds newer hook versions. These PRs are low-risk version bumps but
currently require a human to notice, review, and merge them, adding maintenance overhead.

## Goal

A new workflow automatically merges these PRs once CI is green, without weakening branch
protection or merging anything outside the expected scope.

## Key constraint: no self-approval

GitHub rejects a review submitted by the same identity that opened the PR
("Can not approve your own pull request"). Since the PR is opened with the default
`GITHUB_TOKEN` (as `github-actions[bot]`), an approval step using the same token would fail.

**Decision:** skip the formal "approve" review entirely. Go straight to verifying CI and
merging directly via `gh pr merge`. Merging a PR is not subject to the self-review
restriction, so `GITHUB_TOKEN` can do it.

## Design

### New workflow: `.github/workflows/auto-merge-precommit.yml`

**Trigger:**

```yaml
on:
  workflow_run:
    workflows: ["pre-commit", "Pylint", "Build and test docker", "Dependency review", "Build README"]
    types: [completed]
```

These are the exact `name:` values of this repo's five pull-request-triggered CI workflows.
The job only runs when `github.event.workflow_run.event == 'pull_request'` and
`github.event.workflow_run.conclusion == 'success'` — a failing run in any of them causes the
job to no-op that time (a later trigger, or none, will pick it up).

Because five different workflows can each independently complete and re-fire this trigger,
the job re-evaluates "is everything green yet?" from scratch every time (see CI-complete
check below) rather than assuming the triggering run means everything is done.

### Step 1 — Resolve the associated PR

`workflow_run.pull_requests[0].number` is only populated for same-repo PRs (not forks) — true
here, since `pre-commit-autoupdate.yml` runs in this repo directly. If empty, skip: this
workflow_run wasn't for a PR we care about (e.g. it ran on a direct push to `master`).

### Step 2 — Trusted-actor / scope guard

Using `gh pr view <PR> --json author,headRefName,files`, require **all** of:

- `author.login == "app/github-actions"` (confirmed empirically against merged PR #67 —
  this is how `gh` renders the GitHub Actions bot identity for PRs opened via the default
  `GITHUB_TOKEN`)
- `headRefName == "update/pre-commit-autoupdate"` (hardcoded branch name in
  `pre-commit-autoupdate.yml`)
- every changed file path is in the allow-list `{.pre-commit-config.yaml, README.md}`

README.md is allowed because `build-readme.yml` runs on every `pull_request` (including this
one) and pushes an "Updated README" commit whenever the generated ratings content differs —
which is common, since it embeds live rating data. Without allowing it, most autoupdate PRs
would never qualify for automation. Any other changed file blocks automation.

Any guard failure exits the job quietly (no merge, no error) — a genuinely-scoped PR is
expected to always pass these checks; failing here just means "not our PR to touch."

### Step 3 — CI-complete check

Query `GET /repos/{owner}/{repo}/actions/runs?head_sha={sha}` for **every** workflow run
against the PR's head commit, excluding this workflow's own path
(`.github/workflows/auto-merge-precommit.yml`) to avoid waiting on itself. Require:

- zero runs with `status != completed` (otherwise: still in progress, no-op and rely on a
  later trigger)
- zero runs with `conclusion` other than `success`/`skipped` (otherwise: something failed,
  never merge)

Excluding only this workflow's own path — rather than hardcoding the five expected names —
means any other CI later added to the repo is automatically covered too.

**Explicitly out of scope:** the repository's default CodeQL code-scanning setup (a
GitHub-managed "dynamic" workflow, not a file under `.github/workflows/`) is not included in
this check, per explicit decision during design.

### Step 4 — Merge

```sh
gh pr merge "$PR" --squash --delete-branch=false
```

- Squash merge, matching how recent PRs (#67, #64, #62, #61) were merged and matching repo
  settings (`allow_squash_merge: true`, `allow_merge_commit: false`).
- `--delete-branch=false`, matching the repo setting `delete_branch_on_merge: false` — the
  autoupdate workflow reuses the same branch name (`update/pre-commit-autoupdate`) next run,
  so the branch should remain for `peter-evans/create-pull-request` to reuse/recreate.

### Permissions

```yaml
permissions:
  contents: write
  pull-requests: write
  actions: read
```

### Logging

Every guard/check outcome (skip reason, or "all checks green, merging") is written via
`echo` to the step output so the decision trail is visible in the Actions run log, satisfying
the auditability acceptance criterion.

## Out of scope

- Configuring branch protection rules on `master` (none exist today; not requested by the
  issue, and this design doesn't depend on any).
- Provisioning a separate bot account/PAT for formal PR approval.
- Including CodeQL's default code-scanning check in the merge gate.
