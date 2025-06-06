@echo off
echo Testing package detection...

python -c "import streamlit" >nul 2>&1
set streamlit_installed=%errorlevel%
echo Streamlit check: %streamlit_installed%

python -c "import pandas" >nul 2>&1  
set pandas_installed=%errorlevel%
echo Pandas check: %pandas_installed%

python -c "import openpyxl" >nul 2>&1
set openpyxl_installed=%errorlevel%
echo OpenPyXL check: %openpyxl_installed%

if %streamlit_installed% equ 0 if %pandas_installed% equ 0 if %openpyxl_installed% equ 0 (
    echo All packages found!
) else (
    echo Some packages missing!
)

echo Test complete - press any key...
pause
