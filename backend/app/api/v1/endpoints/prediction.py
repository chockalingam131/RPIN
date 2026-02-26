"""
Prediction API endpoints
Main endpoint for market recommendations
"""
from fastapi import APIRouter, HTTPException, status
from datetime import datetime
import logging
import uuid

from app.models.request import PredictionRequest
from app.models.response import PredictionResponse, ErrorResponse
from app.services.optimization import optimization_service
from app.services.explanation import explanation_service
from app.data.loaders import data_loader
from app.core.exceptions import RPINException

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post(
    "/predict",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Get market recommendations",
    description="Predict best markets for selling crops with profit optimization"
)
async def predict_market(request: PredictionRequest):
    """
    Main prediction endpoint
    
    Analyzes multiple markets and returns recommendations sorted by expected profit.
    Includes price predictions, demand classification, spoilage risk, and transport costs.
    """
    request_id = f"req_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    start_time = datetime.now()
    
    logger.info(
        f"[{request_id}] Prediction request: {request.quantity_kg}kg {request.crop_type} "
        f"from {request.village_location}, harvest: {request.harvest_date}"
    )
    
    try:
        # Validate village exists
        village_data = data_loader.get_village_distances(request.village_location)
        if not village_data:
            supported_villages = data_loader.get_supported_villages()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "VillageNotFound",
                    "message": f"Village '{request.village_location}' not found",
                    "supported_villages": supported_villages
                }
            )
        
        # Validate crop exists
        crop = data_loader.get_crop(request.crop_type)
        if not crop:
            supported_crops = data_loader.get_supported_crops()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "CropNotFound",
                    "message": f"Crop '{request.crop_type}' not found",
                    "supported_crops": supported_crops
                }
            )
        
        # Optimize markets
        recommendations = optimization_service.optimize_markets(
            village_id=request.village_location,
            crop_id=request.crop_type,
            quantity_kg=request.quantity_kg,
            harvest_date=request.harvest_date
        )
        
        if not recommendations:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "NoMarketsFound",
                    "message": f"No suitable markets found near {request.village_location}"
                }
            )
        
        # Get best recommendation
        best_recommendation = recommendations[0]
        
        # Generate explanation
        explanation = explanation_service.generate_explanation(
            village_location=request.village_location,
            crop_type=request.crop_type,
            quantity_kg=request.quantity_kg,
            best_recommendation=best_recommendation,
            all_recommendations=recommendations
        )
        
        # Calculate response time
        response_time_ms = (datetime.now() - start_time).total_seconds() * 1000
        
        logger.info(
            f"[{request_id}] Generated {len(recommendations)} recommendations, "
            f"best: {best_recommendation.market_name} (₹{best_recommendation.net_profit:,.0f}), "
            f"response time: {response_time_ms:.0f}ms"
        )
        
        # Create response
        response = PredictionResponse(
            request_id=request_id,
            timestamp=datetime.now(),
            village_location=request.village_location,
            crop_type=request.crop_type,
            quantity_kg=request.quantity_kg,
            markets=recommendations,
            best_market=best_recommendation.market_name,
            best_market_id=best_recommendation.market_id,
            explanation=explanation,
            total_markets_analyzed=len(recommendations),
            forecast_days=7
        )
        
        return response
    
    except HTTPException:
        raise
    
    except RPINException as e:
        logger.error(f"[{request_id}] RPIN error: {e.message}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": e.__class__.__name__,
                "message": e.message,
                "details": e.details
            }
        )
    
    except Exception as e:
        logger.error(f"[{request_id}] Unexpected error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "An unexpected error occurred while processing your request",
                "request_id": request_id
            }
        )
