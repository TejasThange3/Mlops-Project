"""
Test script for model versioning features
"""

import requests
import json

API_BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_list_versions():
    """Test listing all model versions"""
    print_section("Test 1: List Model Versions")
    
    response = requests.get(f"{API_BASE_URL}/models/versions")
    print(f"Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"\nCurrent Version: {data['current_version']}")
        print(f"Total Versions: {data['total_versions']}")
        print("\nAvailable Versions:")
        for version in data['versions']:
            print(f"  - {version['version']}")
            print(f"    Samples: {version['training_samples']}")
            print(f"    Accuracy: {version['accuracy']:.4f}")
            print(f"    CV Accuracy: {version['cv_accuracy']:.4f}")
            print(f"    Current: {version['is_current']}")
    else:
        print(f"Error: {response.text}")

def test_get_current_model():
    """Test getting current model info"""
    print_section("Test 2: Get Current Model")
    
    response = requests.get(f"{API_BASE_URL}/models/current")
    print(f"Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"\nCurrent Model: {data['version']}")
        print(f"Details: {json.dumps(data['info'], indent=2)}")
    else:
        print(f"Error: {response.text}")

def test_prediction():
    """Test making a prediction"""
    print_section("Test 3: Make Prediction")
    
    sample_data = {
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
    
    response = requests.post(f"{API_BASE_URL}/predict", json=sample_data)
    print(f"Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"\nPrediction: {data['potability_label']}")
        print(f"Confidence: {data['confidence']:.4f}")
        return sample_data  # Return for retraining test
    else:
        print(f"Error: {response.text}")
        return None

def test_retrain(sample_data):
    """Test retraining with new data"""
    print_section("Test 4: Retrain Model")
    
    if not sample_data:
        print("Skipping - no sample data from prediction")
        return
    
    retrain_request = {
        "water_quality": sample_data,
        "actual_potability": 1  # Simulating user feedback
    }
    
    print("Starting retraining... (this may take a minute)")
    response = requests.post(f"{API_BASE_URL}/retrain", json=retrain_request, timeout=120)
    print(f"Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"\n✅ Retraining Successful!")
        print(f"New Version: {data['version']}")
        print(f"Training Samples: {data['training_samples']}")
        print(f"Incremental Samples: {data['incremental_samples']}")
        print(f"Training Accuracy: {data['accuracy']:.4f}")
        print(f"CV Accuracy: {data['cv_accuracy']:.4f}")
    else:
        print(f"Error: {response.text}")

def test_switch_version():
    """Test switching between versions"""
    print_section("Test 5: Switch Version")
    
    # First, get list of versions
    versions_response = requests.get(f"{API_BASE_URL}/models/versions")
    if not versions_response.ok:
        print("Cannot get versions list")
        return
    
    versions = versions_response.json()['versions']
    
    # Try switching to Original
    print("\nSwitching to Original version...")
    switch_request = {"version": "Original"}
    response = requests.post(f"{API_BASE_URL}/models/switch", json=switch_request)
    print(f"Status: {response.status_code}")
    
    if response.ok:
        data = response.json()
        print(f"✅ {data['message']}")
    else:
        print(f"Error: {response.text}")

def main():
    print("\n🧪 Model Versioning API Tests")
    print("="*60)
    
    try:
        # Test 1: List versions
        test_list_versions()
        
        # Test 2: Get current model
        test_get_current_model()
        
        # Test 3: Make prediction
        sample_data = test_prediction()
        
        # Test 4: Retrain model (creates V1)
        print("\n⚠️  IMPORTANT: Retraining will create a new model version.")
        user_input = input("Do you want to test retraining? (yes/no): ").strip().lower()
        if user_input == 'yes':
            test_retrain(sample_data)
            
            # After retraining, list versions again
            test_list_versions()
            
            # Test 5: Switch versions
            test_switch_version()
            
            # List versions one more time
            test_list_versions()
        else:
            print("\nSkipping retraining test.")
        
        print_section("✅ All Tests Completed!")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Cannot connect to API server!")
        print("Make sure the server is running on http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    main()
