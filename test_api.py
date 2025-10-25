"""
Test script for Water Potability Prediction API
Run this after starting the FastAPI server to verify it's working correctly
"""

import requests
import json

# API base URL
BASE_URL = "http://localhost:8000"

def test_health_check():
    """Test the health check endpoint"""
    print("\n" + "="*50)
    print("Testing Health Check Endpoint")
    print("="*50)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Health check failed!"
    print("✓ Health check passed!")


def test_single_prediction():
    """Test single prediction endpoint"""
    print("\n" + "="*50)
    print("Testing Single Prediction Endpoint")
    print("="*50)
    
    # Sample water quality data
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
    
    print(f"Input: {json.dumps(sample_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=sample_data
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 200, "Prediction failed!"
    
    result = response.json()
    assert "potability" in result, "Missing 'potability' in response"
    assert "potability_label" in result, "Missing 'potability_label' in response"
    assert "confidence" in result, "Missing 'confidence' in response"
    
    print("✓ Single prediction passed!")


def test_batch_prediction():
    """Test batch prediction endpoint"""
    print("\n" + "="*50)
    print("Testing Batch Prediction Endpoint")
    print("="*50)
    
    # Multiple water samples
    batch_data = [
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
        },
        {
            "ph": 8.0,
            "Hardness": 250.0,
            "Solids": 25000.0,
            "Chloramines": 8.0,
            "Sulfate": 400.0,
            "Conductivity": 450.0,
            "Organic_carbon": 16.0,
            "Trihalomethanes": 80.0,
            "Turbidity": 5.0
        }
    ]
    
    print(f"Number of samples: {len(batch_data)}")
    
    response = requests.post(
        f"{BASE_URL}/predict/batch",
        json=batch_data
    )
    
    print(f"\nStatus Code: {response.status_code}")
    result = response.json()
    print(f"Response: {json.dumps(result, indent=2)}")
    
    assert response.status_code == 200, "Batch prediction failed!"
    assert "predictions" in result, "Missing 'predictions' in response"
    assert len(result["predictions"]) == 3, "Expected 3 predictions"
    
    print("✓ Batch prediction passed!")


def test_invalid_input():
    """Test API with invalid input"""
    print("\n" + "="*50)
    print("Testing Invalid Input Handling")
    print("="*50)
    
    # Invalid data (missing required fields)
    invalid_data = {
        "ph": 7.0,
        "Hardness": 200.0
        # Missing other required fields
    }
    
    print(f"Sending invalid input: {json.dumps(invalid_data, indent=2)}")
    
    response = requests.post(
        f"{BASE_URL}/predict",
        json=invalid_data
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    assert response.status_code == 422, "Expected validation error!"
    print("✓ Invalid input handling passed!")


def run_all_tests():
    """Run all API tests"""
    try:
        print("\n" + "="*50)
        print("🧪 Water Potability API Test Suite")
        print("="*50)
        
        test_health_check()
        test_single_prediction()
        test_batch_prediction()
        test_invalid_input()
        
        print("\n" + "="*50)
        print("✅ All tests passed successfully!")
        print("="*50)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to the API")
        print("Please make sure the FastAPI server is running:")
        print("  python main.py")
        print("\nThen run this test script again.")
        
    except AssertionError as e:
        print(f"\n❌ Test failed: {e}")
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    run_all_tests()
