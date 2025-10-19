#!/usr/bin/env python3
"""
Test Azure OpenAI Configuration
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Testing Azure OpenAI Configuration...")
print("-" * 50)

print(f"OPENAI_API_BASE: {os.getenv('OPENAI_API_BASE')}")
print(f"OPENAI_API_KEY: {'Set' if os.getenv('OPENAI_API_KEY') else 'Not set'}")
print(f"OPENAI_DEPLOYMENT_NAME: {os.getenv('OPENAI_DEPLOYMENT_NAME')}")
print(f"OPENAI_API_VERSION: {os.getenv('OPENAI_API_VERSION')}")

# Try different import approaches
print("\nTrying different import approaches...")

try:
    from langchain_openai import AzureOpenAI
    print("SUCCESS: langchain_openai.AzureOpenAI imported successfully")
    
    # Try to create instance
    llm = AzureOpenAI(
        azure_endpoint=os.getenv('OPENAI_API_BASE'),
        api_key=os.getenv('OPENAI_API_KEY'),
        api_version=os.getenv('OPENAI_API_VERSION', '2024-02-15-preview'),
        azure_deployment=os.getenv('OPENAI_DEPLOYMENT_NAME', 'gpt-4'),
        temperature=0.7,
        max_tokens=200
    )
    print("SUCCESS: AzureOpenAI instance created successfully")
    
except Exception as e:
    print(f"ERROR: Error with langchain_openai.AzureOpenAI: {e}")

try:
    from openai import AzureOpenAI as OpenAIAzureOpenAI
    print("SUCCESS: openai.AzureOpenAI imported successfully")
    
    # Try to create instance
    client = OpenAIAzureOpenAI(
        azure_endpoint=os.getenv('OPENAI_API_BASE'),
        api_key=os.getenv('OPENAI_API_KEY'),
        api_version=os.getenv('OPENAI_API_VERSION', '2024-02-15-preview'),
        azure_deployment=os.getenv('OPENAI_DEPLOYMENT_NAME', 'gpt-4')
    )
    print("SUCCESS: OpenAI AzureOpenAI instance created successfully")
    
except Exception as e:
    print(f"ERROR: Error with openai.AzureOpenAI: {e}")

print("\nPackage versions:")
try:
    import langchain_openai
    print(f"langchain-openai: {langchain_openai.__version__}")
except:
    print("langchain-openai version not available")

try:
    import openai
    print(f"openai: {openai.__version__}")
except:
    print("openai version not available")
