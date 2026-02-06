from pydantic import BaseModel
from pathlib import Path
import json

DEFAULT_PATH = Path.home() / ".nanopybot" / "config.json"

class ProviderCfg(BaseModel):
    api_key: str | None = None
    base_url: str = "https://api.openai.com/v1"
    model: str = "gpt-4.1-mini"

class AppCfg(BaseModel):
    provider: ProviderCfg = ProviderCfg()
    memory_path: str = str(Path.home() / ".nanopybot" / "memory.json")
    scheduler_db: str = str(Path.home() / ".nanopybot" / "jobs.sqlite")

def load_config() -> AppCfg:
    # 1. Check current directory first for local development
    local_path = Path("config.json")
    if local_path.exists():
        return AppCfg(**json.loads(local_path.read_text(encoding="utf-8")))

    # 2. Fallback to home directory
    if not DEFAULT_PATH.exists():
        DEFAULT_PATH.parent.mkdir(parents=True, exist_ok=True)
        cfg = AppCfg()
        DEFAULT_PATH.write_text(cfg.model_dump_json(indent=2), encoding="utf-8")
        return cfg
    
    return AppCfg(**json.loads(DEFAULT_PATH.read_text(encoding="utf-8")))