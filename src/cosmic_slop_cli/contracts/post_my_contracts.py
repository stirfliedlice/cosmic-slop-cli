#!/usr/bin/env python3

from typing import Annotated

import typer

from cosmic_slop_cli.console import console

app = typer.Typer()


@app.command(name="accept", help="Accept a contract")
def post_accept_contracts() -> None:
    console.print("post_accept_contracts called")


@app.command(name="deliver", help="Deliver contract cargo")
def post_deliver_contract_cargo() -> None:
    console.print("post_deliver_contract_cargo called")


@app.command(name="fulfill", help="Fulfill a contract")
def post_fulfill_contracts(contract_id: Annotated[str, typer.Argument()]) -> None:
    console.print("post_fulfill_contracts called with contract_id:", contract_id)
