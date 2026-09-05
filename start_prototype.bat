@echo off
echo =======================================================
echo          CRYANALYZE 2.0 - WINNING PROTOTYPE
echo       CODE BUILD 1.0 (TRACK 02) - TEAM FOXFIN
echo =======================================================
echo.
echo Starting Backend (FastAPI on http://localhost:8000)...
start "CryAnalyze Backend" cmd /k "cd backend && venv\Scripts\python.exe -m uvicorn main:app --reload --port 8000"

timeout /t 2 /nobreak >nul

echo Starting Frontend (Vite on http://localhost:5173)...
start "CryAnalyze Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo =======================================================
echo Both Backend and Frontend are starting!
echo Frontend will be accessible at: http://localhost:5173
echo Backend API docs available at:  http://localhost:8000/docs
echo =======================================================
pause
