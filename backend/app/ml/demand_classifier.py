"""
Demand classification service
Classifies demand as Low/Medium/High based on price trends and market factors
"""
import logging
from typing import List
from datetime import date

from app.models.domain import DemandLevel
from app.data.agmarknet import agmarknet_client

logger = logging.getLogger(__name__)


class DemandClassifier:
    """Demand level classification service"""
    
    def classify_demand(
        self,
        crop_id: str,
        market_id: str,
        predicted_prices: List[float]
    ) -> tuple[DemandLevel, float]:
        """
        Classify demand level based on price trends
        
        Args:
            crop_id: Crop identifier
            market_id: Market identifier
            predicted_prices: List of predicted prices
        
        Returns:
            Tuple of (DemandLevel, confidence_score)
        """
        logger.info(f"Classifying demand for {crop_id} in {market_id}")
        
        try:
            # Get historical prices for comparison
            historical_data = agmarknet_client.fetch_historical_prices(
                crop_id, market_id, days=14
            )
            
            if not historical_data or not predicted_prices:
                logger.warning("Insufficient data for demand classification")
                return (DemandLevel.MEDIUM, 0.5)
            
            # Calculate historical average
            historical_prices = [p.modal_price for p in historical_data]
            historical_avg = sum(historical_prices) / len(historical_prices)
            
            # Calculate predicted average
            predicted_avg = sum(predicted_prices) / len(predicted_prices)
            
            # Calculate price change percentage
            price_change_pct = ((predicted_avg - historical_avg) / historical_avg) * 100
            
            # Calculate price trend (slope)
            if len(predicted_prices) >= 2:
                price_trend = predicted_prices[-1] - predicted_prices[0]
                trend_pct = (price_trend / predicted_prices[0]) * 100
            else:
                trend_pct = 0
            
            # Calculate price volatility
            if len(historical_prices) >= 2:
                price_std = self._calculate_std(historical_prices)
                volatility = (price_std / historical_avg) * 100
            else:
                volatility = 0
            
            # Classification logic
            confidence = 0.7  # Base confidence
            
            # High demand indicators:
            # - Rising prices (>5% increase)
            # - Positive trend
            # - Low volatility (stable market)
            if price_change_pct > 5 and trend_pct > 3:
                demand_level = DemandLevel.HIGH
                confidence = min(0.9, 0.7 + (price_change_pct / 100))
            
            # Low demand indicators:
            # - Falling prices (>5% decrease)
            # - Negative trend
            # - High volatility (unstable market)
            elif price_change_pct < -5 and trend_pct < -3:
                demand_level = DemandLevel.LOW
                confidence = min(0.9, 0.7 + (abs(price_change_pct) / 100))
            
            # Medium demand (default):
            # - Stable prices
            # - Mixed signals
            else:
                demand_level = DemandLevel.MEDIUM
                confidence = 0.6
            
            # Adjust confidence based on volatility
            if volatility > 20:
                confidence *= 0.8  # Reduce confidence in volatile markets
            
            logger.info(
                f"Demand classified as {demand_level.value} "
                f"(confidence: {confidence:.2f}, price change: {price_change_pct:.1f}%)"
            )
            
            return (demand_level, round(confidence, 2))
        
        except Exception as e:
            logger.error(f"Error classifying demand: {e}")
            return (DemandLevel.MEDIUM, 0.5)
    
    def _calculate_std(self, values: List[float]) -> float:
        """Calculate standard deviation"""
        if len(values) < 2:
            return 0.0
        
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / len(values)
        return variance ** 0.5
    
    def classify_demand_simple(
        self,
        current_price: float,
        historical_avg: float
    ) -> DemandLevel:
        """
        Simple demand classification based on price comparison
        
        Args:
            current_price: Current/predicted price
            historical_avg: Historical average price
        
        Returns:
            DemandLevel
        """
        price_ratio = current_price / historical_avg if historical_avg > 0 else 1.0
        
        if price_ratio > 1.1:  # 10% above average
            return DemandLevel.HIGH
        elif price_ratio < 0.9:  # 10% below average
            return DemandLevel.LOW
        else:
            return DemandLevel.MEDIUM


# Global classifier instance
demand_classifier = DemandClassifier()
