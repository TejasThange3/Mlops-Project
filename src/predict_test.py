"""
Prediction script for test dataset (without labels)
Generates predictions and saves them
"""

import pandas as pd
import joblib
import os


def generate_predictions(test_path, model_path, predictions_output_path):
    """
    Generate predictions for test data (no labels)
    
    Args:
        test_path: Path to test data CSV (features only)
        model_path: Path to trained model
        predictions_output_path: Path to save predictions
    """
    print("="*60)
    print("GENERATING PREDICTIONS FOR TEST DATASET")
    print("="*60)
    
    print(f"\n📂 Loading test data from {test_path}...")
    test_data = pd.read_csv(test_path)
    print(f"   Test data shape: {test_data.shape}")
    
    # Load the trained model
    print(f"\n🤖 Loading model from {model_path}...")
    model = joblib.load(model_path)
    print(f"   ✓ Model loaded successfully!")
    
    # Make predictions
    print("\n🔮 Making predictions on test data...")
    predictions = model.predict(test_data)
    
    # Get prediction probabilities if available
    if hasattr(model, 'predict_proba'):
        probabilities = model.predict_proba(test_data)
        confidence = probabilities.max(axis=1)
    else:
        confidence = [1.0] * len(predictions)
    
    # Create predictions DataFrame
    predictions_df = pd.DataFrame({
        'Prediction': predictions,
        'Prediction_Label': ['Potable' if p == 1 else 'Not Potable' for p in predictions],
        'Confidence': confidence
    })
    
    # Add original features for reference
    predictions_df = pd.concat([test_data, predictions_df], axis=1)
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(predictions_output_path) if os.path.dirname(predictions_output_path) else '.', exist_ok=True)
    
    # Save predictions
    print(f"\n💾 Saving predictions to {predictions_output_path}...")
    predictions_df.to_csv(predictions_output_path, index=False)
    
    # Display statistics
    print("\n" + "="*60)
    print("✅ PREDICTIONS GENERATED SUCCESSFULLY!")
    print("="*60)
    print(f"📊 Prediction Statistics:")
    print(f"   - Total samples: {len(predictions)}")
    print(f"   - Predicted Potable: {(predictions == 1).sum()} ({(predictions == 1).sum()/len(predictions)*100:.1f}%)")
    print(f"   - Predicted Not Potable: {(predictions == 0).sum()} ({(predictions == 0).sum()/len(predictions)*100:.1f}%)")
    print(f"   - Average confidence: {confidence.mean():.4f}")
    print("="*60)


if __name__ == "__main__":
    # Define paths
    TEST_PATH = "data/test.csv"
    MODEL_PATH = "models/model.joblib"
    PREDICTIONS_OUTPUT_PATH = "predictions.csv"
    
    # Generate predictions
    generate_predictions(TEST_PATH, MODEL_PATH, PREDICTIONS_OUTPUT_PATH)
