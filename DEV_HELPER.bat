@echo off
title Development Helper - Column Mapping Tool
echo.
echo ================================================
echo    Development Helper - Column Mapping Tool
echo ================================================
echo.

echo 📂 This script helps you manage the single-source files.
echo.
echo 🔧 Available options:
echo    1. Test the tool (runs from main directory)
echo    2. Update distribution package (copies files)
echo    3. View file locations
echo.

:menu
echo.
set /p choice="Enter your choice (1-3, or Q to quit): "

if /i "%choice%"=="1" goto test
if /i "%choice%"=="2" goto update
if /i "%choice%"=="3" goto info
if /i "%choice%"=="q" goto exit
if /i "%choice%"=="quit" goto exit

echo Invalid choice. Please try again.
goto menu

:test
echo.
echo 🚀 Starting development server...
echo 📍 Running from main directory (latest files)
set STREAMLIT_SERVER_MAX_UPLOAD_SIZE=1024
python -m streamlit run app.py
goto menu

:update
echo.
echo 📂 Updating distribution package with latest files...
copy app.py "CLEAN_DISTRIBUTION_PACKAGE\" >nul 2>&1
copy file_utils.py "CLEAN_DISTRIBUTION_PACKAGE\" >nul 2>&1
copy mapping_logic.py "CLEAN_DISTRIBUTION_PACKAGE\" >nul 2>&1
copy ui_sections.py "CLEAN_DISTRIBUTION_PACKAGE\" >nul 2>&1
copy requirements.txt "CLEAN_DISTRIBUTION_PACKAGE\" >nul 2>&1
echo ✅ Distribution package updated with latest files!
echo 📦 CLEAN_DISTRIBUTION_PACKAGE is now ready to share with team members
echo 💡 Team members can copy this entire folder and use RUN_MAPPING_TOOL.bat
goto menu

:info
echo.
echo 📁 File Management Information:
echo.
echo 🔧 MAIN DIRECTORY (You edit these):
echo    - app.py
echo    - file_utils.py  
echo    - mapping_logic.py
echo    - ui_sections.py
echo    - requirements.txt
echo.
echo 📦 DISTRIBUTION PACKAGE (Self-contained):
echo    - CLEAN_DISTRIBUTION_PACKAGE\
echo    - Contains ALL files needed to run
echo    - Can be shared as a complete folder
echo    - Team members don't need the main directory
echo.
echo 💡 Workflow:
echo    1. Edit files in main directory
echo    2. Test with option 1
echo    3. Update distribution with option 2
echo    4. Share entire CLEAN_DISTRIBUTION_PACKAGE folder with team
echo    5. Team members use the 3 batch files to run the tool
goto menu

:exit
echo.
echo 👋 Goodbye!
pause
