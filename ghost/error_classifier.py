def classify_error(code: int, err: str, cmd: str = ""):
    t = err.lower()
    if code == 127 or "command not found" in t or ("not found" in t and not ("file" in t or "directory" in t)):
        return "command_not_found", "err_cmd_not_found"
    if code == 126 or "permission denied" in t or "access denied" in t:
        return "permission_denied", "err_permission_denied"
    if "syntax error" in t or "unexpected token" in t:
        return "syntax_error", "err_syntax_error"
    if "no such file or directory" in t or "cannot open" in t:
        return "not_found", "err_file_not_found"
    if "git" in cmd.lower() and "not a git repository" in t:
        return "not_found", "err_git_not_repo"
    if ("python" in cmd.lower() or "node" in cmd.lower()) and ("modulenotfounderror" in t or "cannot find module" in t):
        return "not_found", "err_module_not_found"
    return "generic_error", "err_generic"
