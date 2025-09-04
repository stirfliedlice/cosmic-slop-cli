#!/usr/bin/env python3

import typer

from .get_my_contracts import app as get_my_contracts_app
from .post_my_contracts import app as post_my_contracts_app
from .post_negotiate_contract import app as post_negotiate_contract_app

app = typer.Typer(no_args_is_help=True)

app.add_typer(get_my_contracts_app)
app.add_typer(post_my_contracts_app)
app.add_typer(post_negotiate_contract_app)
