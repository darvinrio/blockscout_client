"""Address commands"""

import click
from rich.console import Console
from ..formatters import format_output
from ...client import BlockScoutClient
from ...exceptions import BlockScoutError

console = Console()

@click.group(name='address')
def address_group():
    """Address commands"""
    pass

@address_group.command()
@click.argument('address_hash')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def info(ctx, address_hash, output_format):
    """Get address information"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching address info for {address_hash}..."):
                address = client.get_address(address_hash)
            
            output = format_output(address, format_type, f"Address Info: {address_hash}")
            console.print(output)
            
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()

@address_group.command()
@click.argument('address_hash')
@click.option('--filter', 'filter_type', 
              type=click.Choice(['to', 'from']),
              help='Filter transactions by direction')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def transactions(ctx, address_hash, filter_type, output_format):
    """Get address transactions"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching transactions for {address_hash}..."):
                result = client.get_address_transactions(address_hash, filter_type)
            
            if not result.items:
                console.print("No transactions found.", style="yellow")
                return
            
            limited_results = result.items[:config.max_items]
            output = format_output(
                limited_results, 
                format_type, 
                f"Transactions for {address_hash}"
            )
            console.print(output)
            
            if len(result.items) > config.max_items:
                console.print(f"\n[yellow]Showing {config.max_items} of {len(result.items)} transactions[/yellow]")
                
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()

@address_group.command()
@click.argument('address_hash')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def tokens(ctx, address_hash, output_format):
    """Get address token balances"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching token balances for {address_hash}..."):
                balances = client.get_address_token_balances(address_hash)
            
            if not balances:
                console.print("No token balances found.", style="yellow")
                return
            
            limited_results = balances[:config.max_items]
            output = format_output(
                limited_results, 
                format_type, 
                f"Token Balances for {address_hash}"
            )
            console.print(output)
            
            if len(balances) > config.max_items:
                console.print(f"\n[yellow]Showing {config.max_items} of {len(balances)} tokens[/yellow]")
                
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()