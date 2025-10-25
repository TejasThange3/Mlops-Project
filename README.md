# 🌊 Water Potability Prediction - MLOps Project

An end-to-end machine learning project that predicts water potability (safe to drink or not) based on physicochemical properties. This project demonstrates MLOps best practices using **DVC** for pipeline orchestration and **FastAPI** for model deployment.

## 📋 Project Overview

This project builds a binary classification system to determine if water is safe for human consumption based on 9 water quality features. The entire ML pipeline is version-controlled and reproducible using DVC.

### Features

- ✅ **Data Version Control** with DVC
- ✅ **Reproducible ML Pipeline** (preprocess → train → evaluate)
- ✅ **Configurable Hyperparameters** via `params.yaml`
- ✅ **Multiple Model Support** (RandomForest, XGBoost)
- ✅ **REST API** with FastAPI and Swagger documentation
- ✅ **Automated Metrics Tracking**

## 🏗️ Project Structure

```
Mlops-Project/
├── data/
│   ├── water_quality.csv      # Raw dataset (DVC tracked)
│   ├── train.csv              # Training data (generated)
│   └── test.csv               # Test data (generated)
├── src/
│   ├── preprocess.py          # Data preprocessing script
│   ├── train.py               # Model training script
│   └── evaluate.py            # Model evaluation script
├── models/
│   └── model.joblib           # Trained model (generated)
├── dvc.yaml                   # DVC pipeline definition
├── params.yaml                # Hyperparameters configuration
├── requirements.txt           # Python dependencies
├── main.py                    # FastAPI application
├── metrics.json               # Evaluation metrics (generated)
└── README.md                  # This file
```

## 🚀 Quick Start

### 1. Installation

```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Run the DVC Pipeline

The pipeline consists of three stages: preprocess, train, and evaluate.

```bash
# Run the entire pipeline
dvc repro

# Or run stages individually:
dvc repro preprocess  # Preprocess data
dvc repro train       # Train model
dvc repro evaluate    # Evaluate model
```

### 3. View Metrics

```bash
# Show metrics from the latest run
dvc metrics show

# Compare metrics across different runs
dvc metrics diff
```

### 4. Deploy the API

```bash
# Start the FastAPI server
python main.py

# Or use uvicorn directly:
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:

- **API Endpoint**: http://localhost:8000
- **Interactive Docs (Swagger)**: http://localhost:8000/docs
- **Alternative Docs (ReDoc)**: http://localhost:8000/redoc

## 📊 Dataset

The project uses the **Water Quality** dataset containing 3,276 samples with 9 physicochemical features:

| Feature           | Description                   | Unit                           |
| ----------------- | ----------------------------- | ------------------------------ |
| `ph`              | pH value                      | 0-14 scale                     |
| `Hardness`        | Water hardness                | mg/L                           |
| `Solids`          | Total dissolved solids        | ppm                            |
| `Chloramines`     | Chloramines concentration     | ppm                            |
| `Sulfate`         | Sulfate concentration         | mg/L                           |
| `Conductivity`    | Electrical conductivity       | μS/cm                          |
| `Organic_carbon`  | Organic carbon content        | ppm                            |
| `Trihalomethanes` | Trihalomethanes concentration | μg/L                           |
| `Turbidity`       | Turbidity                     | NTU                            |
| **Potability**    | Target variable               | 0 (Not Potable) or 1 (Potable) |

## ⚙️ Configuration

Edit `params.yaml` to customize the pipeline:

```yaml
preprocess:
  test_size: 0.2 # Train-test split ratio
  random_state: 42 # Random seed
  imputation_strategy: "mean" # 'mean', 'median', or 'most_frequent'

train:
  model_type: "RandomForest" # 'RandomForest' or 'XGBoost'
  n_estimators: 100 # Number of trees
  max_depth: 10 # Maximum tree depth
  min_samples_split: 5 # Min samples to split node
  min_samples_leaf: 2 # Min samples in leaf node
```

## 🔄 DVC Pipeline Stages

### Stage 1: Preprocess

