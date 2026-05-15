"""
Quick Start Script for Vision Assistant
Automates setup and launches the application
"""

import subprocess
import sys
import os

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("\n📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "opencv-python", "ultralytics", "pyttsx3"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def test_modules():
    """Test individual modules"""
    print("\n🧪 Testing modules...")
    
    modules = [
        ("camera.py", "Camera module"),
        ("detector.py", "Detector module"), 
        ("audio.py", "Audio module")
    ]
    
    for module, name in modules:
        try:
            result = subprocess.run([sys.executable, module], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ {name} - OK")
            else:
                print(f"❌ {name} - Error: {result.stderr}")
                return False
        except subprocess.TimeoutExpired:
            print(f"⚠️  {name} - Test timeout (expected for camera)")
        except Exception as e:
            print(f"❌ {name} - Error: {e}")
            return False
    
    return True

def launch_application():
    """Launch the main application"""
    print("\n🚀 Launching Vision Assistant...")
    print("Controls:")
    print("  'q' - Quit")
    print("  'v' - Toggle voice")
    print("  'h' - Help")
    print("\nStarting in 3 seconds...")
    
    import time
    time.sleep(3)
    
    try:
        subprocess.run([sys.executable, "main.py"])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error running application: {e}")

def main():
    """Main setup and launch process"""
    print("🎯 Vision Assistant Quick Start")
    print("=" * 40)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check if we're in the right directory
    if not os.path.exists("main.py"):
        print("❌ main.py not found. Please run this script from the project directory.")
        return
    
    # Ask user what to do
    print("\nWhat would you like to do?")
    print("1. Install dependencies only")
    print("2. Test modules only") 
    print("3. Install dependencies and test")
    print("4. Install, test, and launch application")
    print("5. Launch application (skip tests)")
    
    try:
        choice = input("\nEnter choice (1-5): ").strip()
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled")
        return
    
    success = True
    
    if choice == "1":
        success = install_dependencies()
    elif choice == "2":
        success = test_modules()
    elif choice == "3":
        success = install_dependencies()
        if success:
            success = test_modules()
    elif choice == "4":
        success = install_dependencies()
        if success:
            success = test_modules()
        if success:
            launch_application()
    elif choice == "5":
        launch_application()
    else:
        print("❌ Invalid choice. Running full setup...")
        success = install_dependencies()
        if success:
            success = test_modules()
        if success:
            launch_application()
    
    if success and choice in ["1", "2", "3"]:
        print("\n✅ Setup completed successfully!")
        print("Run 'python main.py' to start the application")
    elif not success:
        print("\n❌ Setup failed. Please check the error messages above.")

if __name__ == "__main__":
    main()
