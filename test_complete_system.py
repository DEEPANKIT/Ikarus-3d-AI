#!/usr/bin/env python3
"""
Complete System Test for Ikarus 3D Product Recommendation System
Tests all major components and endpoints
"""

import requests
import json
import time
import sys
from pathlib import Path

# Configuration
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"

def test_backend_health():
    """Test backend health endpoint"""
    print("🔍 Testing Backend Health...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Backend is healthy")
            return True
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend health check error: {e}")
        return False

def test_products_endpoint():
    """Test products endpoint"""
    print("\n🔍 Testing Products Endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/products/sample", timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Products endpoint working - {len(products)} products returned")
            
            # Test first product structure
            if products:
                first_product = products[0]
                required_fields = ['id', 'title', 'brand', 'price', 'material']
                missing_fields = [field for field in required_fields if field not in first_product]
                if not missing_fields:
                    print("✅ Product structure is correct")
                else:
                    print(f"⚠️ Missing fields in product: {missing_fields}")
            return True
        else:
            print(f"❌ Products endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Products endpoint error: {e}")
        return False

def test_analytics_endpoint():
    """Test analytics endpoint"""
    print("\n🔍 Testing Analytics Endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/api/v1/analytics/overview", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                analytics_data = data.get('data', {})
                print(f"✅ Analytics endpoint working")
                print(f"   - Total products: {analytics_data.get('total_products', 'N/A')}")
                print(f"   - Average price: ${analytics_data.get('average_price', 'N/A'):.2f}")
                print(f"   - Price range: ${analytics_data.get('price_range', {}).get('min', 'N/A')} - ${analytics_data.get('price_range', {}).get('max', 'N/A')}")
                return True
            else:
                print(f"❌ Analytics endpoint returned error status")
                return False
        else:
            print(f"❌ Analytics endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Analytics endpoint error: {e}")
        return False

def test_ai_description_endpoint():
    """Test AI description generation endpoint"""
    print("\n🔍 Testing AI Description Endpoint...")
    try:
        # Test with a sample product
        test_product = {
            "title": "Modern Leather Sofa",
            "brand": "TestBrand",
            "material": "Leather",
            "categories": "Furniture, Sofas",
            "price": "$299.99",
            "description": "A comfortable leather sofa"
        }
        
        response = requests.post(
            f"{BACKEND_URL}/api/v1/products/generate-description",
            json=test_product,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            description = data.get('ai_description', '')
            if description and len(description) > 10:
                print("✅ AI description generation working")
                print(f"   Generated: {description[:100]}...")
                return True
            else:
                print("⚠️ AI description generation returned empty or short description")
                return False
        else:
            print(f"❌ AI description endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ AI description endpoint error: {e}")
        return False

def test_frontend_availability():
    """Test if frontend is accessible"""
    print("\n🔍 Testing Frontend Availability...")
    try:
        response = requests.get(FRONTEND_URL, timeout=10)
        if response.status_code == 200:
            print("✅ Frontend is accessible")
            return True
        else:
            print(f"⚠️ Frontend returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"⚠️ Frontend not accessible: {e}")
        print("   This is expected if frontend is not running")
        return False

def test_data_files():
    """Test if required data files exist"""
    print("\n🔍 Testing Data Files...")
    
    required_files = [
        "data/raw/intern_data_ikarus.csv",
        "notebooks/data_analysis.ipynb",
        "notebooks/model_training.ipynb"
    ]
    
    all_exist = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path} exists")
        else:
            print(f"❌ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_services_initialization():
    """Test if services are properly initialized"""
    print("\n🔍 Testing Services Initialization...")
    
    try:
        # Test if we can import the services
        sys.path.append('backend')
        from services.nlp_service import nlp_service
        from services.cv_service import cv_service
        from services.langchain_service import langchain_service
        
        print("✅ Service imports successful")
        
        # Test NLP service
        if nlp_service.is_initialized:
            print("✅ NLP service initialized")
        else:
            print("⚠️ NLP service not initialized")
        
        # Test CV service
        if cv_service.is_initialized:
            print("✅ CV service initialized")
        else:
            print("⚠️ CV service not initialized")
        
        # Test LangChain service
        if langchain_service.is_initialized:
            print("✅ LangChain service initialized")
        else:
            print("⚠️ LangChain service not initialized")
        
        return True
        
    except Exception as e:
        print(f"❌ Service initialization test error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Complete System Test for Ikarus 3D")
    print("=" * 60)
    
    tests = [
        ("Backend Health", test_backend_health),
        ("Products Endpoint", test_products_endpoint),
        ("Analytics Endpoint", test_analytics_endpoint),
        ("AI Description", test_ai_description_endpoint),
        ("Frontend Availability", test_frontend_availability),
        ("Data Files", test_data_files),
        ("Services Initialization", test_services_initialization)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\n🎯 Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
    elif passed >= total * 0.8:
        print("⚠️ Most tests passed. System is mostly functional.")
    else:
        print("❌ Multiple tests failed. System needs attention.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
