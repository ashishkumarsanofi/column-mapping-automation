"""
Launcher script for the Streamlit app when packaged as executable
Fixed version to prevent infinite browser tabs and process issues
"""
import subprocess
import sys
import os
import time
import socket
import signal
import atexit
import threading
import webbrowser

# Global variable to track the Streamlit process
streamlit_process = None

def find_free_port(start_port=8501):
    """Find a free port for the Streamlit server starting from a specific port"""
    port = start_port
    while port < start_port + 100:  # Try up to 100 ports
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            port += 1
    raise RuntimeError("Could not find a free port")

def cleanup_process():
    """Clean up the Streamlit process when exiting"""
    global streamlit_process
    if streamlit_process and streamlit_process.poll() is None:
        print("\n🧹 Cleaning up Streamlit process...")
        try:
            streamlit_process.terminate()
            streamlit_process.wait(timeout=5)
        except:
            try:
                streamlit_process.kill()
            except:
                pass

def open_browser_delayed(url, delay=5):
    """Open browser after a delay to ensure server is ready"""
    def open_browser():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 Browser opened at: {url}")
        except Exception as e:
            print(f"⚠️ Could not open browser: {e}")
            print(f"🔗 Please manually open: {url}")
    
    thread = threading.Thread(target=open_browser, daemon=True)
    thread.start()

def main():
    """Launch the Streamlit app"""
    global streamlit_process
    
    print("🚀 Starting Advanced Column Mapping & Transformation Tool...")
    print("📊 Initializing application components...")
    print("━" * 50)
    
    # Register cleanup function
    atexit.register(cleanup_process)
    
    # Set upload size limit (1024MB as configured in app.py)
    os.environ["STREAMLIT_SERVER_MAX_UPLOAD_SIZE"] = "1024"
    
    # Get the directory where the script is located
    if getattr(sys, 'frozen', False):
        # Running as compiled executable
        app_dir = sys._MEIPASS
        print("📦 Running from executable")
    else:
        # Running as script - look in parent directory
        app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        print("🐍 Running from script")
    
    app_path = os.path.join(app_dir, "app.py")
    
    # Check if app.py exists
    if not os.path.exists(app_path):
        print(f"❌ Could not find app.py at: {app_path}")
        print("📁 Files in app directory:")
        try:
            for file in os.listdir(app_dir):
                print(f"   - {file}")
        except Exception as e:
            print(f"   Error listing directory: {e}")
        input("Press Enter to exit...")
        return
    
    # Find a free port
    try:
        port = find_free_port()
        url = f"http://localhost:{port}"
        print(f"🌐 Server will start at: {url}")
        print("📁 File upload limit: 1024MB per file")
        print("📝 Press Ctrl+C or close this window to stop the application")
        print("━" * 50)
    except RuntimeError as e:
        print(f"❌ {e}")
        input("Press Enter to exit...")
        return
    
    try:
        # Launch Streamlit with proper configuration
        cmd = [
            sys.executable, "-m", "streamlit", "run", 
            app_path,
            "--server.port", str(port),
            "--server.address", "localhost",
            "--browser.gatherUsageStats", "false",
            "--server.headless", "true",  # Don't let Streamlit open browser
            "--server.runOnSave", "false",
            "--server.allowRunOnSave", "false"
        ]
        
        print("🔧 Starting Streamlit server...")
        print("⏳ This may take a moment...")
        
        # Start the process without waiting for it to complete
        streamlit_process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == 'nt' else 0
        )
        
        # Open browser after a delay
        open_browser_delayed(url, delay=3)
        
        print("✅ Streamlit server started!")
        print(f"🌐 Your app should open at: {url}")
        print("📝 Press Ctrl+C to stop the application")
        print("━" * 50)
        
        # Wait for the process to complete or be interrupted
        try:
            streamlit_process.wait()
        except KeyboardInterrupt:
            print("\n👋 Application stopped by user")
            cleanup_process()
        
    except FileNotFoundError:
        print("❌ Python or Streamlit not found!")
        print("🔧 Make sure Python and Streamlit are installed")
        input("Press Enter to exit...")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"🔗 If the browser didn't open, go to: {url}")
        input("Press Enter to exit...")
    finally:
        cleanup_process()

if __name__ == "__main__":
    main()
