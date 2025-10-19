"""
Pinecone Index Setup Script for Ikarus 3D
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

class PineconeSetup:
    """Setup and manage Pinecone index for Ikarus 3D"""
    
    def __init__(self):
        self.pc = None
        self.index = None
        self.embedding_model = None
        
    def initialize_pinecone(self):
        """Initialize Pinecone client"""
        try:
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
            if not api_key:
                raise ValueError("PINECONE_API_KEY not found in environment variables")
            
            pinecone.init(api_key=api_key, environment=environment)
            logger.info("Pinecone client initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing Pinecone: {e}")
            return False
    
    def create_index(self, index_name: str = "ikarus-products", dimension: int = 384):
        """Create Pinecone index"""
        try:
            # Check if index already exists
            existing_indexes = pinecone.list_indexes()
            if any(idx.name == index_name for idx in existing_indexes):
                logger.info(f"Index '{index_name}' already exists")
                return True
            
            # Create new index
            logger.info(f"Creating index '{index_name}' with dimension {dimension}")
            pinecone.create_index(
                name=index_name,
                dimension=dimension,
                metric="cosine"
            )
            
            # Wait for index to be ready
            logger.info("Waiting for index to be ready...")
            time.sleep(10)
            
            logger.info(f"Index '{index_name}' created successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error creating index: {e}")
            return False
    
    def load_embedding_model(self):
        """Load sentence transformer model"""
        try:
            logger.info("Loading embedding model...")
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            logger.info("Embedding model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading embedding model: {e}")
            return False
    
    def load_products_data(self, csv_path: str = "data/raw/intern_data_ikarus.csv"):
        """Load products data"""
        try:
            logger.info(f"Loading products data from {csv_path}")
            df = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(df)} products")
            return df
        except Exception as e:
            logger.error(f"Error loading products data: {e}")
            return None
    
    def prepare_product_text(self, row):
        """Prepare text for embedding from product row"""
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
    
    def generate_embeddings(self, df, batch_size: int = 100):
        """Generate embeddings for all products"""
        try:
            logger.info("Generating embeddings for all products...")
            embeddings = []
            texts = []
            
            for _, row in df.iterrows():
                text = self.prepare_product_text(row)
                texts.append(text)
            
            # Generate embeddings in batches
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.embedding_model.encode(batch_texts)
                embeddings.extend(batch_embeddings)
                logger.info(f"Processed {min(i + batch_size, len(texts))}/{len(texts)} products")
            
            return np.array(embeddings)
            
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return None
    
    def upload_to_pinecone(self, df, embeddings, index_name: str = "ikarus-products"):
        """Upload embeddings to Pinecone index"""
        try:
            # Connect to index
            self.index = pinecone.Index(index_name)
            
            # Prepare vectors for upload
            vectors_to_upsert = []
            
            for idx, (_, row) in enumerate(df.iterrows()):
                vector_id = str(row.get('uniq_id', f'product_{idx}'))
                metadata = {
                    'title': str(row.get('title', '')),
                    'brand': str(row.get('brand', '')),
                    'price': str(row.get('price', '')),
                    'categories': str(row.get('categories', '')),
                    'material': str(row.get('material', '')),
                    'description': str(row.get('description', ''))[:1000]  # Limit description length
                }
                
                vectors_to_upsert.append({
                    'id': vector_id,
                    'values': embeddings[idx].tolist(),
                    'metadata': metadata
                })
            
            # Upload in batches
            batch_size = 100
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                self.index.upsert(vectors=batch)
                logger.info(f"Uploaded batch {i//batch_size + 1}/{(len(vectors_to_upsert) + batch_size - 1)//batch_size}")
            
            logger.info(f"Successfully uploaded {len(vectors_to_upsert)} vectors to Pinecone")
            return True
            
        except Exception as e:
            logger.error(f"Error uploading to Pinecone: {e}")
            return False
    
    def test_search(self, query: str = "modern black leather sofa", top_k: int = 5):
        """Test search functionality"""
        try:
            if not self.index:
                self.index = pinecone.Index("ikarus-products")
            
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
    
    def setup_complete_index(self):
        """Complete setup process"""
        try:
            logger.info("Starting complete Pinecone setup...")
            
            # Initialize Pinecone
            if not self.initialize_pinecone():
                return False
            
            # Create index
            if not self.create_index():
                return False
            
            # Load embedding model
            if not self.load_embedding_model():
                return False
            
            # Load products data
            df = self.load_products_data()
            if df is None:
                return False
            
            # Generate embeddings
            embeddings = self.generate_embeddings(df)
            if embeddings is None:
                return False
            
            # Upload to Pinecone
            if not self.upload_to_pinecone(df, embeddings):
                return False
            
            # Test search
            logger.info("Testing search functionality...")
            self.test_search()
            
            logger.info("Pinecone setup completed successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Error in complete setup: {e}")
            return False

def main():
    """Main execution function"""
    setup = PineconeSetup()
    
    if setup.setup_complete_index():
        print("\n" + "="*50)
        print("SUCCESS! PINECONE SETUP COMPLETED!")
        print("="*50)
        print("Your index is ready for recommendations!")
        print("Index name: ikarus-products")
        print("Dimensions: 384")
        print("Metric: cosine")
        print("\nYou can now use the recommendation API endpoints.")
    else:
        print("\n" + "="*50)
        print("FAILED! PINECONE SETUP ERROR!")
        print("="*50)
        print("Please check your API keys and try again.")

if __name__ == "__main__":
    main()

