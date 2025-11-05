# 🌊 Water Potability Prediction - Complete MLOps Project

A production-ready machine learning system that predicts whether water is safe to drink based on its chemical properties. This project demonstrates a complete MLOps pipeline from data processing to cloud deployment.

---

## 📚 What This Project Does

**Problem:** How do we know if water is safe to drink?  
**Solution:** Feed water quality measurements into an AI model that predicts if it's potable or not.

**Real Example:**

- You measure water: pH=7.5, Hardness=150, Turbidity=3.5, etc.
- The model analyzes these 9 parameters
- Result: ✅ **Water is Potable** (Confidence: 85%)

---

## 🏗️ How It's Built - The Complete Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│  START: Raw Data (Water Quality Samples)                        │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 1: Data Preprocessing (Clean & Prepare Data)              │
│  - Loads 2,293 water samples from Data-set/train_dataset.csv    │
│  - Standardizes numerical features (scaling)                    │
│  - Handles missing values                                       │
│  - Outputs: data/train.csv, data/test.csv                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 2: Model Training (Build the AI Brain)                   │
│  - Creates 3 different AI algorithms:                           │
│    • Random Forest (250 trees)                                  │
│    • XGBoost (300 boosted trees)                                │
│    • Gradient Boosting (250 trees)                              │
│  - Combines them into one powerful Ensemble Model               │
│  - Achieves ~84% accuracy on test data                          │
│  - Saves: models/model.joblib, models/scaler.joblib             │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 3: Model Evaluation (Measure Performance)                 │
│  - Tests accuracy, precision, recall, F1-score                  │
│  - Cross-validates with 5-fold validation                       │
│  - Generates metrics.json with results                          │
│  - Confusion matrix to see false positives/negatives            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 4: Containerization (Package for Production)              │
│  - Wraps everything in Docker container                         │
│  - Creates image: ghcr.io/tejasthange3/mlops-water-potability   │
│  - Ensures it runs the same on any machine                      │
│  - Includes health checks                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│  STEP 5: Cloud Deployment (Go Live on AWS)                      │
│  - Deploys Docker container on EC2 instance                     │
│  - Creates web interface for predictions                        │
│  - API endpoints for programmatic access                        │
│  - Stores data on S3                                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
         🎉 Live Application Running on AWS! 🎉
         Access at: http://<EC2_IP>:8000
```

---

## 🔄 How Each Step Works (In Simple Terms)

### **Step 1: Data Preprocessing** 📊

**What:** Clean and prepare messy data for AI training

**How:**

```
Raw Water Samples (with noise, missing values)
           ↓
    Remove bad entries
    Fix missing values (drop or fill)
    Standardize numbers (pH 0-14, Conductivity 0-1000, etc.)
           ↓
    Clean, normalized data ready for AI
```

**Code:** `src/preprocess_presplit.py`  
**Parameters:** `params.yaml` (controls scaling, feature engineering)  
**Input:** `Data-set/train_dataset.csv`, `Data-set/test_dataset.csv`  
**Output:** `data/train.csv`, `data/test.csv`

---

### **Step 2: Model Training** 🤖

**What:** Teach the AI to predict potability using cleaned data

**How - Ensemble Approach:**

```
Instead of trusting 1 AI model, we use 3 smart models and let them vote:

