"""Block commands"""

import click
from rich.console import Console
from ..formatters import format_output
from ...client import BlockScoutClient
from ...exceptions import BlockScoutError

console = Console()


@click.group(name="block")
def block_group():
    """Block commands"""
    pass


@block_group.command()
@click.option(
    "--type",
    "block_type",
    type=click.Choice(["block", "uncle", "reorg"]),
    help="Filter blocks by type",
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    help="Output format (overrides config)",
)
@click.pass_context
def list(ctx, block_type, output_format):
    """List recent blocks"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status("Fetching blocks..."):
                result = client.get_blocks(block_type)

            if not result.items:
                console.print("No blocks found.", style="yellow")
                return

            limited_results = result.items[: config.max_items]
            output = format_output(limited_results, format_type, "Recent Blocks")
            console.print(output)

            if len(result.items) > config.max_items:
                console.print(
                    f"\n[yellow]Showing {config.max_items} of {len(result.items)} blocks[/yellow]"
                )

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()


@block_group.command()
@click.argument("block_number_or_hash")
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    help="Output format (overrides config)",
)
@click.pass_context
def info(ctx, block_number_or_hash, output_format):
    """Get block details"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            with console.status(f"Fetching block {block_number_or_hash}..."):
                block = client.get_block(block_number_or_hash)

            output = format_output(block, format_type, f"Block: {block_number_or_hash}")
            console.print(output)

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()
