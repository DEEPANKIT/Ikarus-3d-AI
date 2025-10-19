#!/usr/bin/env python3
"""
Debug Recommendation Service
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append('backend')

from services.recommendation_service import recommendation_service
from services.nlp_service import nlp_service

def debug_recommendation_service():
    """Debug the recommendation service"""
    print("Debugging Recommendation Service...")
    print("-" * 50)
    
    # Check service initialization
    print(f"Service Initialized: {recommendation_service.is_initialized}")
    print(f"Products Data Loaded: {recommendation_service.products_data is not None}")
    if recommendation_service.products_data is not None:
        print(f"Number of Products: {len(recommendation_service.products_data)}")
    
    # Check NLP service
    print(f"NLP Service Initialized: {nlp_service.is_initialized}")
    
    # Test embedding generation
    print("\nTesting embedding generation...")
    test_query = "modern leather sofa"
    query_embedding = nlp_service.get_text_embedding(test_query)
    if query_embedding is not None:
        print(f"Query embedding generated: {len(query_embedding)} dimensions")
    else:
        print("ERROR: Failed to generate query embedding")
        return
    
    # Test product embeddings
    print("\nTesting product embeddings...")
    if hasattr(recommendation_service, 'product_embeddings'):
        print(f"Product embeddings exist: {recommendation_service.product_embeddings is not None}")
        if recommendation_service.product_embeddings is not None:
            print(f"Number of product embeddings: {len(recommendation_service.product_embeddings)}")
    else:
        print("Product embeddings not generated yet")
    
    # Try to generate product embeddings
    print("\nGenerating product embeddings...")
    try:
        success = recommendation_service.generate_embeddings()
        print(f"Embedding generation result: {success}")
        if hasattr(recommendation_service, 'product_embeddings'):
            print(f"Product embeddings after generation: {recommendation_service.product_embeddings is not None}")
            if recommendation_service.product_embeddings is not None:
                print(f"Number of embeddings: {len(recommendation_service.product_embeddings)}")
    except Exception as e:
        print(f"Error generating embeddings: {e}")
    
    # Test similarity calculation
    print("\nTesting similarity calculation...")
    try:
        recommendations = recommendation_service.get_similar_products("modern leather sofa", 3)
        print(f"Recommendations found: {len(recommendations)}")
        for i, rec in enumerate(recommendations):
            print(f"  {i+1}. {rec.get('title', 'N/A')[:50]}... (Score: {rec.get('similarity_score', 0):.3f})")
    except Exception as e:
        print(f"Error getting recommendations: {e}")

if __name__ == "__main__":
    debug_recommendation_service()
