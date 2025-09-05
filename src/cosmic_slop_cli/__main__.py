#!/usr/bin/env python3

from typing import Annotated

import typer

from cosmic_slop_cli import __version__
from cosmic_slop_cli.console import console

from .agents import app as agents_app
from .contracts import app as contracts_app
from .data import app as data_app
from .factions import app as factions_app
from .post_register_agent import app as post_register_agent_app
from .scripts.mining_drone import app as mining_drone_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(post_register_agent_app)
app.add_typer(agents_app, name="agents", help="Commands to manage and view agents")
app.add_typer(contracts_app, name="contracts", help="Commands to manage and view contracts")
app.add_typer(factions_app, name="factions", help="Commands to view factions")
app.add_typer(data_app, name="data", help="Commands to view game data")
app.add_typer(mining_drone_app)


@app.callback(invoke_without_command=True, help="SpaceTrader CLI")
def main(version: Annotated[bool, typer.Option("--version", "-v", help="Show the version and exit.")] = False) -> None:
    """Show the version and exit."""
    if version:
        console.print(f"cosmic_slop_cli, version {__version__}")


if __name__ == "__main__":
    console.print("[bold green]SpaceTrader CLI[/bold green]")
    app()
