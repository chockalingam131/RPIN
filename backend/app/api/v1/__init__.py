"""API v1 router"""
from fastapi import APIRouter

from app.api.v1.endpoints import prediction, markets, crops

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(prediction.router, tags=["predictions"])
api_router.include_router(markets.router, tags=["markets"])
api_router.include_router(crops.router, tags=["crops"])
