#!/usr/bin/env python3

from typing import Annotated

import typer

from cosmic_slop_cli.console import console

app: typer.Typer = typer.Typer(no_args_is_help=True)


@app.command(name="my")
def get_my_faction_details(json: Annotated[bool, typer.Option(help="Output details in JSON format")] = False) -> None:
    """Fetch and display details of my faction."""
    url: str = "https://api.spacetraders.io/v2/my/factions"
    console.print("Fetching my faction details from " + url)
