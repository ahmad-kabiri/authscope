
from __future__ import annotations
from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional, Literal

class Subject(BaseModel):
    name: str
    token: str
    claims: Dict[str, Any] = Field(default_factory=dict)

class WhenClause(BaseModel):
    method: Literal["GET","POST","PUT","PATCH","DELETE"]
    path: str

class Invariant(BaseModel):
    name: str
    when: WhenClause
    allow_if: str

class Scenario(BaseModel):
    method: str
    path: str
    path_params: Dict[str, str] = Field(default_factory=dict)
    params: Dict[str, Any] = Field(default_factory=dict)
    json: Optional[Any] = None

class ResponseStub(BaseModel):
    status: int
    headers: Dict[str, str] = Field(default_factory=dict)
    body: str = ""

class Finding(BaseModel):
    invariant: str
    path: str
    method: str
    subject: str
    evidence: ResponseStub
