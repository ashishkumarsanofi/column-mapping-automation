"""
Simple batch script to create executable using auto-py-to-exe
This provides a GUI interface for creating executables
"""
import subprocess
import sys

def setup_auto2exe():
    """Install and run auto-py-to-exe"""
    
    print("Installing auto-py-to-exe...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "auto-py-to-exe"])
        
        print("\n🎯 Starting auto-py-to-exe GUI...")
        print("📋 In the GUI:")
        print("   1. Select 'app_launcher.py' as your script")
        print("   2. Choose 'One File'")
        print("   3. Choose 'Window Based (hide the console)'")
        print("   4. Add these additional files:")
        print("      - ui_sections.py")
        print("      - file_utils.py") 
        print("      - mapping_logic.py")
        print("   5. Click 'Convert .py to .exe'")
        
        subprocess.run([sys.executable, "-m", "auto_py_to_exe"])
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    setup_auto2exe()
