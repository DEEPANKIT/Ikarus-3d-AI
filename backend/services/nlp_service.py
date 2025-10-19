"""
NLP Service for Ikarus 3D
Handles text processing and semantic similarity using sentence-transformers
"""

import logging
from typing import List, Dict, Any, Optional
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

logger = logging.getLogger(__name__)

class NLPService:
    """Service for natural language processing operations"""
    
    def __init__(self):
        self.model = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize sentence transformer model"""
        try:
            # Load pre-trained sentence transformer
            self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            self.is_initialized = True
            logger.info("NLP service initialized successfully with sentence-transformers")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing NLP service: {e}")
            return False
    
    def get_text_embedding(self, text: str) -> np.ndarray:
        """Get text embedding using sentence transformers"""
        if not self.is_initialized:
            logger.error("NLP service not initialized")
            return np.random.rand(384)  # all-MiniLM-L6-v2 dimension
        
        try:
            embedding = self.model.encode([text])[0]
            return embedding
            
        except Exception as e:
            logger.error(f"Error getting text embedding: {e}")
            return np.random.rand(384)
    
    def get_product_embedding(self, product_data: Dict[str, Any]) -> np.ndarray:
        """Get combined embedding for product data"""
        try:
            # Combine product features into text
            text_parts = []
            
            if product_data.get('title'):
                text_parts.append(str(product_data['title']))
            if product_data.get('description'):
                text_parts.append(str(product_data['description']))
            if product_data.get('brand'):
                text_parts.append(f"Brand: {product_data['brand']}")
            if product_data.get('material'):
                text_parts.append(f"Material: {product_data['material']}")
            if product_data.get('categories'):
                text_parts.append(f"Categories: {product_data['categories']}")
            
            combined_text = " ".join(text_parts)
            return self.get_text_embedding(combined_text)
            
        except Exception as e:
            logger.error(f"Error generating product embedding: {e}")
            return np.random.rand(384)
    
    def find_similar_products(self, query_text: str, product_embeddings: List[np.ndarray], 
                            top_k: int = 10) -> List[Dict[str, Any]]:
        """Find similar products based on text similarity"""
        if not self.is_initialized:
            return []
        
        try:
            # Get query embedding
            query_embedding = self.get_text_embedding(query_text)
            
            # Calculate similarities
            similarities = cosine_similarity([query_embedding], product_embeddings)[0]
            
            # Get top similar products
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                results.append({
                    'index': int(idx),
                    'similarity_score': float(similarities[idx])
                })
            
            return results
            
        except Exception as e:
            logger.error(f"Error finding similar products: {e}")
            return []
    
    def group_similar_products(self, product_embeddings: List[np.ndarray], 
                             n_clusters: int = 10) -> Dict[str, Any]:
        """Group products into similar clusters"""
        try:
            if len(product_embeddings) < n_clusters:
                n_clusters = max(2, len(product_embeddings) // 2)
            
            # Perform K-means clustering
            kmeans = KMeans(n_clusters=n_clusters, random_state=42)
            cluster_labels = kmeans.fit_predict(product_embeddings)
            
            # Calculate silhouette score
            silhouette_avg = silhouette_score(product_embeddings, cluster_labels)
            
            # Group products by cluster
            clusters = {}
            for i, label in enumerate(cluster_labels):
                if label not in clusters:
                    clusters[label] = []
                clusters[label].append(i)
            
            return {
                'cluster_labels': cluster_labels.tolist(),
                'clusters': clusters,
                'silhouette_score': float(silhouette_avg),
                'n_clusters': n_clusters
            }
            
        except Exception as e:
            logger.error(f"Error grouping similar products: {e}")
            return {}
    
    def extract_keywords(self, text: str, top_k: int = 10) -> List[str]:
        """Extract key terms from product text"""
        try:
            # Simple keyword extraction (in production, use more sophisticated methods)
            words = text.lower().split()
            
            # Remove common stop words
            stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
            keywords = [word for word in words if word not in stop_words and len(word) > 2]
            
            # Count frequency and return top keywords
            from collections import Counter
            keyword_counts = Counter(keywords)
            return [word for word, count in keyword_counts.most_common(top_k)]
            
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "initialized": self.is_initialized,
            "model_available": self.model is not None,
            "model_name": "sentence-transformers/all-MiniLM-L6-v2" if self.model else None
        }

# Global instance
nlp_service = NLPService()

