#!/usr/bin/env python3

from typing import Annotated

import requests
import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console

app: typer.Typer = typer.Typer()


@app.command(name="details")
def get_public_agent_details(
    agent_symbol: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False,
) -> None:
    """Fetch and display details of a public agent by symbol."""
    url: str = f"https://api.spacetraders.io/v2/agents/{agent_symbol}"
    response: requests.Response = requests.Response()
    api_data: dict[str, str | int] = {}
    try:
        response = requests.get(url, timeout=10)
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
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Details"))
    else:
        table = Table(title="Agent Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for key, value in api_data.items():
            table.add_row(str(key), str(value))
        console.print(table)


@app.command(name="all")
def get_all_public_agents(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display a list of all public agents."""
    # print("list_public_agents called")
    url: str = "https://api.spacetraders.io/v2/agents"
    response: requests.Response = requests.Response()
    api_data: list[dict[str, str | int]] = []
    total_agents: int = 100  # Placeholder for total agents
    page: int = 1
    agent_list: list[dict[str, str | int]] = []
    while len(agent_list) < total_agents:
        try:
            url = f"https://api.spacetraders.io/v2/agents?page={page}&limit=20"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            api_data = response.json()["data"]
            total_agents = response.json()["meta"]["total"]
            agent_list.extend(api_data)
            page += 1
        except requests.exceptions.RequestException as e:
            console.print(f"Request failed: {e}")
            if response.json():
                console.print(Panel.fit(JSON.from_data(response.json()), title="Response JSON"))
            else:
                console.print(f"Response: {response.text}")
            raise typer.Exit(code=1) from None
    if json:
        console.print(Panel.fit(JSON.from_data(agent_list), title="Agent Details"))
    else:
        table = Table(title="Agent Summary")
        table.add_column("symbol")
        table.add_column("headquarters", justify="center")
        table.add_column("credits", justify="right")
        table.add_column("startingFaction")
        table.add_column("shipCount", justify="right")
        for item in agent_list:
            table.add_row(
                str(item.get("symbol", "")),
                str(item.get("headquarters", "")),
                str(item.get("credits", "")),
                str(item.get("startingFaction", "")),
                str(item.get("shipCount", "")),
            )
        console.print(table)
