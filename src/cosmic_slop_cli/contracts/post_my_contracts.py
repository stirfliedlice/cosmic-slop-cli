#!/usr/bin/env python3

from typing import Annotated

import typer

from cosmic_slop_cli.console import console

app = typer.Typer()


@app.command()
def post_accept_my_contracts() -> None:
    console.print("post_accept_my_contracts called")


@app.command()
def post_deliver_contract_cargo() -> None:
    console.print("post_deliver_contract_cargo called")


@app.command()
def get_my_contract_details(contract_id: Annotated[str, typer.Argument()]) -> None:
    console.print("get_my_contract_details called with contract_id:", contract_id)