Random Forest: "I think it's potable" ✓
XGBoost: "I agree, it's potable" ✓
Gradient Boosting: "I also say it's potable" ✓
Final Decision: POTABLE (3 out of 3 agree = confident prediction)
```

**Hyperparameters (Tuning knobs):**

- **Random Forest:** 250 trees, max depth 6, balances classes
- **XGBoost:** 300 boosted trees, learning rate 0.05, handles imbalanced data
- **Gradient Boosting:** 250 trees, 75% subsampling

**Code:** `src/train_ensemble.py`  
**Controlled by:** `params.yaml` (all hyperparameters)  
**Output:** `models/model.joblib` (the trained AI brain)

---

### **Step 3: Model Evaluation** 📈

**What:** Check how well the model actually works

**Metrics Generated:**

- **Accuracy:** 84% of predictions are correct
- **Precision:** When it says "potable", it's right 82% of the time
- **Recall:** It catches 83% of actual potable water
- **F1-Score:** 83% balanced performance

**Output:** `metrics.json` (stored for tracking over time)

**Code:** `src/evaluate.py`

---

### **Step 4: Web Application & API** 🌐

**What:** User-friendly interface to make predictions

**Features:**

- **Web UI** (`static/index.html`) - Beautiful dashboard

  - Input 9 water quality parameters
  - Get instant prediction: "Potable" or "Not Potable"
  - See confidence score (0-100%)
  - Feedback button: "This prediction was wrong!" → triggers retraining
  - View historical predictions

- **REST API** (`main.py`) - For developers
  - `/predict` - Make predictions programmatically
  - `/versions` - See all model versions
  - `/switch-version` - Change which model to use
  - `/retrain` - Add new labeled data to improve model
  - `/metrics` - Get performance metrics

**Tech Stack:**

- **FastAPI** - High-performance API framework
- **Uvicorn** - Application server
- **Pydantic** - Data validation

---

### **Step 5: Containerization with Docker** 🐳

**What:** Package everything into a single, portable container

**Why Docker?**

```
Developer's laptop: "It works on my machine!"
Production server: "It doesn't work here..."
Docker: "It works everywhere!" ✓
```

**Dockerfile Strategy:**

```dockerfile
FROM python:3.12-slim
# Install system dependencies
COPY requirements.txt .
# Install Python packages
COPY . /app
# Copy all project files
EXPOSE 8000
# Make port 8000 available
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
# Run the API
```

**Built Image:**

- Hosted on GitHub Container Registry: `ghcr.io/tejasthange3/mlops-water-potability:latest`
- ~500 MB (optimized)
- Runs in seconds

---

### **Step 6: Automated Testing & Continuous Integration** 🧪

**What:** Every code change is automatically tested

**MLOps Pipeline (`mlops-pipeline.yml` - Daily at 2 AM UTC):**

1. **Data Validation** - Check datasets are intact
2. **Model Training** - Run complete DVC pipeline
3. **Model Evaluation** - Generate metrics
4. **Unit Tests** - Test individual functions
5. **API Tests** - Test prediction endpoints
6. **Artifacts Upload** - Store metrics and coverage reports

**Deploy Workflow (`deploy.yml` - On every push to main):**

1. Checkout code
2. Run tests
3. Build Docker image
4. Push to GitHub Container Registry
5. SSH into EC2
6. Pull latest image
7. Restart containers
8. Verify health

---

### **Step 7: Cloud Deployment on AWS** ☁️

**What:** Make the application publicly accessible

**Architecture:**

```
┌────────────────────────────────────┐
│    User's Browser                  │
│  http://46.137.144.250:8000        │
└─────────────┬──────────────────────┘
              │
              ↓
┌────────────────────────────────────┐
│    AWS EC2 Instance (Ubuntu)       │
│  ├─ Port 8000: FastAPI Server      │
│  ├─ Docker Container               │
│  │  ├─ Model (model.joblib)        │
│  │  ├─ Scaler (scaler.joblib)      │
│  │  └─ App (uvicorn)               │
│  └─ Volumes                        │
│     ├─ models/ (persistent)        │
│     └─ data/ (persistent)          │
└────────────────────────────────────┘
              │
              ↓
┌────────────────────────────────────┐
│    AWS S3 Bucket                   │
│  Backup training datasets          │
│  Versioned models                  │
└────────────────────────────────────┘
```

**Deployment Steps:**

1. GitHub Actions automatically triggers on code push
2. Builds Docker image with new code
3. SSH into EC2 instance
4. `docker-compose down` (stop old version)
5. `docker-compose up -d` (start new version)
6. Container automatically starts serving requests

---

## 📁 Project Structure Explained

```
Mlops-Project/
│
├── 📊 DATA & MODELS
│   ├── Data-set/
│   │   ├── train_dataset.csv      (2,293 labeled water samples)
│   │   └── test_dataset.csv       (1,000 unlabeled samples)
│   ├── data/
│   │   ├── train.csv              (preprocessed training data)
│   │   └── test.csv               (preprocessed test data)
│   └── models/
│       ├── model.joblib            (current trained model)
│       ├── scaler.joblib           (data standardizer)
│       └── versions/               (model history)
│           ├── model_V1.joblib     (first trained version)
│           ├── model_V2.joblib     (improved version)
│           └── metadata.json       (version info & metrics)
│
├── 🤖 ML PIPELINE CODE
│   ├── src/
│   │   ├── preprocess_presplit.py  (Step 1: Clean data)
│   │   ├── train_ensemble.py       (Step 2: Train models)
│   │   ├── evaluate.py             (Step 3: Test models)
│   │   ├── predict_test.py         (Make predictions)
│   │   └── model_manager.py        (Handle versions)
│   │
│   ├── main.py                      (FastAPI server - Step 4)
│   ├── dvc.yaml                     (DVC pipeline definition)
│   └── params.yaml                  (All hyperparameters)
│
├── 🌐 WEB INTERFACE
│   └── static/
│       ├── index.html               (Web dashboard)
│       ├── js/app.js                (Frontend logic)
│       └── css/style.css            (Styling)
│
├── 🐳 DEPLOYMENT & AUTOMATION
│   ├── Dockerfile                   (Container definition)
│   ├── docker-compose.yml           (Multi-container setup)
│   ├── requirements.txt             (Python dependencies)
│   │
│   ├── .github/workflows/
│   │   ├── deploy.yml               (Build & deploy on push)
│   │   └── mlops-pipeline.yml       (Train & test daily)
│   │
│   └── aws_setup.py                 (AWS infrastructure script)
│
└── 📚 DOCUMENTATION
    ├── README_COMPREHENSIVE.md      (Full technical guide)
    ├── AWS_DEPLOYMENT_GUIDE.md      (AWS setup)
    ├── DOCKER_GUIDE.md              (Docker usage)
    ├── GITHUB_ACTIONS_SETUP.md      (CI/CD setup)
    └── QUICKSTART.md                (Getting started)
