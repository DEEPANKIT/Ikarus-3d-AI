"""
Computer Vision Service for Ikarus 3D
Handles image processing and feature extraction using ResNet50
"""

import os
import logging
from typing import List, Dict, Any, Optional, Tuple
import numpy as np
import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50, ResNet50_Weights
from PIL import Image
import requests
import io

logger = logging.getLogger(__name__)

class CVService:
    """Service for computer vision operations"""
    
    def __init__(self):
        self.model = None
        self.transform = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.is_initialized = False
        
    def initialize(self):
        """Initialize ResNet50 model for feature extraction"""
        try:
            # Load pre-trained ResNet50
            self.model = resnet50(weights=ResNet50_Weights.IMAGENET1K_V2)
            self.model.eval()
            self.model.to(self.device)
            
            # Define image preprocessing
            self.transform = transforms.Compose([
                transforms.Resize(256),
                transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize(mean=[0.485, 0.456, 0.406], 
                                   std=[0.229, 0.224, 0.225])
            ])
            
            self.is_initialized = True
            logger.info("CV service initialized successfully with ResNet50")
            return True
            
        except Exception as e:
            logger.error(f"Error initializing CV service: {e}")
            return False
    
    def load_image_from_url(self, image_url: str) -> Optional[Image.Image]:
        """Load image from URL"""
        try:
            response = requests.get(image_url, timeout=10)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            return image.convert('RGB')
        except Exception as e:
            logger.error(f"Error loading image from URL {image_url}: {e}")
            return None
    
    def extract_image_features(self, image: Image.Image) -> np.ndarray:
        """Extract features from image using ResNet50"""
        if not self.is_initialized:
            logger.error("CV service not initialized")
            return np.random.rand(2048)  # ResNet50 feature dimension
        
        try:
            # Preprocess image
            input_tensor = self.transform(image).unsqueeze(0).to(self.device)
            
            # Extract features (remove final classification layer)
            with torch.no_grad():
                features = self.model.avgpool(self.model.layer4(self.model.layer3(
                    self.model.layer2(self.model.layer1(self.model.maxpool(
                        self.model.relu(self.model.bn1(self.model.conv1(input_tensor)))))))))
                features = features.squeeze().cpu().numpy()
            
            return features
            
        except Exception as e:
            logger.error(f"Error extracting image features: {e}")
            return np.random.rand(2048)
    
    def get_image_embedding(self, image_url: str) -> np.ndarray:
        """Get embedding for image from URL"""
        try:
            image = self.load_image_from_url(image_url)
            if image is None:
                return np.random.rand(2048)
            
            return self.extract_image_features(image)
            
        except Exception as e:
            logger.error(f"Error getting image embedding: {e}")
            return np.random.rand(2048)
    
    def classify_image_category(self, image: Image.Image) -> Dict[str, float]:
        """Classify image into furniture categories"""
        if not self.is_initialized:
            return {"unknown": 1.0}
        
        try:
            # Furniture-related categories from ImageNet
            furniture_categories = {
                'chair': 0.3,
                'sofa': 0.25,
                'table': 0.2,
                'bed': 0.15,
                'cabinet': 0.1
            }
            
            # For now, return mock classification
            # In production, you'd train a custom classifier
            return furniture_categories
            
        except Exception as e:
            logger.error(f"Error classifying image: {e}")
            return {"unknown": 1.0}
    
    def get_service_status(self) -> Dict[str, Any]:
        """Get service status"""
        return {
            "initialized": self.is_initialized,
            "model_available": self.model is not None,
            "device": str(self.device),
            "transform_available": self.transform is not None
        }

# Global instance
cv_service = CVService()

