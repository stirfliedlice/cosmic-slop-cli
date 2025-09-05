#!/usr/bin/env python3

from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_get_request

app: typer.Typer = typer.Typer()


@app.command(name="details")
def get_public_agent_details(
    agent_symbol: Annotated[str, typer.Argument()],
    json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False,
) -> None:
    """Fetch and display details of a public agent by symbol."""
    url: str = f"https://api.spacetraders.io/v2/agents/{agent_symbol}"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(url)
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Details"))
    else:
        table = Table(title="Agent Summary")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for key, value in api_data["data"].items():
            table.add_row(str(key), str(value))
        console.print(table)


@app.command(name="all")
def get_all_public_agents(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display a list of all public agents."""
    api_url: str = "https://api.spacetraders.io/v2/agents"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(api_url + "?page=1&limit=20")
    agent_list: list[dict[str, str | int]] = []
    agent_list.extend(api_data["data"])
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title=f"Agent Details Page {api_data['meta']['page']}"))

    if api_data["meta"]["total"] > api_data["meta"]["limit"]:
        while len(agent_list) < api_data["meta"]["total"]:
            url = f"{api_url}?page={api_data['meta']['page'] + 1}&limit=20"
            api_data = send_get_request(url)
            if json:
                console.print(
                    Panel.fit(JSON.from_data(api_data), title=f"Agent Details Page {api_data['meta']['page']}")
                )
            agent_list.extend(api_data["data"])

    if not json:
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
        console.print(f"Total Agents: {api_data['meta']['total']}")
