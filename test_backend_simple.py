#!/usr/bin/env python3
"""
Simple backend test to check if all imports work
"""

import sys
import os
sys.path.append('backend')

try:
    print("Testing imports...")
    
    # Test basic imports
    from backend.services.nlp_service import nlp_service
    print("✓ NLP service imported")
    
    from backend.services.cv_service import cv_service
    print("✓ CV service imported")
    
    from backend.services.langchain_service import langchain_service
    print("✓ LangChain service imported")
    
    from backend.services.pinecone_service import pinecone_service
    print("✓ Pinecone service imported")
    
    from backend.services.recommendation_service import recommendation_service
    print("✓ Recommendation service imported")
    
    print("\n✅ All services imported successfully!")
    
except Exception as e:
    print(f"❌ Import error: {e}")
    import traceback
    traceback.print_exc()