```

---

## 🚀 Running the Project Locally

### **Prerequisites**

- Python 3.12+
- Git
- Docker (optional)
- 4GB RAM minimum

### **Setup**

```bash
# Clone repository
git clone https://github.com/TejasThange3/Mlops-Project.git
cd Mlops-Project

# Install dependencies
pip install -r requirements.txt

# Install DVC
pip install dvc
```

### **Train the Model (Complete Pipeline)**

```bash
# Run the entire DVC pipeline:
# 1. Preprocess data
# 2. Train models
# 3. Evaluate performance
dvc repro

# This generates: metrics.json, trained models, preprocessed data
```

### **Run the Web Application**

```bash
# Start the API server
uvicorn main:app --host 0.0.0.0 --port 8000

# Open browser: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### **Run with Docker Locally**

```bash
# Build and run
docker-compose up -d

# Access: http://localhost:8000
# View logs: docker-compose logs -f
```

---

## ☁️ Deploying to AWS

### **Quick Deploy**

```bash
# On your EC2 instance (Ubuntu):
git clone https://github.com/TejasThange3/Mlops-Project.git
cd Mlops-Project
docker-compose up -d

# Access: http://<your-ec2-ip>:8000
```

### **Automatic Deployment via GitHub Actions**

```
When you push to main branch:
1. GitHub Actions automatically runs tests
2. Builds Docker image
3. Pushes to GitHub Container Registry
4. Deploys to EC2 automatically
5. Application updates in 2-3 minutes
```

---

## 🔄 How Model Versioning & Retraining Works

### **Initial Training**

- Trains on 2,293 water samples
- Creates `Original` version
- Achieves 84% accuracy

### **Incremental Retraining**

When user provides feedback (e.g., "This prediction was wrong"):

1. Collects new labeled sample
2. Combines with original training data
3. Retrains ensemble model (takes ~30 seconds)
4. Creates new version: V1, V2, V3, etc.
5. Saves new model with metrics
6. User can switch between versions

### **Accessing Versions**

- **API Endpoint:** `/versions` - Lists all model versions
- **Web UI:** Dropdown menu to switch versions
- **Metadata:** `models/versions/metadata.json` - Version history

---

## 📊 What the Model Predicts

**Input (9 Water Quality Parameters):**

1. **pH** - Acidity/Alkalinity (0-14)
2. **Hardness** - Mineral content (mg/L)
3. **Solids** - Dissolved salts (ppm)
4. **Chloramines** - Disinfectant level (ppm)
5. **Sulfate** - Sulfate concentration (mg/L)
6. **Conductivity** - Electrical conductivity (μS/cm)
7. **Organic Carbon** - Organic matter (ppm)
8. **Trihalomethanes** - Disinfection byproducts (μg/L)
9. **Turbidity** - Cloudiness (NTU)

**Output:**

- **Potability:** 0 (Not Potable) or 1 (Potable)
- **Confidence:** 0-100% (how sure the model is)
- **Individual Model Votes:** What each of 3 models said

---

## 🧪 Testing

### **Run All Tests**

```bash
# Unit tests + API tests
pytest -v

# With coverage report
pytest --cov=src
```

### **Manual API Testing**

```bash
# Test prediction endpoint
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "ph": 7.0,
    "Hardness": 200,
    "Solids": 20000,
    "Chloramines": 7.5,
    "Sulfate": 350,
    "Conductivity": 400,
    "Organic_carbon": 14,
    "Trihalomethanes": 70,
    "Turbidity": 4.0
  }'

# Get model versions
curl http://localhost:8000/api/versions
```

---

## 🔐 Security & Scaling

### **Security Features**

