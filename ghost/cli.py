import argparse, os, sys
from ghost.cache import compute_cache_key, get_cached_explanation, store_cached_explanation
from ghost.config import get_project_root, load_config, save_config
from ghost.danger_rules import check_command_danger
from ghost.error_classifier import classify_error
from ghost.model_client import check_server_health, query_local_model
from ghost.rule_explanations import get_rule_explanation
from ghost.sound_player import find_system_player, play_sound_event

CG = "[1;35m"
CF = "[1;32m"
CW = "[1;31m"
CR = "[0m"
CD = "[2m"

def handle_check(args):
    d, reason = check_command_danger(args.command)
    if not d: return 0
    play_sound_event("dangerous_command")
    print(f"{CW}👻 GHOST SHELL GUARDIAN: DANGEROUS COMMAND INTERCEPTED!{CR}")
    print(f"{CW}──────────────────────────────────────────────────────────{CR}")
    print(f"{CD}Target:{CR} {args.command}")
    print(f"{CD}Peril:{CR}  {reason}")
    print(f"{CW}──────────────────────────────────────────────────────────{CR}")
    try:
        if os.path.exists("/dev/tty"):
            with open("/dev/tty", "r") as t:
                sys.stderr.write(f"Type '{CF}yes{CR}' to continue, or anything else to cancel: ")
                sys.stderr.flush()
                resp = t.readline().strip()
        else:
            resp = input(f"Type '{CF}yes{CR}' to continue, or anything else to cancel: ").strip()
    except Exception:
        print("Command cancelled.")
        return 1
    if resp.lower() == "yes":
        print(f"{CD}Proceeding at your own risk...{CR}")
        return 0
    print(f"{CG}Command prevented. The spirits have preserved your files.{CR}")
    return 1

def handle_explain(args):
    cat, _ = classify_error(args.exit_code, args.stderr or "", args.command or "")
    play_sound_event(cat)
    k = compute_cache_key(args.command or "", args.stderr or "", cat)
    cached = get_cached_explanation(k)
    if cached:
        spooky, fix = cached
    else:
        res = get_rule_explanation(cat, args.stderr or "", args.command or "")
        if res:
            spooky, fix = res
        else:
            llm = query_local_model(args.command or "", args.stderr or "")
            if llm: spooky, fix = llm
            else:
                spooky = "A cold chill fills the terminal... an unknown phantom caused this failure."
                fix = f"Fix: Inspect command '{args.command}' or check logs for details."
        store_cached_explanation(k, spooky, fix)
    print(f"{CG}👻 {spooky}{CR}")
    print(f"{CF}{fix}{CR}")
    return 0

def handle_play(args): play_sound_event(args.event); return 0
def handle_mute(args):
    c = load_config(); c["sound_enabled"] = False; save_config(c); print("Sounds muted."); return 0
def handle_unmute(args):
    c = load_config(); c["sound_enabled"] = True; save_config(c); print("Sounds enabled."); return 0

def handle_status(args):
    c = load_config()
    p = find_system_player()
    online = check_server_health()
    mf = os.path.exists(os.path.join(get_project_root(), "models", c.get("model_file", "")))
    h = os.path.expanduser("~")
    brc = os.path.exists(os.path.join(h, ".bashrc")) and "ghost.bash" in open(os.path.join(h, ".bashrc"), errors="ignore").read()
    zrc = os.path.exists(os.path.join(h, ".zshrc")) and "ghost.zsh" in open(os.path.join(h, ".zshrc"), errors="ignore").read()
    print(f"{CG}=== Ghost Shell Status ==={CR}")
    print(f"Sounds: {'Enabled' if c.get('sound_enabled') else 'Muted'} (Player: {' '.join(p) if p else 'None - silent'})")
    print(f"Model Server: {'Online' if online else 'Offline (rules active)'}")
    print(f"Model File: {'Present' if mf else 'Not downloaded yet (optional)'}")
    print(f"Hook ~/.bashrc: {'Installed' if brc else 'Not installed'}")
    print(f"Hook ~/.zshrc:  {'Installed' if zrc else 'Not installed'}")
    return 0

def main():
    p = argparse.ArgumentParser(prog="ghost")
    s = p.add_subparsers(dest="subcommand")
    p1 = s.add_parser("check-command"); p1.add_argument("command"); p1.set_defaults(func=handle_check)
    p2 = s.add_parser("explain-error")
    p2.add_argument("--exit-code", type=int, required=True); p2.add_argument("--command", default=""); p2.add_argument("--stderr", default="")
    p2.set_defaults(func=handle_explain)
    p3 = s.add_parser("play-sound"); p3.add_argument("event"); p3.set_defaults(func=handle_play)
    p4 = s.add_parser("mute"); p4.set_defaults(func=handle_mute)
    p5 = s.add_parser("unmute"); p5.set_defaults(func=handle_unmute)
    p6 = s.add_parser("status"); p6.set_defaults(func=handle_status)
    args = p.parse_args()
    return args.func(args) if args.subcommand else p.print_help() or 0

if __name__ == "__main__":
    sys.exit(main())
