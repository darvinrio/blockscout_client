"""Block-related models"""

from typing import List, Optional
from .base import BaseBlockScoutModel, AddressParam


class Reward(BaseBlockScoutModel):
    """Block reward"""

    reward: int
    type: str  # "Miner Reward" | "Emission Reward" | "Chore Reward" | "Uncle Reward"


class Block(BaseBlockScoutModel):
    """Block model"""

    base_fee_per_gas: Optional[str] = None
    burnt_fees: Optional[str] = None
    burnt_fees_percentage: Optional[float] = None
    difficulty: str
    extra_data: str
    gas_limit: str
    gas_target_percentage: Optional[float] = None
    gas_used: str
    gas_used_percentage: Optional[float] = None
    hash: str
    height: int
    miner: AddressParam
    nonce: str
    parent_hash: str
    priority_fee: Optional[str] = None
    rewards: List[Reward] = []
    size: int
    state_root: str
    timestamp: str
    total_difficulty: str
    transaction_count: int
    transaction_fees: Optional[str] = None
    type: str
    uncles_hashes: List[str] = []
    withdrawals_count: Optional[int] = None


class Withdrawal(BaseBlockScoutModel):
    """Withdrawal model"""

    index: int
    amount: str
    validator_index: int
    receiver: Optional[AddressParam] = None
    block_number: Optional[int] = None
    timestamp: Optional[str] = None
