# Ghost Shell Bash Hook
GDIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GPY="$(which python3 2>/dev/null || which python 2>/dev/null)"
G_PREV=0
G_INT=0

_ghost_preexec() {
    [ -z "$COMP_LINE" ] || return 0
    [ "$BASH_COMMAND" = "$PROMPT_COMMAND" ] && return 0
    case "$BASH_COMMAND" in *"ghost.py"*|*"_ghost_"*|"return 1") return 0;; esac
    if [ -x "$GPY" ]; then
        "$GPY" "$GDIR/ghost.py" check-command "$BASH_COMMAND"
        if [ $? -ne 0 ]; then G_INT=1; return 1; fi
    fi
    G_INT=0; return 0
}

_ghost_prompt() {
    local exit_code=$?
    if [ $G_INT -eq 1 ]; then G_INT=0; return 0; fi
    if [ $exit_code -eq 0 ]; then
        if [ $G_PREV -eq 1 ]; then
            "$GPY" "$GDIR/ghost.py" play-sound relief >/dev/null 2>&1 &
            G_PREV=0
        fi
    else
        local cmd
        cmd="$(HISTTIMEFORMAT= history 1 | sed 's/^[ ]*[0-9]*[ ]*//')"
        case "$cmd" in *"ghost.py"*|*"_ghost_"*) ;; *)
            G_PREV=1
            "$GPY" "$GDIR/ghost.py" explain-error --exit-code "$exit_code" --command "$cmd"
            ;;
        esac
    fi
}

shopt -s extdebug
trap '_ghost_preexec' DEBUG
if [[ ";$PROMPT_COMMAND;" != *";_ghost_prompt;"* ]]; then
    PROMPT_COMMAND="_ghost_prompt${PROMPT_COMMAND:+;$PROMPT_COMMAND}"
fi
