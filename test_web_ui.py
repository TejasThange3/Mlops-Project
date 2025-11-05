"""
Water Potability API - Browser Test
Automatically opens the web interface in Chrome browser
"""

import webbrowser
import time
import requests
import sys
import os

API_URL = "http://127.0.0.1:8000"
FRONTEND_URL = f"{API_URL}/"

def check_server_running():
    """Check if the API server is running"""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def wait_for_server(max_attempts=10, delay=1):
    """Wait for server to start"""
    print("🔍 Checking if server is running...")
    for attempt in range(max_attempts):
        if check_server_running():
            print("✅ Server is running!")
            return True
        print(f"⏳ Waiting for server... ({attempt + 1}/{max_attempts})")
        time.sleep(delay)
    return False

def open_browser():
    """Open the web interface in Chrome"""
    print(f"\n🌐 Opening web interface in browser...")
    print(f"📍 URL: {FRONTEND_URL}")
    
    try:
        # Try to open in Chrome specifically
        chrome_path = None
        
        # Common Chrome paths
        chrome_paths = [
            'C:/Program Files/Google/Chrome/Application/chrome.exe',
            'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
            r'C:\Users\%USERNAME%\AppData\Local\Google\Chrome\Application\chrome.exe'
        ]
        
        for path in chrome_paths:
            if os.path.exists(path.replace('%USERNAME%', os.environ.get('USERNAME', ''))):
                chrome_path = path.replace('%USERNAME%', os.environ.get('USERNAME', ''))
                break
        
        if chrome_path:
            webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(chrome_path))
            webbrowser.get('chrome').open(FRONTEND_URL, new=2)
        else:
            # Fallback to default browser
            webbrowser.open(FRONTEND_URL, new=2)
        
        print("✅ Browser opened successfully!")
        print("\n" + "="*60)
        print("🎉 Water Potability Prediction System")
        print("="*60)
        print(f"📱 Frontend:  {FRONTEND_URL}")
        print(f"📚 API Docs:  {API_URL}/docs")
        print(f"💚 Health:    {API_URL}/health")
        print("="*60)
        print("\n💡 Tips:")
        print("  - Enter pH value between 5-10 for best results")
        print("  - All fields are required for prediction")
        print("  - Results will show in a beautiful table")
        print("  - Press Ctrl+L to load sample data")
        print("\n✨ Enjoy using the Water Potability Prediction System!")
        return True
    except Exception as e:
        print(f"❌ Error opening browser: {e}")
        print(f"💡 Please manually open: {FRONTEND_URL}")
        return False

def main():
    """Main function"""
    import os
    
    print("="*60)
    print("🚀 Water Potability Prediction - Browser Test")
    print("="*60)
    
    # Check if server is running
    if not check_server_running():
        print("\n❌ Server is not running!")
        print("\n📝 Please start the server first:")
        print("   D:/Python/python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000")
        print("\n   Or run in separate PowerShell window:")
        print("   Start-Job -ScriptBlock { Set-Location 'd:\\Mlops-Project'; & 'D:/Python/python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000 }")
        sys.exit(1)
    
    # Open browser
    open_browser()
    
    print("\n🎯 Test the application:")
    print("  1. Enter water quality parameters")
    print("  2. Click 'Predict Water Quality' button")
    print("  3. View beautiful results with confidence score")
    print("\n✋ Press Ctrl+C to exit this script (server will keep running)")
    
    try:
        # Keep script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n\n👋 Test script stopped. Server is still running.")
        print("💡 To stop the server, close the server terminal window.")

if __name__ == "__main__":
    main()
