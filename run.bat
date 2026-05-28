

@echo off
echo Starting AI Smart Placement Advisor...
echo.
echo Installing dependencies...
pip install -r requirements.txt
echo.
echo Starting backend server...
start http://127.0.0.1:5000
python backend.py
pause
