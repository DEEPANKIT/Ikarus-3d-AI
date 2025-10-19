#!/usr/bin/env python3
"""
Pinecone Population Script - Real Vector Database Integration
Populates Pinecone with all 312 products for real-time vector search
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import pinecone
from sentence_transformers import SentenceTransformer
import time
import json

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PineconePopulator:
    """Handles population of Pinecone index with product data and embeddings."""
    
    def __init__(self):
        self.pc = None
        self.index = None
        self.index_name = os.getenv('PINECONE_INDEX_NAME', 'ikarus-products')
        self.dimension = 384  # For all-MiniLM-L6-v2
        self.embedding_model = None
        self.is_initialized = False
        
    def initialize_pinecone(self):
        """Initialize Pinecone client and ensure index exists."""
        try:
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
            
            if not api_key:
                logger.error("PINECONE_API_KEY not found in .env")
                return False
            
            # Initialize Pinecone
            pinecone.init(api_key=api_key, environment=environment)
            
            # Check if index exists, create if not
            existing_indexes = pinecone.list_indexes()
            index_exists = any(idx.name == self.index_name for idx in existing_indexes)
            
            if not index_exists:
                logger.info(f"Creating new Pinecone index '{self.index_name}'...")
                pinecone.create_index(
                    name=self.index_name,
                    dimension=self.dimension,
                    metric="cosine"
                )
                logger.info("Waiting for index to be ready...")
                time.sleep(10)  # Give Pinecone time to initialize
            
            # Connect to index
            self.index = pinecone.Index(self.index_name)
            self.is_initialized = True
            logger.info(f"Pinecone index '{self.index_name}' ready.")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            return False
    
    def load_embedding_model(self):
        """Load the sentence transformer model."""
        try:
            logger.info("Loading SentenceTransformer model...")
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            logger.info("SentenceTransformer model loaded successfully.")
            return True
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            return False
    
    def load_products_data(self, csv_path: str = "data/raw/intern_data_ikarus.csv"):
        """Load product data from CSV."""
        try:
            logger.info(f"Loading products data from {csv_path}")
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} products.")
            return df
        except Exception as e:
            logger.error(f"Error loading products data: {e}")
            return None
    
    def prepare_product_text(self, row):
        """Prepare text for embedding from product row."""
        text_parts = []
        
        if pd.notna(row.get('title')):
            text_parts.append(str(row['title']))
        if pd.notna(row.get('description')):
            text_parts.append(str(row['description']))
        if pd.notna(row.get('brand')):
            text_parts.append(f"Brand: {row['brand']}")
        if pd.notna(row.get('material')):
            text_parts.append(f"Material: {row['material']}")
        if pd.notna(row.get('categories')):
            text_parts.append(f"Categories: {row['categories']}")
        
        return " ".join(text_parts)
    
    def populate_pinecone(self, df: pd.DataFrame, batch_size: int = 50):
        """Generate embeddings and populate Pinecone with all products."""
        if not self.is_initialized:
            logger.error("Pinecone not initialized.")
            return False
        
        logger.info("Generating embeddings and uploading to Pinecone...")
        vectors_to_upsert = []
        
        for idx, row in df.iterrows():
            try:
                product_id = str(row.get('uniq_id', f'product_{idx}'))
                
                # Prepare text for embedding
                combined_text = self.prepare_product_text(row)
                
                # Generate embedding
                embedding = self.embedding_model.encode([combined_text])[0]
                
                # Prepare metadata
                metadata = {
                    'title': str(row.get('title', '')),
                    'brand': str(row.get('brand', '')),
                    'price': str(row.get('price', '')),
                    'categories': str(row.get('categories', '')),
                    'material': str(row.get('material', '')),
                    'description': str(row.get('description', ''))[:1000],  # Limit description length
                    'image': str(row.get('images', ''))[:500]  # Limit image URL length
                }
                
                vectors_to_upsert.append({
                    'id': product_id,
                    'values': embedding.tolist(),
                    'metadata': metadata
                })
                
                # Upload in batches
                if len(vectors_to_upsert) >= batch_size:
                    self.index.upsert(vectors=vectors_to_upsert)
                    logger.info(f"Uploaded batch {len(vectors_to_upsert)} vectors")
                    vectors_to_upsert = []
                    
            except Exception as e:
                logger.warning(f"Error processing product {idx}: {e}")
                continue
        
        # Upload remaining vectors
        if vectors_to_upsert:
            self.index.upsert(vectors=vectors_to_upsert)
            logger.info(f"Uploaded final batch of {len(vectors_to_upsert)} vectors")
        
        logger.info(f"Successfully populated Pinecone with {len(df)} products.")
        return True
    
    def test_search(self, query: str = "modern leather sofa", top_k: int = 5):
        """Test search functionality."""
        try:
            if not self.index:
                self.index = pinecone.Index(self.index_name)
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Search
            results = self.index.query(
                vector=query_embedding.tolist(),
                top_k=top_k,
                include_metadata=True
            )
            
            logger.info(f"Search results for '{query}':")
            for match in results['matches']:
                logger.info(f"  - {match['metadata']['title']} (Score: {match['score']:.3f})")
            
            return results
            
        except Exception as e:
            logger.error(f"Error testing search: {e}")
            return None
    
    def get_index_stats(self):
        """Get index statistics."""
        try:
            stats = self.index.describe_index_stats()
            return {
                'total_vector_count': stats.total_vector_count,
                'dimension': stats.dimension,
                'index_fullness': stats.index_fullness
            }
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}

def main():
    """Main function to populate Pinecone."""
    logger.info("Starting Pinecone population...")
    
    populator = PineconePopulator()
    
    # Initialize Pinecone
    if not populator.initialize_pinecone():
        logger.error("Failed to initialize Pinecone")
        return
    
    # Load embedding model
    if not populator.load_embedding_model():
        logger.error("Failed to load embedding model")
        return
    
    # Load products data
    df = populator.load_products_data()
    if df is None:
        logger.error("Failed to load products data")
        return
    
    # Populate Pinecone
    if not populator.populate_pinecone(df):
        logger.error("Failed to populate Pinecone")
        return
    
    # Test search
    logger.info("Testing search functionality...")
    populator.test_search()
    
    # Get index stats
    stats = populator.get_index_stats()
    logger.info(f"Index stats: {stats}")
    
    logger.info("Pinecone population completed successfully!")

if __name__ == "__main__":
    main()
