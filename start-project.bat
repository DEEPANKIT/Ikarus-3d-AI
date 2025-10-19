@echo off
echo Starting Ikarus 3D Product Recommendation System...
echo.

echo Step 1: Activating Python 3.12 virtual environment...
call venv-3.12\Scripts\activate

echo Step 2: Starting FastAPI backend server...
start "Backend Server" cmd /k "cd backend && python main.py"

echo Step 3: Waiting for backend to start...
timeout /t 3 /nobreak > nul

echo Step 4: Starting React frontend...
start "Frontend Server" cmd /k "cd frontend && npm start"

echo.
echo ✅ Both servers are starting!
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause > nul



