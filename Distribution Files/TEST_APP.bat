@echo off
title Test Column Mapping Tool
echo.
echo 🧪 Testing Column Mapping Tool Executable...
echo.
echo This will start the app for 30 seconds and then stop it automatically.
echo Watch for any error messages in the console.
echo.
pause

echo.
echo 🚀 Starting ColumnMappingTool.exe...
echo.

REM Start the executable in the background
start /min "ColumnMappingTool" "dist\ColumnMappingTool.exe"

REM Wait 30 seconds
echo ⏳ Waiting 30 seconds to test startup...
timeout /t 30 /nobreak

REM Stop the process
echo.
echo 🛑 Stopping test...
taskkill /F /IM "ColumnMappingTool.exe" 2>nul

echo.
echo ✅ Test complete! 
echo.
echo If you saw the Streamlit app start in your browser, the fix worked!
echo If you got connection errors, we need to investigate further.
echo.
pause
