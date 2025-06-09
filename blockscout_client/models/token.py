"""Token-related models"""

from typing import List, Optional, Union, TYPE_CHECKING
from pydantic import Field
from .base import BaseBlockScoutModel, AddressParam, TokenInfo

if TYPE_CHECKING:
    pass


class Token(BaseBlockScoutModel):
    """Token model"""

    name: str
    decimals: str
    symbol: str
    address: str
    type: str
    holders: int
    exchange_rate: str
    total_supply: str


class TotalERC20(BaseBlockScoutModel):
    """ERC-20 token total"""

    decimals: str
    value: str


class TotalERC721(BaseBlockScoutModel):
    """ERC-721 token total"""

    token_id: str
    token_instance: Optional["NFTInstance"] = None


class TotalERC1155(BaseBlockScoutModel):
    """ERC-1155 token total"""

    token_id: str
    decimals: Optional[str] = None
    value: str
    token_instance: Optional["NFTInstance"] = None


class NFTInstance(BaseBlockScoutModel):
    """NFT instance"""

    is_unique: bool
    id: str
    holder_address_hash: Optional[str] = None
    image_url: Optional[str] = None
    animation_url: Optional[str] = None
    external_app_url: Optional[str] = None
    metadata: Optional[dict] = None
    owner: Optional[AddressParam] = None
    token: Optional[TokenInfo] = None


class TokenTransfer(BaseBlockScoutModel):
    """Token transfer"""

    block_hash: str
    from_: AddressParam = Field(alias="from")
    log_index: int
    method: Optional[str] = None
    timestamp: Optional[str] = None
    to: AddressParam
    token: TokenInfo
    total: Union[TotalERC20, TotalERC721, TotalERC1155]
    transaction_hash: str
    type: str


class TokenBalance(BaseBlockScoutModel):
    """Token balance"""

    token_instance: Optional[NFTInstance] = None
    value: str
    token_id: Optional[str] = None
    token: Token


class TokenCounters(BaseBlockScoutModel):
    """Token counters"""

    token_holders_count: str
    transfers_count: str


class Holder(BaseBlockScoutModel):
    """Token holder"""

    address: AddressParam
    value: str
    token_id: Optional[str] = None


class AddressNFTInstance(BaseBlockScoutModel):
    """Address NFT instance"""

    is_unique: bool
    id: str
    holder_address_hash: Optional[str] = None
    image_url: Optional[str] = None
    animation_url: Optional[str] = None
    external_app_url: Optional[str] = None
    metadata: Optional[dict] = None
    owner: Optional[AddressParam] = None
    token: Optional[TokenInfo] = None
    token_type: str
    value: str


class AddressNFTInstanceCollection(BaseBlockScoutModel):
    """Address NFT instance for collection"""

    is_unique: bool
    id: str
    holder_address_hash: Optional[str] = None
    image_url: Optional[str] = None
    animation_url: Optional[str] = None
    external_app_url: Optional[str] = None
    metadata: Optional[dict] = None
    owner: Optional[AddressParam] = None
    token: Optional[dict] = None  # Can be null in collection context
    token_type: str
    value: str


class AddressNFTCollection(BaseBlockScoutModel):
    """Address NFT collection"""

    token: TokenInfo
    amount: Optional[str] = None
    token_instances: List[AddressNFTInstanceCollection] = Field(default_factory=list)
