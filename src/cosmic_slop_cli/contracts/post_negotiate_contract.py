#!/usr/bin/env python3

import typer

from cosmic_slop_cli.console import console

app = typer.Typer()


@app.command()
def post_negotiate_contract() -> None:
    console.print("post_negotiate_contract called")
