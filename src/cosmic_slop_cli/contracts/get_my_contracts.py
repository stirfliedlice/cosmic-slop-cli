#!/usr/bin/env python3

from typing import Annotated, Any

import requests
import typer
from requests.exceptions import HTTPError
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.read_agent_token import read_agent_token

app: typer.Typer = typer.Typer(no_args_is_help=True)


def construct_table(api_data: dict[str, Any], table: Table) -> Table:
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


@app.command(name="details", help="Get my contract details")
def get_my_contract_details(
    contract_id: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False,
) -> None:
    """Fetch and display details of my contract."""
    agent_token: dict[str, str | int] = {}
    agent_token = read_agent_token()
    url: str = "https://api.spacetraders.io/v2/my/contracts/" + contract_id
    headers: dict[str, str] = {"Authorization": f"Bearer {agent_token['token']}", "Content-Type": "application/json"}
    response: requests.Response = requests.Response()
    api_data: dict[str, str | int] = {}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        api_data = response.json()["data"]
    except HTTPError as e:
        console.print(f"Request failed: {e}")
        if response.json():
            console.print(Panel.fit(JSON.from_data(response.json()), title="Response JSON"))
        else:
            console.print(f"Response: {response.text}")
        raise typer.Exit(code=1) from None
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
    else:
        table: Table = Table(title="Contract Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        table = construct_table(api_data, table)
        console.print(table)


@app.command(name="list", help="Get my contracts list")
def get_my_contracts_list(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of my contract."""
    agent_token: dict[str, str | int] = {}
    agent_token = read_agent_token()
    url: str = "https://api.spacetraders.io/v2/my/contracts"
    headers: dict[str, str] = {"Authorization": f"Bearer {agent_token['token']}", "Content-Type": "application/json"}
    response: requests.Response = requests.Response()
    api_data: dict[str, str | int] = {}
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        api_data = response.json()["data"]
    except HTTPError as e:
        console.print(f"Request failed: {e}")
        if response.json():
            console.print(Panel.fit(JSON.from_data(response.json()), title="Response JSON"))
        else:
            console.print(f"Response: {response.text}")
        raise typer.Exit(code=1) from None
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Contract Details"))
    else:
        for index, item in enumerate(api_data):
            table: Table = Table(title=f"Contract {index + 1} Summary")
            table.add_column("Key", style="cyan", no_wrap=True)
            table.add_column("Value", style="magenta")
            table = construct_table(item, table)
            console.print(table)
