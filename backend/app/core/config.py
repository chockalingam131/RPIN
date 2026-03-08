"""
Configuration management for RPIN application
"""
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    """Application settings"""
    
    # Project metadata
    PROJECT_NAME: str = "RPIN - Rural Producer Intelligence Network"
    VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"
    
    # CORS settings
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:5173",
        "https://*.vercel.app",
        "*"  # Allow all for demo (remove in production)
    ]
    
    # Database settings
    DATABASE_URL: str = "sqlite:///./rpin.db"
    
    # External API keys
    OPENWEATHER_API_KEY: str = ""
    LLM_API_KEY: str = ""
    AGMARKNET_API_URL: str = "https://api.data.gov.in/resource"
    
    # ML Model settings
    MODEL_CACHE_DIR: str = "./models"
    ENABLE_MODEL_CACHING: bool = True
    
    # Data directories
    DATA_DIR: str = "./data"
    CROPS_DATA_FILE: str = "./data/crops.json"
    MARKETS_DATA_FILE: str = "./data/markets.json"
    DISTANCES_DATA_FILE: str = "./data/distances.json"
    
    # Prediction settings
    FORECAST_DAYS: int = 7
    MIN_MARKETS_TO_ANALYZE: int = 3
    MAX_TRANSPORT_DISTANCE_KM: int = 500
    
    # Transport cost settings (INR per km per quintal)
    TRANSPORT_COST_PER_KM_MIN: float = 3.0
    TRANSPORT_COST_PER_KM_MAX: float = 5.0
    
    # Performance settings
    REQUEST_TIMEOUT_SECONDS: int = 30
    CACHE_TTL_HOURS: int = 24
    MAX_RESPONSE_TIME_SECONDS: int = 10
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
