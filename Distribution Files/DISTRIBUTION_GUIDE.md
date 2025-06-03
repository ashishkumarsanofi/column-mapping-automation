# Column Mapping Tool - Distribution Guide

## 📦 Creating a Standalone Application

You have several options to package your Streamlit app for distribution:

### Option 1: PyInstaller Executable (Recommended)

**Benefits:** Single .exe file, no Python installation required

1. **Build the executable:**
   ```bash
   python build_exe.py
   ```

2. **Distribute:**
   - Share the `ColumnMappingTool.exe` file from the `dist` folder
   - Users just double-click to run!

### Option 2: Auto-py-to-exe (GUI Method)

**Benefits:** Easy GUI interface for building

1. **Setup:**
   ```bash
   python setup_gui_builder.py
   ```

2. **Configure in GUI:**
   - Script Location: `app_launcher.py`
   - One File: Yes
   - Console Window: No (Window Based)
   - Additional Files: Add all .py files

### Option 3: Portable Distribution

**Benefits:** Smaller size, requires Python on target machine

1. **Package files:**
   - Copy all `.py` files
   - Copy `requirements.txt`
   - Copy `run_app.bat`

2. **Distribute:**
   - Share the folder
   - Users run `run_app.bat`

## 📋 Distribution Checklist

### For .exe Distribution:
- ✅ Single file (`ColumnMappingTool.exe`)
- ✅ No dependencies required
- ✅ Works on Windows machines without Python

### For Portable Distribution:
- ✅ All Python files (`.py`)
- ✅ `requirements.txt`
- ✅ `run_app.bat` launcher
- ✅ User needs Python 3.8+ installed

## 🎯 User Instructions

### For .exe users:
1. Download `ColumnMappingTool.exe`
2. Double-click to run
3. Browser opens automatically
4. Close command window to stop

### For portable version users:
1. Download and extract the folder
2. Double-click `run_app.bat`
3. Browser opens automatically
4. Press Ctrl+C in command window to stop

## 🔧 Advanced Options

### Custom Icon:
- Add `icon.ico` to your folder
- Rebuild with `python build_exe.py`

### Optimize Size:
- Use `--onefile` flag (included)
- Exclude unused modules with `--exclude-module`

### Cross-Platform:
- Use `cx_Freeze` for Linux/Mac compatibility
- Consider Docker containers for universal deployment
