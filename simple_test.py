#!/usr/bin/env python3
"""
Simple System Test for Ikarus 3D Product Recommendation System
Tests all major components and endpoints
"""

import requests
import json
import time
import sys
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"

def test_backend_health():
    """Test backend health endpoint"""
    print("Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("SUCCESS: Backend is healthy")
            return True
        else:
            print(f"FAILED: Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Backend health check error: {e}")
        return False

def test_products_endpoint():
    """Test products endpoint"""
    print("\nTesting Products Endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/products/sample", timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"SUCCESS: Products endpoint working - {len(products)} products returned")
            return True
        else:
            print(f"FAILED: Products endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Products endpoint error: {e}")
        return False

def test_analytics_endpoint():
    """Test analytics endpoint"""
    print("\nTesting Analytics Endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/analytics/overview", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                analytics_data = data.get('data', {})
                print(f"SUCCESS: Analytics endpoint working")
                print(f"  - Total products: {analytics_data.get('total_products', 'N/A')}")
                print(f"  - Average price: ${analytics_data.get('average_price', 'N/A'):.2f}")
                return True
            else:
                print(f"FAILED: Analytics endpoint returned error status")
                return False
        else:
            print(f"FAILED: Analytics endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"ERROR: Analytics endpoint error: {e}")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\nTesting Data Files...")
    
    required_files = [
        "data/raw/intern_data_ikarus.csv",
        "notebooks/data_analysis.ipynb",
        "notebooks/model_training.ipynb"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"SUCCESS: {file_path} exists")
        else:
            print(f"FAILED: {file_path} missing")
            all_exist = False
    
    return all_exist

def main():
    """Run all tests"""
    print("Starting Complete System Test for Ikarus 3D")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Products Endpoint", test_products_endpoint),
        ("Analytics Endpoint", test_analytics_endpoint),
        ("Data Files", test_data_files)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"ERROR: {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{status}: {test_name}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("All tests passed! System is ready for use.")
    elif passed >= total * 0.8:
        print("Most tests passed. System is mostly functional.")
    else:
        print("Multiple tests failed. System needs attention.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
