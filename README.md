# 👻 Ghost Shell

::: {align="center"}
``` text
       .-.
      (o o) boo!
      | O \
       \   \
        `~~~'
```

**A haunted terminal assistant for students.**

![Python](https://img.shields.io/badge/python-3.8+-purple.svg)
![License](https://img.shields.io/badge/License-MIT-blue.svg)
![Privacy](https://img.shields.io/badge/Privacy-Local-success.svg)
![Audio](https://img.shields.io/badge/Audio-Procedural%20PCM%20WAV-orange.svg)
:::

Ghost Shell is a lightweight terminal guardian designed to help students
learn the command line without fear. It watches commands, explains
common errors in plain English with a little spooky atmosphere, plays
procedural sound effects, and checks potentially destructive commands
against deterministic safety rules.

-   🛑 **Dangerous-command checks:** identifies configured destructive
    command patterns and explains the potential impact before execution.
-   🔊 **Procedural sound effects:** generates audio cues for errors,
    alerts, and successful fixes.
-   👻 **Error explanations:** combines spooky lore with a clearly
    labelled, actionable `Fix:` instruction.
-   ⚡ **Rule-first responses:** common errors can be handled by
    built-in templates without calling an AI model.
-   🔒 **Local-first design:** everyday rule-based features work
    locally. An optional local model can be used as a fallback for
    unusual errors.

> **Note:** Feature behaviour depends on the shell hook being installed
> and active. The optional local model is not required for the core
> rule-based features.

## Demo preview

``` text
student@haunted-laptop:~$ pythno app.py
bash: pythno: command not found
[🔊 Door creaks eerily in the background...]

👻 The terminal graveyard echoes in silence... 'pythno' has no soul in this realm.
Fix: Check for typos in 'pythno' or install it via your package manager.

student@haunted-laptop:~$ python3 app.py
Hello, World!
[🔊 Soft harmonic relief chime plays...]

student@haunted-laptop:~$ rm -rf /
[🔊 Deep funeral bell tolls...]

👻 GHOST SHELL GUARDIAN: DANGEROUS COMMAND INTERCEPTED!
Target: rm -rf /
Peril: Destructive deletion could wipe out essential files or system directories.
Type 'yes' to continue, or anything else to cancel: no
Command prevented. The spirits have preserved your files.
```

Add a real screen recording or GIF at `demo/demo.gif` when one is
available.

## Core features

### 1. Deterministic danger interception

Safety checks are rule-based rather than delegated to an AI model.
Commands are checked against configured patterns associated with
destructive actions.

When a command is flagged, the intended flow is to: 1. Stop the command
from proceeding through the hook. 2. Play a warning sound. 3. Explain
what the command could destroy. 4. Ask the user to explicitly confirm
before proceeding.

Examples of patterns described by the project:

  -----------------------------------------------------------------------
  Protected pattern                   Potential impact
  ----------------------------------- -----------------------------------
  `rm -rf` targeting `/`, `~`,        Can delete root, user, or system
  `$HOME`, `.`, `*`, `..`, `/etc`,    files
  and similar paths                   

  `git reset --hard`                  Discards uncommitted changes and
                                      staged edits

  `git clean -fd`                     Deletes untracked files and
                                      directories

  `git push --force`, `-f`, or        Rewrites remote branch history and
  `+branch`                           can disrupt collaborators

  `chmod -R 777` or recursive         Can weaken file and system security
  permission changes                  

  `dd` writing to a device such as    Can overwrite disk data and
  `/dev/sd*`, `nvme*`, or `hd*`       partition information

  `mkfs` / `mkfs.ext4`                Formats a target filesystem

  Redirection into files such as      Can overwrite important system or
  `/etc/...` or `~/.bashrc`           shell configuration

  `DROP DATABASE` / `DROP TABLE`      Deletes database objects or data

  Fork-bomb patterns such as          Can exhaust system resources
  `:(){ :\|:& };:`                    
  -----------------------------------------------------------------------

These are examples of patterns documented for the project; the actual
rules are defined by the implementation in `ghost/danger_rules.py`.

### 2. Spooky lore + clear fix

Error explanations are designed to have two parts: - A short,
atmospheric ghost-themed message. - A clearly labelled `Fix:` line with
a practical next step.

The spooky wording is for personality; the fix should remain
understandable and actionable.

### 3. Procedural sound design

Sound effects are generated mathematically using Python's built-in
`wave` and `math` modules. The project does not require external audio
libraries or prerecorded sound samples for synthesis.

  -----------------------------------------------------------------------
  Event                   Audio asset / sound     Description
  ----------------------- ----------------------- -----------------------
  Command not found       `door_creak.wav`        Creaky wooden-door
                                                  groan

  Permission denied       `chains.wav`            Metallic rattling /
                                                  chain-like sound

  Syntax error            `wail.wav`              Modulated ascending and
                                                  descending wail

  File or directory not   `footsteps.wav`         Muffled rhythmic
  found                                           footsteps

  Dangerous command       `bell.wav`              Deep warning bell
  blocked                                         

  Error fixed / resolved  `chime.wav`             Gentle major-triad
                                                  chime

  Generic or other error  `moan.wav`              Low resonant phantom
                                                  moan
  -----------------------------------------------------------------------

Generate the sound assets with:

``` bash
python3 sounds/generate_sounds.py
```

On Windows PowerShell:

``` powershell
python sounds\generate_sounds.py
```

## Installation and setup

### Prerequisites

-   Python 3.8 or higher.
-   The core rule-based functionality uses the Python standard library;
    no `pip` packages are required for those features.
-   A supported shell for the integration hook you intend to use.

### 1. Clone the repository

Replace the example repository URL with the actual repository URL:

``` bash
git clone https://github.com/your-username/ghost-shell.git
cd ghost-shell
```

### 2. Generate sound assets

``` bash
python3 sounds/generate_sounds.py
```

On Windows:

``` powershell
python sounds\generate_sounds.py
```

## Shell integration

Choose the instructions for the shell you use. Run commands from the
repository root unless otherwise stated.

### Windows --- PowerShell / VS Code terminal

The repository includes `hooks/ghost.ps1`. The documented hook uses
PSReadLine for command-line interception. If PSReadLine is unavailable
in your PowerShell session, that particular hook may not work as
written.

To test the repository hook in the current session:

``` powershell
. .\hooks\ghost.ps1
```

To allow locally created scripts to run for your Windows user, if your
execution policy blocks the hook:

``` powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

