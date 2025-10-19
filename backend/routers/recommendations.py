"""
Recommendations API Router
Handles recommendation endpoints
"""

from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import logging
from services.recommendation_service import recommendation_service
from models.recommendation import RecommendationRequest, RecommendationResponse

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """Get product recommendations based on query"""
    try:
        logger.info(f"Getting recommendations for query: {request.query}")
        
        # Get similar products
        similar_products = recommendation_service.get_similar_products(
            query=request.query,
            top_k=request.limit or 10
        )
        
        # Format response
        response = RecommendationResponse(
            recommendations=similar_products,
            query=request.query,
            total_found=len(similar_products),
            processing_time=0.1  # TODO: Add actual timing
        )
        
        logger.info(f"Found {len(similar_products)} recommendations")
        return response
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar/{product_id}")
async def get_similar_products(
    product_id: str,
    limit: int = Query(10, ge=1, le=50)
):
    """Get similar products for a specific product"""
    try:
        logger.info(f"Getting similar products for: {product_id}")
        
        similar_products = recommendation_service.get_content_based_recommendations(
            product_id=product_id,
            top_k=limit
        )
        
        return {
            "product_id": product_id,
            "similar_products": similar_products,
            "total_found": len(similar_products)
        }
        
    except Exception as e:
        logger.error(f"Error getting similar products: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/category/{category}")
async def get_category_recommendations(
    category: str,
    limit: int = Query(10, ge=1, le=50)
):
    """Get recommendations by category"""
    try:
        logger.info(f"Getting recommendations for category: {category}")
        
        category_products = recommendation_service.get_category_recommendations(
            category=category,
            top_k=limit
        )
        
        return {
            "category": category,
            "products": category_products,
            "total_found": len(category_products)
        }
        
    except Exception as e:
        logger.error(f"Error getting category recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

