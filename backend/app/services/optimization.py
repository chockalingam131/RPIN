"""
Optimization service for transport cost calculation and profit maximization
"""
import logging
from typing import List, Optional
from datetime import date

from app.core.config import settings
from app.data.loaders import data_loader
from app.models.domain import MarketRecommendation, DemandLevel
from app.ml.price_predictor import price_predictor
from app.ml.demand_classifier import demand_classifier
from app.ml.spoilage_predictor import spoilage_predictor

logger = logging.getLogger(__name__)


class OptimizationService:
    """Service for transport cost calculation and profit optimization"""
    
    def __init__(self):
        self.transport_cost_per_km_min = settings.TRANSPORT_COST_PER_KM_MIN
        self.transport_cost_per_km_max = settings.TRANSPORT_COST_PER_KM_MAX
        self.max_distance_km = settings.MAX_TRANSPORT_DISTANCE_KM
    
    def calculate_transport_cost(
        self,
        distance_km: float,
        quantity_kg: float
    ) -> float:
        """
        Calculate transport cost based on distance and quantity
        
        Args:
            distance_km: Distance in kilometers
            quantity_kg: Quantity in kilograms
        
        Returns:
            Transport cost in INR
        """
        # Convert kg to quintals (1 quintal = 100 kg)
        quantity_quintals = quantity_kg / 100
        
        # Base rate per km per quintal
        # Use lower rate for longer distances (economies of scale)
        if distance_km > 200:
            rate_per_km = self.transport_cost_per_km_min
        elif distance_km > 100:
            rate_per_km = (self.transport_cost_per_km_min + self.transport_cost_per_km_max) / 2
        else:
            rate_per_km = self.transport_cost_per_km_max
        
        # Calculate cost
        cost = distance_km * quantity_quintals * rate_per_km
        
        # Add fixed costs (loading/unloading)
        fixed_cost = 500  # INR
        
        total_cost = cost + fixed_cost
        
        logger.debug(
            f"Transport cost: {distance_km}km × {quantity_quintals:.2f}quintals "
            f"× ₹{rate_per_km}/km = ₹{total_cost:.2f}"
        )
        
        return round(total_cost, 2)
    
    def calculate_net_profit(
        self,
        predicted_price: float,
        quantity_kg: float,
        spoilage_risk_percent: float,
        transport_cost: float
    ) -> float:
        """
        Calculate net profit considering spoilage and transport cost
        
        Formula: Net_Profit = (Predicted_Price × Remaining_Quantity) - Transport_Cost
        
        Args:
            predicted_price: Predicted price per kg
            quantity_kg: Initial quantity in kg
            spoilage_risk_percent: Spoilage risk percentage
            transport_cost: Transport cost in INR
        
        Returns:
            Net profit in INR
        """
        # Calculate remaining quantity after spoilage
        remaining_quantity = spoilage_predictor.calculate_remaining_quantity(
            quantity_kg,
            spoilage_risk_percent
        )
        
        # Calculate revenue
        revenue = predicted_price * remaining_quantity
        
        # Calculate net profit
        net_profit = revenue - transport_cost
        
        logger.debug(
            f"Net profit: ₹{predicted_price}/kg × {remaining_quantity}kg - ₹{transport_cost} "
            f"= ₹{net_profit:.2f}"
        )
        
        return round(net_profit, 2)
    
    def optimize_markets(
        self,
        village_id: str,
        crop_id: str,
        quantity_kg: float,
        harvest_date: date
    ) -> List[MarketRecommendation]:
        """
        Optimize market selection for maximum profit
        
        Args:
            village_id: Village identifier
            crop_id: Crop identifier
            quantity_kg: Quantity in kg
            harvest_date: Harvest date
        
        Returns:
            List of MarketRecommendation sorted by net profit (descending)
        """
        logger.info(
            f"Optimizing markets for {quantity_kg}kg {crop_id} from {village_id}"
        )
        
        # Get nearby markets
        nearby_markets = data_loader.get_nearby_markets(
            village_id,
            max_distance_km=self.max_distance_km
        )
        
        if not nearby_markets:
            logger.warning(f"No markets found near {village_id}")
            return []
        
        recommendations = []
        
        for market_id, distance_km in nearby_markets:
            try:
                # Get market information
                market = data_loader.get_market(market_id)
                if not market:
                    continue
                
                # Calculate transport days (assume 100km per day)
                transport_days = max(1, int(distance_km / 100))
                
                # Calculate optimal selling day (harvest date + transport days)
                optimal_selling_day = harvest_date
                
                # Predict price for optimal selling day
                price_predictions = price_predictor.predict_prices(
                    crop_id,
                    market_id,
                    harvest_date,
                    days=settings.FORECAST_DAYS
                )
                
                if not price_predictions:
                    continue
                
                # Find best day within forecast period
                best_day_idx = 0
                best_profit = float('-inf')
                
                for idx, (pred_date, pred_price, confidence) in enumerate(price_predictions):
                    # Calculate days from harvest
                    days_from_harvest = (pred_date - harvest_date).days
                    
                    # Calculate spoilage risk for this scenario
                    spoilage_risk = spoilage_predictor.calculate_spoilage_risk(
                        crop_id,
                        days_from_harvest,
                        market.location,
                        harvest_date
                    )
                    
                    # Calculate transport cost
                    transport_cost = self.calculate_transport_cost(
                        distance_km,
                        quantity_kg
                    )
                    
                    # Calculate net profit
                    net_profit = self.calculate_net_profit(
                        pred_price,
                        quantity_kg,
                        spoilage_risk,
                        transport_cost
                    )
                    
                    # Track best day
                    if net_profit > best_profit:
                        best_profit = net_profit
                        best_day_idx = idx
                
                # Use best day's data
                optimal_date, predicted_price, price_confidence = price_predictions[best_day_idx]
                days_to_sell = (optimal_date - harvest_date).days
                
                # Calculate final metrics for best day
                spoilage_risk = spoilage_predictor.calculate_spoilage_risk(
                    crop_id,
                    days_to_sell,
                    market.location,
                    harvest_date
                )
                
                transport_cost = self.calculate_transport_cost(
                    distance_km,
                    quantity_kg
                )
                
                net_profit = self.calculate_net_profit(
                    predicted_price,
                    quantity_kg,
                    spoilage_risk,
                    transport_cost
                )
                
                # Classify demand
                all_prices = [p for _, p, _ in price_predictions]
                demand_level, demand_confidence = demand_classifier.classify_demand(
                    crop_id,
                    market_id,
                    all_prices
                )
                
                # Create recommendation
                recommendation = MarketRecommendation(
                    market_id=market_id,
                    market_name=market.name,
                    predicted_price=predicted_price,
                    demand_level=demand_level,
                    spoilage_risk_percent=spoilage_risk,
                    transport_cost=transport_cost,
                    net_profit=net_profit,
                    confidence_score=round((price_confidence + demand_confidence) / 2, 2),
                    optimal_selling_day=optimal_date,
                    distance_km=distance_km
                )
                
                recommendations.append(recommendation)
                
                logger.debug(
                    f"Market {market.name}: ₹{predicted_price}/kg, "
                    f"profit: ₹{net_profit:.2f}, demand: {demand_level.value}"
                )
            
            except Exception as e:
                logger.error(f"Error optimizing market {market_id}: {e}")
                continue
        
        # Sort by net profit (descending)
        recommendations.sort(key=lambda x: x.net_profit, reverse=True)
        
        logger.info(
            f"Generated {len(recommendations)} market recommendations, "
            f"best profit: ₹{recommendations[0].net_profit:.2f}" if recommendations else "no recommendations"
        )
        
        return recommendations
    
    def get_best_market(
        self,
        recommendations: List[MarketRecommendation]
    ) -> Optional[MarketRecommendation]:
        """Get the best market recommendation (highest profit)"""
        if not recommendations:
            return None
        return recommendations[0]


# Global service instance
optimization_service = OptimizationService()
