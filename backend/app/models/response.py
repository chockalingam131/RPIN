"""
Response models for API endpoints
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

from app.models.domain import MarketRecommendation, Market, CropInfo


class PredictionResponse(BaseModel):
    """Response model for market prediction"""
    request_id: str = Field(..., description="Unique request identifier")
    timestamp: datetime = Field(..., description="Response timestamp")
    village_location: str = Field(..., description="Input village location")
    crop_type: str = Field(..., description="Input crop type")
    quantity_kg: float = Field(..., description="Input quantity in kg")
    
    markets: List[MarketRecommendation] = Field(
        ...,
        description="List of market recommendations sorted by net profit"
    )
    best_market: str = Field(..., description="Recommended market name")
    best_market_id: str = Field(..., description="Recommended market ID")
    explanation: str = Field(..., description="Natural language explanation")
    
    total_markets_analyzed: int = Field(..., description="Number of markets analyzed")
    forecast_days: int = Field(default=7, description="Number of days forecasted")
    
    class Config:
        json_schema_extra = {
            "example": {
                "request_id": "req_20240225_123456",
                "timestamp": "2024-02-25T12:34:56",
                "village_location": "theni",
                "crop_type": "tomato",
                "quantity_kg": 1000,
                "markets": [
                    {
                        "market_id": "madurai",
                        "market_name": "Madurai Mandi",
                        "predicted_price": 28.5,
                        "demand_level": "High",
                        "spoilage_risk_percent": 5.2,
                        "transport_cost": 2400.0,
                        "net_profit": 20800.0,
                        "confidence_score": 0.85,
                        "optimal_selling_day": "2024-02-28",
                        "distance_km": 80
                    }
                ],
                "best_market": "Madurai Mandi",
                "best_market_id": "madurai",
                "explanation": "For 1000 kg of tomatoes from Theni, selling in Madurai after 3 days gives ₹20,800 profit which is ₹7,300 more than the local market due to rising prices and lower spoilage risk.",
                "total_markets_analyzed": 3,
                "forecast_days": 7
            }
        }


class MarketListResponse(BaseModel):
    """Response model for market listing"""
    location: str = Field(..., description="Query location")
    markets: List[Market] = Field(..., description="List of available markets")
    total_count: int = Field(..., description="Total number of markets")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "theni",
                "markets": [
                    {
                        "market_id": "madurai",
                        "name": "Madurai Mandi",
                        "location": "Madurai",
                        "coordinates": [9.9252, 78.1198],
                        "operating_days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
                        "capacity_tons": 500
                    }
                ],
                "total_count": 3
            }
        }


class CropListResponse(BaseModel):
    """Response model for crop listing"""
    crops: List[CropInfo] = Field(..., description="List of supported crops")
    total_count: int = Field(..., description="Total number of crops")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crops": [
                    {
                        "crop_id": "tomato",
                        "name": "Tomato",
                        "shelf_life_days": 7,
                        "optimal_temperature": 15,
                        "humidity_tolerance": 85,
                        "handling_requirements": ["gentle_handling", "avoid_direct_sunlight"]
                    }
                ],
                "total_count": 6
            }
        }


class ErrorResponse(BaseModel):
    """Response model for errors"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "ValidationError",
                "message": "Invalid crop type provided",
                "details": {
                    "field": "crop_type",
                    "value": "unknown_crop",
                    "supported_crops": ["tomato", "onion", "potato", "cabbage", "carrot", "cauliflower"]
                },
                "timestamp": "2024-02-25T12:34:56"
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check"""
    status: str = Field(..., description="Service status")
    service: str = Field(..., description="Service name")
    version: str = Field(..., description="Service version")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
    components: Optional[Dict[str, str]] = Field(None, description="Component health status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "service": "RPIN - Rural Producer Intelligence Network",
                "version": "1.0.0",
                "timestamp": "2024-02-25T12:34:56",
                "components": {
                    "database": "healthy",
                    "ml_models": "loaded",
                    "external_apis": "available"
                }
            }
        }
