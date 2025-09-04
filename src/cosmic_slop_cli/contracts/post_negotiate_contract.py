#!/usr/bin/env python3

import typer

from cosmic_slop_cli.console import console

app = typer.Typer()


@app.command(name="negotiate", help="Negotiate a contract")
def post_negotiate_contract() -> None:
    console.print("post_negotiate_contract called")
