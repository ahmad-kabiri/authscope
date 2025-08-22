
from __future__ import annotations
import httpx
from typing import List, Dict
from urllib.parse import urljoin
from authscope.core.models import Subject, Scenario, Invariant, Finding, ResponseStub
from authscope.core.safe_eval import safe_eval

def render_path(path: str, path_params: Dict[str, str], sub: Subject, others: List[Subject]) -> str:
    final = path
    for k, v in (path_params or {}).items():
        if v == "SELF":
            cand = sub.claims.get(k) or sub.claims.get("sub") or sub.claims.get("id") or "1"
        elif v == "OTHER":
            other = next((o for o in others if o.name != sub.name), None)
            cand = (other.claims.get(k) if other else None) or (other.claims.get("sub") if other else None) or "999"
        else:
            cand = v
        final = final.replace("{%s}" % k, str(cand))
    return final

async def fire(client, base: str, sub: Subject, sc: Scenario, subjects: List[Subject]):
    headers = {"Authorization": f"Bearer {sub.token}"}
    others = [o for o in subjects if o.name != sub.name]
    url = urljoin(base, render_path(sc.path, sc.path_params, sub, others))
    r = await client.request(sc.method, url, headers=headers, params=sc.params, json=sc.json)
    body = await r.aread()
    try:
        body_txt = body.decode("utf-8", errors="replace")[:8192]
    except Exception:
        body_txt = ""
    return ResponseStub(status=r.status_code, headers=dict(r.headers), body=body_txt)

async def run(base: str, subjects: List[Subject], scenarios: List[Scenario], invariants: List[Invariant]):
    findings: List[Finding] = []
    async with httpx.AsyncClient(timeout=15.0, verify=False) as client:
        for sc in scenarios:
            results: Dict[str, ResponseStub] = {}
            for sub in subjects:
                res = await fire(client, base, sub, sc, subjects)
                results[sub.name] = res
            for inv in invariants:
                if inv.when.path == sc.path and inv.when.method.upper() == sc.method.upper():
                    for sub in subjects:
                        ctx = { "subject": sub, "path": sc.path_params, "resp": results[sub.name] }
                        try:
                            allowed = safe_eval(inv.allow_if, ctx)
                        except Exception:
                            allowed = True
                        resp = results[sub.name]
                        if not allowed and resp.status in (200, 201, 204):
                            findings.append(Finding(
                                invariant=inv.name,
                                path=sc.path,
                                method=sc.method,
                                subject=sub.name,
                                evidence=resp,
                            ))
    return findings
