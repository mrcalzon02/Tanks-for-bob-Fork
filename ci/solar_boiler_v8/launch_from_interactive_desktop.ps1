# Run ONLY inside the logged-on user's visible Windows desktop, not as an
# Actions service (Session 0 cannot initialize Factorio D3D11 output).
# This script never modifies the user's Factorio installation, Steam files,
# game saves, or installed mods; the existing Python capture isolates them.
[CmdletBinding()]
param(
  [string]$FactorioExe = '',
  [string]$OutputDirectory = '',
  [int]$MaxSeconds = 360
)
$ErrorActionPreference='Stop'
$ProgressPreference='SilentlyContinue'
if (-not $IsWindows -and $PSVersionTable.PSEdition -eq 'Core') {
  throw 'Real client capture requires an interactive Windows desktop'
}
$session = [System.Diagnostics.Process]::GetCurrentProcess().SessionId
if ($session -eq 0) {
  throw 'INTERACTIVE_DESKTOP_REQUIRED: this is Windows Session 0 (service). Launch PowerShell from a logged-on desktop before running Factorio GUI screenshots.'
}
Write-Host "SOLAR_V8_INTERACTIVE_SESSION $session"
if (@(Get-Process -Name factorio -ErrorAction SilentlyContinue).Count -ne 0) {
  throw 'Factorio is already running. Stop this capture attempt rather than interrupt a user game.'
}
$root = (Resolve-Path (Join-Path $PSScriptRoot '../..')).Path
$script = Join-Path $PSScriptRoot 'visual_capture.py'
$native = Join-Path $root 'models/island-survival/solar-boiler/generated-v8/solar-boiler-v8.blend'
$graphics = Join-Path $root 'tanks_for_bob_fork_1.8.102/graphics/entity/solar-boiler-v8/working-256.png'
foreach ($file in @($script,$native,$graphics)) {
  if (-not (Test-Path -LiteralPath $file -PathType Leaf)) {
    throw "Incomplete checked-out Tanks V8 source; missing $file"
  }
}
$candidates=@(
  'C:\Program Files\Python312\python.exe',
  'C:\Program Files\Python311\python.exe',
  'C:\Program Files\Blender Foundation\Blender 5.2\5.2\python\bin\python.exe'
)
$cmd=Get-Command python.exe -ErrorAction SilentlyContinue
if ($cmd) { $candidates+= [string]$cmd.Source }
$python=$null
foreach ($candidate in @($candidates | Select-Object -Unique)) {
  if (-not (Test-Path -LiteralPath $candidate -PathType Leaf)) { continue }
  $v=((& $candidate -c 'import sys;print(sys.version_info.major,sys.version_info.minor)' 2>&1) | Out-String).Trim()
  if ($LASTEXITCODE -eq 0 -and $v -match '^3\s+1[0-9]$') {
    $python=$candidate
    break
  }
}
if (-not $python) { throw 'Python 3.10+ is required for the real screenshot verifier.' }
$stamp=(Get-Date).ToUniversalTime().ToString('yyyyMMdd-HHmmss')
$work=Join-Path $env:TEMP ("solar-boiler-v8-gui-$stamp")
if (Test-Path -LiteralPath $work) { throw "Refusing to overwrite $work" }
New-Item -ItemType Directory -Path $work | Out-Null
if ([string]::IsNullOrWhiteSpace($OutputDirectory)) {
  $OutputDirectory=Join-Path $root "models/island-survival/solar-boiler/generated-v8/visual-client-$stamp"
}
$out=[IO.Path]::GetFullPath($OutputDirectory)
if (Test-Path -LiteralPath $out) { throw "Refusing to overwrite screenshot evidence: $out" }
# Keep any missing Pillow dependency in disposable scratch, never system Python.
& $python -c 'from PIL import Image; print(Image.__version__)' 2>$null
if ($LASTEXITCODE -ne 0) {
  $deps=Join-Path $work 'python-deps'
  New-Item -ItemType Directory -Path $deps | Out-Null
  & $python -m pip install --disable-pip-version-check --no-input --only-binary=:all: --target $deps 'Pillow==11.3.0'
  if ($LASTEXITCODE -ne 0) { throw 'Isolated Pillow dependency installation failed' }
  $env:PYTHONPATH=$deps
}
$args=@($script,'--output',$out,'--working',(Join-Path $work 'isolated-runtime'),'--max-seconds',[string]$MaxSeconds)
if ($FactorioExe) { $args+=@('--client',$FactorioExe) }
Write-Host 'Launching the REAL graphical Factorio 2.1 Windows client in this interactive session.'
Write-Host 'The user game installation, saves and registered mods are read-only.'
Write-Host "Screenshots will be saved under: $out"
& $python @args
if ($LASTEXITCODE -ne 0) {
  throw "Real Factorio screenshot capture failed. Inspect $out\client-capture-error.json and $work\isolated-runtime\graphical-factorio.log. No visual approval recorded."
}
$qa=Join-Path $out 'client-capture-qa.json'
if (-not (Test-Path -LiteralPath $qa -PathType Leaf)) { throw 'Missing native screenshot QA receipt' }
$receipt=Get-Content -LiteralPath $qa -Raw | ConvertFrom-Json
if (-not $receipt.passed -or $receipt.factorio_headless -or $receipt.screen_capture_count -ne 16) {
  throw 'Native Factorio screenshots did not pass required proof gates'
}
Write-Host 'SOLAR_V8_ACTUAL_GUI_SCREENSHOTS_VERIFIED count=16'
Write-Host "Four-way genuine game contact sheet: $(Join-Path $out 'factorio-client-pipes-all-four.png')"
Write-Host "Source comparison: $(Join-Path $out 'client-vs-approved-v8.png')"
Write-Host 'Review pipe mouth alignment visually before marking issue #4 complete.'
