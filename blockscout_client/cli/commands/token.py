"""Token commands"""

import click
from rich.console import Console
from ..formatters import format_output
from ...client import BlockScoutClient
from ...exceptions import BlockScoutError

console = Console()


@click.group(name="token")
def token_group():
    """Token commands"""
    pass


@token_group.command()
@click.option("--query", "-q", help="Search query for token name or symbol")
@click.option(
    "--type", "token_type", help="Filter by token type (ERC-20,ERC-721,ERC-1155)"
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    help="Output format (overrides config)",
)
@click.pass_context
def list(ctx, query, token_type, output_format):
    """List tokens"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status("Fetching tokens..."):
                result = client.get_tokens(query, token_type)

            if not result.items:
                console.print("No tokens found.", style="yellow")
                return

            limited_results = result.items[: config.max_items]
            output = format_output(limited_results, format_type, "Tokens")
            console.print(output)

            if len(result.items) > config.max_items:
                console.print(
                    f"\n[yellow]Showing {config.max_items} of {len(result.items)} tokens[/yellow]"
                )

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()


@token_group.command()
@click.argument("address_hash")
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    help="Output format (overrides config)",
)
@click.pass_context
def info(ctx, address_hash, output_format):
    """Get token information"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching token info for {address_hash}..."):
                token = client.get_token(address_hash)

            output = format_output(token, format_type, f"Token: {address_hash}")
            console.print(output)

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()
