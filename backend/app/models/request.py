"""
Request models for API endpoints
"""
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime, timedelta
from typing import Optional


class PredictionRequest(BaseModel):
    """Request model for market prediction"""
    village_location: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Village or location name"
    )
    crop_type: str = Field(
        ...,
        min_length=2,
        max_length=50,
        description="Type of crop (e.g., tomato, onion, potato)"
    )
    quantity_kg: float = Field(
        ...,
        gt=0,
        le=1000000,
        description="Quantity in kilograms"
    )
    harvest_date: date = Field(
        ...,
        description="Expected harvest date (YYYY-MM-DD)"
    )
    
    @field_validator('village_location')
    @classmethod
    def validate_village_location(cls, v):
        """Validate and normalize village location"""
        # Convert to lowercase for consistency
        v = v.strip().lower()
        if not v:
            raise ValueError("Village location cannot be empty")
        return v
    
    @field_validator('crop_type')
    @classmethod
    def validate_crop_type(cls, v):
        """Validate and normalize crop type"""
        # Convert to lowercase for consistency
        v = v.strip().lower()
        if not v:
            raise ValueError("Crop type cannot be empty")
        return v
    
    @field_validator('harvest_date')
    @classmethod
    def validate_harvest_date(cls, v):
        """Ensure harvest date is within reasonable future timeframe"""
        today = date.today()
        max_future_date = today + timedelta(days=30)
        
        if v < today:
            raise ValueError(f"Harvest date cannot be in the past. Today is {today}")
        
        if v > max_future_date:
            raise ValueError(f"Harvest date cannot be more than 30 days in the future. Maximum date: {max_future_date}")
        
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "village_location": "theni",
                "crop_type": "tomato",
                "quantity_kg": 1000,
                "harvest_date": "2024-02-28"
            }
        }


class MarketQueryRequest(BaseModel):
    """Request model for querying available markets"""
    location: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Location to find nearby markets"
    )
    max_distance_km: Optional[float] = Field(
        default=500,
        gt=0,
        le=1000,
        description="Maximum distance in kilometers"
    )
    
    @field_validator('location')
    @classmethod
    def validate_location(cls, v):
        """Validate and normalize location"""
        v = v.strip().lower()
        if not v:
            raise ValueError("Location cannot be empty")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "theni",
                "max_distance_km": 300
            }
        }


class CropQueryRequest(BaseModel):
    """Request model for querying crop information"""
    crop_type: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=50,
        description="Specific crop type to query (optional)"
    )
    
    @field_validator('crop_type')
    @classmethod
    def validate_crop_type(cls, v):
        """Validate and normalize crop type"""
        if v:
            v = v.strip().lower()
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_type": "tomato"
            }
        }
