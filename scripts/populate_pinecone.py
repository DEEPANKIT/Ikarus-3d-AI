"""
Pinecone Population Script for Ikarus 3D
Populates Pinecone vector database with product embeddings
"""

import os
import sys
import logging
import pandas as pd
import numpy as np
from pathlib import Path
from dotenv import load_dotenv
import pinecone
import time

# Add backend to path
sys.path.append(str(Path(__file__).parent.parent / "backend"))

from services.nlp_service import nlp_service
from services.cv_service import cv_service
from services.langchain_service import langchain_service

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_services():
    """Initialize all ML services"""
    logger.info("Initializing ML services...")
    
    # Initialize services
    nlp_success = nlp_service.initialize()
    cv_success = cv_service.initialize()
    langchain_success = langchain_service.initialize()
    
    logger.info(f"NLP Service: {'✅' if nlp_success else '❌'}")
    logger.info(f"CV Service: {'✅' if cv_success else '❌'}")
    logger.info(f"LangChain Service: {'✅' if langchain_success else '❌'}")
    
    return nlp_success and cv_success and langchain_success

def load_products_data():
    """Load products from CSV"""
    try:
        data_path = Path(__file__).parent.parent / "data" / "raw" / "intern_data_ikarus.csv"
        df = pd.read_csv(data_path)
        logger.info(f"Loaded {len(df)} products from dataset")
        return df
    except Exception as e:
        logger.error(f"Error loading products data: {e}")
        return None

def create_combined_embedding(product_data, nlp_embedding, cv_embedding):
    """Create combined embedding from text and image features"""
    try:
        # Normalize embeddings
        nlp_norm = nlp_embedding / np.linalg.norm(nlp_embedding)
        cv_norm = cv_embedding / np.linalg.norm(cv_embedding)
        
        # Combine embeddings (weighted average)
        combined = 0.7 * nlp_norm + 0.3 * cv_norm
        
        # Ensure it's the right dimension for Pinecone (384 for sentence-transformers)
        if len(combined) > 384:
            combined = combined[:384]
        elif len(combined) < 384:
            # Pad with zeros if needed
            combined = np.pad(combined, (0, 384 - len(combined)), 'constant')
        
        return combined.tolist()
        
    except Exception as e:
        logger.error(f"Error creating combined embedding: {e}")
        return np.random.rand(384).tolist()

def populate_pinecone():
    """Main function to populate Pinecone"""
    try:
        # Initialize services
        if not initialize_services():
            logger.error("Failed to initialize services")
            return False
        
        # Load products data
        df = load_products_data()
        if df is None:
            return False
        
        # Initialize Pinecone
        api_key = os.getenv('PINECONE_API_KEY')
        if not api_key:
            logger.error("PINECONE_API_KEY not found")
            return False
        
        pinecone.init(api_key=api_key, environment=os.getenv('PINECONE_ENVIRONMENT', 'us-east-1'))
        index_name = os.getenv('PINECONE_INDEX_NAME', 'ikarus-products')
        
        # Connect to index
        try:
            index = pinecone.Index(index_name)
            logger.info(f"Connected to Pinecone index: {index_name}")
        except Exception as e:
            logger.error(f"Error connecting to Pinecone index: {e}")
            return False
        
        # Process products in batches
        batch_size = 50
        total_products = len(df)
        
        logger.info(f"Starting to process {total_products} products...")
        
        for i in range(0, total_products, batch_size):
            batch_df = df.iloc[i:i+batch_size]
            vectors_to_upsert = []
            
            logger.info(f"Processing batch {i//batch_size + 1}/{(total_products-1)//batch_size + 1}")
            
            for idx, row in batch_df.iterrows():
                try:
                    # Prepare product data
                    product_data = {
                        'id': str(row.get('uniq_id', f'product_{idx}')),
                        'title': str(row.get('title', '')),
                        'brand': str(row.get('brand', '')),
                        'material': str(row.get('material', '')),
                        'categories': str(row.get('categories', '')),
                        'price': str(row.get('price', '')),
                        'description': str(row.get('description', '')),
                        'image': str(row.get('images', ''))
                    }
                    
                    # Generate embeddings
                    nlp_embedding = nlp_service.get_product_embedding(product_data)
                    
                    # Get image embedding (use first image URL if available)
                    cv_embedding = np.random.rand(2048)  # Default for now
                    if product_data['image'] and product_data['image'] != 'nan':
                        try:
                            # Parse image URLs (they're stored as string representation of list)
                            import ast
                            image_urls = ast.literal_eval(product_data['image'])
                            if image_urls and len(image_urls) > 0:
                                cv_embedding = cv_service.get_image_embedding(image_urls[0])
                        except:
                            pass
                    
                    # Create combined embedding
                    combined_embedding = create_combined_embedding(
                        product_data, nlp_embedding, cv_embedding
                    )
                    
                    # Prepare metadata
                    metadata = {
                        'title': product_data['title'][:1000],  # Limit length
                        'brand': product_data['brand'][:100],
                        'material': product_data['material'][:100],
                        'categories': product_data['categories'][:500],
                        'price': product_data['price'][:50],
                        'description': product_data['description'][:1000],
                        'image': product_data['image'][:500]
                    }
                    
                    # Add to batch
                    vectors_to_upsert.append({
                        'id': product_data['id'],
                        'values': combined_embedding,
                        'metadata': metadata
                    })
                    
                except Exception as e:
                    logger.error(f"Error processing product {idx}: {e}")
                    continue
            
            # Upsert batch to Pinecone
            if vectors_to_upsert:
                try:
                    index.upsert(vectors=vectors_to_upsert)
                    logger.info(f"Successfully upserted {len(vectors_to_upsert)} vectors")
                except Exception as e:
                    logger.error(f"Error upserting batch: {e}")
            
            # Small delay to avoid rate limiting
            time.sleep(0.1)
        
        # Get final index stats
        stats = index.describe_index_stats()
        logger.info(f"Final index stats: {stats}")
        
        logger.info("✅ Pinecone population completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Error in populate_pinecone: {e}")
        return False

if __name__ == "__main__":
    success = populate_pinecone()
    if success:
        print("🎉 Pinecone population completed successfully!")
    else:
        print("❌ Pinecone population failed!")
        sys.exit(1)

