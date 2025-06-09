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
def holders(ctx, address_hash, output_format):
    """Get token holders"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching holders for token {address_hash}..."):
                result = client.get_token_holders(address_hash)

            if not result.items:
                console.print("No holders found.", style="yellow")
                return

            limited_results = result.items[: config.max_items]
            output = format_output(
                limited_results, format_type, f"Token Holders for {address_hash}"
            )
            console.print(output)

            if len(result.items) > config.max_items:
                console.print(
                    f"\n[yellow]Showing {config.max_items} of {len(result.items)} holders[/yellow]"
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
def transfers(ctx, address_hash, output_format):
    """Get token transfers"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching transfers for token {address_hash}..."):
                result = client.get_token_token_transfers(address_hash)

            if not result.items:
                console.print("No transfers found.", style="yellow")
                return

            limited_results = result.items[: config.max_items]
            output = format_output(
                limited_results, format_type, f"Token Transfers for {address_hash}"
            )
            console.print(output)

            if len(result.items) > config.max_items:
                console.print(
                    f"\n[yellow]Showing {config.max_items} of {len(result.items)} transfers[/yellow]"
                )

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()


@token_group.command()
@click.argument("address_hash")
@click.pass_context
def counters(ctx, address_hash):
    """Get token counters (holders count, transfers count)"""
    config = ctx.obj["config"]

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching counters for token {address_hash}..."):
                counters = client.get_token_counters(address_hash)

            console.print("Token Counters:", style="bold")
            console.print(f"📊 Holders: {counters.token_holders_count}")
            console.print(f"🔄 Transfers: {counters.transfers_count}")

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()
