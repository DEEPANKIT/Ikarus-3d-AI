"""
Pinecone Service for Ikarus 3D
Handles vector database operations
"""

import os
import logging
from typing import List, Dict, Any, Optional
import numpy as np
import pinecone
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

class PineconeService:
    """Service for Pinecone vector database operations"""
    
    def __init__(self):
        self.pc = None
        self.index = None
        self.embedding_model = None
        self.index_name = "ikarus-products"
        
    def initialize(self):
        """Initialize Pinecone client and index"""
        try:
            # Initialize Pinecone client
            api_key = os.getenv('PINECONE_API_KEY')
            if not api_key:
                raise ValueError("PINECONE_API_KEY not found in environment variables")
            
            pinecone.init(api_key=api_key, environment=os.getenv('PINECONE_ENVIRONMENT', 'us-east-1'))
            
            # Connect to index
            self.index = pinecone.Index(self.index_name)
            
            # Load embedding model
            self.embedding_model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            
            logger.info("Pinecone service initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing Pinecone service: {e}")
            return False
    
    def search_similar_products(self, query: str, top_k: int = 10, filters: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """Search for similar products using vector similarity"""
        try:
            if not self.index:
                raise ValueError("Pinecone index not initialized")
            
            # Generate query embedding
            query_embedding = self.embedding_model.encode([query])[0]
            
            # Prepare search parameters
            search_params = {
                'vector': query_embedding.tolist(),
                'top_k': top_k,
                'include_metadata': True
            }
            
            # Add filters if provided
            if filters:
                search_params['filter'] = filters
            
            # Perform search
            results = self.index.query(**search_params)
            
            # Format results
            products = []
            for match in results['matches']:
                product = {
                    'id': match['id'],
                    'score': match['score'],
                    **match['metadata']
                }
                products.append(product)
            
            logger.info(f"Found {len(products)} similar products for query: {query}")
            return products
            
        except Exception as e:
            logger.error(f"Error searching similar products: {e}")
            return []
    
    def get_product_by_id(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific product by ID"""
        try:
            if not self.index:
                raise ValueError("Pinecone index not initialized")
            
            # Fetch product by ID
            results = self.index.fetch(ids=[product_id])
            
            if product_id in results['vectors']:
                vector_data = results['vectors'][product_id]
                return {
                    'id': product_id,
                    **vector_data['metadata']
                }
            
            return None
            
        except Exception as e:
            logger.error(f"Error getting product by ID: {e}")
            return None
    
    def get_similar_products_by_id(self, product_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Get similar products for a specific product ID"""
        try:
            if not self.index:
                raise ValueError("Pinecone index not initialized")
            
            # First get the product vector
            product_data = self.get_product_by_id(product_id)
            if not product_data:
                return []
            
            # Fetch the vector for similarity search
            results = self.index.fetch(ids=[product_id])
            if product_id not in results['vectors']:
                return []
            
            vector = results['vectors'][product_id]['values']
            
            # Search for similar products
            search_results = self.index.query(
                vector=vector,
                top_k=top_k + 1,  # +1 to exclude the original product
                include_metadata=True
            )
            
            # Filter out the original product
            similar_products = []
            for match in search_results['matches']:
                if match['id'] != product_id:
                    product = {
                        'id': match['id'],
                        'score': match['score'],
                        **match['metadata']
                    }
                    similar_products.append(product)
            
            logger.info(f"Found {len(similar_products)} similar products for product {product_id}")
            return similar_products
            
        except Exception as e:
            logger.error(f"Error getting similar products by ID: {e}")
            return []
    
    def get_products_by_category(self, category: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Get products filtered by category"""
        try:
            if not self.index:
                raise ValueError("Pinecone index not initialized")
            
            # Create filter for category
            filters = {
                "categories": {"$regex": category}
            }
            
            # Use a dummy vector for filtering (we're filtering, not searching by similarity)
            dummy_vector = [0.0] * 384  # 384 is the dimension of our embeddings
            
            results = self.index.query(
                vector=dummy_vector,
                top_k=top_k,
                filter=filters,
                include_metadata=True
            )
            
            products = []
            for match in results['matches']:
                product = {
                    'id': match['id'],
                    'score': match['score'],
                    **match['metadata']
                }
                products.append(product)
            
            logger.info(f"Found {len(products)} products in category: {category}")
            return products
            
        except Exception as e:
            logger.error(f"Error getting products by category: {e}")
            return []
    
    def get_index_stats(self) -> Dict[str, Any]:
        """Get index statistics"""
        try:
            if not self.index:
                raise ValueError("Pinecone index not initialized")
            
            stats = self.index.describe_index_stats()
            return {
                'total_vector_count': stats.total_vector_count,
                'dimension': stats.dimension,
                'index_fullness': stats.index_fullness
            }
            
        except Exception as e:
            logger.error(f"Error getting index stats: {e}")
            return {}

# Global instance
pinecone_service = PineconeService()