To configure the hook to load automatically, the README's original
approach is to add its path to your PowerShell profile. First open the
profile:

``` powershell
notepad $PROFILE
```

Then add a dot-source line using the **actual full path** to this
repository's `hooks\ghost.ps1`, for example:

``` powershell
. 'D:\path\to\ghost-shell\hooks\ghost.ps1'
```

Restart PowerShell to test the profile configuration.

#### Windows PowerShell 5.1 session note

During testing, a temporary command-not-found handler was also used in
the current PowerShell session. To turn off that temporary handler for
the current session:

``` powershell
$ExecutionContext.InvokeCommand.CommandNotFoundAction = $null
```

This does not delete project files or uninstall Ghost Shell. It only
clears that session's command-not-found handler. Closing the terminal
also ends the current session.

### Linux --- Bash / Git Bash

Test the hook in the current shell:

``` bash
source hooks/ghost.bash
```

To load it automatically in future Bash sessions, add the following line
to `~/.bashrc` (use the full path to the repository):

``` bash
source /path/to/ghost-shell/hooks/ghost.bash
```

Then reload the file:

``` bash
source ~/.bashrc
```

The repository also lists an installer:

``` bash
bash install.sh
```

### macOS --- Zsh

Test the hook in the current shell:

``` zsh
source hooks/ghost.zsh
```

To load it automatically in future Zsh sessions, add the following line
to `~/.zshrc` (use the full path to the repository):

``` zsh
source /path/to/ghost-shell/hooks/ghost.zsh
```

Then reload the file:

``` zsh
source ~/.zshrc
```

## CLI commands

The project exposes a command-line interface through `ghost.py`.

Use `python` on Windows and `python3` on systems where that is the
configured Python command.

``` bash
# Show system status
python3 ghost.py status

# Mute sound effects
python3 ghost.py mute

# Unmute sound effects
python3 ghost.py unmute

# Play individual sound effects
python3 ghost.py play-sound relief
python3 ghost.py play-sound dangerous_command
python3 ghost.py play-sound chains

# Check a command against danger rules
python3 ghost.py check-command "git reset --hard"
```

Windows examples:

``` powershell
python .\ghost.py status
python .\ghost.py mute
python .\ghost.py unmute
python .\ghost.py play-sound relief
python .\ghost.py check-command "git reset --hard"
```

## Optional local open-source AI model

The AI model is optional. Everyday rule-based error handling and danger
checks are intended to work without it. A local model can be used as a
fallback for unusual errors or complex stack traces.

