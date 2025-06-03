@echo off
echo 🚀 Column Mapping Tool - Portable Version
echo.

REM Check if Python is available
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python not found. Please install Python 3.8+ first.
    echo 📥 Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install requirements if needed
echo 📦 Checking dependencies...
pip install -r requirements.txt --quiet

REM Find free port
set /a PORT=8501
echo 🌐 Starting app on port %PORT%...
echo 📝 Press Ctrl+C to stop the application
echo.

REM Start Streamlit
start "" http://localhost:%PORT%
streamlit run app.py --server.port %PORT% --browser.gatherUsageStats false

pause
