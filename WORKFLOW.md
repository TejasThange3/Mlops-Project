# MLOps Project Workflow - Water Potability Prediction

## Pipeline Stages

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    MLOps Project Workflow                                │
│              (Water Potability Prediction)                               │
└─────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│ 1. Raw Data: water_quality.csv                                           │
│    └─> "Download & Place in data/"                                       │
│         └─> DVC Init & Add Data                                          │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 2. DVC Init & Add Data                                                   │
│    └─> Tracks data version                                               │
│         └─> Data Version Control (DVC Cache)                             │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 3. Data Version Control (DVC Cache)                                      │
│    └─> Input for preprocessing                                           │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 4. DVC Stage: Preprocessing Script (src/preprocess.py)                   │
│    └─> Handles missing values, splits data (train/test)                  │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 5. Processed Data: train.csv & test.csv                                  │
│    └─> Outputs of preprocess stage                                       │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 6. DVC Tracks Processed Data                                             │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 7. DVC Stage: Training Script (src/train.py)                             │
│    └─> Reads train.csv, trains ML model (e.g., RandomForest)             │
│         using params.yaml                                                 │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 8. Trained Model Artifact: models/model.joblib                           │
│    └─> Output of train stage                                             │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 9. DVC Tracks Model Version                                              │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 10. DVC Stage: Evaluation Script (src/evaluate.py)                       │
│     └─> Reads test.csv, uses model.joblib, calculates metrics            │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 11. Evaluation Metrics: metrics.json                                     │
│     └─> Output of evaluate stage, cache: false                           │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 12. DVC Tracks Metrics                                                   │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 13. Experiment Tracking & Model Selection                                │
│     └─> Compare metrics with `dvc exp show`                              │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 14. FastAPI Application (main.py)                                        │
│     └─> Deployed via                                                     │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 15. REST API Endpoint: /api/predict                                      │
│     └─> Exposes                                                           │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 16. Use UI/fronted for a good user experience: / (root)                  │
│     └─> Serves                                                            │
└──────────────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────────────────┐
│ 17. Real-time Water Quality Prediction                                   │
│     └─> Enables                                                           │
└──────────────────────────────────────────────────────────────────────────┘


## Key Components

### DVC Pipeline (dvc.yaml)
- **Stage 1: preprocess** - Data cleaning and splitting
- **Stage 2: train** - Model training with hyperparameters
- **Stage 3: evaluate** - Performance metrics calculation

### Configuration (params.yaml)
- Preprocessing parameters (test_size, imputation strategy)
- Training parameters (model type, n_estimators, max_depth, etc.)
- Evaluation metrics to track

### API Endpoints (main.py)
- **GET /**        - Root endpoint
- **GET /health**  - Health check
- **POST /predict** - Single prediction
- **POST /predict/batch** - Batch predictions
- **GET /docs**    - Interactive Swagger UI

### Data Flow
1. Raw data → DVC tracking
2. Preprocessing → train.csv, test.csv
3. Training → model.joblib
4. Evaluation → metrics.json
5. Deployment → FastAPI → Predictions
```
