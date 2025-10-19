#!/usr/bin/env python3
"""
Test Recommendation Service Directly
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

load_dotenv()

def test_recommendation_service():
    """Test the recommendation service directly"""
    print("Testing Recommendation Service Directly...")
    
    try:
        from services.recommendation_service import recommendation_service
        
        print(f"Service initialized: {recommendation_service.is_initialized}")
        
        if recommendation_service.is_initialized:
            print("Testing recommendation query...")
            results = recommendation_service.get_similar_products("modern sofa", top_k=5)
            print(f"Results: {len(results)} products found")
            
            for i, product in enumerate(results[:3], 1):
                print(f"  {i}. {product.get('title', 'No title')} - Score: {product.get('similarity_score', 0):.3f}")
        else:
            print("ERROR: Recommendation service not initialized")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_recommendation_service()
