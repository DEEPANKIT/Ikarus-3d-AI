"""
Analytics router for Ikarus 3D
Provides real-time analytics data from the product dataset
"""

from fastapi import APIRouter
from typing import Dict, Any, List
import pandas as pd
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Cache for analytics data
_analytics_cache = None

def load_analytics_data():
    """Load and cache analytics data"""
    global _analytics_cache
    
    if _analytics_cache is not None:
        return _analytics_cache
    
    try:
        # Load dataset
        data_path = Path(__file__).parent.parent.parent / "data" / "raw" / "intern_data_ikarus.csv"
        df = pd.read_csv(data_path)
        
        # Clean price data
        df['price_clean'] = df['price'].str.replace('$', '').astype(float)
        
        # Calculate analytics
        analytics = {
            "total_products": len(df),
            "average_price": float(df['price_clean'].mean()),
            "median_price": float(df['price_clean'].median()),
            "price_range": {
                "min": float(df['price_clean'].min()),
                "max": float(df['price_clean'].max())
            },
            "total_brands": df['brand'].nunique(),
            "total_categories": df['categories'].nunique(),
            "total_materials": df['material'].nunique()
        }
        
        # Top categories
        categories = []
        for cat_str in df['categories'].dropna():
            try:
                import ast
                cat_list = ast.literal_eval(cat_str) if isinstance(cat_str, str) else cat_str
                categories.extend(cat_list)
            except:
                continue
        
        from collections import Counter
        category_counts = Counter(categories)
        analytics["top_categories"] = [
            {"name": name, "value": count} 
            for name, count in category_counts.most_common(10)
        ]
        
        # Top brands
        brand_counts = df['brand'].value_counts()
        analytics["top_brands"] = [
            {"name": name, "value": int(count)} 
            for name, count in brand_counts.head(10).items()
        ]
        
        # Price distribution
        price_ranges = [
            (0, 25, "$0-25"),
            (25, 50, "$25-50"),
            (50, 100, "$50-100"),
            (100, 200, "$100-200"),
            (200, float('inf'), "$200+")
        ]
        
        analytics["price_distribution"] = []
        for min_price, max_price, label in price_ranges:
            count = len(df[(df['price_clean'] >= min_price) & (df['price_clean'] < max_price)])
            analytics["price_distribution"].append({
                "range": label,
                "count": int(count)
            })
        
        _analytics_cache = analytics
        logger.info("Analytics data loaded and cached successfully")
        return analytics
        
    except Exception as e:
        logger.error(f"Error loading analytics data: {e}")
        return {
            "total_products": 0,
            "average_price": 0,
            "error": str(e)
        }

@router.get("/overview")
async def get_analytics_overview():
    """Get comprehensive analytics overview"""
    try:
        analytics = load_analytics_data()
        return {
            "status": "success",
            "data": analytics,
            "generated_at": pd.Timestamp.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Error getting analytics overview: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

@router.get("/categories")
async def get_category_analytics():
    """Get category distribution analytics"""
    try:
        analytics = load_analytics_data()
        return {
            "status": "success",
            "categories": analytics.get("top_categories", []),
            "total_categories": analytics.get("total_categories", 0)
        }
    except Exception as e:
        logger.error(f"Error getting category analytics: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/brands")
async def get_brand_analytics():
    """Get brand distribution analytics"""
    try:
        analytics = load_analytics_data()
        return {
            "status": "success",
            "brands": analytics.get("top_brands", []),
            "total_brands": analytics.get("total_brands", 0)
        }
    except Exception as e:
        logger.error(f"Error getting brand analytics: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/pricing")
async def get_pricing_analytics():
    """Get pricing analytics"""
    try:
        analytics = load_analytics_data()
        return {
            "status": "success",
            "average_price": analytics.get("average_price", 0),
            "median_price": analytics.get("median_price", 0),
            "price_range": analytics.get("price_range", {}),
            "price_distribution": analytics.get("price_distribution", [])
        }
    except Exception as e:
        logger.error(f"Error getting pricing analytics: {e}")
        return {"status": "error", "message": str(e)}

@router.get("/summary")
async def get_analytics_summary():
    """Get key metrics summary"""
    try:
        analytics = load_analytics_data()
        return {
            "status": "success",
            "summary": {
                "total_products": analytics.get("total_products", 0),
                "average_price": round(analytics.get("average_price", 0), 2),
                "total_brands": analytics.get("total_brands", 0),
                "total_categories": analytics.get("total_categories", 0),
                "total_materials": analytics.get("total_materials", 0)
            }
        }
    except Exception as e:
        logger.error(f"Error getting analytics summary: {e}")
        return {"status": "error", "message": str(e)}

