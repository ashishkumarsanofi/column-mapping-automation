# Column Mapping Tool - Single Source Management

This directory contains the **single source** version of the Column Mapping Tool - you only need to edit files here!

## Quick Start for Team Members 🚀
**Want to use the tool? Go to the `CLEAN_DISTRIBUTION_PACKAGE` folder and follow the instructions in `README_FIRST.txt`.**

## New Corrected Structure ✨
**Fixed the sharing issue!** 
- **Main Directory**: Source files you edit (app.py, ui_sections.py, etc.)
- **CLEAN_DISTRIBUTION_PACKAGE**: Complete self-contained package with all files

## For Developers 🛠️
1. **Edit files**: Only edit files in this main directory
2. **Test changes**: Run `DEV_HELPER.bat` → Option 1 (or `streamlit run app.py`)
3. **Update distribution**: Run `DEV_HELPER.bat` → Option 2 (copies files to package)
4. **Share with team**: Give them the entire `CLEAN_DISTRIBUTION_PACKAGE` folder

## Benefits ✅
- Edit once, sync to distribution package
- Distribution package is completely self-contained
- Team members get everything they need in one folder
- No dependency on parent directories

## Files You Edit (Main Directory)
- `app.py` - Main application
- `ui_sections.py` - UI components  
- `file_utils.py` - File utilities
- `mapping_logic.py` - Core logic
- `requirements.txt` - Dependencies

## Files Auto-Updated (Distribution Package)
The `CLEAN_DISTRIBUTION_PACKAGE` contains user guides and batch scripts. Python files are automatically copied from main directory when needed.