```bash
python src/preprocess.py
```

- Handles missing values using imputation
- Splits data into training (80%) and testing (20%) sets
- Outputs: `data/train.csv`, `data/test.csv`

### Stage 2: Train

```bash
python src/train.py
```

- Trains a RandomForest or XGBoost classifier
- Uses hyperparameters from `params.yaml`
- Outputs: `models/model.joblib`

### Stage 3: Evaluate

```bash
python src/evaluate.py
```

- Evaluates model on test data
- Calculates accuracy, precision, recall, F1-score
- Outputs: `metrics.json`

## 🌐 API Usage

### Health Check

```bash
curl http://localhost:8000/health
```

### Single Prediction

```bash
curl -X POST "http://localhost:8000/predict" \
  -H "Content-Type: application/json" \
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

**Response:**

```json
{
  "potability": 1,
  "potability_label": "Potable",
  "confidence": 0.85
}
```

### Batch Prediction

```bash
curl -X POST "http://localhost:8000/predict/batch" \
  -H "Content-Type: application/json" \
  -d '[
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
    },
    {
      "ph": 6.5,
      "Hardness": 150.0,
      "Solids": 15000.0,
      "Chloramines": 6.0,
      "Sulfate": 300.0,
      "Conductivity": 350.0,
      "Organic_carbon": 12.0,
      "Trihalomethanes": 60.0,
      "Turbidity": 3.5
    }
  ]'
```

## 📈 Model Performance

After running the pipeline, check `metrics.json` for detailed performance metrics:

```json
{
  "accuracy": 0.6234,
  "precision": 0.6543,
  "recall": 0.5891,
  "f1_score": 0.6201,
  "confusion_matrix": {
    "true_negative": 345,
    "false_positive": 123,
    "false_negative": 89,
    "true_positive": 199
  }
}
```

## 🔧 Advanced Usage

### Experiment Tracking

```bash
# View pipeline DAG
dvc dag

# Check pipeline status
dvc status

# Show parameter dependencies
dvc params diff
```

### Model Versioning

```bash
# Tag a specific model version
dvc tag -a my-model-v1.0 models/model.joblib

# List all versions
dvc tag list
```

### Hyperparameter Tuning

1. Modify `params.yaml` with new parameters
2. Run `dvc repro` to retrain with new settings
3. Compare metrics: `dvc metrics diff`

## 📝 API Endpoints

| Method | Endpoint         | Description             |
| ------ | ---------------- | ----------------------- |
| GET    | `/`              | Root endpoint, API info |
| GET    | `/health`        | Health check            |
| POST   | `/predict`       | Single prediction       |
| POST   | `/predict/batch` | Batch predictions       |
| GET    | `/docs`          | Interactive Swagger UI  |
| GET    | `/redoc`         | ReDoc documentation     |

## 🧪 Testing the API

Visit http://localhost:8000/docs to access the interactive Swagger documentation where you can:

- View all available endpoints
- Test API requests directly from the browser
- See request/response schemas
- Explore example payloads

## 🛠️ Technology Stack

- **ML Framework**: scikit-learn, XGBoost
- **Data Processing**: pandas, numpy
- **Pipeline Orchestration**: DVC
- **API Framework**: FastAPI
- **Web Server**: Uvicorn
- **Validation**: Pydantic
- **Model Serialization**: joblib

## 📦 Requirements

See `requirements.txt` for the complete list of dependencies.

## 🤝 Contributing

1. Modify pipeline stages or parameters
2. Run `dvc repro` to validate changes
3. Check metrics with `dvc metrics show`
4. Test API endpoints thoroughly

## 📄 License

This project is for educational purposes.

## 🌟 Next Steps

- [ ] Add experiment tracking with MLflow or Weights & Biases
- [ ] Implement feature engineering pipeline
- [ ] Add data drift detection
- [ ] Create Docker container for deployment
- [ ] Add CI/CD pipeline with GitHub Actions
- [ ] Implement A/B testing for models
- [ ] Add logging and monitoring

---

**Built with ❤️ using DVC and FastAPI**
