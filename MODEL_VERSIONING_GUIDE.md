# 🚀 Model Retraining & Versioning Feature Guide

## ✨ New Features Added

Your Water Potability Prediction System now includes **advanced model management** capabilities:

### 🎯 Key Features

1. **🔄 Incremental Retraining** - Improve the model with user feedback
2. **📦 Version Management** - Switch between different model versions
3. **📊 Version Tracking** - Track accuracy and samples for each version
4. **🎨 Beautiful UI** - Two new buttons integrated seamlessly

---

## 🖥️ How to Use the New Features

### Step 1: Start the Application

```powershell
# Option 1: Use the launcher
.\launch.ps1

# Option 2: Manual start
Start-Job -ScriptBlock {
    Set-Location 'd:\Mlops-Project'
    & 'D:/Python/python.exe' -m uvicorn main:app --host 127.0.0.1 --port 8000
}
Start-Sleep -Seconds 5
Start-Process "http://127.0.0.1:8000/"
```

### Step 2: Make a Prediction

1. Open **http://127.0.0.1:8000/** in your browser
2. Enter water quality parameters (or press `Ctrl + L` for sample data)
3. Click **"🔮 Predict Water Quality"**
4. View the prediction results

### Step 3: Use Model Versioning

#### 🤖 Active Model Selector (Top of Page)

At the top of the page, you'll see:

```
🤖 Active Model: [Original (Ensemble) ▼] 🔄
```

**Features:**

- **Dropdown**: Shows all available model versions
- **Version Info**: Displays samples count and CV accuracy
- **Refresh Button** (🔄): Updates the list of versions
- **Auto-select**: Current version is pre-selected

**How to Switch:**

1. Click the dropdown
2. Select a version (Original, V1, V2, V3...)
3. Version switches automatically
4. A notification confirms the switch
5. Future predictions use the selected version

### Step 4: Retrain the Model

After making a prediction, scroll down to see:

```
🎯 Help Improve the Model
Was this prediction correct? Help us retrain the model with your feedback!

What is the actual result?
[✅ Water is Potable]  [⛔ Water is Not Potable]
```

**How to Retrain:**

1. Make a prediction first
2. Scroll to the "Help Improve the Model" section
3. Click the button that matches the **actual** result:
   - **✅ Water is Potable** - If water is actually safe
   - **⛔ Water is Not Potable** - If water is actually unsafe
4. Wait for retraining (takes 30-60 seconds)
5. A notification shows success with new version info
6. The new version is automatically activated
7. Version dropdown updates with the new version

---

## 📊 Understanding Model Versions

### Version Naming

- **Original**: The base ensemble model (RF + XGBoost + GB)
- **V1, V2, V3...**: Incrementally retrained versions

### Version Information

Each version tracks:

- **Training Samples**: Total number of samples used
- **Incremental Samples**: New samples added in this version
- **Training Accuracy**: Performance on training data
- **CV Accuracy**: Cross-validation accuracy (real performance)
- **Created At**: Timestamp of creation
- **Description**: What changed in this version

### Example Workflow

```
1. Start with "Original" (2,293 samples, 64.24% CV)
2. Make prediction → Retrain with correct label
3. "V1" created (2,294 samples, ~64.3% CV)
4. Make another prediction → Retrain again
5. "V2" created (2,295 samples, ~64.4% CV)
6. Switch back to "Original" to compare
7. Switch to "V2" to use latest model
```

---

## 🔧 API Endpoints

### List All Versions

```http
GET /models/versions
```

**Response:**

```json
{
  "current_version": "V1",
  "total_versions": 2,
  "versions": [
    {
      "version": "Original",
      "created_at": "2025-10-08T...",
      "training_samples": 2293,
      "accuracy": 0.8439,
      "cv_accuracy": 0.6424,
      "is_current": false
    },
    {
      "version": "V1",
      "created_at": "2025-10-08T...",
      "training_samples": 2294,
      "incremental_samples": 1,
      "accuracy": 0.8445,
      "cv_accuracy": 0.6428,
      "is_current": true
    }
  ]
}
```

### Get Current Model

```http
GET /models/current
```

### Switch Version

```http
POST /models/switch
Content-Type: application/json

{
  "version": "V1"
}
```

### Retrain Model

```http
POST /retrain
Content-Type: application/json

{
  "water_quality": {
    "ph": 7.0,
    "Hardness": 200.0,
    "Solids": 20000.0,
    "Chloramines": 7.5,
    "Sulfate": 350.0,
    "Conductivity": 400.0,
    "Organic_carbon": 14.0,
    "Trihalomethanes": 70.0,
    "Turbidity": 4.0
  },
  "actual_potability": 1
}
```

**Response:**

```json
{
  "success": true,
  "version": "V1",
  "training_samples": 2294,
  "incremental_samples": 1,
  "accuracy": 0.8445,
  "cv_accuracy": 0.6428,
  "message": "Model V1 trained successfully with 2294 samples"
}
```

---

## 📁 File Structure

### New Files Added

