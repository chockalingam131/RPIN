"""
Spoilage risk prediction service
Calculates spoilage risk based on crop characteristics, weather, and transport duration
"""
import logging
from datetime import date, timedelta

from app.data.loaders import data_loader
from app.data.weather import weather_client

logger = logging.getLogger(__name__)


class SpoilagePredictor:
    """Spoilage risk prediction service"""
    
    def calculate_spoilage_risk(
        self,
        crop_id: str,
        transport_days: int,
        market_location: str,
        harvest_date: date
    ) -> float:
        """
        Calculate spoilage risk percentage
        
        Args:
            crop_id: Crop identifier
            transport_days: Number of days for transport
            market_location: Market location for weather data
            harvest_date: Harvest date
        
        Returns:
            Spoilage risk percentage (0-100)
        """
        logger.info(
            f"Calculating spoilage risk for {crop_id}, "
            f"{transport_days} days transport to {market_location}"
        )
        
        try:
            # Get crop information
            crop = data_loader.get_crop(crop_id)
            if not crop:
                logger.warning(f"Crop {crop_id} not found, using default values")
                shelf_life_days = 7
                optimal_temp = 20
                humidity_tolerance = 70
            else:
                shelf_life_days = crop.shelf_life_days
                optimal_temp = crop.optimal_temperature
                humidity_tolerance = crop.humidity_tolerance
            
            # Base risk: ratio of transport time to shelf life
            base_risk = (transport_days / shelf_life_days) * 100
            
            # Get weather forecast for transport period
            try:
                weather_forecast = weather_client.fetch_forecast(
                    market_location,
                    days=min(transport_days, 7)
                )
                
                if weather_forecast:
                    # Calculate average temperature and humidity
                    avg_temp = sum(w.temperature_celsius for w in weather_forecast) / len(weather_forecast)
                    avg_humidity = sum(w.humidity_percent for w in weather_forecast) / len(weather_forecast)
                    
                    # Temperature risk factor
                    temp_diff = abs(avg_temp - optimal_temp)
                    if temp_diff > 10:
                        temp_risk_factor = 1.5  # 50% increase
                    elif temp_diff > 5:
                        temp_risk_factor = 1.2  # 20% increase
                    else:
                        temp_risk_factor = 1.0  # No increase
                    
                    # Humidity risk factor
                    humidity_diff = abs(avg_humidity - humidity_tolerance)
                    if humidity_diff > 20:
                        humidity_risk_factor = 1.3  # 30% increase
                    elif humidity_diff > 10:
                        humidity_risk_factor = 1.15  # 15% increase
                    else:
                        humidity_risk_factor = 1.0  # No increase
                    
                    # Apply weather factors
                    base_risk *= temp_risk_factor * humidity_risk_factor
                    
                    logger.info(
                        f"Weather factors - Temp: {avg_temp:.1f}°C (optimal: {optimal_temp}°C), "
                        f"Humidity: {avg_humidity:.1f}% (tolerance: {humidity_tolerance}%)"
                    )
                else:
                    logger.warning("No weather data available, using base risk only")
            
            except Exception as e:
                logger.warning(f"Error fetching weather data: {e}, using base risk only")
            
            # Handling quality factor
            # Crops with special handling requirements have higher risk
            if crop and len(crop.handling_requirements) > 2:
                base_risk *= 1.1  # 10% increase for delicate crops
            
            # Cap the risk at 100%
            final_risk = min(100.0, base_risk)
            
            logger.info(f"Calculated spoilage risk: {final_risk:.1f}%")
            
            return round(final_risk, 1)
        
        except Exception as e:
            logger.error(f"Error calculating spoilage risk: {e}")
            # Return conservative estimate
            return min(100.0, (transport_days / 7) * 100)
    
    def calculate_remaining_quantity(
        self,
        initial_quantity_kg: float,
        spoilage_risk_percent: float
    ) -> float:
        """
        Calculate remaining quantity after spoilage
        
        Args:
            initial_quantity_kg: Initial quantity in kg
            spoilage_risk_percent: Spoilage risk percentage
        
        Returns:
            Remaining quantity in kg
        """
        spoilage_factor = spoilage_risk_percent / 100
        remaining = initial_quantity_kg * (1 - spoilage_factor)
        return round(remaining, 2)
    
    def is_high_risk(self, spoilage_risk_percent: float) -> bool:
        """Check if spoilage risk is considered high (>20%)"""
        return spoilage_risk_percent > 20.0
    
    def get_risk_category(self, spoilage_risk_percent: float) -> str:
        """
        Categorize spoilage risk
        
        Returns:
            "Low", "Medium", or "High"
        """
        if spoilage_risk_percent < 10:
            return "Low"
        elif spoilage_risk_percent < 20:
            return "Medium"
        else:
            return "High"


# Global predictor instance
spoilage_predictor = SpoilagePredictor()
