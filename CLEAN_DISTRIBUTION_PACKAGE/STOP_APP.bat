@echo off
title Stop Column Mapping Tool
color 0C
echo.
echo ================================================
echo       EMERGENCY STOP - Column Mapping Tool
echo ================================================
echo.

echo 🛑 Stopping all Column Mapping Tool processes...
echo.

REM Stop any ColumnMappingTool executables
echo Stopping ColumnMappingTool executables...
taskkill /F /IM "ColumnMappingTool.exe" 2>nul
taskkill /F /IM "ColumnMappingTool_Simple.exe" 2>nul

REM Stop Streamlit processes
echo Stopping Streamlit processes...
taskkill /F /IM "streamlit.exe" 2>nul

REM Stop Python processes running Streamlit
echo Stopping Python-Streamlit processes...
for /f "tokens=2" %%i in ('tasklist /fo csv ^| findstr /i "python.exe" ^| findstr /i "streamlit"') do (
    taskkill /F /PID %%i 2>nul
)

REM Use WMIC to stop processes by command line
echo Stopping processes by command line...
wmic process where "commandline like '%%streamlit%%'" delete 2>nul
wmic process where "commandline like '%%app.py%%'" delete 2>nul

REM Kill any remaining Python processes that might be hanging
echo Final cleanup...
timeout /t 2 /nobreak >nul

echo.
echo ✅ All processes stopped!
echo.
echo 📝 Notes:
echo    - All Column Mapping Tool processes have been terminated
echo    - You may need to manually close any remaining browser tabs
echo    - If issues persist, restart your computer
echo.
echo Press any key to exit...
pause >nul
