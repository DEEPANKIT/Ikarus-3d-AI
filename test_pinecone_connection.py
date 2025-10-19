#!/usr/bin/env python3
"""
Test Pinecone Connection with Environment Variables
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pinecone_connection():
    """Test Pinecone connection with proper configuration"""
    print("Testing Pinecone connection...")
    
    # Check environment variables
    api_key = os.getenv('PINECONE_API_KEY')
    environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
    index_name = os.getenv('PINECONE_INDEX_NAME', 'ikarus-products')
    
    print(f"API Key: {'SET' if api_key else 'NOT SET'}")
    print(f"Environment: {environment}")
    print(f"Index Name: {index_name}")
    
    if not api_key:
        print("ERROR: PINECONE_API_KEY not found in environment")
        return False
    
    try:
        import pinecone
        
        # Try to create index connection
        print(f"Attempting to connect to index: {index_name}")
        index = pinecone.Index(index_name)
        
        # Test the connection
        print("Testing index connection...")
        stats = index.describe_index_stats()
        print(f"SUCCESS: Connected to Pinecone index!")
        print(f"Total vectors: {stats.total_vector_count}")
        print(f"Dimension: {stats.dimension}")
        
        # Test a simple query
        print("Testing query...")
        test_vector = [0.1] * 384  # Simple test vector
        results = index.query(
            vector=test_vector,
            top_k=3,
            include_metadata=True
        )
        
        print(f"Query returned {len(results.matches)} results")
        for i, match in enumerate(results.matches[:2], 1):
            print(f"  {i}. Score: {match.score:.3f}")
            if match.metadata:
                print(f"     Title: {match.metadata.get('title', 'N/A')[:50]}...")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    success = test_pinecone_connection()
    if success:
        print("\n✅ Pinecone connection successful!")
    else:
        print("\n❌ Pinecone connection failed!")
