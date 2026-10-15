@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>nul
if errorlevel 1 (
  python tools\build.py
) else (
  py -3 tools\build.py
)
if errorlevel 1 (
  echo Build failed. Read README.md for Python dependencies.
  exit /b 1
)
echo Build complete: build\
