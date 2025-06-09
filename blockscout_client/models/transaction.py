"""Transaction-related models"""

from typing import List, Optional, Union, Any
from pydantic import Field
from .base import BaseBlockScoutModel
from .address import AddressParam

class Fee(BaseBlockScoutModel):
    """Transaction fee"""
    type: str  # "maximum" | "actual"
    value: str

class DecodedInputParameter(BaseBlockScoutModel):
    """Decoded input parameter"""
    name: str
    type: str
    value: str

class DecodedInput(BaseBlockScoutModel):
    """Decoded transaction input"""
    method_call: str
    method_id: str
    parameters: List[DecodedInputParameter] = Field(default_factory=list)

class TransactionAction(BaseBlockScoutModel):
    """Base transaction action"""
    data: dict
    protocol: str
    type: str

class Transaction(BaseBlockScoutModel):
    """Transaction model"""
    timestamp: str
    fee: Fee
    gas_limit: int
    block_number: int
    status: str  # "ok" | "error"
    method: Optional[str] = None
    confirmations: int
    type: int
    exchange_rate: str
    to: Optional[AddressParam] = None
    transaction_burnt_fee: Optional[str] = None
    max_fee_per_gas: Optional[str] = None
    result: Optional[str] = None
    hash: str
    gas_price: Optional[str] = None
    priority_fee: Optional[str] = None
    base_fee_per_gas: Optional[str] = None
    from_: AddressParam = Field(alias="from")
    token_transfers: List['TokenTransfer'] = Field(default_factory=list)
    transaction_types: List[str] = Field(default_factory=list)
    gas_used: Optional[str] = None
    created_contract: Optional[AddressParam] = None
    position: int
    nonce: int
    has_error_in_internal_transactions: bool = False
    actions: List[TransactionAction] = Field(default_factory=list)
    decoded_input: Optional[DecodedInput] = None
    token_transfers_overflow: bool = False
    raw_input: str
    value: str
    max_priority_fee_per_gas: Optional[str] = None
    revert_reason: Optional[str] = None
    confirmation_duration: List[float] = Field(default_factory=list)
    transaction_tag: Optional[str] = None

class InternalTransaction(BaseBlockScoutModel):
    """Internal transaction model"""
    block_number: int
    created_contract: Optional[AddressParam] = None
    error: Optional[str] = None
    from_: AddressParam = Field(alias="from")
    gas_limit: str
    index: int
    success: bool
    timestamp: str
    to: Optional[AddressParam] = None
    transaction_hash: str
    type: str
    value: str

class Log(BaseBlockScoutModel):
    """Transaction log model"""
    address: AddressParam
    block_hash: Optional[str] = None
    block_number: Optional[int] = None
    data: str
    decoded: Optional[dict] = None
    index: int
    smart_contract: Optional[AddressParam] = None
    topics: List[str] = Field(default_factory=list)
    transaction_hash: str