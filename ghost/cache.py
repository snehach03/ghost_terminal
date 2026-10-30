import hashlib, json, os
from ghost.config import get_project_root, load_config

def get_cache_path():
    cfg = load_config()
    return os.path.join(get_project_root(), cfg.get("cache_file", ".ghost_cache.json"))

def compute_cache_key(cmd, err, cat):
    raw = f"{cat}:{cmd.strip()}:{err.strip()}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]

def get_cached_explanation(key):
    p = get_cache_path()
    if os.path.exists(p):
        try:
            d = json.load(open(p))
            if key in d: return d[key].get("spooky"), d[key].get("fix")
        except Exception: pass
    return None

def store_cached_explanation(key, spooky, fix):
    p = get_cache_path()
    d = {}
    if os.path.exists(p):
        try: d = json.load(open(p))
        except Exception: d = {}
    d[key] = {"spooky": spooky, "fix": fix}
    try: json.dump(d, open(p, "w"), indent=2)
    except Exception: pass
