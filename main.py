"""
FastAPI Application for Water Potability Prediction
Serves the trained ML model via REST API with Swagger documentation
"""

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import joblib
import numpy as np
import os
import sys
from typing import Dict, Any, List

# Add src directory to path for model_manager import
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
from model_manager import model_manager

# Initialize FastAPI app
app = FastAPI(
    title="Water Potability Prediction API",
    description="API for predicting water potability based on physicochemical properties",
    version="1.0.0"
)

# Add CORS middleware to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global variables to store the model and scaler
model = None
scaler = None
MODEL_PATH = "models/model.joblib"
SCALER_PATH = "models/scaler.joblib"


# Pydantic model for input validation
class WaterQualityFeatures(BaseModel):
    """
    Input schema for water quality features
    """
    ph: float = Field(..., description="pH value of water (0-14)", ge=0, le=14)
    Hardness: float = Field(..., description="Water hardness in mg/L", ge=0)
    Solids: float = Field(..., description="Total dissolved solids in ppm", ge=0)
    Chloramines: float = Field(..., description="Chloramines concentration in ppm", ge=0)
    Sulfate: float = Field(..., description="Sulfate concentration in mg/L", ge=0)
    Conductivity: float = Field(..., description="Electrical conductivity in μS/cm", ge=0)
    Organic_carbon: float = Field(..., description="Organic carbon content in ppm", ge=0)
    Trihalomethanes: float = Field(..., description="Trihalomethanes concentration in μg/L", ge=0)
    Turbidity: float = Field(..., description="Turbidity in NTU", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }


# Pydantic model for prediction response
class PredictionResponse(BaseModel):
    """
    Output schema for prediction results
    """
    potability: int = Field(..., description="Predicted potability (0 = Not Potable, 1 = Potable)")
    potability_label: str = Field(..., description="Human-readable prediction label")
    confidence: float = Field(..., description="Prediction confidence/probability")
    
    class Config:
        json_schema_extra = {
            "example": {
                "potability": 1,
                "potability_label": "Potable",
                "confidence": 0.85
            }
        }


def load_model():
    """Load the trained model and scaler from disk (current version)"""
    global model, scaler
    try:
        # Load current version from model manager
        current_version = model_manager.get_current_version()
        model, scaler = model_manager.load_model_and_scaler(current_version)
        print(f"[OK] Model loaded successfully: {current_version}")
        print(f"[OK] Scaler loaded successfully")
    except Exception as e:
        # Fallback to original loading method
        if not os.path.exists(MODEL_PATH):
            raise FileNotFoundError(
                f"Model file not found at {MODEL_PATH}. "
                "Please train the model first by running: dvc repro"
            )
        model = joblib.load(MODEL_PATH)
        print(f"[OK] Model loaded successfully from {MODEL_PATH}")
        
        # Load scaler if it exists
        if os.path.exists(SCALER_PATH):
            scaler = joblib.load(SCALER_PATH)
            print(f"[OK] Scaler loaded successfully from {SCALER_PATH}")
        else:
            print("[WARN] No scaler found, using raw features")


@app.on_event("startup")
async def startup_event():
    """Load model when the API starts"""
    try:
        load_model()
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")
        print("Model will be loaded on first prediction request.")


@app.get("/", tags=["Root"])
async def root():
    """
    Serve the main frontend page
    """
    return FileResponse("static/index.html")


@app.get("/api", tags=["Root"])
async def api_root() -> Dict[str, Any]:
    """
    API root endpoint - API health check
    """
    return {
        "message": "Water Potability Prediction API",
        "status": "running",
        "docs": "/docs",
        "frontend": "/",
        "model_loaded": model is not None
    }


@app.get("/health", tags=["Health"])
async def health_check() -> Dict[str, Any]:
    """
    Health check endpoint
    """
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }


@app.post("/predict", response_model=PredictionResponse, tags=["Prediction"])
async def predict(features: WaterQualityFeatures) -> PredictionResponse:
    """
    Predict water potability based on physicochemical properties
    
    - **ph**: pH value of water (0-14)
    - **Hardness**: Water hardness in mg/L
    - **Solids**: Total dissolved solids in ppm
    - **Chloramines**: Chloramines concentration in ppm
    - **Sulfate**: Sulfate concentration in mg/L
    - **Conductivity**: Electrical conductivity in μS/cm
    - **Organic_carbon**: Organic carbon content in ppm
    - **Trihalomethanes**: Trihalomethanes concentration in μg/L
    - **Turbidity**: Turbidity in NTU
    
    Returns prediction with confidence score.
    """
    global model
    
    # Load model if not already loaded
    if model is None:
        try:
            load_model()
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Model not available: {str(e)}"
            )
    
    try:
        # Prepare input data
        input_data = np.array([[
            features.ph,
            features.Hardness,
            features.Solids,
            features.Chloramines,
            features.Sulfate,
            features.Conductivity,
            features.Organic_carbon,
            features.Trihalomethanes,
            features.Turbidity
        ]])
        
        # Apply scaler if available
        if scaler is not None:
            input_data = scaler.transform(input_data)
        
        # Make prediction
        prediction = int(model.predict(input_data)[0])
        
        # Get prediction probability/confidence
        if hasattr(model, 'predict_proba'):
            probabilities = model.predict_proba(input_data)[0]
            confidence = float(probabilities[prediction])
        else:
            confidence = 1.0  # Default confidence if probabilities not available
        
        # Prepare response
        potability_label = "Potable" if prediction == 1 else "Not Potable"
        
        return PredictionResponse(
            potability=prediction,
            potability_label=potability_label,
            confidence=confidence
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {str(e)}"
        )


