@echo off
title Column Mapping Tool - Setup
color 0A
echo.
echo ================================================
echo    Column Mapping Tool - First Time Setup
echo ================================================
echo.

echo 🔧 Installing required dependencies...
echo.
echo This will install: streamlit, pandas, openpyxl
echo.

REM Check if pip is available
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Error: Python or pip not found!
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org
    echo 2. Download Python 3.7 or higher
    echo 3. During installation, check "Add to PATH"
    echo 4. Restart your computer
    echo 5. Run this setup again
    echo.
    pause
    exit /b 1
)

echo ✅ Python found, installing packages...
echo.

REM Install requirements
python -m pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ✅ Setup completed successfully!
    echo.
    echo 🚀 You can now run the tool by double-clicking:
    echo    START_MAPPING_TOOL.bat
    echo.
) else (
    echo.
    echo ❌ Setup failed!
    echo.
    echo Please try running this command manually:
    echo pip install streamlit pandas openpyxl
    echo.
)

echo.
pause
