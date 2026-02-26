"""
Domain models for RPIN application
These represent core business entities
"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Tuple, Optional
from datetime import date, datetime
from enum import Enum


class DemandLevel(str, Enum):
    """Demand level classification"""
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"


class Market(BaseModel):
    """Market information model"""
    market_id: str = Field(..., description="Unique market identifier")
    name: str = Field(..., description="Market name")
    location: str = Field(..., description="Market location/city")
    coordinates: Tuple[float, float] = Field(..., description="Latitude and longitude")
    operating_days: List[str] = Field(..., description="Days when market operates")
    capacity_tons: float = Field(..., gt=0, description="Market capacity in tons")
    
    @field_validator('coordinates')
    @classmethod
    def validate_coordinates(cls, v):
        """Validate latitude and longitude"""
        lat, lon = v
        if not (-90 <= lat <= 90):
            raise ValueError(f"Invalid latitude: {lat}")
        if not (-180 <= lon <= 180):
            raise ValueError(f"Invalid longitude: {lon}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "market_id": "madurai",
                "name": "Madurai Mandi",
                "location": "Madurai",
                "coordinates": [9.9252, 78.1198],
                "operating_days": ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday"],
                "capacity_tons": 500
            }
        }


class CropInfo(BaseModel):
    """Crop information model"""
    crop_id: str = Field(..., description="Unique crop identifier")
    name: str = Field(..., description="Crop name")
    shelf_life_days: int = Field(..., gt=0, description="Shelf life in days")
    optimal_temperature: float = Field(..., description="Optimal storage temperature in Celsius")
    humidity_tolerance: float = Field(..., ge=0, le=100, description="Humidity tolerance percentage")
    handling_requirements: List[str] = Field(default_factory=list, description="Special handling requirements")
    
    class Config:
        json_schema_extra = {
            "example": {
                "crop_id": "tomato",
                "name": "Tomato",
                "shelf_life_days": 7,
                "optimal_temperature": 15,
                "humidity_tolerance": 85,
                "handling_requirements": ["gentle_handling", "avoid_direct_sunlight"]
            }
        }


class PriceData(BaseModel):
    """Historical price data model"""
    market_id: str = Field(..., description="Market identifier")
    crop_id: str = Field(..., description="Crop identifier")
    date: date = Field(..., description="Price date")
    min_price: float = Field(..., ge=0, description="Minimum price in INR per kg")
    max_price: float = Field(..., ge=0, description="Maximum price in INR per kg")
    modal_price: float = Field(..., ge=0, description="Modal/average price in INR per kg")
    arrivals_tons: Optional[float] = Field(None, ge=0, description="Quantity arrived in tons")
    
    @field_validator('modal_price')
    @classmethod
    def validate_modal_price(cls, v, info):
        """Ensure modal price is between min and max"""
        values = info.data
        if 'min_price' in values and 'max_price' in values:
            if not (values['min_price'] <= v <= values['max_price']):
                raise ValueError(f"Modal price {v} must be between min {values['min_price']} and max {values['max_price']}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "market_id": "madurai",
                "crop_id": "tomato",
                "date": "2024-02-25",
                "min_price": 20.0,
                "max_price": 30.0,
                "modal_price": 25.0,
                "arrivals_tons": 50.5
            }
        }


class WeatherData(BaseModel):
    """Weather forecast data model"""
    location: str = Field(..., description="Location name")
    date: date = Field(..., description="Forecast date")
    temperature_celsius: float = Field(..., description="Temperature in Celsius")
    humidity_percent: float = Field(..., ge=0, le=100, description="Humidity percentage")
    precipitation_mm: float = Field(default=0, ge=0, description="Precipitation in mm")
    wind_speed_kmh: float = Field(default=0, ge=0, description="Wind speed in km/h")
    
    class Config:
        json_schema_extra = {
            "example": {
                "location": "Madurai",
                "date": "2024-02-25",
                "temperature_celsius": 32.5,
                "humidity_percent": 65.0,
                "precipitation_mm": 0.0,
                "wind_speed_kmh": 12.5
            }
        }


class VillageDistance(BaseModel):
    """Village to market distance information"""
    village_id: str = Field(..., description="Village identifier")
    name: str = Field(..., description="Village name")
    coordinates: Tuple[float, float] = Field(..., description="Latitude and longitude")
    markets: dict[str, float] = Field(..., description="Distance to each market in km")
    
    @field_validator('markets')
    @classmethod
    def validate_distances(cls, v):
        """Ensure all distances are positive"""
        for market_id, distance in v.items():
            if distance < 0:
                raise ValueError(f"Distance to {market_id} cannot be negative: {distance}")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "village_id": "theni",
                "name": "Theni",
                "coordinates": [10.0104, 77.4768],
                "markets": {
                    "madurai": 80,
                    "chennai": 520,
                    "coimbatore": 180
                }
            }
        }


class MarketRecommendation(BaseModel):
    """Market recommendation with all calculated metrics"""
    market_id: str = Field(..., description="Market identifier")
    market_name: str = Field(..., description="Market name")
    predicted_price: float = Field(..., ge=0, description="Predicted price in INR per kg")
    demand_level: DemandLevel = Field(..., description="Demand level classification")
    spoilage_risk_percent: float = Field(..., ge=0, le=100, description="Spoilage risk percentage")
    transport_cost: float = Field(..., ge=0, description="Transport cost in INR")
    net_profit: float = Field(..., description="Expected net profit in INR")
    confidence_score: float = Field(..., ge=0, le=1, description="Prediction confidence score")
    optimal_selling_day: date = Field(..., description="Recommended selling date")
    distance_km: float = Field(..., ge=0, description="Distance from village in km")
    
    class Config:
        json_schema_extra = {
            "example": {
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
        }
