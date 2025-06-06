@echo off
title Column Mapping Tool
echo.
echo ================================================
echo    Advanced Column Mapping Tool Launcher
echo ================================================
echo.

REM Set environment variables
set STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1024
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

echo 🔧 Setting up environment...
echo 📁 Upload limit: 1024MB
echo.

REM Check if we're in the right directory
if not exist "..\app.py" (
    echo ❌ Error: app.py not found!
    echo Please make sure this file is in the Distribution Files folder
    echo and that app.py exists in the parent directory.
    pause
    exit /b 1
)

echo ✅ Found app.py
echo 🚀 Starting Streamlit server...
echo.
echo 📝 Instructions:
echo    - Your browser will open automatically
echo    - Close this window to stop the application
echo    - Press Ctrl+C to stop if needed
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Change to parent directory and run the app
cd /d "%~dp0.."
python -m streamlit run app.py

echo.
echo 👋 Application stopped.
pause
