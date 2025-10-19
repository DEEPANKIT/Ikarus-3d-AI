"""
LangChain Service for Ikarus 3D
Handles AI-powered text generation and embeddings using Azure OpenAI
"""

import os
import logging
from typing import List, Dict, Any, Optional
import numpy as np
from openai import AzureOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import openai

logger = logging.getLogger(__name__)

class LangChainService:
    """Service for LangChain-based AI operations"""
    
    def __init__(self):
        self.llm = None
        self.embeddings = None
        self.description_chain = None
        self.is_initialized = False
        
    def initialize(self):
        """Initialize LangChain with Azure OpenAI"""
        try:
            # Initialize OpenAI client
            self.client = AzureOpenAI(
                azure_endpoint=os.getenv('OPENAI_API_BASE'),
                api_key=os.getenv('OPENAI_API_KEY'),
                api_version=os.getenv('OPENAI_API_VERSION', '2024-02-15-preview'),
                azure_deployment=os.getenv('OPENAI_DEPLOYMENT_NAME', 'gpt-4')
            )
            
            # Create description generation prompt
            self.description_template = """
            You are a creative product description writer for a furniture e-commerce platform.
            
            Product Details:
            Title: {title}
            Brand: {brand}
            Material: {material}
            Categories: {categories}
            Price: {price}
            Current Description: {current_description}
            
            Generate a creative, engaging product description that:
            1. Highlights the key features and benefits
            2. Appeals to potential buyers
            3. Uses persuasive but honest language
            4. Is 2-3 sentences long
            5. Focuses on lifestyle and functionality
            
            Creative Description:
            """
            
            self.is_initialized = True
            logger.info("LangChain service initialized successfully with direct OpenAI client")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing LangChain service: {e}")
            return False
    
    def generate_product_description(self, product_data: Dict[str, Any]) -> str:
        """Generate creative product description using OpenAI"""
        if not self.is_initialized:
            logger.error("LangChain service not initialized")
            return "AI description generation not available."
        
        try:
            # Prepare input data
            input_data = {
                "title": product_data.get('title', 'Unknown Product'),
                "brand": product_data.get('brand', 'Unknown Brand'),
                "material": product_data.get('material', 'Various Materials'),
                "categories": product_data.get('categories', 'General'),
                "price": product_data.get('price', 'Price not available'),
                "current_description": product_data.get('description', 'No description available')
            }
            
            # Format the prompt
            prompt = self.description_template.format(**input_data)
            
            # Generate description using OpenAI
            response = self.client.chat.completions.create(
                model=os.getenv('OPENAI_DEPLOYMENT_NAME', 'gpt-4'),
                messages=[
                    {"role": "system", "content": "You are a creative product description writer for a furniture e-commerce platform."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=200
            )
            
            # Extract the description
            description = response.choices[0].message.content.strip()
            
            # Clean up the result
            if description.startswith('Creative Description:'):
                description = description.replace('Creative Description:', '').strip()
            
            logger.info(f"Generated AI description for product: {input_data['title'][:50]}...")
            return description
            
        except Exception as e:
            logger.error(f"Error generating product description: {e}")
            return "Unable to generate AI description at this time."
    
    def get_text_embedding(self, text: str) -> np.ndarray:
        """Get text embedding using OpenAI embeddings"""
        if not self.is_initialized:
            logger.error("LangChain service not initialized")
            return np.random.rand(1536)  # OpenAI embedding dimension
        
        try:
            # Get embedding from OpenAI
            embedding = self.embeddings.embed_query(text)
            return np.array(embedding)
            
        except Exception as e:
            logger.error(f"Error getting text embedding: {e}")
            return np.random.rand(1536)
    
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
            return np.random.rand(1536)
    
    def generate_batch_descriptions(self, products: List[Dict[str, Any]]) -> List[str]:
        """Generate descriptions for multiple products"""
        descriptions = []
        
        for product in products:
            try:
                description = self.generate_product_description(product)
                descriptions.append(description)
            except Exception as e:
                logger.error(f"Error generating description for product {product.get('id', 'unknown')}: {e}")
                descriptions.append("AI description generation failed.")
        
        return descriptions
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status and configuration"""
        return {
            "initialized": self.is_initialized,
            "llm_available": self.llm is not None,
            "embeddings_available": self.embeddings is not None,
            "description_chain_available": self.description_chain is not None,
            "api_base": os.getenv('OPENAI_API_BASE', 'Not configured'),
            "deployment_name": os.getenv('OPENAI_DEPLOYMENT_NAME', 'Not configured')
        }

# Global instance
langchain_service = LangChainService()
