
from __future__ import annotations
import json, re
from urllib.parse import urlparse
from typing import List, Dict, Any
from authscope.core.models import Scenario

ID_RE = re.compile(r"""
    (?:^|/)
    (?:                                    # heuristics for ids
        [0-9]{2,}                          # numbers 2+ digits
        |[a-fA-F0-9]{16,}                  # hex-like (long)
        |[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}  # uuid
    )
    (?:/|$)
""", re.VERBOSE)

def normalize_path(path: str) -> str:
    # Replace likely ID segments with {id}
    parts = path.split("/")
    norm = []
    for seg in parts:
        if not seg:
            norm.append("")
            continue
        if re.fullmatch(r"[0-9]{2,}", seg) or re.fullmatch(r"[a-fA-F0-9]{16,}", seg) or re.fullmatch(r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}", seg):
            norm.append("{id}")
        else:
            norm.append(seg)
    return "/".join(norm) if norm and norm[0] == "" else "/" + "/".join(norm)

def load_har(path: str, only_get: bool = True) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        har = json.load(f)
    entries = har.get("log", {}).get("entries", [])
    seen = set()
    endpoints: List[Dict[str, Any]] = []
    for e in entries:
        req = e.get("request", {})
        method = req.get("method", "GET").upper()
        if only_get and method != "GET":
            continue
        url = req.get("url", "")
        parsed = urlparse(url)
        pth = parsed.path or "/"
        norm = normalize_path(pth)
        key = (method, norm)
        if key in seen:
            continue
        seen.add(key)
        endpoints.append({"method": method, "path": norm})
    return endpoints

def make_scenarios_from_har(endpoints: List[Dict[str, Any]]) -> List[Scenario]:
    scenarios: List[Scenario] = []
    for ep in endpoints:
        path = ep["path"]
        if "{id}" in path:
            scenarios.append(Scenario(method=ep["method"], path=path, path_params={"id": "SELF"}))
            scenarios.append(Scenario(method=ep["method"], path=path, path_params={"id": "OTHER"}))
        else:
            scenarios.append(Scenario(method=ep["method"], path=path, path_params={}))
    return scenarios
