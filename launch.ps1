# Water Potability Prediction System - Quick Launcher
# This script starts the server and opens the web interface automatically

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 Water Potability Prediction System - Launcher" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Navigate to project directory
Set-Location "d:\Mlops-Project"

Write-Host "📂 Project Directory: $PWD" -ForegroundColor Green
Write-Host ""

# Check if Python is available
Write-Host "🔍 Checking Python..." -ForegroundColor Yellow
$pythonPath = "D:/Python/python.exe"
if (Test-Path $pythonPath) {
    Write-Host "✅ Python found: $pythonPath" -ForegroundColor Green
} else {
    Write-Host "❌ Python not found at: $pythonPath" -ForegroundColor Red
    Write-Host "Please update the path in this script." -ForegroundColor Yellow
    pause
    exit
}

Write-Host ""
Write-Host "🚀 Starting FastAPI server..." -ForegroundColor Yellow

# Start the server in a background job
$job = Start-Job -ScriptBlock {
    Set-Location 'd:\Mlops-Project'
    & 'D:/Python/python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000
}

Write-Host "⏳ Waiting for server to start (5 seconds)..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check if server is running
try {
    $response = Invoke-RestMethod -Uri "http://127.0.0.1:8000/health" -Method GET -TimeoutSec 2
    Write-Host "✅ Server is running!" -ForegroundColor Green
    Write-Host "   Status: $($response.status)" -ForegroundColor Green
    Write-Host "   Model Loaded: $($response.model_loaded)" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Server might not be fully ready yet..." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🌐 Opening web interface in browser..." -ForegroundColor Cyan
Start-Sleep -Seconds 1

# Open browser
Start-Process "http://127.0.0.1:8000/"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🎉 System is Ready!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "📱 Frontend:    http://127.0.0.1:8000/" -ForegroundColor White
Write-Host "📚 API Docs:    http://127.0.0.1:8000/docs" -ForegroundColor White
Write-Host "💚 Health:      http://127.0.0.1:8000/health" -ForegroundColor White
Write-Host "🔧 API Root:    http://127.0.0.1:8000/api" -ForegroundColor White
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "💡 Usage Instructions:" -ForegroundColor Yellow
Write-Host "  1. Browser window should open automatically" -ForegroundColor White
Write-Host "  2. Enter water quality parameters (all 9 fields)" -ForegroundColor White
Write-Host "  3. Click 'Predict Water Quality' button" -ForegroundColor White
Write-Host "  4. View results in beautiful table format" -ForegroundColor White
Write-Host ""
Write-Host "⌨️  Keyboard Shortcuts:" -ForegroundColor Yellow
Write-Host "  - Ctrl + L: Load sample data" -ForegroundColor White
Write-Host ""
Write-Host "🛑 To stop the server:" -ForegroundColor Yellow
Write-Host "  - Close this PowerShell window" -ForegroundColor White
Write-Host "  - Or press Ctrl+C" -ForegroundColor White
Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "✨ Enjoy using the Water Potability Prediction System!" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key to view server logs or Ctrl+C to exit..." -ForegroundColor Yellow

# Wait for user input
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

Write-Host ""
Write-Host "📊 Server Logs:" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Show server output
Receive-Job -Job $job

Write-Host ""
Write-Host "⏸️  Press Ctrl+C to stop the server and exit..." -ForegroundColor Yellow

# Keep script running and show live logs
while ($true) {
    Start-Sleep -Seconds 2
    $output = Receive-Job -Job $job
    if ($output) {
        Write-Host $output
    }
}
