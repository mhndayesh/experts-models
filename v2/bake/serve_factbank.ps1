<#
serve_factbank.ps1 - standard launcher for a baked FactBank GGUF on llama.cpp (llama-server).

WHY THIS EXISTS (issue + fix, 2026-07-15):
  The baked GGUFs carry a 2.73 MB chat-template. LM Studio's raw loader silently truncates
  templates >980 KB to a 48-char sentinel (F-053), so the bank would NOT fire. The fix is to run
  llama.cpp's own llama-server (full template, no size limit). But the bundled ROCm llama-server.exe
  fails to start standalone with exit -1073741515 (STATUS_DLL_NOT_FOUND): the HIP/BLAS runtime DLLs
  (amdhip64_*.dll, hipblas, rocblas) live in a SEPARATE vendor dir that LM Studio normally injects on
  PATH. Fix = prepend the backend dir AND the rocm vendor bin to PATH before launching. This script
  does that. (Also: launch natively via PowerShell, not Git-Bash - the MSYS loader can't find the
  Windows CRT DLLs, giving api-ms-win-crt-heap errors.)

USAGE:
  powershell -File serve_factbank.ps1 -Gguf "<path.gguf>" [-Port 8080] [-Ngl 99] [-Ctx 8192]
             [-BackendsDir "<dir>"]

  -BackendsDir overrides where the ROCm backend + vendor runtime are found. Default:
  $env:LMSTUDIO_BACKENDS if set, else the standard LM Studio extensions path.
#>
param(
  [Parameter(Mandatory=$true)][string]$Gguf,
  [int]$Port = 8080,
  [int]$Ngl  = 99,
  [int]$Ctx  = 8192,
  [int]$Parallel = 1,   # concurrent request slots (llama-server -np). Ctx is split ACROSS slots,
                        # so per-slot context = Ctx / Parallel. Size Ctx accordingly.
  [string]$BackendsDir = $(if ($env:LMSTUDIO_BACKENDS) { $env:LMSTUDIO_BACKENDS } else { "C:\Users\mhnda\.lmstudio\extensions\backends" }),
  [string]$LogDir = "$env:TEMP\factbank-serve"
)
$ErrorActionPreference = "Stop"

# --- validate the GGUF up front (fail clearly, before we touch backends/PATH) ---
if (-not (Test-Path -LiteralPath $Gguf -PathType Leaf)) {
  throw "GGUF not found: $Gguf"
}

$backends = $BackendsDir
if (-not (Test-Path $backends)) { throw "backends dir not found: $backends (set -BackendsDir or `$env:LMSTUDIO_BACKENDS)" }

# Parse a version out of a backend dir name (e.g. '...amd-rocm-1.2.3' -> [version]1.2.3) so the
# "newest" pick is by real version, not lexicographic string order (where '1.10' < '1.9').
function Get-DirVersion([string]$name) {
  $m = [regex]::Match($name, '(\d+(?:\.\d+)+)')
  if ($m.Success) { try { return [version]$m.Value } catch { return $null } }
  return $null
}

# newest rocm backend + its vendor runtime (v6 = amdhip64_7)
$rocmDirs = Get-ChildItem "$backends" -Directory | Where-Object Name -like "*amd-rocm*"
if (-not $rocmDirs) { throw "no *amd-rocm* backend found under $backends" }
# Prefer parsed-version ordering; fall back to lexicographic Name for any dir with no version token.
# (Lexicographic is imperfect - '1.10' sorts before '1.9' - but only used when names lack a version.)
$dir = $rocmDirs |
  Sort-Object @{ Expression = { Get-DirVersion $_.Name } }, @{ Expression = { $_.Name } } |
  Select-Object -Last 1 | ForEach-Object FullName

$vendorDirs = Get-ChildItem "$backends\vendor" -Directory | Where-Object Name -like "*rocm-vendor-v6*"
if (-not $vendorDirs) { throw "rocm vendor dir (*rocm-vendor-v6*) not found under $backends\vendor" }
# deterministic pick: version-then-name, newest last
$vendor = $vendorDirs |
  Sort-Object @{ Expression = { Get-DirVersion $_.Name } }, @{ Expression = { $_.Name } } |
  Select-Object -Last 1 | ForEach-Object { Join-Path $_.FullName "bin" }

if (-not (Test-Path $dir))    { throw "rocm backend not found under $backends" }
if (-not (Test-Path $vendor)) { throw "rocm vendor bin not found" }

$serverExe = Join-Path $dir "llama-server.exe"
if (-not (Test-Path -LiteralPath $serverExe -PathType Leaf)) {
  throw "llama-server.exe not found in backend dir: $serverExe"
}

# --- refuse to launch onto a port already in use (else we could report a FALSE 'READY'
#     against a pre-existing server that has no bank baked in) ---
$portBusy = $false
try {
  $portBusy = (Test-NetConnection -ComputerName 127.0.0.1 -Port $Port -InformationLevel Quiet -WarningAction SilentlyContinue)
} catch {
  # Test-NetConnection unavailable - fall back to a raw socket probe
  try {
    $c = New-Object System.Net.Sockets.TcpClient
    $iar = $c.BeginConnect("127.0.0.1", $Port, $null, $null)
    $portBusy = $iar.AsyncWaitHandle.WaitOne(500) -and $c.Connected
    $c.Close()
  } catch { $portBusy = $false }
}
if ($portBusy) {
  throw "port $Port is already in use - refusing to launch (would risk a false READY against an existing server). Pick a free -Port or stop the other process."
}

$env:PATH = "$dir;$vendor;$env:PATH"           # <-- THE FIX

if (-not (Test-Path $LogDir)) { New-Item -ItemType Directory -Path $LogDir | Out-Null }
$log = Join-Path $LogDir ("llama-" + (Split-Path $Gguf -Leaf) + ".log")
if (Test-Path $log) { Remove-Item $log -Force }

Write-Output "backend: $dir"
Write-Output "vendor : $vendor"
Write-Output "gguf   : $Gguf"
$p = Start-Process -FilePath "$serverExe" `
  -ArgumentList '-m',"$Gguf",'--port',"$Port",'--host','127.0.0.1','-ngl',"$Ngl",'--ctx-size',"$Ctx",'--parallel',"$Parallel",'--jinja' `
  -WorkingDirectory $dir -RedirectStandardOutput $log -RedirectStandardError "$log.err" -PassThru -WindowStyle Hidden
Write-Output "parallel slots: $Parallel  (per-slot ctx = $([math]::Floor($Ctx / $Parallel)))"
Write-Output "PID: $($p.Id)"
Write-Output "LOG: $log"

# wait for readiness (or failure)
$deadline = (Get-Date).AddSeconds(240)
while ((Get-Date) -lt $deadline) {
  Start-Sleep -Seconds 3
  if ($p.HasExited) { Write-Output "SERVER EXITED early (code $($p.ExitCode)). stderr:"; Get-Content "$log.err" -Tail 20 -EA SilentlyContinue; exit 1 }
  try { $h = Invoke-RestMethod "http://127.0.0.1:$Port/health" -TimeoutSec 3; if ($h.status -eq "ok") { Write-Output "READY on :$Port"; exit 0 } } catch {}
}
# timeout: do NOT orphan the process we launched (it would squat VRAM).
Write-Output "TIMEOUT waiting for readiness - stopping launched server (PID $($p.Id))"
try { if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue } } catch {}
exit 1
