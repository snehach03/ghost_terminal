#!/usr/bin/env python3
import os
import subprocess
import sys
import time

R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GHOST = os.path.join(R, "ghost.py")
PYTHON = sys.executable

sys.path.insert(0, R)
from ghost.sound_player import play_sound_event


def run_ghost(*args, input_text=None):
    """Run Ghost Shell with the same Python interpreter running this demo."""
    return subprocess.run(
        [PYTHON, GHOST, *args],
        input=input_text,
        text=True,
        check=False,
    )


def run():
    version = sys.version.split()[0]

    print("\033[1;35m=== GHOST SHELL INTERACTIVE DEMO ===\033[0m")
    print("\033[1;36mstudent@haunted-laptop:~$ \033[0mpythno app.py")
    print("bash: pythno: command not found")

    run_ghost(
        "explain-error",
        "--exit-code", "127",
        "--command", "pythno app.py",
        "--stderr", "command not found",
    )

    time.sleep(1.5)

    print(f"\033[1;36mstudent@haunted-laptop:~$ \033[0mpython --version")
    print(f"Python {version}")
    play_sound_event("relief")
    print("\033[1;32m✓ Fixed! Soft chime plays.\033[0m")

    time.sleep(1.5)

    print("\033[1;36mstudent@haunted-laptop:~$ \033[0mrm -rf /")
    result = run_ghost(
        "check-command",
        "rm -rf /",
        input_text="no\n",
    )

    if result.returncode != 0:
        print("\033[1;32m✓ Dangerous command was intercepted and cancelled.\033[0m")
        print("\033[1;32mDemo completed successfully!\033[0m")
    else:
        print("\033[1;31mDemo check failed: the dangerous command was not cancelled.\033[0m")


if __name__ == "__main__":
    run()
