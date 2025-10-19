"""
Products router
Exposes lightweight endpoints for product listings and samples used by the frontend.
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
import logging
from services.langchain_service import langchain_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/sample")
async def get_sample_products():
    """Return a small set of sample products with image URLs.

    Note: These are static examples to validate the frontend UI and data flow.
    """
    sample_products = [
        {
            "id": "02593e81-5c09-5069-8516-b0b29f439ded",
            "title": "GOYMFK 1pc Free Standing Shoe Rack, Multi-layer Metal Shoe Cap Rack",
            "brand": "GOYMFK",
            "price": "$24.99",
            "material": "Metal",
            "categories": "Home & Kitchen, Storage & Organization",
            "description": "Multi-layer metal rack with hooks for shoes, coats and hats.",
            "image": "https://m.media-amazon.com/images/I/416WaLx10jL._SS522_.jpg",
        },
        {
            "id": "5938d217-b8c5-5d3e-b1cf-e28e340f292e",
            "title": "subrtex Leather Dining Chairs Set of 2, Black",
            "brand": "subrtex",
            "price": "$199.99",
            "material": "Leather",
            "categories": "Home & Kitchen, Furniture, Chairs",
            "description": "Comfortable leather dining chairs for modern spaces.",
            "image": "https://m.media-amazon.com/images/I/31SejUEWY7L._SS522_.jpg",
        },
        {
            "id": "b2ede786-3f51-5a45-9a5b-bcf856958cd8",
            "title": "MUYETOL Wooden Waterproof Transplanting Mat 26.8 x 26.8 in",
            "brand": "MUYETOL",
            "price": "$5.98",
            "material": "Wood",
            "categories": "Patio, Lawn & Garden, Outdoor Décor",
            "description": "Portable wooden foldable mat for indoor gardening work.",
            "image": "https://m.media-amazon.com/images/I/41RgefVq70L._SS522_.jpg",
        },
        {
            "id": "wooden-table-001",
            "title": "Modern Wooden Dining Table, Oak Finish",
            "brand": "IKEA",
            "price": "$299.99",
            "material": "Oak Wood",
            "categories": "Furniture, Tables, Dining Room",
            "description": "Beautiful solid oak wooden dining table for family gatherings.",
            "image": "https://m.media-amazon.com/images/I/41RgefVq70L._SS522_.jpg",
        },
        {
            "id": "leather-sofa-001",
            "title": "Premium Black Leather Sofa, 3-Seater",
            "brand": "West Elm",
            "price": "$899.99",
            "material": "Genuine Leather",
            "categories": "Furniture, Sofas, Living Room",
            "description": "Luxurious black leather sofa perfect for any living room.",
            "image": "https://m.media-amazon.com/images/I/31SejUEWY7L._SS522_.jpg",
        },
    ]

    return {"products": sample_products, "count": len(sample_products)}


@router.post("/{product_id}/generate-description")
async def generate_ai_description(product_id: str, product_data: Dict[str, Any]):
    """Generate AI-powered product description using LangChain"""
    try:
        # Generate AI description
        ai_description = langchain_service.generate_product_description(product_data)
        
        return {
            "product_id": product_id,
            "ai_description": ai_description,
            "original_description": product_data.get('description', ''),
            "generated_by": "LangChain + Azure OpenAI"
        }
        
    except Exception as e:
        logger.error(f"Error generating AI description for product {product_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate AI description")


