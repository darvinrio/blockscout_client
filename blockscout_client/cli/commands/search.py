"""Search commands"""

import click
from rich.console import Console
from ..formatters import format_output
from ...client import BlockScoutClient
from ...exceptions import BlockScoutError

console = Console()

@click.group(name='search')
def search_group():
    """Search commands"""
    pass

@search_group.command()
@click.argument('query')
@click.option('--format', '-f', 'output_format', 
              type=click.Choice(['table', 'json', 'csv']),
              help='Output format (overrides config)')
@click.pass_context
def query(ctx, query, output_format):
    """Search for addresses, transactions, blocks, or tokens"""
    config = ctx.obj['config']
    format_type = output_format or config.output_format
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Searching for '{query}'..."):
                results = client.search(query)
            
            if not results.items:
                console.print("No results found.", style="yellow")
                return
            
            # Limit results
            limited_results = results.items[:config.max_items]
            
            output = format_output(
                limited_results, 
                format_type, 
                f"Search Results for '{query}'"
            )
            console.print(output)
            
            if len(results.items) > config.max_items:
                console.print(f"\n[yellow]Showing {config.max_items} of {len(results.items)} results[/yellow]")
                
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()

@search_group.command()
@click.argument('query')
@click.pass_context
def redirect(ctx, query):
    """Check if search query should redirect to specific page"""
    config = ctx.obj['config']
    
    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Checking redirect for '{query}'..."):
                result = client.search_check_redirect(query)
            
            if result.redirect:
                console.print(f"✅ Redirect to {result.type}: {result.parameter}", style="green")
            else:
                console.print("❌ No redirect available", style="red")
                
    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()