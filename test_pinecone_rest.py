#!/usr/bin/env python3
"""
Test Pinecone REST API - Direct connection to existing index
"""

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

def test_pinecone_rest_api():
    """Test Pinecone using REST API directly"""
    print("Testing Pinecone REST API...")
    
    api_key = os.getenv('PINECONE_API_KEY')
    environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'ikarus-products')
    
    if not api_key:
        print("ERROR: PINECONE_API_KEY not found")
        return
    
    print(f"API Key: {api_key[:10]}...")
    print(f"Environment: {environment}")
    print(f"Index Name: {index_name}")
    
    # Pinecone REST API endpoints
    base_url = f"https://controller.{environment}.pinecone.io"
    headers = {
        "Api-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        # Test 1: List indexes
        print("\n1. Testing list indexes...")
        response = requests.get(f"{base_url}/databases", headers=headers)
        if response.status_code == 200:
            indexes = response.json()
            print(f"SUCCESS: Found {len(indexes)} indexes")
            for idx in indexes:
                print(f"  - {idx.get('name', 'Unknown')}")
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
        
        # Test 2: Get index stats
        print(f"\n2. Testing index stats for '{index_name}'...")
        response = requests.get(f"{base_url}/databases/{index_name}/stats", headers=headers)
        if response.status_code == 200:
            stats = response.json()
            print(f"SUCCESS: Index stats retrieved")
            print(f"  Total vectors: {stats.get('totalVectorCount', 'N/A')}")
            print(f"  Dimension: {stats.get('dimension', 'N/A')}")
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
        
        # Test 3: Query the index
        print(f"\n3. Testing query on '{index_name}'...")
        query_url = f"https://{index_name}-{environment}.svc.pinecone.io/query"
        
        # Create a simple test query vector (384 dimensions for all-MiniLM-L6-v2)
        test_vector = [0.1] * 384  # Simple test vector
        
        query_payload = {
            "vector": test_vector,
            "topK": 3,
            "includeMetadata": True
        }
        
        response = requests.post(query_url, headers=headers, json=query_payload)
        if response.status_code == 200:
            results = response.json()
            matches = results.get('matches', [])
            print(f"SUCCESS: Query returned {len(matches)} results")
            for i, match in enumerate(matches[:2], 1):
                print(f"  {i}. Score: {match.get('score', 0):.3f}")
                metadata = match.get('metadata', {})
                print(f"     Title: {metadata.get('title', 'N/A')[:50]}...")
        else:
            print(f"ERROR: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"ERROR: {e}")

if __name__ == "__main__":
    test_pinecone_rest_api()
