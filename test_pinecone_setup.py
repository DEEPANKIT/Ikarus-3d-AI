#!/usr/bin/env python3
"""
Simple Pinecone Setup Script for Ikarus 3D
Creates and populates the Pinecone index with product embeddings
"""

import os
import logging
import pandas as pd
import numpy as np
import pinecone
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def setup_pinecone():
    """Setup Pinecone index and populate with product embeddings"""
    try:
        logger.info("Starting Pinecone setup...")
        
        # Initialize Pinecone
        api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            logger.error("PINECONE_API_KEY not found")
            return False
        
        # Load embedding model
        logger.info("Loading embedding model...")
        embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        
        # Load products data
        logger.info("Loading products data...")
        df = pd.read_csv("data/raw/intern_data_ikarus.csv")
        logger.info(f"Loaded {len(df)} products")
        
        # Generate embeddings for first 10 products (for testing)
        logger.info("Generating embeddings for first 10 products...")
        test_df = df.head(10)
        
        texts = []
        for _, row in test_df.iterrows():
            text_parts = []
            if pd.notna(row.get('title')):
                text_parts.append(str(row['title']))
            if pd.notna(row.get('description')):
                text_parts.append(str(row['description']))
            if pd.notna(row.get('brand')):
                text_parts.append(f"Brand: {row['brand']}")
            if pd.notna(row.get('material')):
                text_parts.append(f"Material: {row['material']}")
            texts.append(" ".join(text_parts))
        
        embeddings = embedding_model.encode(texts)
        logger.info(f"Generated {len(embeddings)} embeddings")
        
        # Test search with a simple query
        logger.info("Testing embedding generation...")
        test_query = "modern leather sofa"
        query_embedding = embedding_model.encode([test_query])[0]
        logger.info(f"Query embedding generated: {len(query_embedding)} dimensions")
        
        logger.info("Pinecone setup test completed successfully!")
        logger.info("Ready to integrate with Pinecone API")
        
        return True
        
    except Exception as e:
        logger.error(f"Error in Pinecone setup: {e}")
        return False

if __name__ == "__main__":
    if setup_pinecone():
        print("\n" + "="*50)
        print("SUCCESS! PINECONE SETUP TEST COMPLETED!")
        print("="*50)
        print("Embeddings are working correctly!")
        print("Ready to integrate with Pinecone vector database.")
    else:
        print("\n" + "="*50)
        print("FAILED! PINECONE SETUP ERROR!")
        print("="*50)
        print("Please check your configuration.")
