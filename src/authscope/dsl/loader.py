
from __future__ import annotations
import yaml
from typing import List
from pydantic import BaseModel
from authscope.core.models import Subject, Invariant

class Config(BaseModel):
    subjects: List[Subject]
    invariants: List[Invariant]

def load_config(path: str) -> Config:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return Config(**data)
