# Blockscout Client

AI generated based on: [Swagger File](https://raw.githubusercontent.com/blockscout/blockscout-api-v2-swagger/main/swagger.yaml)
also attached to source code

## client usage example

```py
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
```

## cli usage examples

Initial Setup

```bash
# Install the package
pip install -e .

## Configure the CLI

blockscout configure
# This will prompt for:
# - Base URL (e.g., https://blockscout.com/poa/core/api/v2/)
# - Timeout (default: 30)
# - Output format (table/json/csv, default: table)
# - Max items (default: 50)
```

Search Commands

```bash
## Search for anything
blockscout search query "USDT"
blockscout search query "0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9"

## Check redirect
blockscout search redirect "0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9"

## Output in different formats
blockscout search query "USDT" --format json
blockscout search query "USDT" --format csv
```

Help

```bash
# Show all token commands
blockscout token --help

# Commands available:
# - list      List tokens with optional filtering
# - info      Get detailed token information  
# - holders   Get token holders list
# - transfers Get token transfer history
# - counters  Get token statistics (holder count, transfer count)
```

Address Commands

```bash
## Get address info
blockscout address info 0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9

## Get address transactions
blockscout address transactions 0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9
blockscout address transactions 0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9 --filter to

## Get token balances
blockscout address tokens 0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9 --format json
```

Transaction Commands

```bash
## List recent transactions
blockscout tx list
blockscout tx list --filter validated --type token_transfer

## Get specific transaction
blockscout tx info 0x6662ad1ad2ea899e9e27832dc202fd2ef915a5d2816c1142e6933cff93f7c592

## Get transaction token transfers
blockscout tx transfers 0x6662ad1ad2ea899e9e27832dc202fd2ef915a5d2816c1142e6933cff93f7c592
```

Block Commands

```bash
## List recent blocks
blockscout block list
blockscout block list --type block

## Get specific block
blockscout block info 17615720
blockscout block info 0xf569ec751152b2f814001fc730f7797aa155e4bc3ba9cb6ba24bc2c8c9468c1a
```

Token Commands

```bash
## List tokens
blockscout token list
blockscout token list --query "USDT" --type ERC-20

## Get token info
blockscout token info 0xdAC17F958D2ee523a2206206994597C13D831ec7
```

Configuration Commands

```bash
## Show current config
blockscout show-config

## Reconfigure
blockscout configure

## Override config for single command
blockscout --base-url "https://custom.blockscout.com/api/v2/" search query "USDT"
blockscout --output-format json tx list
```

Advanced Usage

```bash
## Pipe to files
blockscout tx list --format csv > transactions.csv
blockscout search query "USDT" --format json > search_results.json

## Use with other tools
blockscout address tokens 0x742d35Cc64C5E2e01b17a2CC7375654e7E3E1Ab9 --format csv | head -10
```

Token Analysis Example

```bash
# Analyze USDT token completely
echo "=== USDT Token Analysis ==="

# 1. Get token info
echo "Token Information:"
blockscout token info 0xdAC17F958D2ee523a2206206994597C13D831ec7

# 2. Get counters
echo -e "\nToken Statistics:"
blockscout token counters 0xdAC17F958D2ee523a2206206994597C13D831ec7

# 3. Get top 100 holders (CSV for analysis)
echo -e "\nExporting top holders to CSV..."
blockscout token holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 --format csv > usdt_holders.csv

# 4. Get recent transfers
echo -e "\nRecent transfers:"
blockscout token transfers 0xdAC17F958D2ee523a2206206994597C13D831ec7 --format table
```

Holder Analysis

```bash
# Get first 100 holders (default)
blockscout token holders 0xdAC17F958D2ee523a2206206994597C13D831ec7

# Get specific number of holders
blockscout token holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 --limit 500

# Get ALL holders (may take time for popular tokens)
blockscout token holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 --all

# Save all holders to CSV directly
blockscout token holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 --all --save-to usdt_holders.csv

# Browse holders page by page interactively
blockscout token holders-interactive 0xdAC17F958D2ee523a2206206994597C13D831ec7

# Export all holders to CSV
blockscout token export-holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 -o all_holders.csv

# Export max 10,000 holders
blockscout token export-holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 -o top_holders.csv --max-holders 10000

# Export only holders with balance >= 1000 tokens
blockscout token export-holders 0xdAC17F958D2ee523a2206206994597C13D831ec7 -o whale_holders.csv --min-balance 1000
```
