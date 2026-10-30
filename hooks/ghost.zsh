# Ghost Shell Zsh Hook
GDIR="$(cd "$(dirname "${(%):-%x}")/.." && pwd)"
GPY="$(which python3 2>/dev/null || which python 2>/dev/null)"
G_PREV=0

_ghost_zle_accept_line() {
    local cmd="$BUFFER"
    if [[ -n "$cmd" && -x "$GPY" ]]; then
        case "$cmd" in *"ghost.py"*|*"_ghost_"*) ;; *)
            "$GPY" "$GDIR/ghost.py" check-command "$cmd"
            if [[ $? -ne 0 ]]; then BUFFER=""; zle redisplay; return 1; fi
            ;;
        esac
    fi
    zle .accept-line
}
zle -N accept-line _ghost_zle_accept_line

_ghost_preexec() { G_LAST="$1"; }
_ghost_precmd() {
    local ec=$?
    if [[ -z "$G_LAST" ]]; then return 0; fi
    case "$G_LAST" in *"ghost.py"*|*"_ghost_"*) return 0;; esac
    if [[ $ec -eq 0 ]]; then
        if [[ $G_PREV -eq 1 ]]; then
            "$GPY" "$GDIR/ghost.py" play-sound relief >/dev/null 2>&1 &
            G_PREV=0
        fi
    else
        G_PREV=1
        "$GPY" "$GDIR/ghost.py" explain-error --exit-code "$ec" --command "$G_LAST"
    fi
    G_LAST=""
}
autoload -Uz add-zsh-hook
add-zsh-hook preexec _ghost_preexec
add-zsh-hook precmd _ghost_precmd
