# 🔄 MLOps Workflow Diagram

Complete end-to-end pipeline for Water Potability Prediction project

---

## 📊 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    DEVELOPER WORKFLOW                               │
│                                                                     │
│  1. Make Code Changes  →  2. Commit & Push  →  3. GitHub Actions  │
│                                                                     │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  GITHUB ACTIONS CI/CD PIPELINE                      │
│                                                                     │
│  ┌─ Build Job ────────────────────────────────────────────────┐   │
│  │ ├─ Install Dependencies                                   │   │
│  │ ├─ Run Tests (pytest)                                     │   │
│  │ ├─ Build Docker Image                                     │   │
│  │ └─ Push to GitHub Container Registry (ghcr.io)           │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                          │                                          │
│                          ▼                                          │
│  ┌─ Deploy Job ────────────────────────────────────────────────┐  │
│  │ ├─ SSH into EC2                                            │  │
│  │ ├─ Git Pull Latest Code                                    │  │
│  │ ├─ Docker Compose Down (stop old)                          │  │
│  │ ├─ Docker Compose Up (start new)                           │  │
│  │ └─ Health Check                                            │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────┬───────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│               RUNNING ON AWS EC2 (PRODUCTION)                       │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Ubuntu EC2 Instance (46.137.144.250)                       │  │
│  │                                                              │  │
│  │  ┌─ Docker Container ────────────────────────────────────┐  │  │
│  │  │                                                       │  │  │
│  │  │  FastAPI Application (main.py)                       │  │  │
│  │  │  ├─ REST API (localhost:8000)                        │  │  │
│  │  │  ├─ Web Dashboard (static files)                     │  │  │
│  │  │  └─ Health Checks                                    │  │  │
│  │  │                                                       │  │  │
│  │  │  Model Components:                                   │  │  │
│  │  │  ├─ Trained Model (model.joblib)                     │  │  │
│  │  │  ├─ Feature Scaler (scaler.joblib)                   │  │  │
│  │  │  └─ Model Versions (v1, v2, v3, etc)                │  │  │
│  │  │                                                       │  │  │
│  │  └─────────────────────────────────────────────────────┘  │  │
│  │                                                             │  │
│  │  📁 Persistent Volumes:                                    │  │
│  │  ├─ /app/models/     (model files & versions)             │  │
│  │  ├─ /app/data/       (training data)                      │  │
│  │  └─ /app/Data-set/   (original datasets)                  │  │
│  │                                                             │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
                          │
                          ▼
         🌐 USER ACCESS: http://46.137.144.250:8000
         ✅ Web UI for predictions
         ✅ API endpoints (/docs, /predict, /retrain)
         ✅ Model management (/versions, /switch-version)
```

---

## 🔁 Complete Data & Model Pipeline

```
┌──────────────────────────┐
│  Raw Training Data       │
│ train_dataset.csv (2,293 samples)
│ test_dataset.csv  (1,000 samples)
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────┐
│ STEP 1: DATA PREPROCESSING                           │
│ (src/preprocess_presplit.py)                         │
│                                                      │
│ ✓ Handle missing values                              │
│ ✓ Feature scaling (StandardScaler)                   │
│ ✓ Remove outliers                                    │
│ ✓ Split train/test                                   │
│                                                      │
│ Controlled by: params.yaml (preprocess section)      │
│ Output: data/train.csv, data/test.csv                │
└───────────┬──────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────┐
│ STEP 2: MODEL TRAINING                               │
│ (src/train_ensemble.py)                              │
│                                                      │
│ Trains 3 ensemble models:                            │
│ 1️⃣  Random Forest (250 trees)                       │
│ 2️⃣  XGBoost (300 boosted trees)                     │
│ 3️⃣  Gradient Boosting (250 trees)                   │
│                                                      │
│ Combines via VotingClassifier (soft voting)          │
│ Controlled by: params.yaml (train section)           │
│ Output: models/model.joblib                          │
└───────────┬──────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────┐
│ STEP 3: MODEL EVALUATION                             │
│ (src/evaluate.py)                                    │
│                                                      │
│ Calculate metrics:                                   │
│ • Accuracy: 84.39%                                   │
│ • Precision: 82.40%                                  │
│ • Recall: 83.29%                                     │
│ • F1-Score: 82.84%                                   │
│ • Cross-Val Score: 64.24%                            │
│                                                      │
│ Output: metrics.json                                 │
└───────────┬──────────────────────────────────────────┘
            │
            ▼
