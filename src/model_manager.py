"""
Model Version Manager
Handles multiple model versions, saving, loading, and metadata tracking
"""

import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from typing import Dict, List, Any, Tuple


class ModelVersionManager:
    """Manages multiple versions of trained models"""
    
    def __init__(self, models_dir: str = "models"):
        self.models_dir = Path(models_dir)
        self.versions_dir = self.models_dir / "versions"
        self.versions_dir.mkdir(parents=True, exist_ok=True)
        self.metadata_file = self.versions_dir / "metadata.json"
        self.training_data_file = self.versions_dir / "incremental_training_data.csv"
        
        # Initialize metadata
        self._load_metadata()
    
    def _load_metadata(self):
        """Load metadata from file or create new"""
        if self.metadata_file.exists():
            with open(self.metadata_file, 'r') as f:
                self.metadata = json.load(f)
        else:
            # Initialize with original model
            self.metadata = {
                "current_version": "Original",
                "versions": {
                    "Original": {
                        "created_at": datetime.now().isoformat(),
                        "description": "Original ensemble model (RF + XGBoost + GB)",
                        "training_samples": 2293,
                        "model_path": "model.joblib",
                        "scaler_path": "scaler.joblib",
                        "accuracy": 0.8439,
                        "cv_accuracy": 0.6424
                    }
                }
            }
            self._save_metadata()
    
    def _save_metadata(self):
        """Save metadata to file"""
        with open(self.metadata_file, 'w') as f:
            json.dump(self.metadata, indent=2, fp=f)
    
    def get_current_version(self) -> str:
        """Get the current active model version"""
        return self.metadata["current_version"]
    
    def list_versions(self) -> List[Dict[str, Any]]:
        """List all available model versions"""
        versions = []
        for version_name, version_info in self.metadata["versions"].items():
            versions.append({
                "version": version_name,
                "created_at": version_info["created_at"],
                "description": version_info["description"],
                "training_samples": version_info["training_samples"],
                "accuracy": version_info.get("accuracy", 0.0),
                "cv_accuracy": version_info.get("cv_accuracy", 0.0),
                "is_current": version_name == self.metadata["current_version"]
            })
        
        # Sort: Original first, then by version number
        def sort_key(v):
            if v["version"] == "Original":
                return (0, 0)
            else:
                try:
                    num = int(v["version"].replace("V", ""))
                    return (1, num)
                except:
                    return (2, 0)
        
        versions.sort(key=sort_key)
        return versions
    
    def switch_version(self, version_name: str) -> bool:
        """Switch to a different model version"""
        if version_name not in self.metadata["versions"]:
            return False
        
        self.metadata["current_version"] = version_name
        self._save_metadata()
        return True
    
    def load_model_and_scaler(self, version_name: str = None) -> Tuple[Any, Any]:
        """Load model and scaler for a specific version"""
        if version_name is None:
            version_name = self.metadata["current_version"]
        
        if version_name not in self.metadata["versions"]:
            raise ValueError(f"Version {version_name} not found")
        
        version_info = self.metadata["versions"][version_name]
        
        # Load model
        if version_name == "Original":
            model_path = self.models_dir / version_info["model_path"]
            scaler_path = self.models_dir / version_info["scaler_path"]
        else:
            model_path = self.versions_dir / version_info["model_path"]
            scaler_path = self.versions_dir / version_info["scaler_path"]
        
        model = joblib.load(model_path)
        scaler = joblib.load(scaler_path)
        
        return model, scaler
    
    def _get_next_version_number(self) -> str:
        """Get the next version number"""
        version_nums = []
        for version_name in self.metadata["versions"].keys():
            if version_name.startswith("V"):
                try:
                    num = int(version_name.replace("V", ""))
                    version_nums.append(num)
                except:
                    pass
        
        next_num = max(version_nums) + 1 if version_nums else 1
        return f"V{next_num}"
    
    def retrain_incremental(self, new_data: Dict[str, float], actual_label: int) -> Dict[str, Any]:
        """
        Retrain model with new data point
        
        Args:
            new_data: Dictionary with water quality parameters
            actual_label: Actual potability (0 or 1)
        
        Returns:
            Dictionary with retraining results
        """
        import sys
        import io
        import os
        import warnings
        
        # Suppress all output and warnings to avoid encoding issues
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        warnings.filterwarnings('ignore')
        os.environ['PYTHONIOENCODING'] = 'utf-8'
        
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        
        try:
            return self._do_retrain(new_data, actual_label)
        finally:
            sys.stdout.close()
            sys.stderr.close()
            sys.stdout = old_stdout
            sys.stderr = old_stderr
    
    def _do_retrain(self, new_data: Dict[str, float], actual_label: int) -> Dict[str, Any]:
        """Internal retraining logic"""
        import warnings
        warnings.filterwarnings('ignore')
        
        try:
            # Load current model and scaler
            current_model, current_scaler = self.load_model_and_scaler()
            
            # Load or create incremental training data
            if self.training_data_file.exists():
                incremental_df = pd.read_csv(self.training_data_file)
            else:
                # Start with empty dataframe
                incremental_df = pd.DataFrame(columns=[
                    'ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate',
                    'Conductivity', 'Organic_carbon', 'Trihalomethanes', 'Turbidity',
                    'Potability'
                ])
            
            # Add new data point
            new_row = {
                'ph': new_data.get('ph', 0),
                'Hardness': new_data.get('Hardness', 0),
                'Solids': new_data.get('Solids', 0),
                'Chloramines': new_data.get('Chloramines', 0),
                'Sulfate': new_data.get('Sulfate', 0),
                'Conductivity': new_data.get('Conductivity', 0),
                'Organic_carbon': new_data.get('Organic_carbon', 0),
                'Trihalomethanes': new_data.get('Trihalomethanes', 0),
                'Turbidity': new_data.get('Turbidity', 0),
                'Potability': actual_label
            }
            incremental_df = pd.concat([incremental_df, pd.DataFrame([new_row])], ignore_index=True)
            
            # Save updated incremental data
            incremental_df.to_csv(self.training_data_file, index=False)
            
            # Load original training data
            original_train = pd.read_csv("Data-set/train_dataset.csv")
            
            # Combine original + incremental data
            combined_df = pd.concat([original_train, incremental_df], ignore_index=True)
            
            # Prepare features and labels
            X = combined_df.drop('Potability', axis=1)
            y = combined_df['Potability']
            
            # Fit scaler on combined data
            from sklearn.preprocessing import StandardScaler
            new_scaler = StandardScaler()
            X_scaled = new_scaler.fit_transform(X)
            
            # NO print statements during training to avoid encoding issues
            
            rf_model = RandomForestClassifier(
                n_estimators=250,
                max_depth=6,
                min_samples_split=18,
                min_samples_leaf=9,
                max_features='sqrt',
                class_weight='balanced',
                random_state=42,
                n_jobs=-1
            )
            
            xgb_model = XGBClassifier(
                n_estimators=300,
                max_depth=4,
                learning_rate=0.05,
                subsample=0.75,
                colsample_bytree=0.75,
                gamma=2.5,
                min_child_weight=8,
                reg_alpha=0.5,
                reg_lambda=1.8,
                random_state=42,
                n_jobs=-1,
                eval_metric='logloss'
            )
            
            gb_model = GradientBoostingClassifier(
                n_estimators=250,
                learning_rate=0.05,
                max_depth=4,
                min_samples_split=18,
                min_samples_leaf=9,
                subsample=0.75,
                random_state=42
            )
            
            new_model = VotingClassifier(
                estimators=[
                    ('rf', rf_model),
                    ('xgb', xgb_model),
                    ('gb', gb_model)
                ],
                voting='soft',
                n_jobs=-1
            )
            
            # Train the model
            new_model.fit(X_scaled, y)
            
            # Evaluate with cross-validation
            cv_scores = cross_val_score(new_model, X_scaled, y, cv=5, scoring='accuracy')
            
            # Calculate training accuracy
            train_accuracy = new_model.score(X_scaled, y)
            
            # Generate new version name
            new_version_name = self._get_next_version_number()
            
            # Save new model and scaler
            model_filename = f"model_{new_version_name}.joblib"
            scaler_filename = f"scaler_{new_version_name}.joblib"
            
            joblib.dump(new_model, self.versions_dir / model_filename)
            joblib.dump(new_scaler, self.versions_dir / scaler_filename)
            
            # Update metadata
            self.metadata["versions"][new_version_name] = {
                "created_at": datetime.now().isoformat(),
                "description": f"Retrained with {len(incremental_df)} additional sample(s)",
                "training_samples": len(combined_df),
                "incremental_samples": len(incremental_df),
                "model_path": model_filename,
                "scaler_path": scaler_filename,
                "accuracy": float(train_accuracy),
                "cv_accuracy": float(cv_scores.mean())
            }
            
            # Auto-switch to new version
            self.metadata["current_version"] = new_version_name
            self._save_metadata()
            
            # NO print statements to avoid encoding issues
            
            return {
                "success": True,
                "version": new_version_name,
                "training_samples": len(combined_df),
                "incremental_samples": len(incremental_df),
                "accuracy": float(train_accuracy),
                "cv_accuracy": float(cv_scores.mean()),
                "cv_scores": [float(s) for s in cv_scores],
                "message": f"Model {new_version_name} trained successfully with {len(combined_df)} samples"
            }
        except Exception as e:
            # Sanitize any error messages
            error_str = str(e).encode('ascii', 'ignore').decode('ascii')
            raise RuntimeError(f"Retraining error: {error_str}")
    
    def delete_version(self, version_name: str) -> bool:
        """Delete a model version (cannot delete Original or current)"""
        if version_name == "Original":
            return False
        
        if version_name == self.metadata["current_version"]:
            return False
        
        if version_name not in self.metadata["versions"]:
            return False
        
        # Delete files
        version_info = self.metadata["versions"][version_name]
        model_path = self.versions_dir / version_info["model_path"]
        scaler_path = self.versions_dir / version_info["scaler_path"]
        
        if model_path.exists():
            model_path.unlink()
        if scaler_path.exists():
            scaler_path.unlink()
        
        # Remove from metadata
        del self.metadata["versions"][version_name]
        self._save_metadata()
        
        return True


# Global instance
model_manager = ModelVersionManager()
