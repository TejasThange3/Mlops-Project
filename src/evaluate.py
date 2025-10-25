"""
Model Evaluation Script for Water Potability Prediction
Generates detailed classification metrics, confusion matrix, and cross-validation scores
"""

import pandas as pd
import numpy as np
import joblib
import json
import os
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, 
    confusion_matrix, classification_report, roc_auc_score
)
from sklearn.model_selection import cross_val_score, StratifiedKFold


def evaluate_model(train_path, model_path, metrics_output):
    """
    Comprehensive model evaluation with detailed metrics
    
    Args:
        train_path: Path to training data CSV
        model_path: Path to trained model
        metrics_output: Path to save metrics JSON
    """
    print("\n" + "="*70)
    print("🔍 MODEL EVALUATION - Water Potability Prediction")
    print("="*70 + "\n")
    
    # Load training data and model
    print("📂 Loading data and model...")
    train_data = pd.read_csv(train_path)
    model = joblib.load(model_path)
    
    # Separate features and target
    X = train_data.drop('Potability', axis=1)
    y = train_data['Potability']
    
    print(f"   ✓ Training samples: {len(X)}")
    print(f"   ✓ Features: {X.shape[1]}")
    print(f"   ✓ Class distribution: Not Potable={sum(y==0)}, Potable={sum(y==1)}")
    
    # Make predictions on training set
    print("\n📊 Generating predictions on training data...")
    y_pred = model.predict(X)
    y_pred_proba = model.predict_proba(X)[:, 1]
    
    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)
    precision = precision_score(y, y_pred, zero_division=0)
    recall = recall_score(y, y_pred, zero_division=0)
    f1 = f1_score(y, y_pred, zero_division=0)
    
    try:
        roc_auc = roc_auc_score(y, y_pred_proba)
    except:
        roc_auc = 0.0
    
    # Confusion Matrix
    cm = confusion_matrix(y, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    print("\n" + "="*70)
    print("📈 TRAINING SET PERFORMANCE")
    print("="*70)
    print(f"Accuracy:  {accuracy:.4f} ({accuracy*100:.2f}%)")
    print(f"Precision: {precision:.4f}")
    print(f"Recall:    {recall:.4f}")
    print(f"F1-Score:  {f1:.4f}")
    print(f"ROC-AUC:   {roc_auc:.4f}")
    
    print("\n" + "-"*70)
    print("🔢 CONFUSION MATRIX")
    print("-"*70)
    print(f"                 Predicted Not Potable  |  Predicted Potable")
    print(f"Actual Not Potable:    {tn:>6}         |      {fp:>6}")
    print(f"Actual Potable:        {fn:>6}         |      {tp:>6}")
    print("-"*70)
    print(f"True Negatives (TN):  {tn}")
    print(f"False Positives (FP): {fp}")
    print(f"False Negatives (FN): {fn}")
    print(f"True Positives (TP):  {tp}")
    
    print("\n" + "="*70)
    print("📋 DETAILED CLASSIFICATION REPORT")
    print("="*70)
    print(classification_report(
        y, y_pred, 
        target_names=['Not Potable (0)', 'Potable (1)'],
        digits=4
    ))
    
    # Cross-Validation Evaluation
    print("\n" + "="*70)
    print("🔄 CROSS-VALIDATION ANALYSIS (5-Fold Stratified)")
    print("="*70)
    print("Performing 5-fold cross-validation to assess generalization...")
    
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
    cv_scores = cross_val_score(model, X, y, cv=cv, scoring='accuracy', n_jobs=-1)
    
    print(f"\nFold Scores: {[f'{score:.4f}' for score in cv_scores]}")
    print(f"Mean CV Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
    print(f"Min CV Accuracy:  {cv_scores.min():.4f}")
    print(f"Max CV Accuracy:  {cv_scores.max():.4f}")
    
    # Check for overfitting
    train_accuracy = accuracy
    cv_accuracy = cv_scores.mean()
    overfitting_gap = train_accuracy - cv_accuracy
    
    print("\n" + "-"*70)
    print("⚠️  OVERFITTING CHECK")
    print("-"*70)
    print(f"Training Accuracy:        {train_accuracy:.4f} ({train_accuracy*100:.2f}%)")
    print(f"Cross-Validation Accuracy: {cv_accuracy:.4f} ({cv_accuracy*100:.2f}%)")
    print(f"Overfitting Gap:          {overfitting_gap:.4f} ({overfitting_gap*100:.2f}%)")
    
    if overfitting_gap > 0.10:
        print("❌ WARNING: Model shows significant overfitting (gap > 10%)")
        print("   Consider: Increase regularization, reduce model complexity")
    elif overfitting_gap > 0.05:
        print("⚠️  CAUTION: Model shows moderate overfitting (gap > 5%)")
        print("   Model may benefit from additional regularization")
    else:
        print("✅ GOOD: Model shows minimal overfitting (gap < 5%)")
    
    # Save metrics to JSON
    metrics = {
        "training_metrics": {
            "accuracy": float(accuracy),
            "precision": float(precision),
            "recall": float(recall),
            "f1_score": float(f1),
            "roc_auc": float(roc_auc)
        },
        "confusion_matrix": {
            "true_negatives": int(tn),
            "false_positives": int(fp),
            "false_negatives": int(fn),
            "true_positives": int(tp)
        },
        "cross_validation": {
            "cv_mean_accuracy": float(cv_scores.mean()),
            "cv_std": float(cv_scores.std()),
            "cv_min": float(cv_scores.min()),
            "cv_max": float(cv_scores.max())
        },
        "overfitting_analysis": {
            "training_accuracy": float(train_accuracy),
            "cv_accuracy": float(cv_accuracy),
            "overfitting_gap": float(overfitting_gap),
            "overfitting_status": "high" if overfitting_gap > 0.10 else ("moderate" if overfitting_gap > 0.05 else "low")
        }
    }
    
    # Create output directory if needed
    os.makedirs(os.path.dirname(metrics_output) if os.path.dirname(metrics_output) else ".", exist_ok=True)
    
    # Save metrics
    with open(metrics_output, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print("\n" + "="*70)
    print(f"💾 Metrics saved to: {metrics_output}")
    print("="*70 + "\n")
    
    return metrics


if __name__ == "__main__":
    # Define paths
    TRAIN_PATH = "data/train.csv"
    MODEL_PATH = "models/model.joblib"
    METRICS_OUTPUT = "metrics.json"
    
    # Run evaluation
    evaluate_model(TRAIN_PATH, MODEL_PATH, METRICS_OUTPUT)
