"""
Recommendation Service for Ikarus 3D
Core recommendation logic using ML models and Pinecone
"""

import logging
import numpy as np
from typing import List, Dict, Any, Optional
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import os
import pinecone
from services.nlp_service import nlp_service
from services.langchain_service import langchain_service

logger = logging.getLogger(__name__)

class RecommendationService:
    """Service for generating product recommendations using Pinecone and ML models"""
    
    def __init__(self):
        self.products_data = None
        self.pc = None
        self.index = None
        self.is_initialized = False
        
    def load_products_data(self, csv_path: str = "../data/raw/intern_data_ikarus.csv"):
        """Load products data from CSV"""
        try:
            logger.info(f"Loading products data from {csv_path}")
            self.products_data = pd.read_csv(csv_path)
            logger.info(f"Loaded {len(self.products_data)} products")
            return True
        except Exception as e:
            logger.error(f"Error loading products data: {e}")
            return False
    
    def prepare_text_features(self):
        """Prepare text features for TF-IDF"""
        if self.products_data is None:
            logger.error("Products data not loaded")
            return False
        
        try:
            # Combine text features
            text_features = []
            for _, row in self.products_data.iterrows():
                features = []
                if pd.notna(row.get('title')):
                    features.append(str(row['title']))
                if pd.notna(row.get('description')):
                    features.append(str(row['description']))
                if pd.notna(row.get('brand')):
                    features.append(f"Brand: {row['brand']}")
                if pd.notna(row.get('material')):
                    features.append(f"Material: {row['material']}")
                
                combined_text = " ".join(features)
                text_features.append(combined_text)
            
            # Create TF-IDF matrix
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(text_features)
            
            logger.info("Text features prepared successfully")
            return True
        except Exception as e:
            logger.error(f"Error preparing text features: {e}")
            return False
    
    def generate_embeddings(self):
        """Generate embeddings for all products"""
        if self.products_data is None:
            logger.error("Products data not loaded")
            return False
        
        try:
            logger.info("Generating embeddings for all products...")
            embeddings = []
            
            for _, row in self.products_data.iterrows():
                # Prepare text for embedding
                text_parts = []
                if pd.notna(row.get('title')):
                    text_parts.append(str(row['title']))
                if pd.notna(row.get('description')):
                    text_parts.append(str(row['description']))
                if pd.notna(row.get('brand')):
                    text_parts.append(f"Brand: {row['brand']}")
                if pd.notna(row.get('material')):
                    text_parts.append(f"Material: {row['material']}")
                
                combined_text = " ".join(text_parts)
                embedding = nlp_service.get_text_embedding(combined_text)
                if embedding is not None:
                    embeddings.append(embedding)
                else:
                    # Use zero vector as fallback
                    embeddings.append(np.zeros(384))
            
            self.product_embeddings = np.array(embeddings)
            logger.info(f"Generated embeddings for {len(embeddings)} products")
            return True
        except Exception as e:
            logger.error(f"Error generating embeddings: {e}")
            return False
    
    def get_similar_products(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Get similar products based on query using Pinecone REST API"""
        if not self.is_initialized:
            logger.error("Recommendation service not initialized")
            return []
        
        try:
            # Use Pinecone REST API for vector search if available
            if hasattr(self, 'pinecone_host') and self.pinecone_host:
                logger.info(f"Using Pinecone REST API for query: {query}")
                
                # Generate query embedding
                query_embedding = nlp_service.get_text_embedding(query)
                if query_embedding is None:
                    logger.error("Failed to generate query embedding")
                    return []
                
                # Search Pinecone using REST API
                import requests
                headers = {
                    "Api-Key": self.pinecone_api_key,
                    "Content-Type": "application/json"
                }
                
                query_payload = {
                    "vector": query_embedding.tolist(),
                    "topK": top_k,
                    "includeMetadata": True
                }
                
                response = requests.post(
                    f"{self.pinecone_host}/query",
                    headers=headers,
                    json=query_payload
                )
                
                if response.status_code == 200:
                    search_results = response.json()
                    matches = search_results.get('matches', [])
                    
                    # Format results
                    results = []
                    for match in matches:
                        product = {
                            'id': match['id'],
                            'title': match['metadata'].get('title', ''),
                            'brand': match['metadata'].get('brand', ''),
                            'price': match['metadata'].get('price', ''),
                            'description': match['metadata'].get('description', ''),
                            'material': match['metadata'].get('material', ''),
                            'categories': match['metadata'].get('categories', ''),
                            'image': match['metadata'].get('image', ''),
                            'similarity_score': float(match['score'])
                        }
                        results.append(product)
                    
                    logger.info(f"Found {len(results)} similar products using Pinecone REST API")
                    return results
                else:
                    logger.error(f"Pinecone query failed: {response.status_code} - {response.text}")
                    # Fall back to local search
                    return self._get_similar_products_fallback(query, top_k)
            
            else:
                # Fallback to local vector similarity if Pinecone not available
                logger.info(f"Using fallback vector similarity for query: {query}")
                return self._get_similar_products_fallback(query, top_k)
            
        except Exception as e:
            logger.error(f"Error getting similar products: {e}")
            return []
    
    def _get_similar_products_fallback(self, query: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Fallback method using local vector similarity"""
        try:
            # Use vector similarity search with embeddings
            if self.products_data is None:
                logger.error("Products data not loaded")
                return []
            
            # Generate query embedding
            query_embedding = nlp_service.get_text_embedding(query)
            if query_embedding is None:
                logger.error("Failed to generate query embedding")
                return []
            
            # Generate embeddings for all products if not already done
            if not hasattr(self, 'product_embeddings') or self.product_embeddings is None:
                logger.info("Generating product embeddings...")
                self.generate_embeddings()
            
            if self.product_embeddings is None:
                logger.error("Failed to generate product embeddings")
                return []
            
            # Calculate similarities
            similarities = []
            for idx, row in self.products_data.iterrows():
                if idx < len(self.product_embeddings):
                    product_embedding = self.product_embeddings[idx]
                    similarity = np.dot(query_embedding, product_embedding) / (
                        np.linalg.norm(query_embedding) * np.linalg.norm(product_embedding)
                    )
                    similarities.append((idx, similarity))
            
            # Sort by similarity and get top_k
            similarities.sort(key=lambda x: x[1], reverse=True)
            top_indices = [idx for idx, _ in similarities[:top_k]]
            
            # Format results
            results = []
            for idx in top_indices:
                row = self.products_data.iloc[idx]
                product = {
                    'id': str(row.get('uniq_id', f'product_{idx}')),
                    'title': str(row.get('title', '')),
                    'brand': str(row.get('brand', '')),
                    'price': str(row.get('price', '')),
                    'description': str(row.get('description', '')),
                    'material': str(row.get('material', '')),
                    'categories': str(row.get('categories', '')),
                    'image': str(row.get('images', '')),
                    'similarity_score': float(similarities[top_indices.index(idx)][1])
                }
                results.append(product)
            
            logger.info(f"Found {len(results)} similar products using fallback vector similarity")
            return results
            
        except Exception as e:
            logger.error(f"Error in fallback similarity search: {e}")
            return []
    
    def get_content_based_recommendations(self, product_id: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Get content-based recommendations for a specific product"""
        if self.product_embeddings is None:
            logger.error("Product embeddings not generated")
            return []
        
        try:
            # Find the product index
            product_idx = None
            for idx, row in self.products_data.iterrows():
                if str(row.get('uniq_id', '')) == product_id:
                    product_idx = idx
                    break
            
            if product_idx is None:
                logger.warning(f"Product {product_id} not found")
                return []
            
            # Get product embedding
            product_embedding = self.product_embeddings[product_idx].reshape(1, -1)
            
            # Calculate similarities
            similarities = cosine_similarity(product_embedding, self.product_embeddings)[0]
            
            # Remove the product itself and get top similar
            similarities[product_idx] = -1  # Exclude the product itself
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                if idx != product_idx:  # Double check
                    product = self.products_data.iloc[idx].to_dict()
                    product['similarity_score'] = float(similarities[idx])
                    results.append(product)
            
            logger.info(f"Found {len(results)} content-based recommendations for product {product_id}")
            return results
            
        except Exception as e:
            logger.error(f"Error getting content-based recommendations: {e}")
            return []
    
    def get_category_recommendations(self, category: str, top_k: int = 10) -> List[Dict[str, Any]]:
        """Get recommendations based on category"""
        if self.products_data is None:
            logger.error("Products data not loaded")
            return []
        
        try:
            # Filter products by category
            category_products = self.products_data[
                self.products_data['categories'].str.contains(category, case=False, na=False)
            ]
            
            if len(category_products) == 0:
                logger.warning(f"No products found for category: {category}")
                return []
            
            # Return top products in category (could be sorted by price, rating, etc.)
            results = category_products.head(top_k).to_dict('records')
            
            logger.info(f"Found {len(results)} products in category: {category}")
            return results
            
        except Exception as e:
            logger.error(f"Error getting category recommendations: {e}")
            return []
    
    def initialize_service(self):
        """Initialize the recommendation service with Pinecone and ML models"""
        try:
            logger.info("Initializing recommendation service...")
            
            # Initialize ML services
            nlp_success = nlp_service.initialize()
            langchain_success = langchain_service.initialize()
            
            if not nlp_success:
                logger.error("Failed to initialize NLP service")
                return False
            
            # Initialize Pinecone
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT', 'us-east-1')
            if not api_key:
                logger.error("PINECONE_API_KEY not found")
                return False
            
            # Skip Pinecone initialization due to network connectivity issues
            # Will use fallback local vector similarity search
            logger.warning("Skipping Pinecone initialization due to network issues - using fallback search")
            self.pinecone_host = None
            self.pinecone_api_key = None
            
            # Load products data for fallback
            self.load_products_data()
            
            self.is_initialized = True
            logger.info("Recommendation service initialized successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing recommendation service: {e}")
            return False

# Global instance
recommendation_service = RecommendationService()

