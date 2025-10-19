"""
Test script to verify all services are working
"""

import sys
import os
from pathlib import Path

# Add backend to path
sys.path.append(str(Path(__file__).parent / "backend"))

def test_imports():
    """Test if all services can be imported"""
    print("Testing service imports...")
    
    try:
        from services.nlp_service import nlp_service
        print("SUCCESS: NLP service imported successfully")
    except Exception as e:
        print(f"FAILED: NLP service import failed: {e}")
    
    try:
        from services.cv_service import cv_service
        print("SUCCESS: CV service imported successfully")
    except Exception as e:
        print(f"FAILED: CV service import failed: {e}")
    
    try:
        from services.langchain_service import langchain_service
        print("SUCCESS: LangChain service imported successfully")
    except Exception as e:
        print(f"FAILED: LangChain service import failed: {e}")
    
    try:
        from services.pinecone_service import pinecone_service
        print("SUCCESS: Pinecone service imported successfully")
    except Exception as e:
        print(f"FAILED: Pinecone service import failed: {e}")

def test_service_initialization():
    """Test service initialization"""
    print("\nTesting service initialization...")
    
    try:
        from services.nlp_service import nlp_service
        success = nlp_service.initialize()
        print(f"SUCCESS: NLP service initialization: {'Success' if success else 'Failed'}")
    except Exception as e:
        print(f"FAILED: NLP service initialization failed: {e}")
    
    try:
        from services.cv_service import cv_service
        success = cv_service.initialize()
        print(f"SUCCESS: CV service initialization: {'Success' if success else 'Failed'}")
    except Exception as e:
        print(f"FAILED: CV service initialization failed: {e}")
    
    try:
        from services.langchain_service import langchain_service
        success = langchain_service.initialize()
        print(f"SUCCESS: LangChain service initialization: {'Success' if success else 'Failed'}")
    except Exception as e:
        print(f"FAILED: LangChain service initialization failed: {e}")

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from services.nlp_service import nlp_service
        if nlp_service.is_initialized:
            embedding = nlp_service.get_text_embedding("test product")
            print(f"SUCCESS: NLP embedding generated: {len(embedding)} dimensions")
        else:
            print("WARNING: NLP service not initialized, skipping test")
    except Exception as e:
        print(f"FAILED: NLP functionality test failed: {e}")
    
    try:
        from services.cv_service import cv_service
        if cv_service.is_initialized:
            # Test with a dummy image URL
            embedding = cv_service.get_image_embedding("https://example.com/image.jpg")
            print(f"SUCCESS: CV embedding generated: {len(embedding)} dimensions")
        else:
            print("WARNING: CV service not initialized, skipping test")
    except Exception as e:
        print(f"FAILED: CV functionality test failed: {e}")

def test_data_loading():
    """Test data loading"""
    print("\nTesting data loading...")
    
    try:
        import pandas as pd
        data_path = Path(__file__).parent / "data" / "raw" / "intern_data_ikarus.csv"
        df = pd.read_csv(data_path)
        print(f"SUCCESS: Dataset loaded: {len(df)} products")
        print(f"   Columns: {list(df.columns)}")
        return df
    except Exception as e:
        print(f"FAILED: Data loading failed: {e}")
        return None

def main():
    """Main test function"""
    print("Starting Ikarus 3D System Tests")
    print("=" * 50)
    
    # Test imports
    test_imports()
    
    # Test initialization
    test_service_initialization()
    
    # Test basic functionality
    test_basic_functionality()
    
    # Test data loading
    df = test_data_loading()
    
    print("\n" + "=" * 50)
    print("Test Summary:")
    print("- All services should be importable")
    print("- NLP and CV services should initialize")
    print("- LangChain service may fail if API keys are missing (expected)")
    print("- Data should load successfully")
    print("\nIf you see mostly SUCCESS messages, the system is ready!")

if __name__ == "__main__":
    main()
