"""Address-related models"""

from typing import List, Optional, TYPE_CHECKING
from pydantic import Field, ConfigDict
from .base import (
    BaseBlockScoutModel,
    AddressTag,
    TokenInfo,
    WatchlistName,
    AddressParam,
)

if TYPE_CHECKING:
    from .token import Token


class Address(AddressParam):
    """Full address model"""

    model_config = ConfigDict(populate_by_name=True)

    creator_address_hash: Optional[str] = None
    creation_transaction_hash: Optional[str] = None
    token: Optional[TokenInfo] = None  # Forward reference
    coin_balance: Optional[str] = None
    exchange_rate: Optional[str] = None
    implementation_address: Optional[str] = None
    block_number_balance_updated_at: Optional[int] = None
    has_beacon_chain_withdrawals: Optional[bool] = None
    has_logs: Optional[bool] = None
    has_token_transfers: Optional[bool] = None
    has_tokens: Optional[bool] = None
    has_validated_blocks: Optional[bool] = None


class AddressWithTxCount(Address):
    """Address with transaction count"""

    transaction_count: str


class AddressCounters(BaseBlockScoutModel):
    """Address counters"""

    transactions_count: str
    token_transfers_count: str
    gas_usage_count: str
    validations_count: str


class CoinBalanceHistoryEntry(BaseBlockScoutModel):
    """Coin balance history entry"""

    transaction_hash: Optional[str] = None
    block_number: int
    block_timestamp: str
    delta: str
    value: str


class CoinBalanceHistoryByDaysEntry(BaseBlockScoutModel):
    """Coin balance history by day"""

    date: str
    value: float
