#!/usr/bin/env python3
"""
Test LangChain Service Status
"""

import sys
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sys.path.append('backend')

from services.langchain_service import langchain_service

def test_langchain_service():
    """Test LangChain service status"""
    print("Testing LangChain Service Status...")
    print("-" * 50)
    
    # Check if service is initialized
    print(f"Service Initialized: {langchain_service.is_initialized}")
    print(f"LLM Available: {langchain_service.llm is not None}")
    print(f"Embeddings Available: {langchain_service.embeddings is not None}")
    print(f"Description Chain Available: {langchain_service.description_chain is not None}")
    
    # Check environment variables
    print("\nEnvironment Variables:")
    print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE', 'Not set')}")
    print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
    print(f"OPENAI_DEPLOYMENT_NAME: {os.getenv('OPENAI_DEPLOYMENT_NAME', 'Not set')}")
    
    # Try to initialize manually
    print("\nAttempting manual initialization...")
    try:
        result = langchain_service.initialize()
        print(f"Initialization Result: {result}")
        print(f"Service Initialized After Manual Init: {langchain_service.is_initialized}")
    except Exception as e:
        print(f"Initialization Error: {e}")
    
    # Test description generation
    print("\nTesting Description Generation...")
    test_product = {
        "title": "Test Product",
        "brand": "Test Brand",
        "material": "Test Material",
        "categories": "Test Category",
        "price": "$100",
        "description": "Test description"
    }
    
    try:
        description = langchain_service.generate_product_description(test_product)
        print(f"Generated Description: {description}")
    except Exception as e:
        print(f"Description Generation Error: {e}")

if __name__ == "__main__":
    test_langchain_service()
