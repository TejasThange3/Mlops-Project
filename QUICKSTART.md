# 🚀 Quick Start Guide - Water Potability Prediction

## 🎯 Simplest Way to Run (Choose One)

### Option 1: One-Command Launch ⭐ EASIEST!

```powershell
.\launch.ps1
```

**Done!** Browser opens automatically to the beautiful web interface.

---

### Option 2: Python Script

```powershell
D:/Python/python.exe test_web_ui.py
```

Browser opens automatically!

---

### Option 3: Manual Start

```powershell
# Start server
D:/Python/python.exe -m uvicorn main:app --host 127.0.0.1 --port 8000

# Then open browser to: http://127.0.0.1:8000/
```

---

## 📋 Common Commands

### Run Web Interface

| Command                               | Description                                  |
| ------------------------------------- | -------------------------------------------- |
| `.\launch.ps1`                        | **Best**: Auto-starts server + opens browser |
| `D:/Python/python.exe test_web_ui.py` | Opens browser to web UI                      |

### Stop Server

Press `Ctrl + C` in terminal

### Retrain Model

```powershell
dvc repro
```

### View Metrics

```powershell
dvc metrics show
```

---

## 🆕 First-Time Setup (Only Once)

```powershell
# Install dependencies
pip install -r requirements.txt

# Train the model
dvc repro
```

---

## 🌐 Available URLs

- **Web Interface**: http://127.0.0.1:8000/
- **API Docs**: http://127.0.0.1:8000/docs
- **Health Check**: http://127.0.0.1:8000/health

---

## 💡 Quick Tips

- **Sample Data**: Press `Ctrl + L` in the web form
- **pH Range**: Keep between 5-10 for best results
- **Results**: Color-coded table with status badges

---

## 🛠️ Testing APIs (Optional)

### Test in Terminal

```powershell
# In a new terminal (while the API is running)
python test_api.py
```

### Option 2: Using cURL

#### Health Check

```powershell
curl http://localhost:8000/health
```

#### Make a Prediction

```powershell
curl -X POST "http://localhost:8000/predict" `
  -H "Content-Type: application/json" `
  -d '{
    "ph": 7.0,
    "Hardness": 200.0,
    "Solids": 20000.0,
    "Chloramines": 7.5,
    "Sulfate": 350.0,
    "Conductivity": 400.0,
    "Organic_carbon": 14.0,
    "Trihalomethanes": 70.0,
    "Turbidity": 4.0
  }'
```

### Option 3: Using Python Requests

```python
import requests

response = requests.post(
    "http://localhost:8000/predict",
    json={
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
)
print(response.json())
```

## Common Tasks

### Retrain the Model

```powershell
# Modify params.yaml, then:
dvc repro
```

### View Pipeline Status

```powershell
dvc status
```

### Compare Metrics

```powershell
dvc metrics diff
```

### View Pipeline DAG

```powershell
dvc dag
```

## Troubleshooting

### Issue: "Model file not found"

**Solution:** Run `dvc repro` to generate the model first.

### Issue: "Port 8000 already in use"

**Solution:** Use a different port:

```powershell
uvicorn main:app --port 8001
```

### Issue: "Import errors"

**Solution:** Ensure all dependencies are installed:

```powershell
pip install -r requirements.txt
```

## Next Steps

1. ✅ Explore the interactive API documentation at `/docs`
2. ✅ Try different water quality parameters
3. ✅ Modify hyperparameters in `params.yaml` and retrain
4. ✅ Check out the detailed README.md for more information

---

**Happy Predicting! 🌊**
