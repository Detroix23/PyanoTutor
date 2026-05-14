# PYANO_TUTOR — agent instructions

## Quick start

Prepare the project to be run (if error, stop and ask user).
**Do not use any other commands to build, compile the project.**
**Never install the dependencies by yourself**
```sh
source .venv3-13/bin/activate
pip install --editable .
```


Run the project (if error, stop and ask user).
```
python src/pyano
```

## Commands

| Task | Command |
|------|---------|
| Typecheck | `mypy src/` (strict mode via pyproject.toml) |
| Install editable | `pip install -e .` |
| Run package | `python -m pyano` |

## Architecture

- **Package**: `pyano` — lives under `src/` (setuptools `find` with `where = ["src"]`)
- **Entrypoint**: `src/pyano/__init__.py` (currently a stub)
- **State**: v0.0.1 — no tests, lint, or formatter configured yet
- **Dependencies**: none declared; add to `[project] dependencies` in `pyproject.toml`
- **Python**: >=3.11 (venv is `.venv3-13/`)
- **Build**: setuptools with `build-backend = "setuptools.build_meta"`

## Conventions

- Always activate `.venv3-13/` before running commands
- Add new packages to `src/pyano/` following the existing namespace
- Extend `pyproject.toml` for new tool config rather than standalone config files

## Gotchas

- No tests exist yet — do not assume a test runner or fixture pattern
- `.gitignore` excludes all `.venv*` (including `.venv3-13/`) and standard Python artifacts
