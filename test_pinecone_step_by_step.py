#!/usr/bin/env python3
"""
Test Pinecone Connection Step by Step
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_pinecone_step_by_step():
    """Test Pinecone connection step by step"""
    print("Testing Pinecone Connection Step by Step...")
    
    api_key = os.getenv('PINECONE_API_KEY')
    environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'ikarus-products')
    
    print(f"API Key: {'SET' if api_key else 'NOT SET'}")
    print(f"Environment: {environment}")
    print(f"Index Name: {index_name}")
    
    if not api_key:
        print("ERROR: PINECONE_API_KEY not found")
        return False
    
    try:
        import requests
        
        # Step 1: Test controller API
        print("\n1. Testing Controller API...")
        controller_url = f"https://controller.{environment}.pinecone.io"
        headers = {
            "Api-Key": api_key,
            "Content-Type": "application/json"
        }
        
        response = requests.get(
            f"{controller_url}/databases/{index_name}",
            headers=headers,
            timeout=10
        )
        
        print(f"Controller response: {response.status_code}")
        if response.status_code == 200:
            index_info = response.json()
            print(f"Index info: {index_info}")
            host = index_info.get('host', f"https://{index_name}-{environment}.svc.pinecone.io")
            print(f"Index host: {host}")
        else:
            print(f"Controller error: {response.text}")
            return False
        
        # Step 2: Test index host
        print(f"\n2. Testing Index Host: {host}")
        test_response = requests.post(
            f"{host}/describe_index_stats",
            headers=headers,
            json={},
            timeout=10
        )
        
        print(f"Index stats response: {test_response.status_code}")
        if test_response.status_code == 200:
            stats = test_response.json()
            print(f"Index stats: {stats}")
            return True
        else:
            print(f"Index stats error: {test_response.text}")
            return False
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_pinecone_step_by_step()
    if success:
        print("\n✅ Pinecone connection successful!")
    else:
        print("\n❌ Pinecone connection failed!")
