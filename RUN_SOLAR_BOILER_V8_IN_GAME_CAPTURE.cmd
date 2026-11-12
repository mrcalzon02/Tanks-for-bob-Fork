@echo off
setlocal EnableExtensions DisableDelayedExpansion
title Solar Boiler V8 - REAL Factorio In-Game Pipe Screenshots
cd /d "%~dp0"
echo.
echo Solar Boiler V8 - real graphical Factorio screenshots, four rotations
echo --------------------------------------------------------------
echo This launcher runs ONLY in the signed-in Windows desktop.
echo No Administrator privileges, runner service changes, or saved-game edits.
echo.
set "CAPTURE_SCRIPT=%~dp0ci\solar_boiler_v8\launch_from_interactive_desktop.ps1"
set "GAME_EXE=D:\SteamLibrary B\steamapps\common\Factorio\bin\x64\factorio.exe"
if not exist "%CAPTURE_SCRIPT%" (
  echo ERROR: This is not a full, updated Tanks-for-bob-Fork checkout.
  echo Expected: %CAPTURE_SCRIPT%
  echo Update the checkout, then run this launcher again.
  pause
  exit /b 2
)
where powershell.exe >nul 2>nul
if errorlevel 1 (
  echo ERROR: Windows PowerShell is not installed or available on PATH.
  pause
  exit /b 3
)
if exist "%GAME_EXE%" (
  echo Found approved Factorio graphical client:
  echo %GAME_EXE%
  powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%CAPTURE_SCRIPT%" -FactorioExe "%GAME_EXE%"
) else (
  echo Factorio was not at the last verified location; using isolated Steam-library discovery.
  powershell.exe -NoLogo -NoProfile -ExecutionPolicy Bypass -File "%CAPTURE_SCRIPT%"
)
set "EXIT_CODE=%ERRORLEVEL%"
echo.
if not "%EXIT_CODE%"=="0" (
  echo Capture did not pass. Exit code: %EXIT_CODE%.
  echo Read the error above. No game screenshot acceptance is recorded.
) else (
  echo Actual Factorio screenshot QA passed. The image comparison and ZIP
  echo paths are shown above. Share that ZIP for pipe alignment review.
)
echo.
pause
exit /b %EXIT_CODE%
