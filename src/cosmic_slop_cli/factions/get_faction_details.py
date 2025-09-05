#!/usr/bin/env python3

from typing import Annotated

import typer

from cosmic_slop_cli.console import console

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="list")
def get_all_factions(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display all factions."""
    url: str = "https://api.spacetraders.io/v2/"
    console.print(f"Fetching all factions from {url}factions")


@app.command(name="details")
def get_faction_details(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of a factions."""
    url: str = "https://api.spacetraders.io/v2/"
    console.print(f"Fetching faction details from {url}factions/{{factionSymbol}}")
