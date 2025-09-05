#!/usr/bin/env python3

from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_get_request

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="my")
def get_my_faction_details(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of my faction."""
    api_url: str = "https://api.spacetraders.io/v2/my/factions"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(api_url + "?page=1&limit=20")
    faction_list: list[dict[str, str | int]] = []
    faction_list.extend(api_data["data"])
    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title=f"My Factions Page {api_data['meta']['page']}"))

    if api_data["meta"]["total"] > api_data["meta"]["limit"]:
        while len(faction_list) < api_data["meta"]["total"]:
            url = f"{api_url}?page={api_data['meta']['page'] + 1}&limit=20"
            api_data = send_get_request(url)
            if json:
                console.print(Panel.fit(JSON.from_data(api_data), title=f"My Factions Page {api_data['meta']['page']}"))
            faction_list.extend(api_data["data"])

    if not json:
        table: Table = Table(title="My Factions")
        table.add_column("Key", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for item in faction_list:
            for key, value in item.items():
                table.add_row(str(key), str(value))
        if len(faction_list) > 1:
            table.add_row("", "")
        console.print(table)
