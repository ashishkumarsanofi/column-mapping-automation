"""
Simple and reliable launcher for the Column Mapping Tool
This version focuses on stability and proper process management
"""
import subprocess
import sys
import os
import webbrowser
import time
import signal

def main():
    """Launch the Streamlit app with simple, reliable approach"""
    print("🚀 Column Mapping Tool - Simple Launcher")
    print("=" * 50)
    
    # Set environment variables
    os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "1024"
    
    # Get the app.py path
    if getattr(sys, 'frozen', False):
        # Running as executable
        app_dir = sys._MEIPASS
    else:
        # Running as script
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app_path = os.path.join(app_dir, "app.py")
    
    if not os.path.exists(app_path):
        print(f"❌ Could not find app.py at: {app_path}")
        input("Press Enter to exit...")
        return
    
    print("✅ Found app.py")
    print("🔧 Starting Streamlit...")
    
    # Simple command - let Streamlit handle everything
    cmd = [sys.executable, "-m", "streamlit", "run", app_path]
    
    try:
        # Start the process and wait for it
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Stopped by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
