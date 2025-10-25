# Force Clear Cache and Reopen Browser

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "  🧹 CLEARING BROWSER CACHE & REOPENING" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Kill all browser processes to force fresh start
Write-Host "🛑 Closing all browser windows..." -ForegroundColor Yellow
Get-Process chrome -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process msedge -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Get-Process firefox -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue
Start-Sleep -Seconds 2

Write-Host "✅ Browsers closed" -ForegroundColor Green
Write-Host ""

# Open test page first
Write-Host "🧪 Opening test page to verify buttons render..." -ForegroundColor Cyan
Start-Process "http://127.0.0.1:8000/static/test-buttons.html"
Start-Sleep -Seconds 3

Write-Host ""
Write-Host "👆 The TEST PAGE should show what the buttons look like" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter when you can see the test page buttons..."

# Now open main page in incognito/private mode (no cache)
Write-Host ""
Write-Host "🚀 Opening main page in INCOGNITO mode (no cache)..." -ForegroundColor Cyan

# Try Chrome incognito
$chromePaths = @(
    "C:\Program Files\Google\Chrome\Application\chrome.exe",
    "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe"
)

$chromeFound = $false
foreach ($path in $chromePaths) {
    if (Test-Path $path) {
        Write-Host "✅ Opening in Chrome Incognito..." -ForegroundColor Green
        Start-Process $path -ArgumentList "--incognito", "http://127.0.0.1:8000/"
        $chromeFound = $true
        break
    }
}

if (-not $chromeFound) {
    # Fallback to Edge InPrivate
    Write-Host "✅ Opening in Edge InPrivate..." -ForegroundColor Green
    Start-Process "msedge" -ArgumentList "--inprivate", "http://127.0.0.1:8000/"
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host "  ✅ BOTH PAGES OPENED" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "📋 WHAT YOU SHOULD SEE:" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Tab 1: Test Page" -ForegroundColor Yellow
Write-Host "    - Shows example buttons" -ForegroundColor White
Write-Host "    - Proves buttons CAN render" -ForegroundColor White
Write-Host ""
Write-Host "  Tab 2: Main Page (Incognito)" -ForegroundColor Yellow
Write-Host "    - At TOP: Model version dropdown + refresh button" -ForegroundColor White
Write-Host "    - After prediction: Retrain buttons (scroll down)" -ForegroundColor White
Write-Host ""
Write-Host "🔍 IF YOU STILL DON'T SEE BUTTONS:" -ForegroundColor Red
Write-Host "    1. Press F12 (Developer Tools)" -ForegroundColor White
Write-Host "    2. Look for RED errors in Console" -ForegroundColor White
Write-Host "    3. Tell me what the error says" -ForegroundColor White
Write-Host ""
