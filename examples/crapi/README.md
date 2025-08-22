
# AuthScope x OWASP crAPI (Demo Guide)

This example shows how to run AuthScope against the **OWASP crAPI** intentionally-vulnerable API to surface **BOLA/BFLA**.

> We do NOT redistribute crAPI here. Please use the official repository/images.

## Steps

1) **Run crAPI** (see official instructions):
   - Clone crAPI and start via Docker:
     ```bash
     git clone https://github.com/OWASP/crAPI.git
     cd crAPI
     docker compose up -d
     ```

2) **Create two users** (e.g., Alice and Bob) via the web UI or REST API and obtain their **JWTs**.
   - You can use browser DevTools (Network tab) to copy the `Authorization: Bearer <JWT>` after login.

3) **Capture HAR** from real traffic:
   - With DevTools → Network → Preserve log → interact with a few profile/vehicle endpoints → Save all as HAR.
   - Save it as `examples/crapi/traffic.har` in this repo.

4) **Edit `examples/crapi/config.yaml`**:
   - Paste the two JWTs into the `subjects` section.
   - Adjust `invariants.when.path` to match real crAPI endpoints observed in the HAR (examples provided).

5) **Run AuthScope**:
   ```bash
   authscope run      --base http://localhost:8888      --openapi examples/crapi/openapi-minimal.yaml      --config examples/crapi/config.yaml      --har examples/crapi/traffic.har      --out out
   ```

6) **Review findings**:
   - See `out/report.html` and `out/findings.json`.

## Example Invariants (edit paths to match your crAPI)
```yaml
invariants:
  - name: "User can only read own profile"
    when: { method: GET, path: "/identity/api/v2/user/{id}" }
    allow_if: "subject.claims.sub == path.id or 'admin' in subject.claims.roles"

  - name: "User can only read own vehicles"
    when: { method: GET, path: "/community/api/v2/user/{id}/vehicles" }
    allow_if: "subject.claims.sub == path.id or 'admin' in subject.claims.roles"
```
> If your crAPI version exposes different paths, replace them using endpoints seen in your HAR.

## Notes
- Start with **GET-only** (default) for safe probing.
- Use **HAR** to enrich scenarios even if OpenAPI is incomplete.
- For CI, keep a copy of the config & HAR and compare snapshots across releases (planned command).
