from pydantic import BaseModel, Field
from pathlib import Path
from typing import Any
import json, time, hashlib

def _now(): return time.time()

def _fp(v):
    raw = json.dumps(v, ensure_ascii=False, sort_keys=True, default=str)
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

class MemoryItem(BaseModel):
    key: str
    value: Any
    score: float = 1.0
    fp: str
    updated_at: float = Field(default_factory=_now)

class MemoryStore:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.db = {}
        if self.path.exists():
            self.db = json.loads(self.path.read_text())

    def save(self):
        self.path.write_text(json.dumps(self.db, indent=2, ensure_ascii=False))

    def get(self, key, default=None):
        return self.db.get(key, {}).get("value", default)

    def put(self, key, value, score=1.0):
        self.db[key] = {
            "key": key,
            "value": value,
            "score": score,
            "fp": _fp(value),
            "updated_at": _now(),
        }
        self.save()

    def delete(self, key):
        if key in self.db:
            del self.db[key]
            self.save()

    def keys(self):
        return sorted(self.db.keys())
