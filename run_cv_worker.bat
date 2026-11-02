@echo off
cd /d "%~dp0..\footprint-csi"
if not exist ".venv-sam\Scripts\python.exe" (
  echo .venv-sam not found. Create it and install ultralytics + torch first.
  exit /b 1
)
.venv-sam\Scripts\python.exe -c "import psycopg,dotenv" 2>nul
if errorlevel 1 (
  echo Installing psycopg and python-dotenv into .venv-sam ...
  .venv-sam\Scripts\python.exe -m pip install "psycopg[binary]" python-dotenv
)
.venv-sam\Scripts\python.exe cv_worker.py
