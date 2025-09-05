#!/usr/bin/env python3

from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_post_request

app: typer.Typer = typer.Typer(no_args_is_help=True)

api_data: dict[str, Any] = {}


@app.command(name="accept", help="Accept a contract")
def post_accept_contracts(
    contract_id: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")],
) -> None:
    console.print("post_accept_contracts called")
    url: str = "https://api.spacetraders.io/v2/my/contracts/" + contract_id + "/accept"
    api_data = send_post_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
    else:
        table: Table = Table(title="Contract Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        console.print(table)


@app.command(name="deliver", help="Deliver contract cargo")
def post_deliver_contract_cargo(
    contract_id: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")],
    ship_symbol: Annotated[str, typer.Option(help="ID of the ship delivering the cargo")],
    trade_symbol: Annotated[str, typer.Option(help="Trade symbol of the cargo to deliver")],
    units: Annotated[int, typer.Option(help="Number of units to deliver")],
) -> None:
    console.print("post_deliver_contract_cargo called")
    url: str = "https://api.spacetraders.io/v2/my/contracts/" + contract_id + "/deliver"
    data: dict[str, str | int] = {
        "shipSymbol": ship_symbol,
        "tradeSymbol": trade_symbol,
        "units": units,
    }
    api_data = send_post_request(url, data)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
    else:
        table: Table = Table(title="Contract Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        console.print(table)


@app.command(name="fulfill", help="Fulfill a contract")
def post_fulfill_contracts(
    contract_id: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")],
) -> None:
    console.print("post_fulfill_contracts called with contract_id:", contract_id)
    url: str = "https://api.spacetraders.io/v2/my/contracts/" + contract_id + "/fulfill"
    api_data = send_post_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
    else:
        table: Table = Table(title="Contract Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        console.print(table)
