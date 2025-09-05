#!/usr/bin/env python3

import json as libjson
from pathlib import Path
from typing import Annotated, Any

import typer
from rich.json import JSON
from rich.panel import Panel

from cosmic_slop_cli.console import console
from cosmic_slop_cli.read_agent_token import read_account_token
from cosmic_slop_cli.send_request import send_post_request

app = typer.Typer()


@app.command(name="register")
def register_agent(
    agent_symbol: Annotated[str, typer.Argument(help="Agent symbol")] = "QUAIL-CORSET",
    faction: Annotated[str, typer.Argument(help="Faction to join")] = "COSMIC",
    json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False,
) -> None:
    """Register a new agent with the SpaceTraders API."""
    url: str = "https://api.spacetraders.io/v2/register"
    account_toker: str = read_account_token()
    headers: dict[str, str] = {}
    headers = {"Authorization": f"Bearer {account_toker}", "Content-Type": "application/json"}
    data = {"symbol": agent_symbol, "faction": faction}
    api_data: dict[str, Any] = {}
    api_data = send_post_request(url, headers, data)

    out_file_path: Path = Path.cwd() / "agent_info.json"
    try:
        with open(out_file_path, "w", encoding="utf-8") as out_file:
            libjson.dump(api_data, out_file, indent=4)
        print(f"Agent information written to {out_file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    if json:
        console.print(Panel.fit(JSON.from_data(api_data), title="Agent Details"))
