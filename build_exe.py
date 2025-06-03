"""
Build script to create executable for the Streamlit app
"""
import subprocess
import sys
import os

def create_executable():
    """Create executable using PyInstaller"""
    
    # Install PyInstaller if not present
    try:
        import PyInstaller
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--windowed",
        "--name=ColumnMappingTool",
        "--icon=icon.ico",  # Optional: add if you have an icon
        "--add-data=ui_sections.py;.",
        "--add-data=file_utils.py;.",
        "--add-data=mapping_logic.py;.",
        "--hidden-import=streamlit",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "app_launcher.py"
    ]
    
    # Remove icon parameter if no icon file exists
    if not os.path.exists("icon.ico"):
        cmd = [c for c in cmd if not c.startswith("--icon")]
    
    print("Building executable...")
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Executable created successfully!")
        print("📁 Find your app in the 'dist' folder: ColumnMappingTool.exe")
        print("\n📋 To distribute:")
        print("   1. Share the ColumnMappingTool.exe file")
        print("   2. Users just double-click to run!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")

if __name__ == "__main__":
    create_executable()
