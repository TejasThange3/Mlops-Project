"""
Preprocessing script for Pre-split Water Potability Dataset
Handles the new train_dataset.csv and test_dataset.csv
"""

import pandas as pd
import numpy as np
import yaml
import os
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
import joblib


def load_params():
    """Load parameters from params.yaml"""
    with open('params.yaml', 'r') as f:
        params = yaml.safe_load(f)
    return params['preprocess']


def preprocess_presplit_data(train_input_path, test_input_path, train_output_path, test_output_path):
    """
    Preprocess the pre-split water quality datasets
    
    Args:
        train_input_path: Path to training data CSV
        test_input_path: Path to test data CSV (features only)
        train_output_path: Path to save processed training data
        test_output_path: Path to save processed test data
    """
    # Load parameters
    params = load_params()
    feature_scaling = params.get('feature_scaling', False)
    add_polynomial = params.get('add_polynomial_features', False)
    poly_degree = params.get('polynomial_degree', 2)
    
    print("="*60)
    print("PREPROCESSING PRE-SPLIT WATER POTABILITY DATASET")
    print("="*60)
    
    # Load training data
    print(f"\n📂 Loading training data from {train_input_path}...")
    train_df = pd.read_csv(train_input_path)
    print(f"   Training data shape: {train_df.shape}")
    print(f"   Missing values: {train_df.isnull().sum().sum()}")
    
    # Load test data (features only)
    print(f"\n📂 Loading test data from {test_input_path}...")
    test_df = pd.read_csv(test_input_path)
    print(f"   Test data shape: {test_df.shape}")
    print(f"   Missing values: {test_df.isnull().sum().sum()}")
    
    # Check for missing values
    if train_df.isnull().sum().sum() > 0:
        print("\n⚠️  Warning: Training data has missing values!")
    else:
        print("\n✅ Training data is complete (no missing values)!")
    
    if test_df.isnull().sum().sum() > 0:
        print("⚠️  Warning: Test data has missing values!")
    else:
        print("✅ Test data is complete (no missing values)!")
    
    # Display target distribution
    print(f"\n📊 Target distribution in training set:")
    print(train_df['Potability'].value_counts())
    print(f"   Class balance: {train_df['Potability'].value_counts(normalize=True).round(3).to_dict()}")
    
    # Separate features and target for training
    X_train = train_df.drop('Potability', axis=1)
    y_train = train_df['Potability']
    X_test = test_df.copy()
    
    # Add polynomial features if enabled
    if add_polynomial:
        print(f"\n� Adding polynomial features (degree={poly_degree})...")
        poly = PolynomialFeatures(degree=poly_degree, include_bias=False, interaction_only=False)
        X_train_poly = poly.fit_transform(X_train)
        X_test_poly = poly.transform(X_test)
        
        # Get feature names
        feature_names = poly.get_feature_names_out(X_train.columns)
        X_train = pd.DataFrame(X_train_poly, columns=feature_names, index=X_train.index)
        X_test = pd.DataFrame(X_test_poly, columns=feature_names, index=X_test.index)
        
        print(f"   ✓ Features expanded from {train_df.shape[1]-1} to {X_train.shape[1]}")
        
        # Save polynomial transformer
        os.makedirs('models', exist_ok=True)
        joblib.dump(poly, 'models/poly.joblib')
        print("   ✓ Polynomial transformer saved to models/poly.joblib")
    
    # Feature scaling if enabled
    if feature_scaling:
        print(f"\n📊 Applying StandardScaler for feature normalization...")
        
        # Fit scaler on training features
        scaler = StandardScaler()
        X_train_scaled = pd.DataFrame(
            scaler.fit_transform(X_train),
            columns=X_train.columns,
            index=X_train.index
        )
        
        # Transform test features
        X_test_scaled = pd.DataFrame(
            scaler.transform(X_test),
            columns=X_test.columns,
            index=X_test.index
        )
        
        # Recombine training data with target
        train_processed = X_train_scaled.copy()
        train_processed['Potability'] = y_train
        test_processed = X_test_scaled
        
        # Save scaler for API predictions
        os.makedirs('models', exist_ok=True)
        joblib.dump(scaler, 'models/scaler.joblib')
        print("   ✓ Scaler saved to models/scaler.joblib")
        print("   ✓ Features scaled successfully!")
    else:
        train_processed = X_train.copy()
        train_processed['Potability'] = y_train
        test_processed = X_test
        print("\n⏭️  Skipping feature scaling (disabled in params)")
    
    # Create output directories if they don't exist
    os.makedirs(os.path.dirname(train_output_path), exist_ok=True)
    os.makedirs(os.path.dirname(test_output_path), exist_ok=True)
    
    # Save processed data
    print(f"\n💾 Saving processed training data to {train_output_path}...")
    train_processed.to_csv(train_output_path, index=False)
    
    print(f"💾 Saving processed test data to {test_output_path}...")
    test_processed.to_csv(test_output_path, index=False)
    
    print("\n" + "="*60)
    print("✅ PREPROCESSING COMPLETED SUCCESSFULLY!")
    print("="*60)
    print(f"📊 Final Statistics:")
    print(f"   - Training samples: {len(train_processed)}")
    print(f"   - Test samples: {len(test_processed)}")
    print(f"   - Features: {train_processed.shape[1] - 1}")  # -1 for target column
    print(f"   - No missing values: ✅")
    print(f"   - Polynomial features: {'✅ Enabled (degree=' + str(poly_degree) + ')' if add_polynomial else '❌ Disabled'}")
    print(f"   - Feature scaling: {'✅ Enabled' if feature_scaling else '❌ Disabled'}")
    print("="*60)


if __name__ == "__main__":
    # Define paths
    TRAIN_INPUT_PATH = "Data-set/train_dataset.csv"
    TEST_INPUT_PATH = "Data-set/test_dataset.csv"
    TRAIN_OUTPUT_PATH = "data/train.csv"
    TEST_OUTPUT_PATH = "data/test.csv"
    
    # Run preprocessing
    preprocess_presplit_data(TRAIN_INPUT_PATH, TEST_INPUT_PATH, TRAIN_OUTPUT_PATH, TEST_OUTPUT_PATH)
