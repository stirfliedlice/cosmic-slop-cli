#!/usr/bin/env python3

import typer
from rich import rprint

app = typer.Typer()


@app.command()
def post_negotiate_contract() -> None:
    rprint("post_negotiate_contract called")
