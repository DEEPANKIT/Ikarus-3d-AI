"""
Simple Backend Test Script
Tests the basic FastAPI setup without complex ML dependencies
"""

import os
import sys
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Ikarus 3D Product Recommendation API",
    version="1.0.0",
    description="ML-driven product recommendation and analytics for Ikarus 3D",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def read_root():
    return {"message": "Ikarus 3D Product Recommendation API", "version": "1.0.0", "status": "running"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ikarus-3d-api"}

@app.get("/api/v1/test")
async def test_endpoint():
    """Test endpoint for basic functionality"""
    return {
        "message": "Backend is working!",
        "data": {
            "products_loaded": "312 products available",
            "pinecone_status": "Index ready",
            "recommendations": "Available"
        }
    }

@app.get("/api/v1/products/sample")
async def get_sample_products():
    """Get sample products for testing"""
    sample_products = [
        {
            "id": "02593e81-5c09-5069-8516-b0b29f439ded",
            "title": "GOYMFK 1pc Free Standing Shoe Rack, Multi-layer Metal Shoe Cap Rack With 8 Double Hooks For Living Room, Bathroom, Hallway",
            "brand": "GOYMFK",
            "price": "$24.99",
            "material": "Metal",
            "categories": "Home & Kitchen, Storage & Organization, Clothing & Closet Storage, Shoe Organizers, Free Standing Shoe Racks",
            "description": "multiple shoes, coats, hats, and other items Easy to assemble: Includes all necessary hardware and instructions for easy assembly Versatile: Perfect for use in living rooms, bathrooms, hallways, and more",
            "image": "https://m.media-amazon.com/images/I/416WaLx10jL._SS522_.jpg"
        },
        {
            "id": "5938d217-b8c5-5d3e-b1cf-e28e340f292e", 
            "title": "subrtex Leather Dining Room, Dining Chairs Set of 2, Black",
            "brand": "subrtex",
            "price": "Price not available",
            "material": "Sponge",
            "categories": "Home & Kitchen, Furniture, Dining Room Furniture, Chairs",
            "description": "subrtex Dining chairs Set of 2",
            "image": "https://m.media-amazon.com/images/I/31SejUEWY7L._SS522_.jpg"
        },
        {
            "id": "b2ede786-3f51-5a45-9a5b-bcf856958cd8",
            "title": "Plant Repotting Mat MUYETOL Waterproof Transplanting Mat Indoor 26.8\" x 26.8\" Portable Square Foldable Easy to Clean Gardening Work Mat Soil Changing Mat Succulent Plant Transplanting Mat Garden Gifts",
            "brand": "MUYETOL",
            "price": "$5.98",
            "material": "Polyethylene",
            "categories": "Patio, Lawn & Garden, Outdoor Décor, Doormats",
            "description": "Waterproof transplanting mat for indoor gardening",
            "image": "https://m.media-amazon.com/images/I/41RgefVq70L._SS522_.jpg"
        }
    ]
    return {"products": sample_products, "count": len(sample_products)}

if __name__ == "__main__":
    logger.info("Starting Ikarus 3D API server...")
    uvicorn.run(
        "test_backend:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
