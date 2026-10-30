# Ghost Shell PowerShell Hook
# Load with: . .\hooks\ghost.ps1

$script:GhostDir = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

# Use the Python launcher when available; otherwise use python.exe.
$script:GhostPython = Get-Command py -ErrorAction SilentlyContinue
if (-not $script:GhostPython) {
    $script:GhostPython = Get-Command python -ErrorAction SilentlyContinue
}
if (-not $script:GhostPython) {
    Write-Warning "Ghost Shell: Python was not found. Install Python or add it to PATH."
    return
}
$script:GhostPython = $script:GhostPython.Source
$script:GhostPrevFailed = $false
$script:GhostLastHistoryId = -1

function Invoke-GhostPython {
    param(
        [Parameter(Mandatory = $true)]
        [string[]]$Arguments
    )

    & $script:GhostPython (Join-Path $script:GhostDir "ghost.py") @Arguments
    return $LASTEXITCODE
}

function Invoke-GhostCheck {
    param([string]$Command)

    if ([string]::IsNullOrWhiteSpace($Command)) { return $true }
    if ($Command -like "*ghost.py*") { return $true }

    $exitCode = Invoke-GhostPython -Arguments @("check-command", $Command)
    return ($exitCode -eq 0)
}

# Capture failed PowerShell commands when the next prompt is displayed.
function global:prompt {
    $wasSuccessful = $?
    $nativeExitCode = $LASTEXITCODE
    $latestError = $null

    if (-not $wasSuccessful -and $Error.Count -gt 0) {
        $latestError = $Error[0]
    }

    $historyItem = Get-History -Count 1
    if ($historyItem -and $historyItem.Id -ne $script:GhostLastHistoryId) {
        $script:GhostLastHistoryId = $historyItem.Id
        $failedCommand = $historyItem.CommandLine

        if (-not $wasSuccessful -and
            $failedCommand -notlike "*ghost.py*" -and
            $failedCommand -notlike "*Invoke-Ghost*") {

            $errorText = if ($latestError) {
                $latestError.ToString()
            } else {
                "PowerShell command failed"
            }

            $errorId = if ($latestError) {
                [string]$latestError.FullyQualifiedErrorId
            } else {
                ""
            }

            $ghostExitCode = 1
            if ($errorId -like "*CommandNotFoundException*") {
                $ghostExitCode = 127
            } elseif ($null -ne $nativeExitCode -and $nativeExitCode -ne 0) {
                $ghostExitCode = [int]$nativeExitCode
            }

            Invoke-GhostPython -Arguments @(
                "explain-error",
                "--exit-code", "$ghostExitCode",
                "--command", "$failedCommand",
                "--stderr", "$errorText"
            ) | Out-Host

            $script:GhostPrevFailed = $true
        } elseif ($wasSuccessful -and $script:GhostPrevFailed) {
            Invoke-GhostPython -Arguments @("play-sound", "relief") | Out-Null
            $script:GhostPrevFailed = $false
        }
    }

    "PS $($executionContext.SessionState.Path.CurrentLocation)> "
}

# Intercept dangerous commands before PowerShell executes them.
Import-Module PSReadLine -ErrorAction SilentlyContinue
if (Get-Command Set-PSReadLineKeyHandler -ErrorAction SilentlyContinue) {
    Set-PSReadLineKeyHandler -Key Enter -ScriptBlock {
        $line = ""
        $cursor = 0
        [Microsoft.PowerShell.PSConsoleReadLine]::GetBufferState(
            [ref]$line,
            [ref]$cursor
        )

        if (-not [string]::IsNullOrWhiteSpace($line)) {
            if (-not (Invoke-GhostCheck -Command $line)) {
                [Microsoft.PowerShell.PSConsoleReadLine]::RevertLine()
                return
            }
        }

        [Microsoft.PowerShell.PSConsoleReadLine]::AcceptLine()
    }
} else {
    Write-Warning "Ghost Shell: PSReadLine is unavailable; dangerous-command pre-check is disabled."
}

Write-Host "Ghost Shell PowerShell hook loaded." -ForegroundColor Green
