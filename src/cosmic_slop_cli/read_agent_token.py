#!/usr/bin/env python3

import json
from pathlib import Path

import typer

from cosmic_slop_cli.console import console


def read_agent_token() -> dict[str, str | int]:
    """does stuff"""
    file_path: Path = Path.cwd() / "agent_info.json"
    agent_info: dict[str, str | int] = {}
    try:
        with open(file_path, encoding="utf-8") as file:
            agent_info = json.load(file)
            return agent_info
    except FileNotFoundError:
        console.print(f"Error: The file {file_path} was not found.")
        raise typer.Exit(code=1) from None
    except Exception as e:
        console.print(f"An error occurred: {e}")
        raise typer.Exit(code=1) from None