┌──────────────────────────────────────────────────────┐
│ DVC ORCHESTRATION                                    │
│ (dvc.yaml - ties everything together)                │
│                                                      │
│ dvc repro runs:                                      │
│ 1. preprocess stage                                  │
│ 2. train stage                                       │
│ 3. evaluate stage                                    │
│                                                      │
│ Tracks data versions & reproducibility               │
└──────────────────────────────────────────────────────┘
```

---

## 🐳 Docker & Deployment Pipeline

```
┌────────────────────────────────────┐
│  Dockerfile (Multi-stage build)    │
│                                    │
│  Stage 1: Base (Python 3.12.2)     │
│  ├─ System dependencies            │
│  └─ Environment setup              │
│                                    │
│  Stage 2: Dependencies             │
│  ├─ pip install -r requirements.txt
│  └─ Install DVC, scikit-learn, etc │
│                                    │
│  Stage 3: Application              │
│  ├─ Copy project files             │
│  ├─ Create directories             │
│  ├─ Health checks                  │
│  └─ CMD: uvicorn main:app          │
└────────────────┬───────────────────┘
                 │
                 ▼
        ┌────────────────────┐
        │ Docker Image Built │
        │ ~500 MB optimized  │
        └────────┬───────────┘
                 │
                 ▼
    ┌──────────────────────────────┐
    │ GitHub Container Registry    │
    │ ghcr.io/tejasthange3/        │
    │ mlops-water-potability:latest│
    └────────┬─────────────────────┘
             │
             ▼
┌────────────────────────────────────┐
│  docker-compose.yml                │
│                                    │
│  Services:                         │
│  ├─ mlops-api                      │
│  │  ├─ Image: ghcr.io/...latest  │
│  │  ├─ Port: 8000                 │
│  │  ├─ Volumes: (models, data)    │
│  │  └─ Restart policy             │
│  │                                │
│  └─ Health check every 30 sec      │
└────────┬───────────────────────────┘
         │
         ▼
┌────────────────────────────────────┐
│  EC2 Instance Runs Container       │
│                                    │
│  Commands:                         │
│  $ docker-compose down             │
│  $ docker-compose up -d            │
│                                    │
│  Result:                           │
│  ✅ Container running              │
│  ✅ Port 8000 listening            │
│  ✅ API accepting requests         │
└────────────────────────────────────┘
```

---

## 🔄 CI/CD Automation Workflows

### **Workflow 1: Deploy on Push (deploy.yml)**

```
EVENT: Push to main branch
  │
  ▼
├─ Checkout Code
├─ Setup Python 3.12
├─ Install Dependencies
├─ Run Tests (pytest)
├─ Build Docker Image
│   ├─ Tag: ghcr.io/.../mlops-water-potability:$COMMIT_SHA
│   └─ Tag: ghcr.io/.../mlops-water-potability:latest
├─ Login to GitHub Container Registry
├─ Push Docker Image
│   ├─ Push :$COMMIT_SHA tag
│   └─ Push :latest tag
│
└─ Deploy to EC2 (SSH)
    ├─ Clone/Pull Repository
    ├─ docker compose down
    ├─ docker compose up -d
    ├─ Wait 5 seconds
    ├─ curl http://localhost:8000/health
    └─ ✅ Deployment Complete

RESULT: Application live in 2-3 minutes
```

### **Workflow 2: ML Training Pipeline (mlops-pipeline.yml)**

```
EVENT: Daily at 2 AM UTC (or manual trigger)
  │
  ▼
Job 1: Data Validation
├─ Load datasets
├─ Check structure
├─ Verify non-empty
└─ ✅ Data validated

  │
  ▼
Job 2: Model Training
├─ Run: dvc repro
│   ├─ Preprocess data
│   ├─ Train ensemble model
│   └─ Evaluate performance
├─ Generate metrics.json
└─ ✅ Model trained

  │
  ▼
Job 3: Unit Tests
├─ pytest -v --cov=src
├─ Test all functions
├─ Generate coverage report
└─ ✅ Tests passed

  │
  ▼
Job 4: API Integration Tests
├─ Start uvicorn server
├─ Test /health endpoint
├─ Test /predict endpoint
├─ Verify responses
└─ ✅ API working

  │
  ▼
Upload Artifacts
├─ metrics.json
├─ coverage report
└─ ✅ Artifacts stored
```

---

## 🌍 User Interaction Flow

```
┌─────────────────────────────────────┐
│  USER INTERACTION                   │
│  http://46.137.144.250:8000         │
└──────────────┬──────────────────────┘
               │
        ┌──────┴────────┐
        │               │
        ▼               ▼
   ┌──────────┐   ┌──────────────┐
   │ Web UI   │   │ API Endpoint │
   │ (HTML)   │   │ (/predict)   │
   └──┬───────┘   └───┬──────────┘
      │               │
      │    Input Parameters:
      │    • pH, Hardness, Solids
      │    • Chloramines, Sulfate
      │    • Conductivity
      │    • Organic_carbon
      │    • Trihalomethanes
      │    • Turbidity
      │
      ▼               ▼
    ┌────────────────────────┐
    │  FastAPI Server        │
    │  (main.py)             │
    │                        │
    │  1. Validate input     │
    │  2. Scale features     │
    │  3. Load model         │
    │  4. Make prediction    │
    │  5. Return result      │
    └────────┬───────────────┘
             │
             ▼
    ┌────────────────────────┐
    │  RESPONSE              │
    │  {                     │
    │    "potability": 1,    │
    │    "label": "Potable", │
    │    "confidence": 0.85  │
    │  }                     │
    └────────────────────────┘
             │
        ┌────┴────┐
        ▼         ▼
    Display   Return JSON
    on UI     to API caller
