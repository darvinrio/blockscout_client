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
@click.option("--limit", "-l", type=int, help="Maximum number of holders to fetch")
@click.option(
    "--all",
    "fetch_all",
    is_flag=True,
    help="Fetch all holders (may take time for large tokens)",
)
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    help="Output format (overrides config)",
)
@click.option("--save-to", help="Save results to file (CSV format)")
@click.pass_context
def holders(ctx, address_hash, limit, fetch_all, output_format, save_to):
    """Get token holders with pagination support"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    # Determine actual limit
    if fetch_all:
        actual_limit = None
        console.print(
            "[yellow]⚠️  Fetching ALL holders - this may take a while for popular tokens![/yellow]"
        )
    elif limit:
        actual_limit = limit
    else:
        actual_limit = config.max_items

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            if fetch_all:
                with console.status(
                    f"Fetching ALL holders for token {address_hash} (this may take time)..."
                ):
                    result = client.get_token_holders(
                        address_hash, limit=actual_limit, all_pages=True
                    )
            else:
                with console.status(f"Fetching holders for token {address_hash}..."):
                    result = client.get_token_holders(
                        address_hash, limit=actual_limit, all_pages=False
                    )

            if not result.items:
                console.print("No holders found.", style="yellow")
                return

            total_holders = len(result.items)
            console.print(f"[green]✅ Found {total_holders} holders[/green]")

            # Save to file if requested
            if save_to:
                import pandas as pd

                df = pd.DataFrame([holder.to_dict() for holder in result.items])
                df.to_csv(save_to, index=False)
                console.print(
                    f"[green]💾 Saved {total_holders} holders to {save_to}[/green]"
                )
                return

            # Display results
            display_limit = min(50, total_holders)  # Limit display for readability
            display_items = result.items[:display_limit]

            output = format_output(
                display_items, format_type, f"Token Holders for {address_hash}"
            )
            console.print(output)

            if total_holders > display_limit:
                console.print(
                    f"\n[yellow]Showing {display_limit} of {total_holders} holders[/yellow]"
                )
                console.print(
                    f"[cyan]💡 Use --save-to filename.csv to export all holders[/cyan]"
                )

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()


@token_group.command()
@click.argument("address_hash")
@click.option("--page-size", type=int, default=50, help="Number of holders per page")
@click.option(
    "--format",
    "-f",
    "output_format",
    type=click.Choice(["table", "json", "csv"]),
    help="Output format (overrides config)",
)
@click.pass_context
def holders_interactive(ctx, address_hash, page_size, output_format):
    """Browse token holders interactively with pagination"""
    config = ctx.obj["config"]
    format_type = output_format or config.output_format

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            next_page_params = None
            page_num = 1

            while True:
                with console.status(f"Fetching page {page_num} of holders..."):
                    result = client.get_token_holders_paginated(
                        address_hash, next_page_params
                    )

                if not result.items:
                    console.print("No more holders found.", style="yellow")
                    break

                # Display current page
                console.print(
                    f"\n[bold]Page {page_num} - {len(result.items)} holders[/bold]"
                )
                output = format_output(
                    result.items, format_type, f"Token Holders - Page {page_num}"
                )
                console.print(output)

                # Check if there are more pages
                if not result.next_page_params:
                    console.print("\n[green]✅ No more pages available[/green]")
                    break

                # Ask user what to do next
                console.print(f"\n[cyan]Options:[/cyan]")
                console.print("  [bold]n[/bold] - Next page")
                console.print("  [bold]q[/bold] - Quit")
                console.print("  [bold]a[/bold] - Download all remaining pages")

                choice = click.prompt("Your choice", type=str, default="n").lower()

                if choice == "q":
                    break
                elif choice == "a":
                    # Fetch all remaining pages
                    all_holders = list(result.items)
                    current_params = result.next_page_params

                    with console.status("Fetching all remaining holders..."):
                        while current_params:
                            page_result = client.get_token_holders_paginated(
                                address_hash, current_params
                            )
                            if not page_result.items:
                                break
                            all_holders.extend(page_result.items)
                            current_params = page_result.next_page_params

                    # Save to CSV
                    filename = f"holders_{address_hash}_{len(all_holders)}_total.csv"
                    import pandas as pd

                    df = pd.DataFrame([holder.to_dict() for holder in all_holders])
                    df.to_csv(filename, index=False)
                    console.print(
                        f"[green]💾 Saved {len(all_holders)} holders to {filename}[/green]"
                    )
                    break
                elif choice == "n":
                    next_page_params = result.next_page_params
                    page_num += 1
                else:
                    console.print("[red]Invalid choice, please try again[/red]")
                    continue

    except BlockScoutError as e:
        console.print(f"❌ Error: {e}", style="red")
        raise click.Abort()
    except KeyboardInterrupt:
        console.print("\n[yellow]Operation cancelled by user[/yellow]")


@token_group.command()
@click.argument("address_hash")
@click.option("--output", "-o", required=True, help="Output CSV file path")
@click.option("--max-holders", type=int, help="Maximum number of holders to export")
@click.option("--min-balance", type=float, help="Minimum token balance to include")
@click.pass_context
def export_holders(ctx, address_hash, output, max_holders, min_balance):
    """Export token holders to CSV file with filtering options"""
    config = ctx.obj["config"]

    try:
        with BlockScoutClient(config.base_url, config.timeout) as client:
            console.print(
                f"[cyan]🔍 Exporting holders for token {address_hash}...[/cyan]"
            )

            with console.status(
                "Fetching all holders (this may take several minutes)..."
            ):
                result = client.get_token_holders(
                    address_hash, limit=max_holders, all_pages=True
                )

            if not result.items:
                console.print("No holders found.", style="yellow")
                return

            holders_data = []
            total_holders = len(result.items)

            console.print(f"[green]✅ Found {total_holders} holders[/green]")

            # Process and filter holders
            with console.status("Processing holder data..."):
                for holder in result.items:
                    holder_dict = holder.to_dict()

                    # Apply minimum balance filter
                    if min_balance:
                        try:
                            balance = float(holder_dict.get("value", 0))
                            if balance < min_balance:
                                continue
                        except (ValueError, TypeError):
                            continue

                    holders_data.append(holder_dict)

            if not holders_data:
                console.print(
                    "[yellow]No holders match the specified criteria[/yellow]"
                )
                return

            # Save to CSV
            import pandas as pd

            df = pd.DataFrame(holders_data)
            df.to_csv(output, index=False)

            console.print(
                f"[green]💾 Successfully exported {len(holders_data)} holders to {output}[/green]"
            )

            # Show summary statistics
            if "value" in df.columns:
                try:
                    df["value_numeric"] = pd.to_numeric(df["value"], errors="coerce")
                    console.print(f"[cyan]📊 Summary Statistics:[/cyan]")
                    console.print(f"  Total holders: {len(holders_data)}")
                    console.print(
                        f"  Average balance: {df['value_numeric'].mean():.2f}"
                    )
                    console.print(
                        f"  Median balance: {df['value_numeric'].median():.2f}"
                    )
                    console.print(f"  Max balance: {df['value_numeric'].max():.2f}")
                    console.print(f"  Min balance: {df['value_numeric'].min():.2f}")
                except Exception:
                    pass

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
