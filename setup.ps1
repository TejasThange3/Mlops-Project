# Setup Script for Water Potability Prediction Project
# This script installs dependencies and runs the initial pipeline

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Water Potability Prediction Setup" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Install dependencies
Write-Host "[1/3] Installing Python dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 2: Run DVC pipeline
Write-Host "[2/3] Running DVC pipeline (preprocess → train → evaluate)..." -ForegroundColor Yellow
dvc repro

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Pipeline completed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Pipeline failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Step 3: Show metrics
Write-Host "[3/3] Showing evaluation metrics..." -ForegroundColor Yellow
dvc metrics show

Write-Host ""
Write-Host "=================================" -ForegroundColor Cyan
Write-Host "Setup Complete! 🎉" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Start the API: python main.py" -ForegroundColor White
Write-Host "  2. Open Swagger docs: http://localhost:8000/docs" -ForegroundColor White
Write-Host "  3. Test predictions using the interactive UI" -ForegroundColor White
Write-Host ""
