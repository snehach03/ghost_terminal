import os, shutil, subprocess, sys
from ghost.config import get_project_root, load_config

SOUND_MAPPING = {
    "command_not_found": "door_creak.wav",
    "permission_denied": "chains.wav",
    "syntax_error": "wail.wav",
    "not_found": "footsteps.wav",
    "dangerous_command": "bell.wav",
    "relief": "chime.wav",
    "generic_error": "moan.wav",
}

def find_system_player():
    if sys.platform == "darwin" and shutil.which("afplay"): return ["afplay"]
    if sys.platform.startswith("linux") or "bsd" in sys.platform:
        for p in ["paplay", "aplay"]:
            if shutil.which(p): return [p]
    if sys.platform in ("win32", "cygwin"): return ["powershell", "-c"]
    if os.path.exists("/proc/version"):
        try:
            if "microsoft" in open("/proc/version").read().lower() and shutil.which("powershell.exe"):
                return ["powershell.exe", "-c"]
        except Exception: pass
    return []

def play_sound_event(event):
    cfg = load_config()
    if not cfg.get("sound_enabled", True): return
    wav = os.path.join(get_project_root(), "sounds", SOUND_MAPPING.get(event, "moan.wav"))
    if not os.path.exists(wav): return
    player = find_system_player()
    if not player: return
    try:
        if "powershell" in player[0].lower():
            cmd = player + [f"(New-Object Media.SoundPlayer '{wav}').PlaySync()"]
        else:
            cmd = player + [wav]
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception: pass
