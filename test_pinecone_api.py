#!/usr/bin/env python3
"""
Test Pinecone API - Find the correct interface
"""

import os
from dotenv import load_dotenv

load_dotenv()

def test_pinecone_apis():
    """Test different Pinecone API approaches"""
    print("Testing Pinecone API approaches...")
    
    api_key = os.getenv('PINECONE_API_KEY')
    if not api_key:
        print("ERROR: PINECONE_API_KEY not found")
        return
    
    print(f"API Key found: {api_key[:10]}...")
    
    # Test 1: Try direct import
    try:
        import pinecone
        print("SUCCESS: pinecone imported")
        
        # Try to find working methods
        for attr in dir(pinecone):
            if not attr.startswith('_'):
                print(f"  Found: {attr}")
                
    except Exception as e:
        print(f"ERROR: {e}")
    
    # Test 2: Try different import patterns
    try:
        from pinecone import Pinecone
        print("SUCCESS: Pinecone class imported")
    except Exception as e:
        print(f"ERROR importing Pinecone class: {e}")
    
    # Test 3: Try legacy interface
    try:
        from pinecone import legacy_pinecone_interface
        print("SUCCESS: legacy_pinecone_interface imported")
    except Exception as e:
        print(f"ERROR importing legacy interface: {e}")
    
    # Test 4: Try core module
    try:
        from pinecone import core
        print("SUCCESS: core module imported")
        print(f"Core methods: {[x for x in dir(core) if not x.startswith('_')]}")
    except Exception as e:
        print(f"ERROR importing core: {e}")

if __name__ == "__main__":
    test_pinecone_apis()
