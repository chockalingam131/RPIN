"""
Markets API endpoints
"""
from fastapi import APIRouter, HTTPException, status, Query
from typing import Optional
import logging

from app.models.response import MarketListResponse
from app.data.loaders import data_loader

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/markets",
    response_model=MarketListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get available markets",
    description="Get list of markets near a location"
)
async def get_markets(
    location: str = Query(..., description="Village or location name"),
    max_distance_km: Optional[float] = Query(500, description="Maximum distance in km")
):
    """Get markets near a location"""
    logger.info(f"Getting markets near {location} within {max_distance_km}km")
    
    try:
        # Get nearby markets
        nearby = data_loader.get_nearby_markets(location, max_distance_km)
        
        if not nearby:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "error": "NoMarketsFound",
                    "message": f"No markets found near {location} within {max_distance_km}km",
                    "supported_villages": data_loader.get_supported_villages()
                }
            )
        
        # Get market details
        markets = []
        for market_id, distance in nearby:
            market = data_loader.get_market(market_id)
            if market:
                markets.append(market)
        
        response = MarketListResponse(
            location=location,
            markets=markets,
            total_count=len(markets)
        )
        
        logger.info(f"Found {len(markets)} markets near {location}")
        return response
    
    except HTTPException:
        raise
    
    except Exception as e:
        logger.error(f"Error getting markets: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "Error retrieving markets"
            }
        )


@router.get(
    "/markets/{market_id}",
    status_code=status.HTTP_200_OK,
    summary="Get market details",
    description="Get detailed information about a specific market"
)
async def get_market(market_id: str):
    """Get specific market details"""
    logger.info(f"Getting market details for {market_id}")
    
    market = data_loader.get_market(market_id)
    
    if not market:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "MarketNotFound",
                "message": f"Market '{market_id}' not found",
                "supported_markets": data_loader.get_supported_markets()
            }
        )
    
    return market
