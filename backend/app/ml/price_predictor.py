"""
Price prediction service using simplified model for MVP
For production, replace with trained XGBoost model
"""
import random
from datetime import date, timedelta
from typing import List, Tuple
import logging

from app.data.agmarknet import agmarknet_client
from app.core.config import settings

logger = logging.getLogger(__name__)


class PricePredictor:
    """Price prediction service"""
    
    def __init__(self):
        self.forecast_days = settings.FORECAST_DAYS
    
    def _calculate_trend(self, historical_prices: List[float]) -> float:
        """Calculate price trend from historical data"""
        if len(historical_prices) < 2:
            return 0.0
        
        # Simple linear trend
        n = len(historical_prices)
        x_mean = (n - 1) / 2
        y_mean = sum(historical_prices) / n
        
        numerator = sum((i - x_mean) * (price - y_mean) 
                       for i, price in enumerate(historical_prices))
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return 0.0
        
        trend = numerator / denominator
        return trend
    
    def _calculate_seasonality(self, current_date: date) -> float:
        """Calculate seasonal adjustment factor"""
        # Simple seasonality based on month
        month = current_date.month
        
        # Higher prices in summer months (March-June) for vegetables
        if 3 <= month <= 6:
            return 1.1  # 10% increase
        # Lower prices in harvest season (October-December)
        elif 10 <= month <= 12:
            return 0.9  # 10% decrease
        else:
            return 1.0  # No adjustment
    
    def predict_prices(
        self,
        crop_id: str,
        market_id: str,
        start_date: date,
        days: int = None
    ) -> List[Tuple[date, float, float]]:
        """
        Predict prices for the next N days
        
        Args:
            crop_id: Crop identifier
            market_id: Market identifier
            start_date: Starting date for predictions
            days: Number of days to predict (default: FORECAST_DAYS)
        
        Returns:
            List of tuples (date, predicted_price, confidence)
        """
        if days is None:
            days = self.forecast_days
        
        logger.info(f"Predicting prices for {crop_id} in {market_id} for {days} days")
        
        try:
            # Fetch historical prices
            historical_data = agmarknet_client.fetch_historical_prices(
                crop_id, market_id, days=30
            )
            
            if not historical_data:
                logger.warning(f"No historical data for {crop_id} in {market_id}")
                # Use default base prices
                base_price = 25.0
                confidence = 0.5
            else:
                # Get recent prices
                recent_prices = [p.modal_price for p in historical_data[-7:]]
                base_price = recent_prices[-1]
                
                # Calculate trend
                trend = self._calculate_trend(recent_prices)
                
                # Higher confidence with more data
                confidence = min(0.95, 0.6 + (len(historical_data) / 100))
            
            # Generate predictions
            predictions = []
            current_price = base_price
            
            for i in range(days):
                prediction_date = start_date + timedelta(days=i)
                
                # Apply trend
                if 'trend' in locals():
                    current_price += trend
                
                # Apply seasonality
                seasonal_factor = self._calculate_seasonality(prediction_date)
                adjusted_price = current_price * seasonal_factor
                
                # Add some random variation (market volatility)
                variation = random.uniform(-0.05, 0.05)  # ±5%
                final_price = adjusted_price * (1 + variation)
                
                # Ensure price is positive and reasonable
                final_price = max(5.0, min(final_price, base_price * 2))
                
                # Confidence decreases with forecast horizon
                day_confidence = confidence * (1 - (i * 0.05))  # Decrease 5% per day
                day_confidence = max(0.3, day_confidence)
                
                predictions.append((
                    prediction_date,
                    round(final_price, 2),
                    round(day_confidence, 2)
                ))
                
                current_price = final_price
            
            logger.info(f"Generated {len(predictions)} price predictions")
            return predictions
        
        except Exception as e:
            logger.error(f"Error predicting prices: {e}")
            # Fallback to simple predictions
            predictions = []
            base_price = 25.0
            for i in range(days):
                prediction_date = start_date + timedelta(days=i)
                price = base_price + random.uniform(-3, 5)
                predictions.append((prediction_date, round(price, 2), 0.5))
            return predictions
    
    def get_price_for_date(
        self,
        crop_id: str,
        market_id: str,
        target_date: date
    ) -> Tuple[float, float]:
        """
        Get predicted price for a specific date
        
        Returns:
            Tuple of (price, confidence)
        """
        start_date = date.today()
        days_ahead = (target_date - start_date).days
        
        if days_ahead < 0:
            logger.warning(f"Target date {target_date} is in the past")
            return (0.0, 0.0)
        
        if days_ahead > self.forecast_days:
            logger.warning(f"Target date {target_date} is beyond forecast horizon")
            days_ahead = self.forecast_days
        
        predictions = self.predict_prices(crop_id, market_id, start_date, days_ahead + 1)
        
        if predictions and days_ahead < len(predictions):
            _, price, confidence = predictions[days_ahead]
            return (price, confidence)
        
        return (0.0, 0.0)
    
    def get_average_predicted_price(
        self,
        crop_id: str,
        market_id: str,
        start_date: date,
        days: int = 7
    ) -> float:
        """Calculate average predicted price over a period"""
        predictions = self.predict_prices(crop_id, market_id, start_date, days)
        if not predictions:
            return 0.0
        
        avg_price = sum(price for _, price, _ in predictions) / len(predictions)
        return round(avg_price, 2)


# Global predictor instance
price_predictor = PricePredictor()
