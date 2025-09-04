#!/usr/bin/env python3

import typer

# import requests
# from cosmic_slop_cli.read_agent_token import read_agent_token
from cosmic_slop_cli.console import console

# from rich.panel import Panel
# from rich.json import JSON
# from rich.table import Table


app = typer.Typer()


@app.command()
def register_agent() -> None:
    console.print("post_register_agent called")


"""
import requests
from pathlib import Path
import json
import sys


def main() -> None:
    file_path: Path = Path.cwd() / "account_api_key.txt"
    api_key: str = ""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            api_key = file.read().strip()
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

    url: str = "https://api.spacetraders.io/v2/register"
    headers: dict = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data: dict = {
        "symbol": "QUAIL-CORSET",  # Replace with your desired agent symbol
        "faction": "COSMIC"  # Example faction
    }
    response: requests.Response = requests.Response()
    api_data: dict = {}
    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()  # Raises HTTPError for bad responses
        if response.status_code == 201:
            api_data = response.json()["data"]
        else:
            print(
                f"Failed to retrieve the web page. "
                f"Status code: {response.status_code}"
            )
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        print(f"Response: {response.text}")
        sys.exit(1)

    out_file_path: Path = Path.cwd() / "agent_info.json"
    try:
        with open(out_file_path, "w", encoding="utf-8") as out_file:
            json.dump(api_data, out_file, indent=4)
        print(f"Agent information written to {out_file_path}")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


if __name__ == "__main__":
    main()
"""