```
src/
  model_manager.py          # Model versioning logic

models/
  versions/
    metadata.json           # Version tracking metadata
    incremental_training_data.csv  # New training samples
    model_V1.joblib        # Version 1 model
    scaler_V1.joblib       # Version 1 scaler
    model_V2.joblib        # Version 2 model
    scaler_V2.joblib       # Version 2 scaler
    ...

test_versioning.py         # API testing script
```

### Updated Files

```
main.py                    # Added 4 new endpoints
static/index.html          # Added 2 new UI sections
static/css/style.css       # Added ~300 lines of styling
static/js/app.js           # Added versioning functions
```

---

## 🎨 UI Features

### Model Version Selector

- **Location**: Top of page, below header
- **Style**: Beautiful dropdown with refresh button
- **Animation**: Smooth slide-down effect
- **Responsive**: Works on mobile devices

### Retrain Section

- **Location**: Below results table
- **Visibility**: Only shows after prediction
- **Style**: Gradient background with bordered card
- **Buttons**: Large, color-coded (green/red)
- **Feedback**: Loading states and animations

### Notifications

- **Position**: Top-right corner
- **Types**: Success (green), Error (red), Info (blue)
- **Animation**: Slide in from right
- **Auto-dismiss**: Disappears after 5 seconds
- **Content**: Title + detailed message

---

## 🧪 Testing

### Automated Testing

```powershell
# Run comprehensive API tests
D:/Python/python.exe test_versioning.py
```

### Manual Testing Workflow

1. **Test Version Listing**

   - Open web interface
   - Check dropdown shows "Original"
   - Click refresh button

2. **Test Prediction**

   - Enter water quality data
   - Click predict
   - Verify results appear

3. **Test Retraining**

   - After prediction, scroll down
   - Click either retrain button
   - Wait for notification (30-60 seconds)
   - Check dropdown now shows "V1"

4. **Test Version Switching**
   - Open dropdown
   - Select "Original"
   - Wait for success notification
   - Make prediction (should use Original model)
   - Switch to "V1"
   - Make same prediction (result may differ)

---

## 💡 Best Practices

### When to Retrain

- ✅ When prediction is incorrect
- ✅ When you have verified actual results
- ✅ To add edge cases to training data
- ❌ Don't retrain randomly (adds noise)
- ❌ Don't retrain without verification

### Version Management

- Keep "Original" as baseline for comparison
- Test new versions before relying on them
- Delete old versions if too many accumulate
- Monitor CV accuracy trends across versions

### Performance Expectations

- Each new sample adds minimal improvement
- Need 10-20+ samples for noticeable change
- CV accuracy may fluctuate slightly
- Training accuracy will stay high (~84%)

---

## 🔍 Technical Details

### Incremental Learning Approach

1. **Data Persistence**: New samples saved to CSV
2. **Full Retraining**: Combines original + new data
3. **Same Architecture**: Uses identical ensemble model
4. **Refitted Scaler**: StandardScaler on all data
5. **Cross-Validation**: 5-fold CV for evaluation

### Model Architecture (All Versions)

```python
Ensemble = VotingClassifier(
    estimators=[
        ('rf', RandomForestClassifier(n=250, depth=6, ...)),
        ('xgb', XGBClassifier(n=300, depth=4, ...)),
        ('gb', GradientBoostingClassifier(n=250, depth=4, ...))
    ],
    voting='soft'
)
```

### Storage Details

- **Model Files**: ~2.3 MB per version
- **Scaler Files**: ~1.2 KB per version
- **Metadata**: JSON with all version info
- **Training Data**: CSV with incremental samples

---

## 🆘 Troubleshooting

### "Cannot connect to server"

- Restart server: `.\launch.ps1`
- Check port 8000: `netstat -ano | findstr :8000`

### "Retraining taking too long"

- Normal: 30-60 seconds for full retraining
- Wait for notification
- Check server logs for progress

### "Version not showing in dropdown"

- Click refresh button (🔄)
- Check browser console (F12)
- Verify server running

### "Model predictions identical after retraining"

- One sample has minimal impact
- Add 10-20+ samples for noticeable change
- Check if different inputs show difference

---

## 📈 Future Enhancements

Possible additions (not implemented):

- **Batch Retraining**: Upload CSV with multiple samples
- **Version Comparison**: Side-by-side accuracy comparison
- **Auto-backup**: Save versions to cloud
- **Performance Graphs**: Visualize accuracy trends
- **Version Rollback**: Revert to previous version
- **A/B Testing**: Split traffic between versions

---

## 🎉 Summary

You now have a **production-ready MLOps system** with:

✅ **Beautiful Web Interface** - Modern, responsive, animated  
✅ **Incremental Learning** - Improve model with user feedback  
✅ **Version Management** - Switch between model versions  
✅ **Real-time Updates** - See changes immediately  
✅ **Complete Tracking** - Monitor all version metrics

**Enjoy your advanced MLOps system!** 🚀

---

_For more information, see:_

- `README.md` - General project overview
- `WEB_INTERFACE.md` - Web interface guide
- `QUICKSTART.md` - Simple commands
- `test_versioning.py` - API testing examples
