
# Contributing to AuthScope

Thanks for considering a contribution!

## Setup
- Python 3.10+
- `python -m venv .venv && . .venv/bin/activate`
- `pip install -e . -r requirements.txt`

## Dev loop
- `pytest -q`
- `uvicorn examples.mock_api.server:app --port 8000`
- `authscope run --base http://127.0.0.1:8000 --openapi examples/mock_api/openapi.yaml --config examples/mock_api/config.yaml --out out`

## Coding standards
- Keep MVP simple; prefer composition over deep inheritance.
- No network-aggressive defaults. Default is **GET-only**.
- Keep DSL **safe**. If you add operators to the evaluator, update tests.

## Pull Requests
- Open an issue first for significant changes (design/feature).
- Include tests for new behavior.
- Update README and CHANGELOG.

## Release checklist (maintainers)
- Bump version in `pyproject.toml`
- Update CHANGELOG
- Tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
- Create GitHub Release and attach screenshots/release notes