The documented optional model is **Qwen2.5-0.5B-Instruct** in GGUF
format.

### 1. Download the model

The project provides a setup script:

``` bash
bash scripts/setup_model.sh
```

This downloads the quantized model described by the project
(approximately 397 MB in the original documentation).

### 2. Add `llama-server`

Download a compatible precompiled `llama-server` binary from the
official llama.cpp releases. Place `llama-server` or `llama-server.exe`
inside the project's `models/` directory.

### 3. Start the local server

``` bash
bash scripts/start_server.sh
```

The documented server address is:

``` text
http://127.0.0.1:8080
```

The original project notes describe a four-thread configuration and an
approximate memory use below 500 MB; actual resource use depends on the
model, binary, and machine.

### 4. Use a different GGUF model

To switch models: 1. Place the alternative `.gguf` file in `models/`. 2.
Update the root `config.json`. 3. Restart the local model server.

Example configuration:

``` json
{
  "server_url": "http://127.0.0.1:8080",
  "model_name": "my-custom-model",
  "model_file": "my-custom-model.gguf"
}
```

Other small GGUF models may be usable, provided they are compatible with
the server and the project's prompt/client expectations.

## Why open-source AI?

Ghost Shell is designed around local execution and avoids depending on
cloud AI APIs for its core features.

-   **Local execution:** the optional model can run on a laptop CPU; a
    GPU is not a requirement for the documented small model.
-   **Privacy:** shell commands and error output can remain on the local
    machine when using the local setup. The optional server is
    configured for localhost.
-   **No API account or key:** the local model workflow does not require
    a cloud API key, subscription, or cloud account.
-   **Interchangeable models:** the client uses an OpenAI-compatible
    chat-completions style endpoint, allowing compatible local GGUF
    models to be swapped through configuration.
-   **Deterministic safety:** danger detection is rule-based, not an AI
    guess.
-   **Graceful fallback:** common errors use built-in templates. The
    optional model is only for cases that need additional explanation;
    the core rule-based features do not depend on the model server.

## Project architecture

``` text
ghost-shell/
├── config.example.json       # Example configuration
├── ghost.py                  # Unified CLI entry point
├── install.sh                # Unix installer
├── uninstall.sh              # Unix uninstaller
├── ghost/                    # Core Python package
│   ├── cli.py                # CLI subcommand dispatcher
│   ├── danger_rules.py       # Rule-based danger detection
│   ├── error_classifier.py   # Error code and stderr parser
│   ├── rule_explanations.py  # Built-in explanation templates
│   ├── model_client.py       # Local llama-server HTTP client
│   ├── sound_player.py       # Audio playback
│   ├── cache.py              # Local explanation cache
│   └── config.py             # JSON configuration loader
├── hooks/
│   ├── ghost.bash            # Bash integration
│   ├── ghost.zsh             # Zsh integration
│   └── ghost.ps1             # PowerShell integration
├── sounds/
│   ├── generate_sounds.py    # Procedural sound synthesizer
│   └── *.wav                 # Generated PCM WAV assets
├── scripts/
│   ├── setup_model.sh        # Optional model setup
│   └── start_server.sh       # Starts local model server
├── tests/
│   ├── test_danger_rules.py  # Danger-rule tests
│   ├── test_classifier.py    # Error-classifier tests
│   └── run_tests.py          # Test suite runner
└── demo/
    └── demo_session.py       # Interactive demo script
```

## Testing and verification

Run the automated tests from the repository root:

``` bash
python3 tests/run_tests.py
```

On Windows:

``` powershell
python .\tests\run_tests.py
```

Run the interactive demo:

``` bash
python3 demo/demo_session.py
```

On Windows:

``` powershell
python .\demo\demo_session.py
```

## Uninstalling

### Linux / macOS

Run the project's uninstaller from the repository root:

``` bash
bash uninstall.sh
```

### Windows PowerShell

If you added the hook to your PowerShell profile, open the profile:

``` powershell
notepad $PROFILE
```

Remove the line that dot-sources this repository's `hooks\ghost.ps1`,
save the file, and restart PowerShell.

If you only loaded Ghost Shell in the current session, close that
terminal or clear the temporary command-not-found handler:

``` powershell
$ExecutionContext.InvokeCommand.CommandNotFoundAction = $null
```

This disables the temporary handler in that session; it does not remove
the repository.

## License

Distributed under the MIT License. See the `LICENSE` file for details.
