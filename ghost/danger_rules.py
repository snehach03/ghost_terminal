import re, shlex
from typing import Optional, Tuple

def is_fork_bomb(cmd: str):
    c = re.sub(r"\s+", "", cmd)
    return (":(){:|:&};:" in c or ":(){:|:&};" in c), "A fork bomb spawns processes recursively until exhaustion."

def is_dangerous_rm(toks):
    if not toks or toks[0] != "rm": return False, None
    r, f, tgts = False, False, []
    for t in toks[1:]:
        if t.startswith("-") and t != "--":
            fl = t.lstrip("-")
            if "r" in fl or "R" in fl or t == "--recursive": r = True
            if "f" in fl or t == "--force": f = True
        else: tgts.append(t)
    if not (r and f): return False, None
    crit = {"/", "~", ".", "*", "..", "/*", "~/*"}
    prefixes = ("/etc", "/usr", "/var", "/boot", "/bin", "/sbin", "/lib")
    for tg in tgts:
        norm = tg.strip()
        if norm in crit or norm.startswith("$HOME"):
            return True, f"Destructive deletion 'rm -rf {norm}' will wipe critical files/directories."
        for p in prefixes:
            if norm == p or norm.startswith(p + "/"):
                return True, f"Destructive deletion targeting '{norm}' will corrupt OS components."
    return False, None

def is_dangerous_git_reset(toks):
    if len(toks) >= 2 and toks[0] == "git" and toks[1] == "reset" and "--hard" in toks[2:]:
        return True, "'git reset --hard' discards all uncommitted modifications and staged changes."
    return False, None

def is_dangerous_git_clean(toks):
    if len(toks) >= 2 and toks[0] == "git" and toks[1] == "clean":
        f, d = False, False
        for t in toks[2:]:
            if t.startswith("-"):
                if "f" in t or "--force" in t: f = True
                if "d" in t: d = True
        if f and d: return True, "'git clean -fd' erases untracked files and directories permanently."
    return False, None

def is_dangerous_git_push(toks):
    if len(toks) >= 2 and toks[0] == "git" and toks[1] == "push":
        for t in toks[2:]:
            if t in ("--force", "-f", "--force-with-lease") or t.startswith("+"):
                return True, "'git push --force' overwrites remote history and can destroy shared work."
    return False, None

def is_dangerous_chmod(toks):
    if not toks or toks[0] != "chmod": return False, None
    r, p = False, False
    for t in toks[1:]:
        if t in ("-R", "--recursive") or (t.startswith("-") and "R" in t): r = True
        if t in ("777", "a+rwx", "0777"): p = True
    if r and p: return True, "'chmod -R 777' completely removes permission boundaries."
    return False, None

def is_dangerous_dd(toks):
    if not toks or toks[0] != "dd": return False, None
    for t in toks[1:]:
        if t.startswith("of="):
            tgt = t.split("=", 1)[1].strip()
            if re.match(r"^/dev/(sd[a-z]|nvme[0-9]|hd[a-z]|vd[a-z]|mmcblk)", tgt):
                return True, f"Raw write via 'dd of={tgt}' will overwrite disk/partition data."
    return False, None

def is_dangerous_mkfs(toks):
    if toks and (toks[0] == "mkfs" or toks[0].startswith("mkfs.")):
        return True, f"Executing '{toks[0]}' formats target volumes, destroying existing filesystems."
    return False, None

def is_dangerous_redirect(raw):
    for pat in [r">+\s*/etc/.*", r">+\s*/dev/sd[a-z].*", r">+\s*/dev/nvme.*", r">+\s*~/\.(bashrc|zshrc)"]:
        if re.search(pat, raw): return True, "Overwriting critical config/device nodes via redirection causes system failure."
    return False, None

def is_dangerous_sql_drop(raw):
    u = raw.upper()
    if "DROP DATABASE" in u: return True, "'DROP DATABASE' permanently deletes tables, schemas, and data."
    if "DROP TABLE" in u: return True, "'DROP TABLE' permanently deletes the table structure and rows."
    return False, None

def check_command_danger(raw: str):
    s = raw.strip()
    if not s: return False, None
    d, r = is_fork_bomb(s)
    if d: return True, r
    d, r = is_dangerous_redirect(s)
    if d: return True, r
    d, r = is_dangerous_sql_drop(s)
    if d: return True, r
    try: toks = shlex.split(s)
    except Exception: toks = s.split()
    subs, cur = [], []
    for t in toks:
        if t in (";", "&&", "||", "|", "&"):
            if cur: subs.append(cur); cur = []
        else: cur.append(t)
    if cur: subs.append(cur)
    for sub in subs:
        for fn in [is_dangerous_rm, is_dangerous_git_reset, is_dangerous_git_clean, is_dangerous_git_push, is_dangerous_chmod, is_dangerous_dd, is_dangerous_mkfs]:
            d, r = fn(sub)
            if d: return True, r
    return False, None
