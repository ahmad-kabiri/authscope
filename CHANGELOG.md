
# Changelog

## [0.1.0] - 2025-08-22
### Added
- CLI `authscope run` with OpenAPI-driven scenario generation (SELF/OTHER).
- Config DSL for subjects & authorization invariants.
- Async runner using httpx.
- HTML/JSON reporters.
- Mock vulnerable API (FastAPI) for BOLA demo.
- HAR enrichment (MVP): `--har traffic.har` to add endpoints from real traffic.
- GitHub Actions CI with tests and artifact upload.
- Unit tests for scenario generation and safe evaluator.
- CONTRIBUTING, Code of Conduct, License.

### Security
- Safe expression evaluator (AST allowlist).

### Notes
- Default is **GET-only** for safety.
- Snapshot/compare and GraphQL support are planned.
