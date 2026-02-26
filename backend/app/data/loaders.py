"""
Data loading utilities for JSON files and database operations
"""
import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime
import logging

from app.core.config import settings
from app.core.exceptions import DataNotFoundError, ConfigurationError
from app.models.domain import Market, CropInfo, VillageDistance

logger = logging.getLogger(__name__)


class DataLoader:
    """Utility class for loading static data files"""
    
    def __init__(self):
        self.data_dir = Path(settings.DATA_DIR)
        self._crops_cache: Optional[Dict[str, CropInfo]] = None
        self._markets_cache: Optional[Dict[str, Market]] = None
        self._distances_cache: Optional[Dict[str, VillageDistance]] = None
        self._cache_timestamp: Optional[datetime] = None
    
    def _load_json_file(self, file_path: Path) -> dict:
        """Load and parse JSON file"""
        try:
            if not file_path.exists():
                raise DataNotFoundError(
                    f"Data file not found: {file_path}",
                    details={"file_path": str(file_path)}
                )
            
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            logger.info(f"Loaded data from {file_path}")
            return data
        
        except json.JSONDecodeError as e:
            raise ConfigurationError(
                f"Invalid JSON in file: {file_path}",
                details={"error": str(e)}
            )
        except Exception as e:
            raise DataNotFoundError(
                f"Error loading file: {file_path}",
                details={"error": str(e)}
            )
    
    def load_crops(self, force_reload: bool = False) -> Dict[str, CropInfo]:
        """
        Load crop information from JSON file
        
        Args:
            force_reload: Force reload from file, ignoring cache
        
        Returns:
            Dictionary mapping crop_id to CropInfo
        """
        if self._crops_cache is not None and not force_reload:
            return self._crops_cache
        
        file_path = Path(settings.CROPS_DATA_FILE)
        data = self._load_json_file(file_path)
        
        crops = {}
        for crop_id, crop_data in data.items():
            try:
                crops[crop_id] = CropInfo(**crop_data)
            except Exception as e:
                logger.error(f"Error parsing crop {crop_id}: {e}")
                continue
        
        self._crops_cache = crops
        self._cache_timestamp = datetime.now()
        
        logger.info(f"Loaded {len(crops)} crops")
        return crops
    
    def load_markets(self, force_reload: bool = False) -> Dict[str, Market]:
        """
        Load market information from JSON file
        
        Args:
            force_reload: Force reload from file, ignoring cache
        
        Returns:
            Dictionary mapping market_id to Market
        """
        if self._markets_cache is not None and not force_reload:
            return self._markets_cache
        
        file_path = Path(settings.MARKETS_DATA_FILE)
        data = self._load_json_file(file_path)
        
        markets = {}
        for market_id, market_data in data.items():
            try:
                markets[market_id] = Market(**market_data)
            except Exception as e:
                logger.error(f"Error parsing market {market_id}: {e}")
                continue
        
        self._markets_cache = markets
        self._cache_timestamp = datetime.now()
        
        logger.info(f"Loaded {len(markets)} markets")
        return markets
    
    def load_distances(self, force_reload: bool = False) -> Dict[str, VillageDistance]:
        """
        Load village-to-market distance data from JSON file
        
        Args:
            force_reload: Force reload from file, ignoring cache
        
        Returns:
            Dictionary mapping village_id to VillageDistance
        """
        if self._distances_cache is not None and not force_reload:
            return self._distances_cache
        
        file_path = Path(settings.DISTANCES_DATA_FILE)
        data = self._load_json_file(file_path)
        
        distances = {}
        for village_id, village_data in data.items():
            try:
                distances[village_id] = VillageDistance(**village_data)
            except Exception as e:
                logger.error(f"Error parsing village {village_id}: {e}")
                continue
        
        self._distances_cache = distances
        self._cache_timestamp = datetime.now()
        
        logger.info(f"Loaded {len(distances)} villages")
        return distances
    
    def get_crop(self, crop_id: str) -> Optional[CropInfo]:
        """Get specific crop information"""
        crops = self.load_crops()
        return crops.get(crop_id.lower())
    
    def get_market(self, market_id: str) -> Optional[Market]:
        """Get specific market information"""
        markets = self.load_markets()
        return markets.get(market_id.lower())
    
    def get_village_distances(self, village_id: str) -> Optional[VillageDistance]:
        """Get distance information for a specific village"""
        distances = self.load_distances()
        return distances.get(village_id.lower())
    
    def get_distance(self, village_id: str, market_id: str) -> Optional[float]:
        """Get distance between village and market"""
        village_data = self.get_village_distances(village_id)
        if village_data:
            return village_data.markets.get(market_id.lower())
        return None
    
    def get_nearby_markets(
        self,
        village_id: str,
        max_distance_km: float = 500
    ) -> List[tuple[str, float]]:
        """
        Get list of markets within specified distance
        
        Args:
            village_id: Village identifier
            max_distance_km: Maximum distance in kilometers
        
        Returns:
            List of tuples (market_id, distance_km) sorted by distance
        """
        village_data = self.get_village_distances(village_id)
        if not village_data:
            return []
        
        nearby = [
            (market_id, distance)
            for market_id, distance in village_data.markets.items()
            if distance <= max_distance_km
        ]
        
        # Sort by distance
        nearby.sort(key=lambda x: x[1])
        
        return nearby
    
    def get_supported_crops(self) -> List[str]:
        """Get list of supported crop IDs"""
        crops = self.load_crops()
        return list(crops.keys())
    
    def get_supported_villages(self) -> List[str]:
        """Get list of supported village IDs"""
        distances = self.load_distances()
        return list(distances.keys())
    
    def get_supported_markets(self) -> List[str]:
        """Get list of supported market IDs"""
        markets = self.load_markets()
        return list(markets.keys())
    
    def clear_cache(self):
        """Clear all cached data"""
        self._crops_cache = None
        self._markets_cache = None
        self._distances_cache = None
        self._cache_timestamp = None
        logger.info("Data cache cleared")


# Global data loader instance
data_loader = DataLoader()
