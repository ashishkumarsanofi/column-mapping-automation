"""
Launcher script for the Streamlit app when packaged as executable
"""
import subprocess
import sys
import os
import webbrowser
import time
import socket
from threading import Timer

def find_free_port():
    """Find a free port for the Streamlit server"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        s.listen(1)
        port = s.getsockname()[1]
    return port

def open_browser(url):
    """Open browser after a short delay"""
    time.sleep(2)
    webbrowser.open(url)

def main():
    """Launch the Streamlit app"""
    # Find a free port
    port = find_free_port()
    url = f"http://localhost:{port}"
    
    print(f"🚀 Starting Column Mapping Tool...")
    print(f"🌐 Opening browser at: {url}")
    print("📝 Close this window to stop the application")
    
    # Schedule browser opening
    Timer(2.0, open_browser, [url]).start()
      # Get the directory where the script is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = sys._MEIPASS
    else:
        # Running as script - look in parent directory
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    app_path = os.path.join(app_dir, "app.py")
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            app_path,
            "--server.port", str(port),
            "--server.headless", "true",
            "--browser.gatherUsageStats", "false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
