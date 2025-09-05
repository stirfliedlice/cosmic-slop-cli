#!/usr/bin/env python3

import typer

from .get_faction_details import app as get_faction_details_app
from .get_my_factions import app as get_my_factions_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(get_faction_details_app, name="details", help="Commands to view faction details")
app.add_typer(get_my_factions_app)
