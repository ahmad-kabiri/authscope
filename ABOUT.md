
## About (for GitHub)

**One-liner:**  
AuthScope is a Python-powered authorization invariants tester for Web & API that systematically surfaces BOLA/BFLA and catches auth drift in CI.

**Short description:**  
AuthScope models *who should access what* and verifies those rules against your API in minutes. It generates cross-subject scenarios (SELF vs OTHER) from OpenAPI and real traffic (HAR), runs them asynchronously, and flags unexpected 2xx responses where access should be denied. Use it locally during pentests or wire it into CI to prevent authorization regressions before release.

**Highlights:**
- Ownership & tenant isolation checks as code (simple YAML DSL).
- OpenAPI + HAR-driven scenario generation.
- Cross-subject diffs for the exact same request.
- HTML/JSON reports; CI-friendly and safe-by-default (GET first).
- Designed to demonstrate BOLA/BFLA quickly on real systems like OWASP crAPI.
