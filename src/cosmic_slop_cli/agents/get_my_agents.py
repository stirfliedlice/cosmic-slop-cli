#!/usr/bin/env python3

from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_get_request

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="details")
def get_my_agent_details(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of my agent."""
    url: str = "https://api.spacetraders.io/v2/my/agent"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Details"))
    else:
        table: Table = Table(title="Agent Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for key, value in api_data["data"].items():
            table.add_row(str(key), str(value))
        console.print(table)


@app.command(name="events")
def get_my_agent_events(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display events of my agent."""
    url: str = "https://api.spacetraders.io/v2/my/agent/events"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Details"))
    if not api_data["data"]:
        console.print("No events found for this agent.")
    else:
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Events"))
