#!/usr/bin/env python3

from collections.abc import Mapping
from typing import Any

import requests
import typer
from requests.exceptions import HTTPError
from rich.json import JSON
from rich.panel import Panel

from cosmic_slop_cli.console import console
from cosmic_slop_cli.read_agent_token import read_agent_token


def send_get_request(url: str) -> dict[str, Any]:
    """Send a GET request to the specified URL with authorization headers."""
    agent_token: dict[str, str | int] = {}
    agent_token = read_agent_token()
    headers: dict[str, str] = {}
    headers = {"Authorization": f"Bearer {agent_token['token']}", "Content-Type": "application/json"}
    response: requests.Response = requests.Response()
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        console.print(f"Request failed: {e}")
        if response.json():
            console.print(Panel.fit(JSON.from_data(response.json()), title="Response JSON"))
        else:
            console.print(f"Response: {response.text}")
        raise typer.Exit(code=1) from None


def send_post_request(
    url: str, headers: Mapping[str, Any] | None = None, data: Mapping[str, Any] | None = None
) -> dict[str, Any]:
    """Send a POST request to the specified URL with authorization headers."""
    agent_token: dict[str, str | int] = {}
    agent_token = read_agent_token()
    if headers is None:
        headers = {"Authorization": f"Bearer {agent_token['token']}", "Content-Type": "application/json"}
    response: requests.Response = requests.Response()
    try:
        if data is None:
            response = requests.post(url, headers=headers, timeout=30)
        else:
            response = requests.post(url, headers=headers, json=data, timeout=30)
        response.raise_for_status()
        return response.json()
    except HTTPError as e:
        console.print(f"Request failed: {e}")
        if response.json():
            console.print(Panel.fit(JSON.from_data(response.json()), title="Response JSON"))
        else:
            console.print(f"Response: {response.text}")
        raise typer.Exit(code=1) from None
