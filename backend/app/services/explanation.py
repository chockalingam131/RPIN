"""
Explanation generation service
Generates natural language explanations for market recommendations
"""
import logging
from typing import List

from app.models.domain import MarketRecommendation
from app.core.config import settings

logger = logging.getLogger(__name__)


class ExplanationService:
    """Service for generating natural language explanations"""
    
    def generate_explanation(
        self,
        village_location: str,
        crop_type: str,
        quantity_kg: float,
        best_recommendation: MarketRecommendation,
        all_recommendations: List[MarketRecommendation]
    ) -> str:
        """
        Generate natural language explanation for the recommendation
        
        For MVP, uses template-based generation
        For production, can integrate with LLM API
        
        Args:
            village_location: Village name
            crop_type: Crop type
            quantity_kg: Quantity in kg
            best_recommendation: Best market recommendation
            all_recommendations: All market recommendations
        
        Returns:
            Natural language explanation
        """
        logger.info(f"Generating explanation for {crop_type} from {village_location}")
        
        try:
            # Format numbers for readability
            quantity_display = f"{quantity_kg:,.0f} kg"
            profit_display = f"₹{best_recommendation.net_profit:,.0f}"
            price_display = f"₹{best_recommendation.predicted_price:.2f}/kg"
            
            # Calculate days to sell
            from datetime import date
            days_to_sell = (best_recommendation.optimal_selling_day - date.today()).days
            
            # Build explanation parts
            parts = []
            
            # Main recommendation
            main_part = (
                f"For {quantity_display} of {crop_type} from {village_location.title()}, "
                f"selling in {best_recommendation.market_name}"
            )
            
            if days_to_sell > 0:
                main_part += f" after {days_to_sell} day{'s' if days_to_sell != 1 else ''}"
            else:
                main_part += " today"
            
            main_part += f" gives {profit_display} profit"
            
            parts.append(main_part)
            
            # Compare with other markets if available
            if len(all_recommendations) > 1:
                second_best = all_recommendations[1]
                profit_diff = best_recommendation.net_profit - second_best.net_profit
                
                if profit_diff > 1000:  # Significant difference
                    parts.append(
                        f"which is ₹{profit_diff:,.0f} more than {second_best.market_name}"
                    )
            
            # Key factors
            factors = []
            
            # Price factor
            if best_recommendation.demand_level.value == "High":
                factors.append("rising prices")
            elif best_recommendation.predicted_price > 25:  # Above average
                factors.append("good market price")
            
            # Spoilage factor
            if best_recommendation.spoilage_risk_percent < 10:
                factors.append("lower spoilage risk")
            elif best_recommendation.spoilage_risk_percent > 20:
                factors.append("manageable spoilage risk")
            
            # Distance factor
            if best_recommendation.distance_km < 100:
                factors.append("shorter distance")
            
            # Demand factor
            if best_recommendation.demand_level.value == "High":
                factors.append("high demand")
            
            if factors:
                parts.append(f"due to {', '.join(factors)}")
            
            # Combine all parts
            explanation = " ".join(parts) + "."
            
            # Add additional details
            details = []
            
            details.append(
                f"The predicted price is {price_display} with {best_recommendation.demand_level.value.lower()} demand."
            )
            
            if best_recommendation.spoilage_risk_percent > 15:
                details.append(
                    f"Note: Spoilage risk is {best_recommendation.spoilage_risk_percent:.1f}%, "
                    f"so plan transport carefully."
                )
            
            if best_recommendation.distance_km > 200:
                details.append(
                    f"The market is {best_recommendation.distance_km:.0f} km away, "
                    f"requiring careful logistics planning."
                )
            
            if details:
                explanation += " " + " ".join(details)
            
            logger.info("Generated explanation successfully")
            return explanation
        
        except Exception as e:
            logger.error(f"Error generating explanation: {e}")
            # Fallback to simple explanation
            return (
                f"Recommended market: {best_recommendation.market_name}. "
                f"Expected profit: ₹{best_recommendation.net_profit:,.0f}. "
                f"Price: ₹{best_recommendation.predicted_price:.2f}/kg."
            )
    
    def generate_explanation_with_llm(
        self,
        village_location: str,
        crop_type: str,
        quantity_kg: float,
        best_recommendation: MarketRecommendation,
        all_recommendations: List[MarketRecommendation]
    ) -> str:
        """
        Generate explanation using LLM API (OpenAI, etc.)
        
        This is a placeholder for LLM integration
        Requires LLM_API_KEY in environment
        """
        # Check if LLM API key is configured
        if not settings.LLM_API_KEY:
            logger.info("LLM API key not configured, using template-based explanation")
            return self.generate_explanation(
                village_location,
                crop_type,
                quantity_kg,
                best_recommendation,
                all_recommendations
            )
        
        try:
            # TODO: Implement LLM API integration
            # Example with OpenAI:
            # import openai
            # openai.api_key = settings.LLM_API_KEY
            # 
            # prompt = f"""
            # Generate a simple, farmer-friendly explanation for this market recommendation:
            # 
            # Village: {village_location}
            # Crop: {crop_type}
            # Quantity: {quantity_kg} kg
            # Recommended Market: {best_recommendation.market_name}
            # Expected Profit: ₹{best_recommendation.net_profit}
            # Price: ₹{best_recommendation.predicted_price}/kg
            # Demand: {best_recommendation.demand_level.value}
            # Spoilage Risk: {best_recommendation.spoilage_risk_percent}%
            # 
            # Keep it under 100 words, in simple English.
            # """
            # 
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": "user", "content": prompt}],
            #     max_tokens=150
            # )
            # 
            # return response.choices[0].message.content
            
            # For now, fall back to template-based
            logger.info("LLM integration not implemented, using template-based explanation")
            return self.generate_explanation(
                village_location,
                crop_type,
                quantity_kg,
                best_recommendation,
                all_recommendations
            )
        
        except Exception as e:
            logger.error(f"Error with LLM API: {e}")
            return self.generate_explanation(
                village_location,
                crop_type,
                quantity_kg,
                best_recommendation,
                all_recommendations
            )


# Global service instance
explanation_service = ExplanationService()
