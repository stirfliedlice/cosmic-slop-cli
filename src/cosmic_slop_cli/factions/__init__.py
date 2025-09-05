#!/usr/bin/env python3

import typer

from .get_faction_details import app as get_faction_details_app
from .get_my_factions import app as get_my_factions_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(get_faction_details_app)
app.add_typer(get_my_factions_app)
