import re

def get_rule_explanation(cat: str, err: str, cmd: str):
    c = cmd.strip().split()[0] if cmd.strip() else "command"
    if cat == "command_not_found":
        return f"The terminal graveyard echoes in silence... '{c}' has no soul in this realm.", f"Fix: Check for typos in '{c}' or install it via your package manager (e.g. sudo apt install {c} or brew install {c})."
    if cat == "permission_denied":
        return "Ancient iron chains bind this path. The spirit world refuses entry.", f"Fix: Check file permissions using 'ls -l' or re-run with sudo: 'sudo {cmd}'."
    if cat == "syntax_error":
        return "A broken incantation has perturbed the ghostly order. The shell cannot parse this.", "Fix: Review your command for unclosed quotes, mismatched brackets, or misplaced pipes."
    if cat == "not_found":
        if "not a git repository" in err.lower():
            return "You tread upon unhallowed ground. No git chronicles exist here.", "Fix: Run 'git init' or change into an existing git repository folder."
        if "modulenotfounderror" in err.lower():
            return "A phantasmal dependency vanished into the ether before execution.", "Fix: Install the missing package with 'pip install <package_name>'."
        return "Echoing footsteps through empty halls... target does not exist in this realm.", "Fix: Verify the file or folder path using 'ls' before referencing it."
    return None
