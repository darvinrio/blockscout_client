# Basic usage
from blockscout_client import BlockScoutClient
import pandas as pd

# Initialize client
client = BlockScoutClient("https://blockscout.com/poa/core/api/v2/")

# Search for tokens
search_results = client.search("USDT")
print(f"Found {len(search_results.items)} results")

# Get address information
address = client.get_address("0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9")
print(f"Address balance: {address.coin_balance}")

# Get transactions and convert to DataFrame
transactions_response = client.get_transactions(filter_type="validated")
transactions_df = pd.DataFrame([tx.to_dict() for tx in transactions_response.items])

# Get token balances
balances = client.get_address_token_balances("0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9")
balances_df = pd.DataFrame([balance.to_dict() for balance in balances])

# Close client
client.close()

# Context manager usage
with BlockScoutClient("https://blockscout.com/poa/core/api/v2/") as client:
    block = client.get_block(17615720)
    print(f"Block hash: {block.hash}")