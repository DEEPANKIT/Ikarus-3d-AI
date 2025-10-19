#!/usr/bin/env python3
"""
Comprehensive System Test
"""

import requests
import json
import time

def test_complete_system():
    """Test the complete system end-to-end"""
    print("COMPREHENSIVE SYSTEM TEST")
    print("=" * 60)
    
    # Test 1: Backend Health
    print("\n1. Testing Backend Health...")
    try:
        response = requests.get("http://localhost:8000/health", timeout=10)
        if response.status_code == 200:
            print("SUCCESS: Backend is healthy")
        else:
            print(f"❌ Backend health check failed: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ Backend not accessible: {e}")
        return
    
    # Test 2: Products Endpoint
    print("\n2. Testing Products Endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/products/sample", timeout=10)
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            print(f"✅ Products endpoint working - {len(products)} products")
        else:
            print(f"❌ Products endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Products endpoint error: {e}")
    
    # Test 3: Analytics Endpoint
    print("\n3. Testing Analytics Endpoint...")
    try:
        response = requests.get("http://localhost:8000/api/v1/analytics/overview", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                analytics_data = data.get('data', {})
                print(f"✅ Analytics working - {analytics_data.get('total_products', 'N/A')} products")
            else:
                print("❌ Analytics returned error status")
        else:
            print(f"❌ Analytics failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Analytics error: {e}")
    
    # Test 4: AI Description Generation
    print("\n4. Testing AI Description Generation...")
    try:
        test_product = {
            "title": "Modern Leather Sofa",
            "brand": "TestBrand",
            "material": "Leather",
            "categories": "Furniture, Sofas",
            "price": "$299.99",
            "description": "A comfortable leather sofa"
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/products/test-product/generate-description",
            json=test_product,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            description = data.get('ai_description', '')
            if len(description) > 20:
                print("✅ AI description generation working")
                print(f"   Generated: {description[:100]}...")
            else:
                print("⚠️ AI description generation returned short description")
        else:
            print(f"❌ AI description failed: {response.status_code}")
    except Exception as e:
        print(f"❌ AI description error: {e}")
    
    # Test 5: Vector Recommendations
    print("\n5. Testing Vector Recommendations...")
    try:
        payload = {
            "query": "modern leather sofa",
            "limit": 3
        }
        
        response = requests.post(
            "http://localhost:8000/api/v1/recommendations/",
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            recommendations = data.get('recommendations', [])
            print(f"✅ Recommendations endpoint working - {len(recommendations)} results")
            
            if len(recommendations) > 0:
                print("🎉 VECTOR SEARCH IS WORKING!")
                for i, rec in enumerate(recommendations[:2], 1):
                    print(f"   {i}. {rec.get('title', 'N/A')[:50]}...")
                    print(f"      Similarity: {rec.get('similarity_score', 0):.3f}")
            else:
                print("⚠️ No recommendations returned - check service initialization")
        else:
            print(f"❌ Recommendations failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Recommendations error: {e}")
    
    print("\n" + "=" * 60)
    print("SYSTEM TEST COMPLETE")
    print("=" * 60)

if __name__ == "__main__":
    test_complete_system()
