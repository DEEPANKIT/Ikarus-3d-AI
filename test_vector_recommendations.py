#!/usr/bin/env python3
"""
Test Vector-Based Recommendation System
"""

import requests
import json

def test_vector_recommendations():
    """Test the vector-based recommendation system"""
    print("Testing Vector-Based Recommendation System...")
    print("-" * 60)
    
    # Test queries
    test_queries = [
        "modern leather sofa",
        "wooden dining table",
        "black furniture",
        "comfortable chair",
        "storage solution"
    ]
    
    for query in test_queries:
        print(f"\nTesting query: '{query}'")
        print("-" * 40)
        
        try:
            # Test recommendation endpoint
            url = f"http://localhost:8000/api/v1/recommendations/recommend"
            params = {"query": query, "top_k": 3}
            
            response = requests.get(url, params=params, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                recommendations = data.get('recommendations', [])
                
                print(f"SUCCESS: Found {len(recommendations)} recommendations")
                for i, rec in enumerate(recommendations, 1):
                    print(f"  {i}. {rec.get('title', 'N/A')[:50]}...")
                    print(f"     Brand: {rec.get('brand', 'N/A')}")
                    print(f"     Price: {rec.get('price', 'N/A')}")
                    print(f"     Similarity: {rec.get('similarity_score', 0):.3f}")
                    print()
            else:
                print(f"ERROR: Request failed with status {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"ERROR: Exception occurred - {e}")

if __name__ == "__main__":
    test_vector_recommendations()
