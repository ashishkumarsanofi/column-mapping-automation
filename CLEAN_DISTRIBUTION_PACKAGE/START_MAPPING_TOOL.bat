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

REM Check if application files exist
echo 📂 Checking application files...
if not exist "app.py" (
    echo ❌ Error: app.py not found!
    echo Please make sure all application files are in this folder.
    pause
    exit /b 1
)

echo ✅ Application files found
echo 🚀 Starting Streamlit server...
echo.
echo 📝 Instructions:
echo    - Your browser will open automatically
echo    - Close this window to stop the application
echo    - Press Ctrl+C to stop if needed
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Run the app from the distribution directory (with copied files)
python -m streamlit run app.py

echo.
echo 👋 Application stopped.
pause
