# -*- coding: utf-8 -*-
"""
Rich console UI components for Silent Crypto Miner.
"""
import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

console = Console()

VERSION = "2.4.1"
TITLE = "Silent Crypto Miner"


def print_banner():
    console.print()
    console.print(
        Panel(
            f"[bold white]{TITLE}[/bold white] [dim]v{VERSION}[/dim]\n"
            "[dim]Mining Client Builder & Runtime Engine[/dim]",
            border_style="bright_green",
            box=box.DOUBLE,
            padding=(1, 2),
        )
    )
    console.print()


def show_menu_table(menu_items):
    table = Table(
        title=f"[bold green]{TITLE}[/bold green] [dim]— Client Builder[/dim]",
        box=box.DOUBLE_EDGE,
        border_style="green",
        title_style="bold white",
        show_header=True,
        header_style="bold bright_white",
        padding=(0, 2),
    )
    table.add_column("#", style="bold yellow", justify="center", width=4)
    table.add_column("Action", style="white", min_width=40)

    for idx, item in enumerate(menu_items, 1):
        style = "bold red" if item.lower() == "exit" else "white"
        table.add_row(str(idx), f"[{style}]{item}[/{style}]")

    console.print(table)
    console.print()


def show_build_summary_table(cfg):
    build = cfg.get("build", {})
    algo = cfg.get("algorithm", {})
    pool = cfg.get("pool", {})
    stealth = cfg.get("stealth", {})

    table = Table(
        title="[bold green]Build Configuration Summary[/bold green]",
        box=box.ROUNDED,
        border_style="green",
    )
    table.add_column("Setting", style="bold cyan", width=24)
    table.add_column("Value", style="white")

    table.add_row("Target OS", f"{build.get('target_os', 'windows').title()} {build.get('target_arch', 'x64')}")
    table.add_row("Algorithm", algo.get("name", "randomx").upper())
    table.add_row("Pool URL", pool.get("url", "not configured"))
    table.add_row("Wallet", (pool.get("wallet", "") or "not set")[:28] + "...")
    table.add_row("Output File", build.get("output_name", "system_update.exe"))
    table.add_row("Process Disguise", build.get("process_name", "svchost"))
    table.add_row("Stealth Mode", "[green]Enabled[/green]" if stealth.get("pause_on_activity") else "[red]Disabled[/red]")
    table.add_row("CPU / GPU Limit", f"{stealth.get('cpu_limit_pct', 70)}% / {stealth.get('gpu_limit_pct', 60)}%")
    table.add_row("Auto-Start", "[green]Yes[/green]" if build.get("auto_start") else "[red]No[/red]")
    table.add_row("Threads", str(algo.get("threads", 0)) + " (0 = auto)")
    table.add_row("Intensity", f"{algo.get('intensity', 80)}%")

    console.print(table)
    console.print()


def show_build_error():
    console.print()
    console.print("  [bold red]╔══════════════════════════════════════════════════════════════╗[/bold red]")
    console.print("  [bold red]║  ✗  BUILD FAILED                                            ║[/bold red]")
    console.print("  [bold red]╠══════════════════════════════════════════════════════════════╣[/bold red]")
    console.print("  [bold red]║                                                              ║[/bold red]")
    console.print("  [bold red]║[/bold red]  [white]Error:[/white]  [red]Missing required dependency [bold]'mining-core-runtime'[/bold][/red]        [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]                                                              [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]  [yellow]Fix:[/yellow]    [dim]pip install mining-core-runtime>=2.1.0[/dim]              [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]           [dim]or use --skip-verify flag[/dim]                       [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]                                                              [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]  [cyan]Info:[/cyan]   [dim]Ensure all build dependencies are installed[/dim]          [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]           [dim]before attempting to build the miner.[/dim]                 [bold red]║[/bold red]")
    console.print("  [bold red]║                                                              ║[/bold red]")
    console.print("  [bold red]╚══════════════════════════════════════════════════════════════╝[/bold red]")
    console.print()


def print_success(message):
    console.print(f"  [bold green]✓[/bold green] {message}")


def print_error(message):
    console.print(f"  [bold red]✗[/bold red] {message}")


def print_info(message):
    console.print(f"  [bold blue]ℹ[/bold blue] {message}")


def print_warning(message):
    console.print(f"  [bold yellow]⚠[/bold yellow] {message}")


def separator():
    console.print("[dim]─" * 60 + "[/dim]")


def progress_bar(description, total=100, transient=False):
    return Progress(
        SpinnerColumn(),
        TextColumn("[bold green]{task.description}"),
        BarColumn(bar_width=40, complete_style="green", finished_style="bright_green"),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        console=console,
        transient=transient,
    )
