"""Base model classes"""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from datetime import datetime

class BaseBlockScoutModel(BaseModel):
    """Base model with common functionality"""
    
    class Config:
        allow_population_by_field_name = True
        use_enum_values = True
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.dict(by_alias=True, exclude_none=True)
    
    @classmethod
    def to_dataframe_dict(cls, items: List['BaseBlockScoutModel']) -> List[Dict[str, Any]]:
        """Convert list of models to list of dicts for DataFrame creation"""
        return [item.to_dict() for item in items]

class PaginatedResponse(BaseBlockScoutModel):
    """Base paginated response"""
    items: List[Any] = Field(default_factory=list)
    next_page_params: Optional[Dict[str, Any]] = None

class AddressTag(BaseBlockScoutModel):
    address_hash: str
    display_name: str
    label: str

class WatchlistName(BaseBlockScoutModel):
    display_name: str
    label: str