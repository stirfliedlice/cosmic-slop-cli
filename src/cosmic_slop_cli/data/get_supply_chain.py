#!/usr/bin/env python3

from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_get_request

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="supply-chain")
def get_supply_chain(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of supply chains."""
    url: str = "https://api.spacetraders.io/v2/market/supply-chain"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Supply Chain Details"))
    else:
        table: Table = Table(title="Supply Chain Summary (exportToImportMap)")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for key, value in api_data["data"]["exportToImportMap"].items():
            table.add_row(str(key), str(value))
        console.print(table)
