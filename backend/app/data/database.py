"""
Database setup and operations for RPIN
Using SQLite for simplicity in prototype
"""
from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Create SQLAlchemy engine
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


class HistoricalPrice(Base):
    """Historical price data table"""
    __tablename__ = "historical_prices"
    
    id = Column(Integer, primary_key=True, index=True)
    market_id = Column(String, index=True, nullable=False)
    crop_id = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    min_price = Column(Float, nullable=False)
    max_price = Column(Float, nullable=False)
    modal_price = Column(Float, nullable=False)
    arrivals_tons = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


class WeatherCache(Base):
    """Weather forecast cache table"""
    __tablename__ = "weather_cache"
    
    id = Column(Integer, primary_key=True, index=True)
    location = Column(String, index=True, nullable=False)
    date = Column(Date, index=True, nullable=False)
    temperature_celsius = Column(Float, nullable=False)
    humidity_percent = Column(Float, nullable=False)
    precipitation_mm = Column(Float, default=0)
    wind_speed_kmh = Column(Float, default=0)
    fetched_at = Column(DateTime, default=datetime.now)


class UserSession(Base):
    """User session tracking for analytics"""
    __tablename__ = "user_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, unique=True, index=True, nullable=False)
    village_location = Column(String, nullable=False)
    crop_type = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    harvest_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.now)


class PredictionLog(Base):
    """Prediction request and response logging"""
    __tablename__ = "prediction_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    request_id = Column(String, unique=True, index=True, nullable=False)
    village_location = Column(String, nullable=False)
    crop_type = Column(String, nullable=False)
    quantity_kg = Column(Float, nullable=False)
    harvest_date = Column(Date, nullable=False)
    best_market_id = Column(String, nullable=False)
    best_market_profit = Column(Float, nullable=False)
    total_markets_analyzed = Column(Integer, nullable=False)
    response_time_ms = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.now)


def init_database():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def get_db() -> Session:
    """
    Get database session
    Use as dependency in FastAPI endpoints
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def add_historical_price(
    db: Session,
    market_id: str,
    crop_id: str,
    date: datetime.date,
    min_price: float,
    max_price: float,
    modal_price: float,
    arrivals_tons: float = None
):
    """Add historical price record"""
    price_record = HistoricalPrice(
        market_id=market_id,
        crop_id=crop_id,
        date=date,
        min_price=min_price,
        max_price=max_price,
        modal_price=modal_price,
        arrivals_tons=arrivals_tons
    )
    db.add(price_record)
    db.commit()
    db.refresh(price_record)
    return price_record


def add_weather_cache(
    db: Session,
    location: str,
    date: datetime.date,
    temperature_celsius: float,
    humidity_percent: float,
    precipitation_mm: float = 0,
    wind_speed_kmh: float = 0
):
    """Add weather cache record"""
    weather_record = WeatherCache(
        location=location,
        date=date,
        temperature_celsius=temperature_celsius,
        humidity_percent=humidity_percent,
        precipitation_mm=precipitation_mm,
        wind_speed_kmh=wind_speed_kmh
    )
    db.add(weather_record)
    db.commit()
    db.refresh(weather_record)
    return weather_record


def log_prediction(
    db: Session,
    request_id: str,
    village_location: str,
    crop_type: str,
    quantity_kg: float,
    harvest_date: datetime.date,
    best_market_id: str,
    best_market_profit: float,
    total_markets_analyzed: int,
    response_time_ms: float = None
):
    """Log prediction request"""
    log_record = PredictionLog(
        request_id=request_id,
        village_location=village_location,
        crop_type=crop_type,
        quantity_kg=quantity_kg,
        harvest_date=harvest_date,
        best_market_id=best_market_id,
        best_market_profit=best_market_profit,
        total_markets_analyzed=total_markets_analyzed,
        response_time_ms=response_time_ms
    )
    db.add(log_record)
    db.commit()
    db.refresh(log_record)
    return log_record
