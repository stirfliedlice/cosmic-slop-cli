#!/usr/bin/env python3

import typer

from .get_supply_chain import app as get_supply_chain_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(get_supply_chain_app)
