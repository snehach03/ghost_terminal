import json, os
from typing import Any, Dict

DEFAULT_CONFIG: Dict[str, Any] = {
    "server_url": "http://127.0.0.1:8080",
    "model_name": "qwen2.5-0.5b-instruct",
    "model_file": "qwen2.5-0.5b-instruct-q4_k_m.gguf",
    "sound_enabled": True,
    "request_timeout_seconds": 5.0,
    "max_tokens": 120,
    "cache_file": ".ghost_cache.json",
}

def get_project_root() -> str:
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def get_config_path() -> str:
    root = get_project_root()
    active = os.path.join(root, "config.json")
    return active if os.path.exists(active) else os.path.join(root, "config.example.json")

def load_config() -> Dict[str, Any]:
    cfg = dict(DEFAULT_CONFIG)
    p = get_config_path()
    if os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                cfg.update(json.load(f))
        except Exception: pass
    return cfg

def save_config(cfg: Dict[str, Any]) -> bool:
    try:
        with open(os.path.join(get_project_root(), "config.json"), "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2)
        return True
    except Exception: return False
