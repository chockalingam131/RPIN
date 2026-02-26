"""
AGMARKNET API client for fetching mandi price data
Includes caching and fallback mechanisms
"""
import requests
from datetime import datetime, timedelta, date
from typing import List, Optional, Dict
import logging
import random

from app.core.config import settings
from app.core.exceptions import ExternalAPIError
from app.models.domain import PriceData

logger = logging.getLogger(__name__)


class AGMARKNETClient:
    """Client for AGMARKNET mandi price data"""
    
    def __init__(self):
        self.base_url = settings.AGMARKNET_API_URL
        self.cache: Dict[str, List[PriceData]] = {}
        self.cache_timestamp: Dict[str, datetime] = {}
        self.cache_ttl_hours = settings.CACHE_TTL_HOURS
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached data is still valid"""
        if cache_key not in self.cache_timestamp:
            return False
        
        age = datetime.now() - self.cache_timestamp[cache_key]
        return age.total_seconds() < (self.cache_ttl_hours * 3600)
    
    def _generate_mock_prices(
        self,
        crop_id: str,
        market_id: str,
        days: int = 30
    ) -> List[PriceData]:
        """
        Generate mock historical price data for development/demo
        This is used when AGMARKNET API is unavailable or for testing
        """
        logger.info(f"Generating mock price data for {crop_id} in {market_id}")
        
        # Base prices for different crops (INR per kg)
        base_prices = {
            "tomato": 25.0,
            "onion": 30.0,
            "potato": 20.0,
            "cabbage": 15.0,
            "carrot": 35.0,
            "cauliflower": 40.0
        }
        
        base_price = base_prices.get(crop_id, 25.0)
        prices = []
        
        start_date = date.today() - timedelta(days=days)
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Add some variation and trend
            trend = (i / days) * 5  # Slight upward trend
            variation = random.uniform(-5, 5)
            modal_price = base_price + trend + variation
            
            # Ensure min <= modal <= max
            min_price = modal_price - random.uniform(2, 5)
            max_price = modal_price + random.uniform(2, 5)
            
            # Ensure prices are positive
            min_price = max(min_price, 5.0)
            modal_price = max(modal_price, min_price + 1)
            max_price = max(max_price, modal_price + 1)
            
            arrivals = random.uniform(10, 100)  # tons
            
            price_data = PriceData(
                market_id=market_id,
                crop_id=crop_id,
                date=current_date,
                min_price=round(min_price, 2),
                max_price=round(max_price, 2),
                modal_price=round(modal_price, 2),
                arrivals_tons=round(arrivals, 2)
            )
            prices.append(price_data)
        
        return prices
    
    def fetch_historical_prices(
        self,
        crop_id: str,
        market_id: str,
        days: int = 30,
        use_cache: bool = True
    ) -> List[PriceData]:
        """
        Fetch historical price data from AGMARKNET
        
        Args:
            crop_id: Crop identifier
            market_id: Market identifier
            days: Number of days of historical data
            use_cache: Whether to use cached data
        
        Returns:
            List of PriceData objects
        """
        cache_key = f"{crop_id}_{market_id}_{days}"
        
        # Check cache first
        if use_cache and cache_key in self.cache and self._is_cache_valid(cache_key):
            logger.info(f"Using cached price data for {cache_key}")
            return self.cache[cache_key]
        
        try:
            # Try to fetch from AGMARKNET API
            # Note: For prototype, we'll use mock data
            # In production, implement actual API call here
            logger.info(f"Fetching price data from AGMARKNET for {crop_id} in {market_id}")
            
            # TODO: Implement actual API call when API key is available
            # response = requests.get(
            #     f"{self.base_url}/prices",
            #     params={
            #         "crop": crop_id,
            #         "market": market_id,
            #         "days": days
            #     },
            #     timeout=settings.REQUEST_TIMEOUT_SECONDS
            # )
            # response.raise_for_status()
            # data = response.json()
            
            # For now, use mock data
            prices = self._generate_mock_prices(crop_id, market_id, days)
            
            # Cache the results
            self.cache[cache_key] = prices
            self.cache_timestamp[cache_key] = datetime.now()
            
            return prices
        
        except requests.RequestException as e:
            logger.error(f"AGMARKNET API error: {e}")
            
            # Fallback to cached data if available
            if cache_key in self.cache:
                logger.warning(f"Using stale cached data for {cache_key}")
                return self.cache[cache_key]
            
            # Fallback to mock data
            logger.warning(f"Falling back to mock data for {cache_key}")
            prices = self._generate_mock_prices(crop_id, market_id, days)
            self.cache[cache_key] = prices
            self.cache_timestamp[cache_key] = datetime.now()
            return prices
        
        except Exception as e:
            logger.error(f"Unexpected error fetching price data: {e}")
            raise ExternalAPIError(
                f"Failed to fetch price data for {crop_id} in {market_id}",
                details={"error": str(e)}
            )
    
    def get_latest_price(
        self,
        crop_id: str,
        market_id: str
    ) -> Optional[PriceData]:
        """Get the most recent price data"""
        prices = self.fetch_historical_prices(crop_id, market_id, days=7)
        if prices:
            return prices[-1]  # Return most recent
        return None
    
    def get_average_price(
        self,
        crop_id: str,
        market_id: str,
        days: int = 7
    ) -> float:
        """Calculate average modal price over specified days"""
        prices = self.fetch_historical_prices(crop_id, market_id, days)
        if not prices:
            return 0.0
        
        avg_price = sum(p.modal_price for p in prices) / len(prices)
        return round(avg_price, 2)
    
    def clear_cache(self):
        """Clear all cached price data"""
        self.cache.clear()
        self.cache_timestamp.clear()
        logger.info("AGMARKNET cache cleared")


# Global client instance
agmarknet_client = AGMARKNETClient()
