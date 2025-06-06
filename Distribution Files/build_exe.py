"""
Build script to create executable for the Streamlit app
Updated for latest changes including dynamic upload size handling
"""
import subprocess
import sys
import os

def create_executable():
    """Create executable using PyInstaller"""
    
    print("🔧 Installing required dependencies...")
    # Install PyInstaller if not present
    try:
        import PyInstaller
        print("✅ PyInstaller already installed")
    except ImportError:
        print("📦 Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Install other required packages
    required_packages = ["streamlit", "pandas", "openpyxl"]
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} already installed")
        except ImportError:
            print(f"📦 Installing {package}...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
      # PyInstaller command with enhanced configuration
    cmd = [
        "pyinstaller",
        "--onefile",
        "--console",  # Changed from --windowed to --console for debugging
        "--name=ColumnMappingTool",
        "--add-data=../ui_sections.py;.",
        "--add-data=../file_utils.py;.",
        "--add-data=../mapping_logic.py;.",
        "--add-data=../app.py;.",
        "--hidden-import=streamlit",
        "--hidden-import=pandas",
        "--hidden-import=openpyxl",
        "--hidden-import=xlrd",
        "--hidden-import=xlsxwriter",
        "--hidden-import=io",
        "--hidden-import=warnings",
        "--hidden-import=time",
        "--hidden-import=socket",
        "--hidden-import=subprocess",
        "--collect-data=streamlit",
        "--collect-submodules=streamlit",
        "--noconfirm",  # Overwrite without asking
        "app_launcher.py"
    ]
    
    print("🔨 Building executable...")
    print("📂 This may take a few minutes...")
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Executable created successfully!")
        print("📁 Find your app in the 'dist' folder: ColumnMappingTool.exe")
        print(f"📊 File size: ~{get_file_size('dist/ColumnMappingTool.exe')} MB")
        print("\n📋 Distribution Instructions:")
        print("   1. Copy 'ColumnMappingTool.exe' from the 'dist' folder")
        print("   2. Share this single file with users")
        print("   3. Users just double-click to run - no installation needed!")
        print("   4. The app will open in their default browser automatically")
        print("\n💡 Tips for sharing:")
        print("   • Upload to cloud storage (Google Drive, Dropbox, etc.)")
        print("   • Email as attachment (if file size allows)")
        print("   • Share via USB drive or network folder")
        print("   • Works on any Windows machine without Python installed")
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   • Make sure you're in the 'Distribution Files' folder")
        print("   • Try running: pip install pyinstaller streamlit pandas openpyxl")
        print("   • Check that all .py files exist in the parent directory")

def get_file_size(filepath):
    """Get file size in MB"""
    try:
        size_bytes = os.path.getsize(filepath)
        size_mb = size_bytes / (1024 * 1024)
        return f"{size_mb:.1f}"
    except FileNotFoundError:
        return "Unknown"

if __name__ == "__main__":
    create_executable()