```

---

## 🔁 Model Retraining Loop

```
┌─────────────────────────────────────┐
│ USER PROVIDES FEEDBACK              │
│ "This prediction was wrong!"        │
└──────────────┬──────────────────────┘
               │
               ▼
    ┌─────────────────────────┐
    │ Collect Feedback        │
    │ • Prediction made       │
    │ • Actual label (0 or 1) │
    │ • Timestamp             │
    └──────────┬──────────────┘
               │
               ▼
    ┌─────────────────────────────────────┐
    │ Retrain Endpoint (/retrain)         │
    │                                     │
    │ 1. Add to incremental_training_     │
    │    data.csv                         │
    │ 2. Load original training data      │
    │ 3. Combine datasets                 │
    │ 4. Retrain ensemble model           │
    │ 5. Evaluate new model               │
    │ 6. Save as new version (V1, V2...)  │
    │ 7. Update metadata.json             │
    └──────────┬──────────────────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ NEW MODEL VERSION        │
    │                          │
    │ models/versions/         │
    │ ├─ model_V1.joblib       │
    │ ├─ model_V2.joblib (NEW) │
    │ ├─ scaler_V1.joblib      │
    │ ├─ scaler_V2.joblib (NEW)│
    │ └─ metadata.json (updated)
    └──────────┬───────────────┘
               │
               ▼
    ┌──────────────────────────┐
    │ USER CAN NOW:            │
    │                          │
    │ • Use new model (V2)     │
    │ • Switch back to V1      │
    │ • View metrics for each  │
    │ • Compare versions       │
    └──────────────────────────┘
```

---

## 📂 File Dependencies

```
Data Flow:
Data-set/train_dataset.csv
           ↓
    [preprocess_presplit.py] ← params.yaml (preprocess)
           ↓
      data/train.csv
           ↓
    [train_ensemble.py] ← params.yaml (train)
           ↓
    models/model.joblib
           ↓
    [evaluate.py] ← models/model.joblib
           ↓
    metrics.json
           ↓
    [GitHub Actions] ← stores as artifact

Application Flow:
models/model.joblib
models/scaler.joblib  ──→ [main.py] → FastAPI Server
static/index.html        ↑
src/model_manager.py ─────┘

Deployment:
.github/workflows/deploy.yml
        ↓
    [GitHub Actions]
        ├─ Build Docker Image (Dockerfile)
        ├─ Push to ghcr.io
        └─ Deploy to EC2 (docker-compose.yml)

CI/CD Pipelines:
.github/workflows/mlops-pipeline.yml (daily training)
.github/workflows/deploy.yml (on push to main)
```

---

## 🎯 Key Touchpoints

| Phase          | Technology              | Input        | Output          | Time    |
| -------------- | ----------------------- | ------------ | --------------- | ------- |
| **Preprocess** | Python + scikit-learn   | Raw CSV      | Scaled CSV      | ~2 sec  |
| **Train**      | XGBoost + Random Forest | Scaled CSV   | Model.joblib    | ~30 sec |
| **Evaluate**   | scikit-learn metrics    | Model + Data | metrics.json    | ~5 sec  |
| **Package**    | Docker                  | Code + Model | Container Image | ~2 min  |
| **Deploy**     | GitHub Actions + SSH    | Docker Image | EC2 Running     | ~3 min  |
| **Predict**    | FastAPI                 | JSON params  | JSON result     | ~100 ms |
| **Retrain**    | Model Manager           | Feedback     | New Version     | ~30 sec |

---

## ⚡ Quick Command Reference

```bash
# LOCAL DEVELOPMENT
dvc repro                          # Run full pipeline
python main.py                     # Run locally
pytest -v                          # Run tests

# DOCKER
docker build -t mlops .            # Build image
docker-compose up -d               # Start containers
docker-compose logs -f             # View logs
docker-compose down                # Stop containers

# GIT & DEPLOYMENT
git push origin main               # Trigger CI/CD
# GitHub Actions automatically builds and deploys!

# EC2 MANUAL DEPLOYMENT
ssh -i mlops-project-key.pem ubuntu@<EC2_IP>
cd Mlops-Project
git pull origin main
docker-compose down
docker-compose up -d
curl http://localhost:8000/health # Verify
```

---

**Complete MLOps Workflow: From Data → Model → Container → Cloud ☁️**
