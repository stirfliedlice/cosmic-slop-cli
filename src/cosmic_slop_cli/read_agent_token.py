#!/usr/bin/env python3


import json
from pathlib import Path


def read_agent_token() -> dict[str, str | int]:
    """does stuff"""
    file_path: Path = Path.cwd() / "agent_info.json"
    agent_info: dict[str, str | int] = {}
    try:
        with open(file_path, encoding="utf-8") as file:
            agent_info = json.load(file)
            return agent_info
    except FileNotFoundError:
        print(f"Error: The file {file_path} was not found.")
        return agent_info
    except Exception as e:
        print(f"An error occurred: {e}")
        return agent_info
