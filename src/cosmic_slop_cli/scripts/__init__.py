#!/usr/bin/env python3

import typer

from .mining_drone import app as mining_drone_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(mining_drone_app)
