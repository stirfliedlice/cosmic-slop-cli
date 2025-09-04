#!/usr/bin/env python3

from typing import Annotated

import requests
import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.read_agent_token import read_agent_token

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="details", help="Get my contract details")
def get_my_contract_details(
    contract_id: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False,
) -> None:
    """Fetch and display details of my contract."""
    # print("get_my_contract_details called with contract_id:", contract_id)
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
    except requests.exceptions.RequestException as e:
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
        # for key, value in api_data.items():
        #     table.add_row(str(key), str(value))
        console.print(table)


@app.command(name="list", help="Get my contracts list")
def get_my_contracts_list() -> None:
    print("get_my_contracts_list called")
