
from __future__ import annotations
import re, yaml
from typing import List, Dict, Any
from authscope.core.models import Scenario

VAR_CANDIDATES = {"id","userId","accountId","ownerId","orgId","tenant","tenantId"}

def load_openapi(path: str, only_get: bool = True) -> List[Dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        doc = yaml.safe_load(f)
    paths = doc.get("paths", {})
    endpoints = []
    for p, item in paths.items():
        for method, op in item.items():
            if method.startswith("x-"):
                continue
            if only_get and method.upper() != "GET":
                continue
            endpoints.append({"method": method.upper(), "path": p})
    return endpoints

def guess_path_vars(path: str) -> List[str]:
    return re.findall(r"{([^}]+)}", path)

def make_scenarios(endpoints: List[Dict[str, Any]]) -> List[Scenario]:
    scenarios: List[Scenario] = []
    for ep in endpoints:
        vars_ = guess_path_vars(ep["path"])
        if not vars_:
            scenarios.append(Scenario(method=ep["method"], path=ep["path"], path_params={}))
            continue
        if any(v in VAR_CANDIDATES for v in vars_):
            scenarios.append(Scenario(method=ep["method"], path=ep["path"], path_params={v: "SELF" for v in vars_}))
            scenarios.append(Scenario(method=ep["method"], path=ep["path"], path_params={v: "OTHER" for v in vars_}))
        else:
            scenarios.append(Scenario(method=ep["method"], path=ep["path"], path_params={v: "SELF" for v in vars_}))
    return scenarios
