#!/usr/bin/env python3

from typing import Annotated

import requests
import typer
from requests.exceptions import HTTPError
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.read_agent_token import read_agent_token

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="details")
def get_my_agent_details(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of my agent."""
    agent_token: dict[str, str | int] = {}
    agent_token = read_agent_token()
    url: str = "https://api.spacetraders.io/v2/my/agent"
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
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Details"))
    else:
        table: Table = Table(title="Agent Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for key, value in api_data.items():
            table.add_row(str(key), str(value))
        console.print(table)


@app.command(name="events")
def get_my_agent_events() -> None:
    """Fetch and display events of my agent."""
    agent_token: dict[str, str | int] = {}
    agent_token = read_agent_token()
    url: str = "https://api.spacetraders.io/v2/my/agent/events"
    headers: dict[str, str] = {"Authorization": f"Bearer {agent_token['token']}", "Content-Type": "application/json"}
    response: requests.Response = requests.Response()
    api_data: list[dict[str, str | int]] = []
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
    if not api_data:
        console.print("No events found for this agent.")
    else:
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Events"))
