#!/usr/bin/env python3


import typer

from cosmic_slop_cli import __version__
from cosmic_slop_cli.console import console

app: typer.Typer = typer.Typer()


@app.callback()
def version(temp: bool = False) -> None:
    """Show the version and exit."""
    if temp:
        console.print(f"cosmic_slop_cli, version {__version__}")
