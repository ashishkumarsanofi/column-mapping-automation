# 📦 Distribution Files

This folder contains all the files needed to create distributable versions of your Streamlit Column Mapping Tool.

## 📂 Files in This Folder:

### 🚀 **Main Distribution Scripts:**
- **`app_launcher.py`** - Launcher script that starts Streamlit and opens browser
- **`build_exe.py`** - Automated script to create a single executable using PyInstaller
- **`setup_gui_builder.py`** - GUI tool for building executables using auto-py-to-exe
- **`run_app.bat`** - Batch file for portable distribution (requires Python)

### 📚 **Documentation:**
- **`DISTRIBUTION_GUIDE.md`** - Complete guide with instructions for all distribution methods
- **`README.md`** - This file explaining the folder contents

## 🎯 Quick Start:

### Option 1: Create Single Executable (Recommended)
```powershell
cd "Distribution Files"
python build_exe.py
```
This creates `ColumnMappingTool.exe` in the `dist` folder.

### Option 2: GUI Builder
```powershell
cd "Distribution Files"  
python setup_gui_builder.py
```
Opens a visual interface to configure and build the executable.

### Option 3: Portable Version
```powershell
cd "Distribution Files"
./run_app.bat
```
Runs the app directly (requires Python installation).

## 📋 Main Streamlit App Files:
These files remain in the parent directory:
- `app.py` - Main Streamlit application
- `ui_sections.py` - UI components
- `file_utils.py` - File handling utilities  
- `mapping_logic.py` - Core mapping logic
- `requirements.txt` - Python dependencies

## 🔄 How It Works:

1. **Distribution files** (this folder) handle packaging and launching
2. **Main app files** (parent folder) contain your actual Streamlit application
3. When building executables, the distribution scripts include the main app files
4. When running, the launcher finds and starts the main `app.py` from the parent directory

This separation keeps your main development files clean while providing all the distribution options in one organized location!
