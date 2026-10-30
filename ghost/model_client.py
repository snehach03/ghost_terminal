import json, urllib.request
from ghost.config import load_config

def query_local_model(cmd, err):
    cfg = load_config()
    url = f"{cfg.get('server_url', 'http://127.0.0.1:8080').rstrip('/')}/v1/chat/completions"
    payload = {
        "model": cfg.get("model_name", "qwen2.5-0.5b-instruct"),
        "messages": [
            {"role": "system", "content": "You are Ghost Shell, a spooky assistant. Answer in EXACTLY 2 lines:Line 1: A brief spooky observation.Line 2: Fix: <clear plain-English actionable instructions>."},
            {"role": "user", "content": f"Command: {cmd}Error: {err[:400]}"}
        ],
        "max_tokens": int(cfg.get("max_tokens", 120)),
        "temperature": 0.3
    }
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode(), headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=float(cfg.get("request_timeout_seconds", 5.0))) as res:
            if res.status == 200:
                body = json.loads(res.read().decode())
                txt = body["choices"][0]["message"]["content"].strip()
                lines = [l.strip() for l in txt.splitlines() if l.strip()]
                if len(lines) >= 2:
                    fix = lines[1] if lines[1].startswith("Fix:") else f"Fix: {lines[1]}"
                    return lines[0], fix
    except Exception: pass
    return None

def check_server_health():
    url = f"{load_config().get('server_url', 'http://127.0.0.1:8080').rstrip('/')}/v1/models"
    try:
        with urllib.request.urlopen(urllib.request.Request(url), timeout=1.5) as r:
            return r.status in (200, 404)
    except Exception: return False
