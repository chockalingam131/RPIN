"""
Crops API endpoints
"""
from fastapi import APIRouter, HTTPException, status
from typing import Optional
import logging

from app.models.response import CropListResponse
from app.data.loaders import data_loader

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get(
    "/crops",
    response_model=CropListResponse,
    status_code=status.HTTP_200_OK,
    summary="Get supported crops",
    description="Get list of all supported crop types"
)
async def get_crops():
    """Get all supported crops"""
    logger.info("Getting all supported crops")
    
    try:
        crops_dict = data_loader.load_crops()
        crops = list(crops_dict.values())
        
        response = CropListResponse(
            crops=crops,
            total_count=len(crops)
        )
        
        logger.info(f"Returning {len(crops)} crops")
        return response
    
    except Exception as e:
        logger.error(f"Error getting crops: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalServerError",
                "message": "Error retrieving crops"
            }
        )


@router.get(
    "/crops/{crop_id}",
    status_code=status.HTTP_200_OK,
    summary="Get crop details",
    description="Get detailed information about a specific crop"
)
async def get_crop(crop_id: str):
    """Get specific crop details"""
    logger.info(f"Getting crop details for {crop_id}")
    
    crop = data_loader.get_crop(crop_id)
    
    if not crop:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "CropNotFound",
                "message": f"Crop '{crop_id}' not found",
                "supported_crops": data_loader.get_supported_crops()
            }
        )
    
    return crop
