# -*- coding: utf-8 -*-
"""Pool connection manager — stratum protocol, failover, and latency monitoring."""

import random
import time
from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from engine.ui import console, print_info, print_success, print_warning, print_error, separator


POOLS = {
    "nanopool": {
        "name": "Nanopool",
        "url": "stratum+ssl://xmr.nanopool.org:14433",
        "fee": "1.0%",
        "min_payout": "0.1 XMR",
        "protocols": ["stratum+tcp", "stratum+ssl"],
    },
    "supportxmr": {
        "name": "SupportXMR",
        "url": "stratum+tcp://pool.supportxmr.com:3333",
        "fee": "0.9%",
        "min_payout": "0.3 XMR",
        "protocols": ["stratum+tcp"],
    },
    "p2pool": {
        "name": "P2Pool",
        "url": "stratum+tcp://localhost:3333",
        "fee": "0%",
        "min_payout": "Dynamic",
        "protocols": ["p2p", "stratum"],
    },
    "hashvault": {
        "name": "Hashvault",
        "url": "stratum+ssl://randomx.hashvault.pro:443",
        "fee": "1.0%",
        "min_payout": "0.3 XMR",
        "protocols": ["stratum+tcp", "stratum+ssl"],
    },
    "2miners": {
        "name": "2Miners",
        "url": "stratum+ssl://etc.2miners.com:1010",
        "fee": "1.0%",
        "min_payout": "Varies",
        "protocols": ["stratum+tcp", "stratum+ssl"],
    },
}


def simulate_pool_connection(pool_key: str = None) -> dict:
    """Simulate connecting to a mining pool."""
    if pool_key and pool_key in POOLS:
        pool = POOLS[pool_key]
    else:
        pool = random.choice(list(POOLS.values()))

    latency = round(random.uniform(15, 180), 1)
    workers = random.randint(1, 16)
    difficulty = random.randint(100000, 500000)

    return {
        "pool": pool["name"],
        "url": pool["url"],
        "latency_ms": latency,
        "workers": workers,
        "difficulty": difficulty,
        "status": "Connected" if latency < 150 else "High Latency",
    }


def show_pool_list():
    """Display available pools in a formatted table."""
    table = Table(
        show_header=True,
        header_style="bold bright_blue",
        border_style="blue",
        box=box.ROUNDED,
        title="[bold bright_blue] AVAILABLE POOLS [/]",
    )
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Pool", style="bright_blue")
    table.add_column("Protocols", style="dim")
    table.add_column("Fee", justify="center", style="bright_cyan")
    table.add_column("Min Payout", style="bright_white")

    for i, (key, pool) in enumerate(POOLS.items(), 1):
        table.add_row(
            str(i),
            pool["name"],
            ", ".join(pool["protocols"]),
            pool["fee"],
            pool["min_payout"],
        )

    console.print()
    console.print(table)
    console.print()


def connect_to_pool(pool_key: str = None):
    """Simulate pool connection with progress animation."""
    console.print()
    print_info("Initiating pool connection...")

    with Progress(
        SpinnerColumn(style="bright_green"),
        TextColumn("[bright_green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bright_cyan"),
        console=console,
    ) as progress:
        task = progress.add_task("Connecting...", total=5)
        for step in [
            "Resolving pool address...",
            "Establishing TLS handshake...",
            "Authenticating worker...",
            "Subscribing to mining notifications...",
            "Connection established.",
        ]:
            progress.update(task, description=step)
            time.sleep(0.3)
            progress.advance(task)

    result = simulate_pool_connection(pool_key)

    status_table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.ROUNDED,
        title="[bold bright_green] POOL STATUS [/]",
    )
    status_table.add_column("Property", style="bright_green")
    status_table.add_column("Value", justify="right", style="bright_white")

    status_color = "bright_green" if result["latency_ms"] < 100 else "yellow"
    status_table.add_row("Pool", result["pool"])
    status_table.add_row("URL", result["url"])
    status_table.add_row("Latency", f"{result['latency_ms']} ms")
    status_table.add_row("Active Workers", str(result["workers"]))
    status_table.add_row("Network Difficulty", f"{result['difficulty']:,}")
    status_table.add_row("Status", f"[{status_color}]{result['status']}[/]")

    console.print()
    console.print(status_table)
    console.print()
    return result
