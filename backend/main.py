"""
Ikarus 3D Product Recommendation System - FastAPI Main Application
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import os
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Create FastAPI application
app = FastAPI(
    title="Ikarus 3D Product Recommendation API",
    description="ML-driven furniture product recommendations and analytics",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Ikarus 3D Product Recommendation API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "ikarus-3d-api"}

# Import and include routers
from routers import recommendations
from routers import products
from routers import analytics
from services.recommendation_service import recommendation_service

# Initialize recommendation service
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Initializing recommendation service...")
    if recommendation_service.initialize_service():
        logger.info("Recommendation service initialized successfully")
    else:
        logger.error("Failed to initialize recommendation service")

# Include routers
app.include_router(recommendations.router, prefix="/api/v1/recommendations", tags=["recommendations"])
app.include_router(products.router, prefix="/api/v1/products", tags=["products"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["analytics"])

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
