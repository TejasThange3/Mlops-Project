# 🔧 Troubleshooting Guide

## Common Issues and Solutions

### 1. DVC Issues

#### Problem: "DVC is not recognized"

**Solution:**

```powershell
pip install dvc
```

#### Problem: "DVC repository is not initialized"

**Solution:**

```powershell
dvc init --no-scm
```

#### Problem: "Stage X is not up to date"

**Solution:**

```powershell
dvc repro --force
```

#### Problem: "Cannot find data/water_quality.csv"

**Solution:**
Make sure the dataset is in the correct location:

```powershell
# Check if file exists
Test-Path "data/water_quality.csv"

# If not, copy from dataset folder
Copy-Item "dataset/water_potability.csv" "data/water_quality.csv"

# Add to DVC
dvc add data/water_quality.csv
```

---

### 2. Python/Package Issues

#### Problem: "ModuleNotFoundError: No module named 'X'"

**Solution:**

```powershell
# Reinstall all dependencies
pip install -r requirements.txt

# Or install specific package
pip install <package-name>
```

#### Problem: "scikit-learn version incompatibility"

**Solution:**

```powershell
pip install --upgrade scikit-learn
```

#### Problem: "xgboost import error"

**Solution:**

```powershell
pip install xgboost
# On Windows, you might need Visual C++ redistributable
```

---

### 3. Pipeline Execution Issues

#### Problem: "FileNotFoundError: [Errno 2] No such file or directory"

**Solution:**

```powershell
# Make sure you're in the project root
cd d:\Mlops-Project

# Run pipeline from root
dvc repro
```

#### Problem: "Missing values after preprocessing"

**Solution:**
Check your params.yaml imputation strategy:

```yaml
preprocess:
  imputation_strategy: "mean" # Try 'median' or 'most_frequent'
```

#### Problem: "Model training fails"

**Solution:**

- Check if training data exists: `data/train.csv`
- Verify params.yaml has valid parameters
- Run preprocessing first: `python src/preprocess.py`

---

### 4. FastAPI/API Issues

#### Problem: "Address already in use" (Port 8000 busy)

**Solution:**

```powershell
# Use a different port
uvicorn main:app --port 8001

# Or find and kill the process using port 8000
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process
```

#### Problem: "Model file not found at models/model.joblib"

**Solution:**

```powershell
# Train the model first
dvc repro train

# Or run training directly
python src/train.py
```

#### Problem: "uvicorn is not recognized"

**Solution:**

```powershell
pip install uvicorn[standard]
```

#### Problem: "422 Unprocessable Entity" when making predictions

**Solution:**

- Ensure all 9 features are provided in the request
- Check that feature names match exactly (case-sensitive)
- Verify data types are numeric

Example correct request:

```json
{
  "ph": 7.0,
  "Hardness": 200.0,
  "Solids": 20000.0,
  "Chloramines": 7.5,
  "Sulfate": 350.0,
  "Conductivity": 400.0,
  "Organic_carbon": 14.0,
  "Trihalomethanes": 70.0,
  "Turbidity": 4.0
}
```

---

### 5. API Testing Issues

#### Problem: "Connection refused" when running test_api.py

**Solution:**

```powershell
# Make sure the API is running first
python main.py

# Then in another terminal:
python test_api.py
```

#### Problem: "requests module not found"

**Solution:**

```powershell
pip install requests
```

---

### 6. Performance Issues

#### Problem: "Training takes too long"

**Solution:**
Reduce model complexity in params.yaml:

```yaml
train:
  n_estimators: 50 # Reduce from 100
  max_depth: 5 # Reduce from 10
```

#### Problem: "Out of memory during training"

**Solution:**

```yaml
preprocess:
  test_size: 0.3 # Use less training data
```

---

### 7. Windows-Specific Issues

#### Problem: "PowerShell execution policy error"

**Solution:**

```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

#### Problem: "Long path names error"

**Solution:**
Enable long paths in Windows:

```powershell
# Run as Administrator
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
```

---

### 8. Data Issues

#### Problem: "Dataset has too many missing values"

**Solution:**
The preprocessing script handles this automatically with imputation. Check your strategy:

```yaml
preprocess:
  imputation_strategy: "mean" # Try 'median' for better robustness
```

#### Problem: "Class imbalance warning"

**Solution:**
This is expected for water quality data. Consider:

- Using stratified sampling (already implemented)
- Adjusting class weights in the model
- Using oversampling/undersampling techniques

---

### 9. Metrics Issues

#### Problem: "metrics.json not found"

**Solution:**

```powershell
# Run evaluation stage
dvc repro evaluate

# Or run directly
python src/evaluate.py
```

#### Problem: "Low model accuracy"

**Solution:**

1. Try different model types in params.yaml
2. Tune hyperparameters
3. Add feature engineering
4. Check data quality and preprocessing

---

### 10. Git/Version Control Issues

#### Problem: "Git is not available"

**Solution:**
DVC can work without Git:

```powershell
dvc init --no-scm
```

#### Problem: "Large files in Git"

**Solution:**
They should be tracked by DVC, not Git. Check .gitignore:

```
/data/water_quality.csv
/models/model.joblib
```

---

## Quick Diagnostic Commands

### Check Python Environment

```powershell
python --version
pip list
```

### Check DVC Status

```powershell
dvc status
dvc dag
```

### Check File Structure

```powershell
Get-ChildItem -Recurse -Depth 2
```

### Check API Status

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Or in PowerShell
Invoke-RestMethod -Uri "http://localhost:8000/health"
```

### Verify Dependencies

```powershell
pip check
```

---

## Still Having Issues?

### Reset Everything

```powershell
# 1. Remove generated files
Remove-Item -Recurse data/train.csv, data/test.csv, models/*, metrics.json -ErrorAction SilentlyContinue

# 2. Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# 3. Run pipeline fresh
dvc repro --force
```

### Check Logs

Look for error messages in:

- Terminal output when running commands
- DVC logs in `.dvc/tmp/`
- API server logs (console output)

---

## Getting Help

1. Check the main README.md for detailed documentation
2. Review QUICKSTART.md for setup steps
3. Look at example code in test_api.py
4. Check DVC documentation: https://dvc.org/doc
5. Check FastAPI documentation: https://fastapi.tiangolo.com

---

**Remember**: Most issues can be resolved by ensuring you're in the correct directory and have all dependencies installed!
