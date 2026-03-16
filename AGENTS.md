**Agents**
- This repository now includes an `AGENTS.md` guide for automated coding agents and contributors.

- File: `AGENTS.md`

- Purpose: give agents precise commands to build, lint, test, and follow repository style

Build / Install
- Install project runtime deps: `pip install -r requirements.txt` (see `requirements.txt`).
- Build (docker): see `README.md` — build image under `.docker` then `docker run -e API_TOKEN=$API_TOKEN lichess-docker:v0.1.0 -r Bullet`.

Lint / Formatting / Pre-commit
- Run pre-commit hooks (applies ruff, codespell, etc):
  - `pre-commit install` (one-time) then `pre-commit run -a` to run all hooks locally.
- Ruff (fast linter / formatter):
  - Check: `ruff check .`
  - Auto-fix / format: `ruff format .` or `ruff check --fix .` depending on ruff version.
- Pylint (used in CI):
  - Run full lint similar to CI: `pylint --disable=C0301,E0401 $(git ls-files '*.py')`
  - Lint a single file: `pylint path/to/file.py`.
- Codespell (spelling): `codespell` (configured via `.pre-commit-config.yaml` hook).

Tests
- Run all tests (unittest discovery): `python -m unittest discover -v`.
- Run a single test (unittest):
  - Module + TestCase + method: `python -m unittest test.test_lichess_ascii_tracker.Testing.test_usage`
  - Or run a single file: `python -m unittest test.test_lichess_ascii_tracker -v`.
- Note: this repo uses `unittest` (see `test/test_lichess_ascii_tracker.py`). There is no pytest config by default.

CI / Workflows
- Pylint CI workflow: `.github/workflows/pylint.yml` (runs pylint across multiple Python versions).
- pre-commit CI workflow: `.github/workflows/pre-commit.yml` uses pre-commit/action to run hooks in CI.
- If you need to mirror CI locally, run the same commands in those workflow files.

Repository files of interest
- `lichess_ascii_tracker.py` — main module with `LichessChartGenerator` and `main()` entrypoint.
- `test/test_lichess_ascii_tracker.py` — simple unittest tests.
- `.pre-commit-config.yaml` — pre-commit hooks (ruff, codespell, pre-commit-hooks).
- `.github/workflows/pylint.yml` — CI lint job which uses `pylint`.

Coding / Style Guidelines (for agents)
- Formatting
  - Prefer automated formatting with `ruff format .` (pre-commit already runs formatting hooks). If the project enables Black in future, follow `pyproject.toml` settings.
  - Aim for an 88-character soft line length. CI currently disables the pylint `line-too-long` check but keep lines readable.

- Imports
  - Order imports in three groups with a blank line between them:
    1. Standard library (e.g., `argparse`, `os`, `datetime`)
    2. Third-party (e.g., `berserk`, `asciichartpy`)
    3. Local / project imports
  - Use absolute imports. Avoid relative imports unless inside a package where relative imports are clearer.
  - Keep `from X import Y` for specific symbols; otherwise `import X` and reference `X.Y`.

- Typing and Signatures
  - Use type hints for public functions and methods where feasible. Example:
    - `def get_ratings_from_lichess(self) -> tuple:` can be improved to `-> tuple[str, list[int]]` where appropriate.
  - Keep signatures small and prefer explicit parameter names rather than `*args/**kwargs` unless necessary.

- Naming Conventions
  - Modules / files: `snake_case.py` (already used: `lichess_ascii_tracker.py`).
  - Classes: `PascalCase` / `CamelCase` (e.g., `LichessChartGenerator`).
  - Functions & methods: `snake_case` (e.g., `get_ratings_from_lichess`).
  - Constants: `UPPER_SNAKE` (e.g., `HSIZE = 60`).
  - Private members: single leading underscore `_private`.

- Docstrings / Comments
  - Use triple double-quote docstrings for modules, classes, functions.
  - Docstrings should be short and show parameter and return expectations. Use the style already present in the code.
  - Keep comments focused and avoid commenting obvious code. Use comments to explain non-obvious intent.

- Error Handling / Exceptions
  - Prefer raising specific built-in exceptions (ValueError, TypeError, KeyError, IndexError) with helpful messages.
  - When catching exceptions, avoid bare `except:`. Catch specific exceptions (e.g., `except KeyError as e:`).
  - Preserve original exception context when appropriate using `raise ... from err`.
  - Do not swallow exceptions silently; log or re-raise with context.

- Logging
  - Use the `logging` module for messages intended for operators or debug output instead of `print()` for non-CLI library code.
  - Keep `print()` only for CLI output that is the primary program output (the current `print_to_markdown` prints the ASCII chart — acceptable there).

- CLI / Output
  - Keep CLI parsing simple and explicit (`argparse` is used). Validate required args early.
  - Exit with non-zero status for unrecoverable errors. Use `sys.exit(1)` in `main()` wrappers if needed.

- Tests
  - Tests live under `test/`; prefer `unittest` style for new tests to match current suite, or add pytest later and update this document.
  - Keep tests deterministic (avoid network calls). For code that calls Lichess API, prefer mocking `berserk.Client` methods.

Cursor / Copilot rules
- I searched for repository-level Cursor rules and Copilot instructions and found none in these paths:
  - `.cursor/rules/` — not present
  - `.cursorrules` — not present
  - `.github/copilot-instructions.md` — not present
- If you add Cursor rules, place them in `.cursor/rules/` and mention them here; agents should respect those rules.

Small implementation notes (from scanning current code)
- The main module is `lichess_ascii_tracker.py` and expects `API_TOKEN` environment variable; constructors raise on missing token.
- Networking/API calls go through `berserk.Client`; for test runs or CI, mock `berserk.Client` to avoid real API calls.
- The test suite currently invokes `usage()` from `lichess_ascii_tracker` — update tests to cover generator methods and error paths.

If something's missing
- If you need me to also add a `pyproject.toml` or configure `ruff` / `pylint` settings explicitly, tell me which linter/formatter you prefer and I will add configuration files.
- If you want tests migrated to `pytest`, pick this option and I will convert tests and add a `pytest.ini`.

History
- Created by an automated agent to provide runnable commands, style guidance and references to project CI hooks.