@app.post("/predict/batch", tags=["Prediction"])
async def predict_batch(features_list: list[WaterQualityFeatures]) -> Dict[str, Any]:
    """
    Batch prediction endpoint for multiple water samples
    
    Accepts a list of water quality feature sets and returns predictions for all.
    """
    global model
    
    # Load model if not already loaded
    if model is None:
        try:
            load_model()
        except Exception as e:
            raise HTTPException(
                status_code=503,
                detail=f"Model not available: {str(e)}"
            )
    
    try:
        predictions = []
        
        for features in features_list:
            # Prepare input data
            input_data = np.array([[
                features.ph,
                features.Hardness,
                features.Solids,
                features.Chloramines,
                features.Sulfate,
                features.Conductivity,
                features.Organic_carbon,
                features.Trihalomethanes,
                features.Turbidity
            ]])
            
            # Apply scaler if available
            if scaler is not None:
                input_data = scaler.transform(input_data)
            
            # Make prediction
            prediction = int(model.predict(input_data)[0])
            
            # Get prediction probability/confidence
            if hasattr(model, 'predict_proba'):
                probabilities = model.predict_proba(input_data)[0]
                confidence = float(probabilities[prediction])
            else:
                confidence = 1.0
            
            potability_label = "Potable" if prediction == 1 else "Not Potable"
            
            predictions.append({
                "potability": prediction,
                "potability_label": potability_label,
                "confidence": confidence
            })
        
        return {"predictions": predictions, "count": len(predictions)}
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction failed: {str(e)}"
        )


# ============================================================================
# Model Version Management Endpoints
# ============================================================================

class RetrainRequest(BaseModel):
    """Request schema for retraining with new data"""
    water_quality: WaterQualityFeatures = Field(..., description="Water quality parameters")
    actual_potability: int = Field(..., description="Actual potability label (0 or 1)", ge=0, le=1)
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }


@app.post("/retrain", tags=["Model Management"])
async def retrain_model(request: RetrainRequest) -> Dict[str, Any]:
    """
    Retrain the model with a new data point
    
    This endpoint allows incremental learning by adding new labeled data
    and creating a new model version.
    """
    import sys
    import io
    import traceback
    
    try:
        # Suppress stdout/stderr during retraining to avoid encoding issues
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = io.StringIO()
        sys.stderr = io.StringIO()
        
        try:
            # Convert Pydantic model to dict
            water_data = {
                'ph': request.water_quality.ph,
                'Hardness': request.water_quality.Hardness,
                'Solids': request.water_quality.Solids,
                'Chloramines': request.water_quality.Chloramines,
                'Sulfate': request.water_quality.Sulfate,
                'Conductivity': request.water_quality.Conductivity,
                'Organic_carbon': request.water_quality.Organic_carbon,
                'Trihalomethanes': request.water_quality.Trihalomethanes,
                'Turbidity': request.water_quality.Turbidity
            }
            
            # Retrain using model manager
            result = model_manager.retrain_incremental(water_data, request.actual_potability)
            
            # Reload the model (new version is now current)
            load_model()
            
            # Return sanitized version
            return {
                "success": result.get("success", True),
                "version": result.get("version", "V1"),
                "training_samples": result.get("training_samples", 0),
                "incremental_samples": result.get("incremental_samples", 1),
                "accuracy": result.get("accuracy", 0.0),
                "cv_accuracy": result.get("cv_accuracy", 0.0),
                "message": f"Model {result.get('version', 'V1')} trained successfully"
            }
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr
        
    except Exception as e:
        # Sanitize error message
        try:
            error_msg = str(e).encode('ascii', 'ignore').decode('ascii')
        except:
            error_msg = "Encoding error during retraining"
        
        raise HTTPException(
            status_code=500,
            detail=f"Retraining failed: {error_msg}"
        )


@app.get("/models/versions", tags=["Model Management"])
async def list_model_versions() -> Dict[str, Any]:
    """
    List all available model versions
    
    Returns information about all trained model versions including
    accuracy metrics and creation dates.
    """
    try:
        versions = model_manager.list_versions()
        current_version = model_manager.get_current_version()
        
        return {
            "current_version": current_version,
            "versions": versions,
            "total_versions": len(versions)
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to list versions: {str(e)}"
        )


class SwitchVersionRequest(BaseModel):
    """Request schema for switching model version"""
    version: str = Field(..., description="Version name to switch to (e.g., 'Original', 'V1', 'V2')")
    
    class Config:
        json_schema_extra = {
            "example": {
                "version": "V1"
            }
        }


@app.post("/models/switch", tags=["Model Management"])
async def switch_model_version(request: SwitchVersionRequest) -> Dict[str, Any]:
    """
    Switch to a different model version
    
    Changes the active model version used for predictions.
    """
    try:
        success = model_manager.switch_version(request.version)
        
        if not success:
            raise HTTPException(
                status_code=404,
                detail=f"Version '{request.version}' not found"
            )
        
        # Reload the model with new version
        load_model()
        
        return {
            "success": True,
            "message": f"Switched to model version: {request.version}",
            "current_version": model_manager.get_current_version()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to switch version: {str(e)}"
        )


@app.get("/models/current", tags=["Model Management"])
async def get_current_model() -> Dict[str, Any]:
    """
    Get information about the current active model
    """
    try:
        current_version = model_manager.get_current_version()
        versions = model_manager.list_versions()
        
        # Find current version info
        current_info = next((v for v in versions if v["version"] == current_version), None)
        
        return {
            "version": current_version,
            "info": current_info
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to get current model: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
