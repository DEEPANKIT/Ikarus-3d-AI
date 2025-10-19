"""
Simple Embedding Service for Ikarus 3D
Basic text embedding using TF-IDF for now
"""

import logging
import numpy as np
from typing import Dict, Any, List
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

logger = logging.getLogger(__name__)

class EmbeddingService:
    """Service for generating text embeddings"""
    
    def __init__(self):
        self.vectorizer = None
        self.is_initialized = False
        
    def initialize(self, texts: List[str]):
        """Initialize the TF-IDF vectorizer with sample texts"""
        try:
            self.vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            self.vectorizer.fit(texts)
            self.is_initialized = True
            logger.info("Embedding service initialized successfully")
            return True
        except Exception as e:
            logger.error(f"Error initializing embedding service: {e}")
            return False
    
    def get_text_embedding(self, text: str) -> np.ndarray:
        """Get embedding for a single text"""
        if not self.is_initialized:
            # Return random embedding if not initialized
            return np.random.rand(100)
        
        try:
            embedding = self.vectorizer.transform([text]).toarray()[0]
            return embedding
        except Exception as e:
            logger.error(f"Error generating text embedding: {e}")
            return np.random.rand(100)
    
    def get_product_embedding(self, product_data: Dict[str, Any]) -> np.ndarray:
        """Get embedding for product data"""
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
            return np.random.rand(100)

# Global instance
embedding_service = EmbeddingService()