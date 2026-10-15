@echo off
setlocal
cd /d "%~dp0"
if "%~1"=="" (
  echo Usage: BUILD.bat "C:\path\Japanese.ws"
  exit /b 2
)
py -3 build.py "%~1"
if errorlevel 1 exit /b 1
py -3 -m unittest discover -s tests -v
exit /b %errorlevel%
