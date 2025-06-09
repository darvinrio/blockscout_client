"""Main CLI entry point"""

import click
from rich.console import Console
from .config import Config
from .commands import search, address, transaction, block, token

console = Console()

@click.group()
@click.option('--config', '-c', help='Path to configuration file')
@click.option('--base-url', help='BlockScout API base URL')
@click.option('--timeout', type=int, help='Request timeout in seconds')
@click.option('--output-format', '-f', 
              type=click.Choice(['table', 'json', 'csv']), 
              help='Output format')
@click.option('--max-items', type=int, help='Maximum number of items to fetch')
@click.pass_context
def cli(ctx, config, base_url, timeout, output_format, max_items):
    """BlockScout API CLI client"""
    # Load configuration
    ctx.ensure_object(dict)
    config_obj = Config.load(config)
    
    # Override with command line options
    if base_url:
        config_obj.base_url = base_url
    if timeout:
        config_obj.timeout = timeout
    if output_format:
        config_obj.output_format = output_format
    if max_items:
        config_obj.max_items = max_items
    
    ctx.obj['config'] = config_obj

@cli.command()
@click.option('--base-url', prompt=True, help='BlockScout API base URL')
@click.option('--timeout', type=int, default=30, help='Request timeout in seconds')
@click.option('--output-format', 
              type=click.Choice(['table', 'json', 'csv']), 
              default='table',
              help='Default output format')
@click.option('--max-items', type=int, default=50, help='Maximum number of items to fetch')
@click.pass_context
def configure(ctx, base_url, timeout, output_format, max_items):
    """Configure the CLI settings"""
    config = Config(
        base_url=base_url,
        timeout=timeout,
        output_format=output_format,
        max_items=max_items
    )
    config.save()
    console.print("✅ Configuration saved successfully!", style="green")

@cli.command()
@click.pass_context
def show_config(ctx):
    """Show current configuration"""
    config = ctx.obj['config']
    console.print("Current Configuration:", style="bold")
    console.print(f"Base URL: {config.base_url}")
    console.print(f"Timeout: {config.timeout}s")
    console.print(f"Output Format: {config.output_format}")
    console.print(f"Max Items: {config.max_items}")

# Add command groups
cli.add_command(search.search_group)
cli.add_command(address.address_group)
cli.add_command(transaction.transaction_group)
cli.add_command(block.block_group)
cli.add_command(token.token_group)

if __name__ == '__main__':
    cli()