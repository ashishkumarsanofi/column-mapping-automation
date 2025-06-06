"""
Simple build script for the Column Mapping Tool
Creates a reliable executable without complex configurations
"""
import subprocess
import sys
import os

def create_simple_executable():
    """Create a simple, reliable executable"""
    
    print("🔧 Installing PyInstaller if needed...")
    try:
        import PyInstaller
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    print("🔨 Building simple executable...")
    
    # Simple PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",
        "--name=ColumnMappingTool_Simple",
        "--add-data=../app.py;.",
        "--add-data=../ui_sections.py;.",
        "--add-data=../file_utils.py;.",
        "--add-data=../mapping_logic.py;.",
        "--noconfirm",
        "simple_launcher.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Simple executable created!")
        print("📁 Find your app: dist/ColumnMappingTool_Simple.exe")
        print("\n🎯 Instructions:")
        print("1. Double-click ColumnMappingTool_Simple.exe")
        print("2. Wait for Streamlit to start")
        print("3. Browser will open automatically")
        print("4. Close the console window to stop")
    except Exception as e:
        print(f"❌ Build failed: {e}")

if __name__ == "__main__":
    create_simple_executable()
