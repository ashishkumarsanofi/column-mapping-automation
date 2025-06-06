@echo off
title Column Mapping Tool - Smart Launcher
color 0B
echo.
echo ================================================
echo    🚀 Column Mapping Tool - Smart Launcher
echo ================================================
echo.

REM Check if Python is installed
echo 🔍 Checking for Python installation...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not found in PATH!
    echo.
    echo 📥 Please install Python first:
    echo    1. Go to: https://www.python.org/downloads/
    echo    2. Download Python 3.8 or newer
    echo    3. During installation, check "Add Python to PATH"
    echo    4. After installation, restart this script
    echo.
    echo 💡 Alternative: Install from Microsoft Store
    echo    - Search "Python" in Microsoft Store
    echo    - Install "Python 3.12" or newer
    echo.
    echo 🌐 Opening Python download page...
    start https://www.python.org/downloads/
    echo.
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% found!
echo.

REM Check if pip is available
echo 🔍 Checking for pip (package installer)...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip not found! Python installation may be incomplete.
    echo Please reinstall Python and ensure pip is included.
    pause
    exit /b 1
)
echo ✅ pip is available!
echo.

REM Check if this is first run (check for installed packages)
echo 🔍 Checking for required packages...

REM Use pip list to check for packages (more reliable)
python -m pip show streamlit >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Streamlit...
    python -m pip install streamlit --quiet
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Streamlit. Check your internet connection.
        pause
        exit /b 1
    )
    echo ✅ Streamlit installed!
)

python -m pip show pandas >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing Pandas...
    python -m pip install pandas --quiet
    if %errorlevel% neq 0 (
        echo ❌ Failed to install Pandas. Check your internet connection.
        pause
        exit /b 1
    )
    echo ✅ Pandas installed!
)

python -m pip show openpyxl >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 Installing OpenPyXL...
    python -m pip install openpyxl --quiet
    if %errorlevel% neq 0 (
        echo ❌ Failed to install OpenPyXL. Check your internet connection.
        pause
        exit /b 1
    )
    echo ✅ OpenPyXL installed!
)

echo ✅ All required packages are ready!
echo.

REM Set environment variables
echo 🔧 Setting up environment...
set STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1024
set STREAMLIT_BROWSER_GATHER_USAGE_STATS=false
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
echo ✅ Application files found!
echo.

echo 🚀 Starting Column Mapping Tool...
echo.
echo 📝 Instructions:
echo    - Your browser will open automatically
echo    - Close this window to stop the application
echo    - Press Ctrl+C to stop if needed
echo.
echo ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
echo.

REM Add a small delay to ensure everything is ready
timeout /t 2 /nobreak >nul

REM Run the application
echo Starting Streamlit server...
python -m streamlit run app.py

echo.
echo 👋 Application stopped.
echo Press any key to exit...
pause >nul
