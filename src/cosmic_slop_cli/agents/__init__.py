#!/usr/bin/env python3

import typer

from .get_my_agents import app as get_my_agents_app
from .get_public_agents import app as get_public_agents_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(get_my_agents_app, name="my", help="Commands to manage your agents")
app.add_typer(get_public_agents_app, name="public", help="Commands to view public agents")