- ✅ CORS enabled for cross-origin requests
- ✅ Input validation (Pydantic)
- ✅ Health checks (Docker)
- ✅ Error handling with informative messages

### **Scalability**

- Docker container can be replicated across multiple EC2 instances
- Load balancer distributes traffic
- Models are cached in memory for fast predictions (<100ms)
- Data persisted on S3 for reliability

---

## 📈 Monitoring & Metrics

### **Available Metrics**

```json
{
  "accuracy": 0.8439,
  "precision": 0.824,
  "recall": 0.8329,
  "f1_score": 0.8284,
  "cv_accuracy": 0.6424,
  "training_samples": 2293,
  "timestamp": "2025-11-05T10:30:00Z"
}
```

### **Check Metrics**

```bash
# Via API
curl http://localhost:8000/api/metrics

# Via file
cat metrics.json
```

---

## 🛠️ Common Tasks

### **Update Model Hyperparameters**

1. Edit `params.yaml`
2. Run `dvc repro` to retrain
3. Commit and push to GitHub
4. GitHub Actions automatically deploys

### **Switch Model Version**

```bash
# Via API
curl -X POST http://localhost:8000/api/switch-version \
  -H "Content-Type: application/json" \
  -d '{"version": "V2"}'

# Via Web UI: Dropdown menu
```

### **View Training Logs**

```bash
# Docker logs
docker-compose logs -f mlops-api

# GitHub Actions
Visit: https://github.com/TejasThange3/Mlops-Project/actions
```

### **Check Model Size**

```bash
ls -lh models/
# model.joblib: ~50 MB
# scaler.joblib: ~5 KB
```

---

## 🎓 Key Concepts Explained

### **Ensemble Learning**

Instead of trusting one model, combine multiple weak learners into one strong model:

- **Random Forest:** Good at capturing data patterns
- **XGBoost:** Good at learning from mistakes
- **Gradient Boosting:** Good at boosting weak predictions
- **Together:** More accurate and robust

### **DVC (Data Version Control)**

Like Git for machine learning:

- Tracks data, models, and pipeline
- Enables reproducible experiments
- Stores which exact data produced which model

### **Cross-Validation**

Test model on different data slices to ensure it generalizes:

- Split data into 5 folds
- Train on 4, test on 1
- Repeat 5 times
- Average results

### **Feature Scaling**

Normalize features to same range (0-1) so high-value features don't dominate:

- pH (0-14) vs Conductivity (0-1000)
- Scaling makes training faster and more stable

---

## 🐛 Troubleshooting

### **Issue: "Model not found" error**

```bash
# Solution: Train the model
dvc repro
```

### **Issue: Docker container exits immediately**

```bash
# Check logs
docker-compose logs mlops-api

# Likely: Port 8000 already in use
# Solution: Change port in docker-compose.yml
```

### **Issue: Predictions very slow**

```bash
# Model might be loading from disk each time
# Check: model_manager.py caching
# Solution: Restart container to reload model into memory
```

### **Issue: Retraining fails**

```bash
# Check docker-compose.yml has Data-set volume mounted
# This folder is needed for retraining
volumes:
  - ./Data-set:/app/Data-set
```

---

## 📞 Support & Documentation

- **Quick Start:** `QUICKSTART.md`
- **AWS Setup:** `AWS_DEPLOYMENT_GUIDE.md`
- **Docker Guide:** `DOCKER_GUIDE.md`
- **GitHub Actions:** `GITHUB_ACTIONS_SETUP.md`
- **Comprehensive Guide:** `README_COMPREHENSIVE.md`
- **Troubleshooting:** `TROUBLESHOOTING.md`

---

## 🎯 Next Steps to Enhance the Project

1. **Add Database** - PostgreSQL to store prediction history
2. **Redis Caching** - Speed up repeated predictions
3. **Monitoring** - Prometheus + Grafana for metrics
4. **Multi-Region** - Deploy across multiple AWS regions
5. **Mobile App** - iOS/Android app for predictions
6. **Model Explainability** - SHAP values to explain predictions
7. **A/B Testing** - Compare model versions in production
8. **Auto-Scaling** - Kubernetes for automatic scaling

---

## 📄 License & Attribution

This is an educational project demonstrating MLOps best practices.

**Technologies Used:**

- Python 3.12
- FastAPI, Uvicorn
- scikit-learn, XGBoost, Pandas, NumPy
- DVC (Data Version Control)
- Docker, Docker Compose
- GitHub Actions
- AWS EC2, S3

---

**Built with ❤️ for learning MLOps**

📧 Questions? Check the documentation or review the code comments!

🚀 **Ready to deploy? Follow the AWS_DEPLOYMENT_GUIDE.md**
