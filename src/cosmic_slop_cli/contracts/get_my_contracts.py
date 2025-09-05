#!/usr/bin/env python3

from collections.abc import Mapping
from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_get_request

app: typer.Typer = typer.Typer(no_args_is_help=True)


def construct_table(api_data: Mapping[str, Any], table: Table) -> Table:
    """Construct a table for displaying contract details."""
    for key, value in api_data.items():
        if isinstance(value, dict):
            table.add_row("")
            table.add_row(str(key), "")
            construct_table(value, table)
        elif isinstance(value, list):
            table.add_row("")
            table.add_row(str(key), "")
            for item in value:
                if isinstance(item, dict):
                    construct_table(item, table)
                else:
                    table.add_row(str(key), str(item))
            table.add_row("")
        else:
            table.add_row(str(key), str(value))
    return table


@app.command(name="details")
def get_my_contract_details(
    contract_id: Annotated[str, typer.Argument(help="Get my contract details")],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False,
) -> None:
    """Fetch and display details of my contract."""
    url: str = "https://api.spacetraders.io/v2/my/contracts/" + contract_id
    api_data: dict[str, Any] = {}
    api_data = send_get_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
    else:
        table: Table = Table(title="Contract Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        table = construct_table(api_data["data"], table)
        console.print(table)


@app.command(name="list")
def get_my_contracts_list(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of my contract."""
    api_url: str = "https://api.spacetraders.io/v2/my/contracts"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(api_url + "?page=1&limit=20")
    contract_list: list[dict[str, str | int]] = []
    contract_list.extend(api_data["data"])
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))

    if api_data["meta"]["total"] > api_data["meta"]["limit"]:
        while len(contract_list) < api_data["meta"]["total"]:
            url = f"{api_url}?page={api_data['meta']['page'] + 1}&limit=20"
            api_data = send_get_request(url)
            if json:
                console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
            contract_list.extend(api_data["data"])

    if not json:
        for index, item in enumerate(contract_list):
            table: Table = Table(title=f"Contract {index + 1} Summary")
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            table = construct_table(item, table)
            console.print(table)
