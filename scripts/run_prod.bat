@echo off

echo Starting GST Reconciliation System (Production Mode)...

:: Check for .env file
if not exist ".env" (
    echo [ERROR] .env file not found!
    echo Please copy .env.example to .env and configure your secrets.
    pause
    exit /b 1
)

:: Activate venv if it exists
if exist ".venv\Scripts\activate.bat" (
    call .venv\Scripts\activate.bat
)

:: 1. Start Backend (No reload, workers=4)
echo [1/2] Starting Backend...
start /B python -m uvicorn backend.main:app --host 0.0.0.0 --port 8001 --workers 4

:: Wait for backend to be ready (dumb wait)
timeout /t 5 /nobreak >nul

:: 2. Start Frontend
echo [2/2] Starting Dashboard...
streamlit run frontend/dashboard.py --server.port 8502 --server.address 0.0.0.0

