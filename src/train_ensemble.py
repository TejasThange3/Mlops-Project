"""
Ensemble Training script for Water Potability Prediction
Combines RandomForest, XGBoost, and GradientBoosting using VotingClassifier
"""

import pandas as pd
import yaml
import joblib
import os
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier, VotingClassifier
from xgboost import XGBClassifier


def load_params():
    """Load parameters from params.yaml"""
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    return params['train']


def train_ensemble_model(train_path, model_output_path):
    """
    Train a classifier (single or ensemble)
    
    Args:
        train_path: Path to training data CSV
        model_output_path: Path to save the trained model
    """
    # Load parameters
    params = load_params()
    random_state = params['random_state']
    model_type = params.get('model_type', 'Ensemble')
    
    print(f"Loading training data from {train_path}...")
    train_data = pd.read_csv(train_path)
    
    # Separate features and target
    X_train = train_data.drop('Potability', axis=1)
    y_train = train_data['Potability']
    
    print(f"Training data shape: {X_train.shape}")
    print(f"Target distribution:\n{y_train.value_counts()}")
    
    # Split for early stopping validation
    from sklearn.model_selection import train_test_split
    X_tr, X_val, y_tr, y_val = train_test_split(
        X_train, y_train, test_size=0.2, random_state=random_state, stratify=y_train
    )
    print(f"   Train: {len(X_tr)}, Validation: {len(X_val)}")
    
    # Train based on model type
    if model_type == "XGBoost":
        print(f"\n🚀 Training XGBoost Model (optimized for 80% accuracy)...")
        
        model = XGBClassifier(
            learning_rate=params.get('learning_rate', 0.01),
            max_depth=params.get('max_depth_xgb', 4),
            n_estimators=params.get('n_estimators_xgb', 500),
            scale_pos_weight=params.get('scale_pos_weight', 1.56),
            subsample=params.get('subsample', 0.8),
            colsample_bytree=params.get('colsample_bytree', 0.8),
            gamma=params.get('gamma', 1.0),
            min_child_weight=params.get('min_child_weight', 3),
            reg_alpha=params.get('reg_alpha', 0.3),
            reg_lambda=params.get('reg_lambda', 1.5),
            random_state=random_state,
            n_jobs=-1,
            eval_metric='logloss'
        )
        print("  ✓ XGBoost configured with optimized hyperparameters")
        
        # Train with early stopping
        early_stop = params.get('early_stopping_rounds', 50)
        model.fit(
            X_tr, y_tr,
            eval_set=[(X_val, y_val)],
            verbose=False
        )
        
        print(f"\n✓ XGBoost training completed!")
        print(f"  - Best iteration: {model.best_iteration if hasattr(model, 'best_iteration') else 'N/A'}")
        print(f"  - Training samples: {len(X_train)}")
        print(f"  - Features: {X_train.shape[1]}")
        
    else:  # Ensemble mode
        print(f"\n🌳 Initializing Ensemble Models...")
        
        # Model 1: RandomForest
        rf_model = RandomForestClassifier(
            n_estimators=params.get('n_estimators', 150),
            max_depth=params.get('max_depth', 8),
            min_samples_split=params.get('min_samples_split', 15),
            min_samples_leaf=params.get('min_samples_leaf', 8),
            max_features=params.get('max_features', 'sqrt'),
            class_weight=params.get('class_weight', 'balanced'),
            random_state=random_state,
            n_jobs=-1
        )
        print("  ✓ RandomForest configured")
        
        # Model 2: XGBoost
        xgb_model = XGBClassifier(
            learning_rate=params.get('learning_rate', 0.01),
            max_depth=params.get('max_depth_xgb', 4),
            n_estimators=params.get('n_estimators_xgb', 500),
            scale_pos_weight=params.get('scale_pos_weight', 1.56),
            subsample=params.get('subsample', 0.8),
            colsample_bytree=params.get('colsample_bytree', 0.8),
            gamma=params.get('gamma', 1.0),
            min_child_weight=params.get('min_child_weight', 3),
            reg_alpha=params.get('reg_alpha', 0.3),
            reg_lambda=params.get('reg_lambda', 1.5),
            random_state=random_state,
            n_jobs=-1,
            eval_metric='logloss'
        )
        print("  ✓ XGBoost configured")
        
        # Model 3: Gradient Boosting (fine-tuned for 80% target)
        gb_model = GradientBoostingClassifier(
            n_estimators=250,
            learning_rate=0.05,
            max_depth=4,
            min_samples_split=18,
            min_samples_leaf=9,
            max_features='sqrt',
            subsample=0.75,
            random_state=random_state
        )
        print("  ✓ GradientBoosting configured (fine-tuned)")
        
        # Create Voting Ensemble
        print(f"\n🗳️  Creating Voting Ensemble (soft voting)...")
        model = VotingClassifier(
            estimators=[
                ('rf', rf_model),
                ('xgb', xgb_model),
                ('gb', gb_model)
            ],
            voting='soft',
            n_jobs=-1
        )
        
        # Train the ensemble
        print(f"\n🚀 Training Ensemble Model...")
        model.fit(X_train, y_train)
        
        print("\n✓ Ensemble training completed!")
        print(f"  - Models in ensemble: RandomForest, XGBoost, GradientBoosting")
        print(f"  - Voting method: soft (probability-based)")
        print(f"  - Training samples: {len(X_train)}")
        print(f"  - Features: {X_train.shape[1]}")
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(model_output_path), exist_ok=True)
    
    # Save the trained model
    print(f"\n💾 Saving model to {model_output_path}...")
    joblib.dump(model, model_output_path)
    
    print(f"\n✅ Model saved successfully! (Type: {model_type})")


if __name__ == "__main__":
    # Define paths
    TRAIN_PATH = "data/train.csv"
    MODEL_OUTPUT_PATH = "models/model.joblib"
    
    # Run training
    train_ensemble_model(TRAIN_PATH, MODEL_OUTPUT_PATH)
