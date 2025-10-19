"""
Simple Pinecone Test Script - No Unicode
Tests your Pinecone API key and creates the index
"""

import os
from pinecone import Pinecone
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pinecone():
    """Test Pinecone connection and create index"""
    
    # Check if API key is set
    api_key = os.getenv('PINECONE_API_KEY')
    if not api_key or api_key == 'your_pinecone_api_key_here':
        print("ERROR: Please set your PINECONE_API_KEY in the .env file")
        print("Get your API key from: https://app.pinecone.io/")
        return False
    
    try:
        # Initialize Pinecone
        print("Testing Pinecone connection...")
        pc = Pinecone(api_key=api_key)
        
        # List existing indexes
        print("Checking existing indexes...")
        indexes = pc.list_indexes()
        print(f"Found {len(indexes)} existing indexes")
        
        # Check if our index exists
        index_name = "ikarus-products"
        existing_indexes = [idx.name for idx in indexes]
        
        if index_name in existing_indexes:
            print(f"SUCCESS: Index '{index_name}' already exists!")
            return True
        
        # Create new index
        print(f"Creating index '{index_name}'...")
        pc.create_index(
            name=index_name,
            dimension=384,  # For sentence-transformers/all-MiniLM-L6-v2
            metric="cosine",
            spec={
                "serverless": {
                    "cloud": "aws",
                    "region": "us-east-1"
                }
            }
        )
        
        print(f"SUCCESS: Index '{index_name}' created successfully!")
        print("\nYour Pinecone setup is complete!")
        print("You can now run the full setup script.")
        
        return True
        
    except Exception as e:
        print(f"ERROR: {e}")
        return False

if __name__ == "__main__":
    print("Pinecone Setup Test")
    print("=" * 30)
    
    if test_pinecone():
        print("\nSUCCESS! Your Pinecone is ready.")
    else:
        print("\nFAILED! Please check your API key.")
