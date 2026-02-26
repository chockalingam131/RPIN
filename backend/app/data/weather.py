"""
Weather API client for fetching weather forecasts
Supports OpenWeatherMap API with caching and fallback
"""
import requests
from datetime import datetime, timedelta, date
from typing import List, Optional, Dict
import logging
import random

from app.core.config import settings
from app.core.exceptions import ExternalAPIError
from app.models.domain import WeatherData

logger = logging.getLogger(__name__)


class WeatherClient:
    """Client for weather forecast data"""
    
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.cache: Dict[str, List[WeatherData]] = {}
        self.cache_timestamp: Dict[str, datetime] = {}
        self.cache_ttl_hours = 6  # Weather data refreshes every 6 hours
    
    def _is_cache_valid(self, cache_key: str) -> bool:
        """Check if cached weather data is still valid"""
        if cache_key not in self.cache_timestamp:
            return False
        
        age = datetime.now() - self.cache_timestamp[cache_key]
        return age.total_seconds() < (self.cache_ttl_hours * 3600)
    
    def _generate_mock_weather(
        self,
        location: str,
        days: int = 7
    ) -> List[WeatherData]:
        """
        Generate mock weather forecast data for development/demo
        This is used when OpenWeather API is unavailable or API key is not set
        """
        logger.info(f"Generating mock weather data for {location}")
        
        # Typical weather patterns for Tamil Nadu
        base_temp = 30.0  # Base temperature in Celsius
        base_humidity = 65.0  # Base humidity percentage
        
        weather_data = []
        start_date = date.today()
        
        for i in range(days):
            current_date = start_date + timedelta(days=i)
            
            # Add daily variation
            temp_variation = random.uniform(-3, 5)
            humidity_variation = random.uniform(-10, 15)
            
            temperature = base_temp + temp_variation
            humidity = max(30, min(95, base_humidity + humidity_variation))
            
            # Random chance of precipitation
            precipitation = random.uniform(0, 10) if random.random() < 0.3 else 0
            wind_speed = random.uniform(5, 20)
            
            weather = WeatherData(
                location=location,
                date=current_date,
                temperature_celsius=round(temperature, 1),
                humidity_percent=round(humidity, 1),
                precipitation_mm=round(precipitation, 1),
                wind_speed_kmh=round(wind_speed, 1)
            )
            weather_data.append(weather)
        
        return weather_data
    
    def _fetch_from_openweather(
        self,
        location: str,
        days: int = 7
    ) -> List[WeatherData]:
        """
        Fetch weather forecast from OpenWeatherMap API
        
        Args:
            location: Location name
            days: Number of days to forecast
        
        Returns:
            List of WeatherData objects
        """
        if not self.api_key:
            raise ExternalAPIError(
                "OpenWeather API key not configured",
                details={"location": location}
            )
        
        try:
            # First, get coordinates for the location
            geo_url = f"{self.base_url}/weather"
            geo_params = {
                "q": f"{location},IN",  # IN for India
                "appid": self.api_key
            }
            
            geo_response = requests.get(
                geo_url,
                params=geo_params,
                timeout=settings.REQUEST_TIMEOUT_SECONDS
            )
            geo_response.raise_for_status()
            geo_data = geo_response.json()
            
            lat = geo_data["coord"]["lat"]
            lon = geo_data["coord"]["lon"]
            
            # Fetch forecast data
            forecast_url = f"{self.base_url}/forecast"
            forecast_params = {
                "lat": lat,
                "lon": lon,
                "appid": self.api_key,
                "units": "metric",  # Celsius
                "cnt": days * 8  # 8 forecasts per day (3-hour intervals)
            }
            
            forecast_response = requests.get(
                forecast_url,
                params=forecast_params,
                timeout=settings.REQUEST_TIMEOUT_SECONDS
            )
            forecast_response.raise_for_status()
            forecast_data = forecast_response.json()
            
            # Process forecast data - aggregate by day
            daily_forecasts: Dict[date, List[dict]] = {}
            
            for item in forecast_data.get("list", []):
                forecast_date = datetime.fromtimestamp(item["dt"]).date()
                if forecast_date not in daily_forecasts:
                    daily_forecasts[forecast_date] = []
                daily_forecasts[forecast_date].append(item)
            
            # Create WeatherData objects
            weather_data = []
            for forecast_date, forecasts in sorted(daily_forecasts.items())[:days]:
                # Average the forecasts for the day
                avg_temp = sum(f["main"]["temp"] for f in forecasts) / len(forecasts)
                avg_humidity = sum(f["main"]["humidity"] for f in forecasts) / len(forecasts)
                total_precip = sum(f.get("rain", {}).get("3h", 0) for f in forecasts)
                avg_wind = sum(f["wind"]["speed"] * 3.6 for f in forecasts) / len(forecasts)  # Convert m/s to km/h
                
                weather = WeatherData(
                    location=location,
                    date=forecast_date,
                    temperature_celsius=round(avg_temp, 1),
                    humidity_percent=round(avg_humidity, 1),
                    precipitation_mm=round(total_precip, 1),
                    wind_speed_kmh=round(avg_wind, 1)
                )
                weather_data.append(weather)
            
            return weather_data
        
        except requests.RequestException as e:
            logger.error(f"OpenWeather API error: {e}")
            raise ExternalAPIError(
                f"Failed to fetch weather data from OpenWeather API",
                details={"location": location, "error": str(e)}
            )
    
    def fetch_forecast(
        self,
        location: str,
        days: int = 7,
        use_cache: bool = True
    ) -> List[WeatherData]:
        """
        Fetch weather forecast for location
        
        Args:
            location: Location name
            days: Number of days to forecast (max 7)
            use_cache: Whether to use cached data
        
        Returns:
            List of WeatherData objects
        """
        cache_key = f"{location.lower()}_{days}"
        
        # Check cache first
        if use_cache and cache_key in self.cache and self._is_cache_valid(cache_key):
            logger.info(f"Using cached weather data for {cache_key}")
            return self.cache[cache_key]
        
        try:
            # Try to fetch from OpenWeather API
            if self.api_key:
                logger.info(f"Fetching weather forecast from OpenWeather for {location}")
                weather_data = self._fetch_from_openweather(location, days)
            else:
                logger.warning("OpenWeather API key not set, using mock data")
                weather_data = self._generate_mock_weather(location, days)
            
            # Cache the results
            self.cache[cache_key] = weather_data
            self.cache_timestamp[cache_key] = datetime.now()
            
            return weather_data
        
        except ExternalAPIError:
            # Fallback to cached data if available
            if cache_key in self.cache:
                logger.warning(f"Using stale cached weather data for {cache_key}")
                return self.cache[cache_key]
            
            # Fallback to mock data
            logger.warning(f"Falling back to mock weather data for {cache_key}")
            weather_data = self._generate_mock_weather(location, days)
            self.cache[cache_key] = weather_data
            self.cache_timestamp[cache_key] = datetime.now()
            return weather_data
        
        except Exception as e:
            logger.error(f"Unexpected error fetching weather data: {e}")
            
            # Try mock data as last resort
            weather_data = self._generate_mock_weather(location, days)
            return weather_data
    
    def get_current_weather(self, location: str) -> Optional[WeatherData]:
        """Get current weather for location"""
        forecast = self.fetch_forecast(location, days=1)
        if forecast:
            return forecast[0]
        return None
    
    def get_average_temperature(
        self,
        location: str,
        days: int = 7
    ) -> float:
        """Calculate average temperature over forecast period"""
        forecast = self.fetch_forecast(location, days)
        if not forecast:
            return 30.0  # Default temperature
        
        avg_temp = sum(w.temperature_celsius for w in forecast) / len(forecast)
        return round(avg_temp, 1)
    
    def get_average_humidity(
        self,
        location: str,
        days: int = 7
    ) -> float:
        """Calculate average humidity over forecast period"""
        forecast = self.fetch_forecast(location, days)
        if not forecast:
            return 65.0  # Default humidity
        
        avg_humidity = sum(w.humidity_percent for w in forecast) / len(forecast)
        return round(avg_humidity, 1)
    
    def clear_cache(self):
        """Clear all cached weather data"""
        self.cache.clear()
        self.cache_timestamp.clear()
        logger.info("Weather cache cleared")


# Global client instance
weather_client = WeatherClient()
