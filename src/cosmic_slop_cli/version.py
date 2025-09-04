#!/usr/bin/env python3


import typer
from spacetrader_cli import __version__
from spacetrader_cli.console import console

app: typer.Typer = typer.Typer()


@app.callback()
def version(temp: bool = False) -> None:
    """Show the version and exit."""
    if temp:
        console.print(f"spacetrader_cli, version {__version__}")
