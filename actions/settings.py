# -*- coding: utf-8 -*-
"""Settings action — pool, mining, resource configuration display."""

from pathlib import Path

from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.ui import console, print_info, print_warning


def action_settings():
    """Display setup instructions: config.json fields."""
    table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.ROUNDED,
        title="[bold bright_green] ◈ CONFIGURATION ◈ [/]",
        title_style="bright_green",
    )
    table.add_column("Setting", style="bright_green")
    table.add_column("Section", style="bright_cyan")
    table.add_column("Description", style="dim")
    table.add_column("Example", style="bright_black")

    table.add_row("pool.url", "pool", "Stratum pool URL", "stratum+ssl://xmr.nanopool.org:14433")
    table.add_row("pool.wallet", "pool", "Mining wallet address", "4xMR...wallet")
    table.add_row("pool.worker", "pool", "Worker name", "rig-01")
    table.add_row("pool.algorithm", "pool", "Mining algorithm", "randomx / ethash")
    table.add_row("mining.threads", "mining", "CPU threads (0=auto)", "0")
    table.add_row("mining.intensity", "mining", "Utilization %", "80")
    table.add_row("mining.gpu_enabled", "mining", "GPU mining toggle", "true")
    table.add_row("resources.max_cpu_temp", "resources", "CPU thermal limit", "85")
    table.add_row("resources.max_gpu_temp", "resources", "GPU thermal limit", "80")
    table.add_row("resources.schedule", "resources", "Mining schedule", "00:00-08:00")

    panel = Panel(
        table,
        title="[bold bright_green] Silent Crypto Miner Settings [/]",
        border_style="bright_green",
        box=box.DOUBLE,
    )

    console.print()
    console.print(panel)

    base_dir = Path(__file__).parent.parent
    config_path = base_dir / "config.json"

    console.print()
    console.print("[dim]Configuration file:[/]")
    console.print(f"  [bright_green]config.json[/]  → {config_path}")
    console.print()
    console.print(
        "[bright_green]Pool configuration in config.json:[/]\n"
        '  • [dim]Set pool.url, pool.wallet, pool.worker[/]\n'
        "  • Add failover pools in pool.failover array\n"
        "  • Choose algorithm: randomx, ethash, kawpow, kheavyhash"
    )
    console.print()
    print_warning("Never share your wallet address publicly. Keep config.json secure.")
    print_info("Edit config files with any text editor (e.g. VS Code, Notepad).")
