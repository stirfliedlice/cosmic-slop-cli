#!/usr/bin/env python3

from typing import Annotated

import typer

from cosmic_slop_cli import __version__
from cosmic_slop_cli.console import console

app = typer.Typer(no_args_is_help=True)


@app.callback(invoke_without_command=True, help="SpaceTrader CLI")
def main(version: Annotated[bool, typer.Option("--version", "-v", help="Show the version and exit.")] = False) -> None:
    """Show the version and exit."""
    if version:
        console.print(f"cosmic_slop_cli, version {__version__}")


if __name__ == "__main__":
    console.print("[bold green]SpaceTrader CLI[/bold green]")
    app()
