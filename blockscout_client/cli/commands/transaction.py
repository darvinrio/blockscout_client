"""Transaction commands"""

import click
from rich.console import Console
from ..formatters import format_output
from ...client import BlockScoutClient
from ...exceptions import BlockScoutError

console = Console()

@click.group(name='tx')
def transaction_group():
    """Transaction commands"""
    pass

@transaction_group.command()
@click.option('--filter', 'filter_type', 
              type=click.Choice(['pending', 'validated']),
              help='Filter transactions by status')
@click.option('--type', 'tx_type',
              help='Filter by transaction type (comma-separated)')
@click.option('--method',
              help='Filter by method name (comma-separated)')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def list(ctx, filter_type, tx_type, method, output_format):
    """List recent transactions"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status("Fetching transactions..."):
                result = client.get_transactions(filter_type, tx_type, method)
            
            if not result.items:
                console.print("No transactions found.", style="yellow")
                return
            
            limited_results = result.items[:config.max_items]
            output = format_output(
                limited_results, 
                format_type, 
                "Recent Transactions"
            )
            console.print(output)
            
            if len(result.items) > config.max_items:
                console.print(f"\n[yellow]Showing {config.max_items} of {len(result.items)} transactions[/yellow]")
                
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()

@transaction_group.command()
@click.argument('tx_hash')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def info(ctx, tx_hash, output_format):
    """Get transaction details"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching transaction {tx_hash}..."):
                transaction = client.get_transaction(tx_hash)
            
            output = format_output(transaction, format_type, f"Transaction: {tx_hash}")
            console.print(output)
            
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()

@transaction_group.command()
@click.argument('tx_hash')
@click.option('--type', 'token_type',
              help='Filter by token type (ERC-20,ERC-721,ERC-1155)')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def transfers(ctx, tx_hash, token_type, output_format):
    """Get transaction token transfers"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching token transfers for {tx_hash}..."):
                result = client.get_transaction_token_transfers(tx_hash, token_type)
            
            if not result.items:
                console.print("No token transfers found.", style="yellow")
                return
            
            limited_results = result.items[:config.max_items]
            output = format_output(
                limited_results, 
                format_type, 
                f"Token Transfers for {tx_hash}"
            )
            console.print(output)
            
            if len(result.items) > config.max_items:
                console.print(f"\n[yellow]Showing {config.max_items} of {len(result.items)} transfers[/yellow]")
                
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()