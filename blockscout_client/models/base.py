"""Base model classes"""

from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime


class BaseBlockScoutModel(BaseModel):
    """Base model with common functionality"""

    model_config = ConfigDict(
        populate_by_name=True,  # Renamed from allow_population_by_field_name
        use_enum_values=True,
        validate_assignment=True,
        extra="forbid",
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.model_dump(by_alias=True, exclude_none=True)

    @classmethod
    def to_dataframe_dict(
        cls, items: List["BaseBlockScoutModel"]
    ) -> List[Dict[str, Any]]:
        """Convert list of models to list of dicts for DataFrame creation"""
        return [item.to_dict() for item in items]


class PaginatedResponse(BaseBlockScoutModel):
    """Base paginated response"""

    items: List[Any] = Field(default_factory=list)
    next_page_params: Optional[Dict[str, Any]] = None


class AddressTag(BaseBlockScoutModel):
    """Address tag model"""

    address_hash: str
    display_name: str
    label: str


class WatchlistName(BaseBlockScoutModel):
    """Watchlist name model"""

    display_name: str
    label: str


class AddressParam(BaseBlockScoutModel):
    """Address parameter model - moved here to avoid circular imports"""

    hash: str
    implementation_name: Optional[str] = None
    name: Optional[str] = None
    ens_domain_name: Optional[str] = None
    metadata: Optional[dict] = None
    is_contract: bool
    private_tags: List[AddressTag] = Field(default_factory=list)
    watchlist_names: List[WatchlistName] = Field(default_factory=list)
    public_tags: List[AddressTag] = Field(default_factory=list)
    is_verified: bool

    implementations: Optional[List] = None
    is_scam: Optional[bool] = None
    proxy_type: Optional[str] = None
    watchlist_address_id: Optional[str] = None


class TokenInfo(BaseBlockScoutModel):
    """Token information - moved here to avoid circular imports"""

    address: str
    circulating_market_cap: Optional[str] = None
    icon_url: Optional[str] = None
    symbol: str
    name: str
    decimals: Optional[str] = None
    type: str  # "ERC-20", "ERC-721", "ERC-1155"
    holders: Optional[str] = None
    exchange_rate: Optional[str] = None
    total_supply: Optional[str] = None
