"""BlockScout API Client"""

import httpx
from typing import List, Optional, Dict, Any, Union
from urllib.parse import urljoin

from .exceptions import BlockScoutAPIError, BlockScoutError
from .models import *


class BlockScoutClient:
    """BlockScout API Client"""

    def __init__(self, base_url: str, timeout: int = 30):
        """
        Initialize BlockScout client

        Args:
            base_url: Base URL for BlockScout API (e.g., "https://blockscout.com/poa/core/api/v2/")
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/") + "/"
        self.client = httpx.Client(timeout=timeout)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.client.close()

    async def __aenter__(self):
        self.client = httpx.AsyncClient(timeout=self.client.timeout)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.client.aclose()

    def _make_request(
        self, endpoint: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Make HTTP request to API"""
        url = urljoin(self.base_url, endpoint.lstrip("/"))

        try:
            response = self.client.get(url, params=params)
            response.raise_for_status()
            return response.json()
        except httpx.HTTPStatusError as e:
            raise BlockScoutAPIError(
                status_code=e.response.status_code,
                message=str(e),
                response_data=e.response.json() if e.response.content else {},
            )
        except Exception as e:
            raise BlockScoutError(f"Request failed: {str(e)}")

    # Search endpoints
    def search(self, query: str) -> PaginatedResponse:
        """Search for addresses, transactions, blocks, tokens"""
        data = self._make_request("/search", {"q": query})
        items = []
        for item in data.get("items", []):
            item_type = item.get("type")
            if item_type == "token":
                items.append(SearchResultToken(**item))
            elif item_type in ["address", "contract"]:
                items.append(SearchResultAddressOrContract(**item))
            elif item_type == "block":
                items.append(SearchResultBlock(**item))
            elif item_type == "transaction":
                items.append(SearchResultTransaction(**item))

        return PaginatedResponse(
            items=items, next_page_params=data.get("next_page_params")
        )

    def search_check_redirect(self, query: str) -> SearchResultRedirect:
        """Check if search should redirect"""
        data = self._make_request("/search/check-redirect", {"q": query})
        return SearchResultRedirect(**data)

    # Transaction endpoints
    def get_transactions(
        self,
        filter_type: Optional[str] = None,
        tx_type: Optional[str] = None,
        method: Optional[str] = None,
    ) -> PaginatedResponse:
        """Get transactions list"""
        params = {}
        if filter_type:
            params["filter"] = filter_type
        if tx_type:
            params["type"] = tx_type
        if method:
            params["method"] = method

        data = self._make_request("/transactions", params)
        transactions = [Transaction(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=transactions, next_page_params=data.get("next_page_params")
        )

    def get_transaction(self, tx_hash: str) -> Transaction:
        """Get transaction by hash"""
        data = self._make_request(f"/transactions/{tx_hash}")
        return Transaction(**data)

    def get_transaction_token_transfers(
        self, tx_hash: str, token_type: Optional[str] = None
    ) -> PaginatedResponse:
        """Get transaction token transfers"""
        params = {"type": token_type} if token_type else {}
        data = self._make_request(f"/transactions/{tx_hash}/token-transfers", params)
        transfers = [TokenTransfer(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=transfers, next_page_params=data.get("next_page_params")
        )

    # Address endpoints
    def get_address(self, address_hash: str) -> Address:
        """Get address information"""
        data = self._make_request(f"/addresses/{address_hash}")
        return Address(**data)

    def get_address_transactions(
        self, address_hash: str, filter_type: Optional[str] = None
    ) -> PaginatedResponse:
        """Get address transactions"""
        params = {"filter": filter_type} if filter_type else {}
        data = self._make_request(f"/addresses/{address_hash}/transactions", params)
        transactions = [Transaction(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=transactions, next_page_params=data.get("next_page_params")
        )

    def get_address_token_balances(self, address_hash: str) -> List[TokenBalance]:
        """Get address token balances"""
        data = self._make_request(f"/addresses/{address_hash}/token-balances")
        return [TokenBalance(**item) for item in data]

    # Block endpoints
    def get_blocks(self, block_type: Optional[str] = None) -> PaginatedResponse:
        """Get blocks list"""
        params = {"type": block_type} if block_type else {}
        data = self._make_request("/blocks", params)
        blocks = [Block(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=blocks, next_page_params=data.get("next_page_params")
        )

    def get_block(self, block_number_or_hash: Union[str, int]) -> Block:
        """Get block by number or hash"""
        data = self._make_request(f"/blocks/{block_number_or_hash}")
        return Block(**data)

    # Token endpoints
    def get_tokens(
        self, query: Optional[str] = None, token_type: Optional[str] = None
    ) -> PaginatedResponse:
        """Get tokens list"""
        params = {}
        if query:
            params["q"] = query
        if token_type:
            params["type"] = token_type

        data = self._make_request("/tokens", params)
        tokens = [TokenInfo(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=tokens, next_page_params=data.get("next_page_params")
        )

    def get_token(self, address_hash: str) -> TokenInfo:
        """Get token information"""
        data = self._make_request(f"/tokens/{address_hash}")
        return TokenInfo(**data)

    def get_token_holders(
        self, address_hash: str, limit: Optional[int] = None, all_pages: bool = False
    ) -> PaginatedResponse:
        """
        Get token holders with pagination support

        Args:
            address_hash: Token contract address
            limit: Maximum number of holders to return (None for API default)
            all_pages: If True, fetch all pages of results
        """
        all_holders = []
        next_page_params = None

        while True:
            # Make request with pagination params
            params = {}
            if next_page_params:
                params.update(next_page_params)

            data = self._make_request(f"/tokens/{address_hash}/holders", params)
            holders = [Holder(**item) for item in data.get("items", [])]

            all_holders.extend(holders)

            # Check if we should continue fetching
            next_page_params = data.get("next_page_params")

            if not all_pages or not next_page_params or not holders:
                break

            if limit and len(all_holders) >= limit:
                all_holders = all_holders[:limit]
                break

        # Apply limit if specified
        if limit and len(all_holders) > limit:
            all_holders = all_holders[:limit]

        return PaginatedResponse(
            items=all_holders,
            next_page_params=next_page_params if not all_pages else None,
        )

    def get_token_holders_paginated(
        self, address_hash: str, page_params: Optional[Dict] = None
    ) -> PaginatedResponse:
        """Get single page of token holders"""
        params = page_params or {}
        data = self._make_request(f"/tokens/{address_hash}/holders", params)
        holders = [Holder(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=holders, next_page_params=data.get("next_page_params")
        )

    def get_token_token_transfers(self, address_hash: str) -> PaginatedResponse:
        """Get token transfers for a specific token"""
        data = self._make_request(f"/tokens/{address_hash}/transfers")
        transfers = [TokenTransfer(**item) for item in data.get("items", [])]

        return PaginatedResponse(
            items=transfers, next_page_params=data.get("next_page_params")
        )

    def get_token_counters(self, address_hash: str) -> TokenCounters:
        """Get token counters"""
        data = self._make_request(f"/tokens/{address_hash}/counters")
        return TokenCounters(**data)

    def close(self):
        """Close the HTTP client"""
        self.client.close()
