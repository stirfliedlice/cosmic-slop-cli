#!/usr/bin/env python3

import logging
import os
from pathlib import Path
from typing import Any

import typer
from rich import print as rprint
from rich.table import Table

from cosmic_slop_cli.console import console
from cosmic_slop_cli.send_request import send_get_request, send_post_request

app: typer.Typer = typer.Typer(no_args_is_help=True)

logger = logging.getLogger(__name__)
file_path = Path.cwd() / "temp" / "app.log"
file_handler = logging.FileHandler(file_path, mode="a", encoding="utf-8")
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    "{asctime} - {levelname} - {message}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)


def find_marketplace():
    api_url: str = "https://api.spacetraders.io/v2/systems/X1-C30/waypoints"
    api_data: dict[str, Any] = {}
    api_data = send_get_request(api_url + "?traits=MARKETPLACE&page=1&limit=20")
    marketplace_list: list[dict[str, str | int]] = []
    marketplace_list.extend(api_data["data"])

    if api_data["meta"]["total"] > api_data["meta"]["limit"]:
        while len(marketplace_list) < api_data["meta"]["total"]:
            url = f"{api_url}?traits=MARKETPLACE&page={api_data['meta']['page'] + 1}&limit=20"
            api_data = send_get_request(url)
            marketplace_list.extend(api_data["data"])

    out_file_path: Path = Path.cwd() / "temp" / "marketplace.txt"
    try:
        with open(out_file_path, "w", encoding="utf-8") as out_file:
            for item in marketplace_list:
                out_file.write(f"{item},\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    return marketplace_list


def get_market_data(marketplace_list):
    market_goods = []
    for item in marketplace_list:
        api_url: str = f"https://api.spacetraders.io/v2/systems/X1-C30/waypoints/{item['symbol']}/market"
        api_data = send_get_request(api_url)
        market_goods.append(api_data["data"])

    out_file_path: Path = Path.cwd() / "temp" / "market_goods.txt"
    try:
        with open(out_file_path, "w", encoding="utf-8") as out_file:
            for item in market_goods:
                out_file.write(f"{item},\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

    return market_goods


def market_good_table(marketplace_list, market_goods):
    table = Table(title="Mining Drone Market Data")
    table.add_column("Symbol", justify="left", style="cyan", no_wrap=True)
    table.add_column("Type", justify="center", style="green")
    table.add_column("X", justify="right", style="magenta")
    table.add_column("Y", justify="right", style="magenta")
    table.add_column("Export", justify="right", style="yellow")
    table.add_column("Import", justify="right", style="yellow")
    table.add_column("Exchange", justify="right", style="yellow")

    for index, item in enumerate(marketplace_list):
        exports = ""
        imports = ""
        exchange = ""
        for jtem in market_goods[index]["exports"]:
            exports += jtem["symbol"] + "\n"
        for jtem in market_goods[index]["imports"]:
            imports += jtem["symbol"] + "\n"
        for jtem in market_goods[index]["exchange"]:
            exchange += jtem["symbol"] + "\n"
        table.add_row(
            item["symbol"],
            item["type"],
            str(item["x"]),
            str(item["y"]),
            str(exports),
            str(imports),
            str(exchange),
        )

    console.print(table)

    out_file_path: Path = Path.cwd() / "temp" / "market_goods_table.txt"
    try:
        with open(out_file_path, "w", encoding="utf-8") as out_file:
            rprint(table, file=out_file)
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")


def market_data_script():
    out_file_path: Path = Path.cwd() / "temp" / "marketplace.txt"
    if not os.path.exists(out_file_path):
        marketplace_list = find_marketplace()
    else:
        marketplace_list = []
        try:
            with open(out_file_path, encoding="utf-8") as out_file:
                for line in out_file:
                    item = line.strip().rstrip(",")
                    if item:
                        marketplace_list.append(item)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    out_file_path: Path = Path.cwd() / "temp" / "market_goods.txt"
    if not os.path.exists(out_file_path):
        market_goods = get_market_data(marketplace_list)
    else:
        market_goods = []
        try:
            with open(out_file_path, encoding="utf-8") as out_file:
                for line in out_file:
                    item = line.strip().rstrip(",")
                    if item:
                        market_goods.append(item)
        except Exception as e:
            print(f"An error occurred while reading the file: {e}")

    out_file_path: Path = Path.cwd() / "temp" / "market_goods_table.txt"
    if not os.path.exists(out_file_path):
        market_good_table(marketplace_list, market_goods)


@app.command(name="mining-drone")
def mining_drone_loop() -> None:
    """Fetch and display details of ."""

    market_data_script()

    url = "https://api.spacetraders.io/v2/my/ships/QUAIL-CORSET-3/nav"
    api_data = send_get_request(url)
    if api_data["data"]["status"] == "IN_TRANSIT":
        pass
    elif api_data["data"]["status"] == "IN_ORBIT":
        console.print("Ship is in orbit, need to dock")
        url = "https://api.spacetraders.io/v2/my/ships/QUAIL-CORSET-3/dock"
        api_data = send_get_request(url)
        console.print(api_data)
    elif api_data["data"]["status"] == "DOCKED":
        console.print("Ship is docked, can perform actions")
        url = "https://api.spacetraders.io/v2/my/ships/QUAIL-CORSET-3/warp"
        payload = {"waypointSymbol": "X1-C30-43-4A"}
        api_data = send_post_request(url, payload)
        console.print(api_data)
    else:
        console.print(f"Ship status is {api_data['data']['status']}")

    raise typer.Exit()
