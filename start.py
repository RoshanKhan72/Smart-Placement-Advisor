#!/usr/bin/env python3
import subprocess
import webbrowser
import time
import os

def main():
    print("🚀 Starting AI Smart Placement Advisor...")
    print("📱 The application will open automatically in your browser")
    print("⏳ Please wait...\n")
    
    # Change to the current directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # Start Streamlit in background
    process = subprocess.Popen([
        'streamlit', 'run', 'app.py', 
        '--server.headless=true',
        '--server.open=true'
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Wait a moment for the server to start
    time.sleep(3)
    
    # Open browser automatically
    try:
        webbrowser.open('http://localhost:8501')
        print("✅ Browser opened successfully!")
    except:
        print("⚠️ Could not open browser automatically")
        print("🌐 Please manually open: http://localhost:8501")
    
    print("\n🎯 AI Smart Placement Advisor is running!")
    print("📝 Press Ctrl+C to stop the server")
    
    # Keep the script running
    try:
        process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server...")
        process.terminate()
        print("✅ Server stopped")

if __name__ == "__main__":
    main()
