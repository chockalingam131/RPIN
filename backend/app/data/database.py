"""
Database setup and operations for RPIN
Simplified version for serverless deployment (no SQLAlchemy)
"""
import json
import logging
from datetime import datetime, date
from pathlib import Path
from typing import List, Optional, Dict

from app.core.config import settings

logger = logging.getLogger(__name__)

# In-memory storage for serverless environment
_historical_prices: List[Dict] = []
_weather_cache: List[Dict] = []
_prediction_logs: List[Dict] = []


def init_database():
    """Initialize database (no-op for serverless)"""
    logger.info("Database initialized (in-memory mode for serverless)")
    return True


def get_db():
    """Get database session (no-op for serverless)"""
    yield None


def add_historical_price(
    db,
    market_id: str,
    crop_id: str,
    price_date: date,
    min_price: float,
    max_price: float,
    modal_price: float,
    arrivals_tons: float = None
):
    """Add historical price record"""
    record = {
        "id": len(_historical_prices) + 1,
        "market_id": market_id,
        "crop_id": crop_id,
        "date": price_date.isoformat() if isinstance(price_date, date) else price_date,
        "min_price": min_price,
        "max_price": max_price,
        "modal_price": modal_price,
        "arrivals_tons": arrivals_tons,
        "created_at": datetime.now().isoformat()
    }
    _historical_prices.append(record)
    logger.debug(f"Added historical price record: {record}")
    return record


def add_weather_cache(
    db,
    location: str,
    weather_date: date,
    temperature_celsius: float,
    humidity_percent: float,
    precipitation_mm: float = 0,
    wind_speed_kmh: float = 0
):
    """Add weather cache record"""
    record = {
        "id": len(_weather_cache) + 1,
        "location": location,
        "date": weather_date.isoformat() if isinstance(weather_date, date) else weather_date,
        "temperature_celsius": temperature_celsius,
        "humidity_percent": humidity_percent,
        "precipitation_mm": precipitation_mm,
        "wind_speed_kmh": wind_speed_kmh,
        "fetched_at": datetime.now().isoformat()
    }
    _weather_cache.append(record)
    logger.debug(f"Added weather cache record: {record}")
    return record


def log_prediction(
    db,
    request_id: str,
    village_location: str,
    crop_type: str,
    quantity_kg: float,
    harvest_date: date,
    best_market_id: str,
    best_market_profit: float,
    total_markets_analyzed: int,
    response_time_ms: float = None
):
    """Log prediction request"""
    record = {
        "id": len(_prediction_logs) + 1,
        "request_id": request_id,
        "village_location": village_location,
        "crop_type": crop_type,
        "quantity_kg": quantity_kg,
        "harvest_date": harvest_date.isoformat() if isinstance(harvest_date, date) else harvest_date,
        "best_market_id": best_market_id,
        "best_market_profit": best_market_profit,
        "total_markets_analyzed": total_markets_analyzed,
        "response_time_ms": response_time_ms,
        "created_at": datetime.now().isoformat()
    }
    _prediction_logs.append(record)
    logger.info(f"Logged prediction: {request_id}")
    return record


def get_historical_prices(market_id: str = None, crop_id: str = None, limit: int = 100) -> List[Dict]:
    """Get historical prices with optional filtering"""
    filtered = _historical_prices
    
    if market_id:
        filtered = [p for p in filtered if p.get("market_id") == market_id]
    
    if crop_id:
        filtered = [p for p in filtered if p.get("crop_id") == crop_id]
    
    return filtered[-limit:] if limit else filtered


def get_weather_cache(location: str = None, limit: int = 100) -> List[Dict]:
    """Get weather cache with optional filtering"""
    filtered = _weather_cache
    
    if location:
        filtered = [w for w in filtered if w.get("location") == location]
    
    return filtered[-limit:] if limit else filtered


def get_prediction_logs(limit: int = 100) -> List[Dict]:
    """Get prediction logs"""
    return _prediction_logs[-limit:] if limit else _prediction_logs

