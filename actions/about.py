# -*- coding: utf-8 -*-
"""About action — project info, features, requirements for Silent Crypto Miner."""

from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.ui import console


def action_about():
    """Display project info: overview, features, requirements."""
    features_table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.SIMPLE,
        title="[bold bright_green] ◈ FEATURES ◈ [/]",
        title_style="bright_green",
    )
    features_table.add_column("Feature", style="bright_green")
    features_table.add_column("Status", justify="center", style="bright_cyan")

    for feat in [
        "Multi-algorithm support — RandomX, Ethash, KawPow, KHeavyHash",
        "CPU and GPU mining with auto-detection",
        "Stealth mode — auto-pause on system activity",
        "Pool failover with automatic switching",
        "Real-time hashrate and temperature monitoring",
        "Profitability tracker with earnings history",
        "Mining schedule with time-based activation",
        "Remote web dashboard for monitoring",
        "Session persistence and history tracking",
        "Cross-platform support (Win/Linux/macOS)",
        "Rich terminal UI with live statistics",
        "Resource management with thermal protection",
    ]:
        features_table.add_row(feat, "✓")

    algo_table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.MINIMAL_HEAVY_HEAD,
        title="[bold bright_cyan] ◈ SUPPORTED ALGORITHMS ◈ [/]",
        title_style="bright_cyan",
    )
    algo_table.add_column("Algorithm", style="bright_cyan")
    algo_table.add_column("Type", style="dim")
    algo_table.add_column("Primary Coin", style="bright_white")

    algo_table.add_row("RandomX", "CPU", "Monero (XMR)")
    algo_table.add_row("Ethash", "GPU", "Ethereum Classic (ETC)")
    algo_table.add_row("KawPow", "GPU", "Ravencoin (RVN)")
    algo_table.add_row("KHeavyHash", "GPU", "Kaspa (KAS)")
    algo_table.add_row("Autolykos2", "GPU", "Ergo (ERG)")
    algo_table.add_row("Cryptonight-V8", "CPU/GPU", "MoneroV")
    algo_table.add_row("Zhash", "GPU", "Bitcoin Gold (BTG)")

    setup_table = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="magenta",
        box=box.MINIMAL_HEAVY_HEAD,
        title="[bold bright_magenta] ◈ REQUIREMENTS & SETUP ◈ [/]",
        title_style="bright_magenta",
    )
    setup_table.add_column("Item", style="bright_magenta")
    setup_table.add_column("Note", style="dim")
    setup_table.add_row("Python", "3.10 or higher")
    setup_table.add_row("pip", "Latest version recommended")
    setup_table.add_row("Libraries", "rich, cryptography, psutil, requests, schedule, aiohttp")
    setup_table.add_row("Install", "pip install -r requirements.txt")
    setup_table.add_row("Run", "python main.py")
    setup_table.add_row("Hardware", "Any modern CPU; GPU optional but recommended")

    console.print()
    console.print(Panel(features_table, border_style="green", box=box.ROUNDED))
    console.print()
    console.print(Panel(algo_table, border_style="cyan", box=box.ROUNDED))
    console.print()
    console.print(Panel(setup_table, border_style="magenta", box=box.ROUNDED))
    console.print()
    console.print(
        "[dim]Silent Crypto Miner — advanced multi-algorithm mining with stealth mode "
        "and intelligent resource management. Configure pool and wallet in Settings to begin.[/]"
    )
    console.print()
    console.print("[dim]Contact:[/] [bright_green]0x7a3B1c9E45d82f06aD3e17C4b58F92d1A60cE834[/] (ETH/EVM)")
    console.print()
