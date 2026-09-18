# -*- coding: utf-8 -*-
"""Hash algorithm manager — algorithm registry, benchmarking, and selection."""

import random
import time

from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.ui import console, print_info, print_success, separator


ALGORITHMS = {
    "randomx": {
        "name": "RandomX",
        "type": "CPU",
        "coins": ["Monero (XMR)"],
        "description": "CPU-optimized PoW algorithm, ASIC-resistant",
        "efficiency": 5,
    },
    "ethash": {
        "name": "Ethash",
        "type": "GPU",
        "coins": ["Ethereum Classic (ETC)", "EthereumPoW (ETHW)"],
        "description": "Memory-hard GPU algorithm with DAG generation",
        "efficiency": 4,
    },
    "cryptonight_v8": {
        "name": "Cryptonight-V8",
        "type": "CPU/GPU",
        "coins": ["MoneroV", "BitTube"],
        "description": "Legacy Monero algorithm, CPU and GPU compatible",
        "efficiency": 4,
    },
    "kawpow": {
        "name": "KawPow",
        "type": "GPU",
        "coins": ["Ravencoin (RVN)"],
        "description": "Memory-hard algorithm optimized for GPU mining",
        "efficiency": 3,
    },
    "kheavyhash": {
        "name": "KHeavyHash",
        "type": "GPU",
        "coins": ["Kaspa (KAS)"],
        "description": "High-throughput GPU algorithm for blockDAG chains",
        "efficiency": 5,
    },
    "autolykos2": {
        "name": "Autolykos2",
        "type": "GPU",
        "coins": ["Ergo (ERG)"],
        "description": "Efficient GPU algorithm with low power consumption",
        "efficiency": 4,
    },
    "zhash": {
        "name": "Zhash",
        "type": "GPU",
        "coins": ["Bitcoin Gold (BTG)"],
        "description": "Equihash variant for GPU mining",
        "efficiency": 3,
    },
}


def benchmark_algorithm(algo_key: str) -> dict:
    """Simulate algorithm benchmark on current hardware."""
    algo = ALGORITHMS.get(algo_key, {})
    base_rates = {
        "randomx": (4500, 8500),
        "ethash": (25.0, 55.0),
        "cryptonight_v8": (2.5, 5.0),
        "kawpow": (12.0, 28.0),
        "kheavyhash": (1.5, 3.5),
        "autolykos2": (80.0, 160.0),
        "zhash": (3.0, 7.0),
    }
    lo, hi = base_rates.get(algo_key, (1.0, 10.0))
    rate = round(random.uniform(lo, hi), 2)
    power = round(random.uniform(45, 120), 1)
    temp = random.randint(55, 78)
    return {
        "algorithm": algo.get("name", algo_key),
        "type": algo.get("type", "Unknown"),
        "hashrate": rate,
        "unit": "H/s" if algo.get("type") == "CPU" else "MH/s",
        "power_w": power,
        "temp_c": temp,
        "efficiency": f"{round(rate / max(power, 1) * 1000, 1)} H/W",
    }


def show_algorithm_list():
    """Display available algorithms in a formatted table."""
    table = Table(
        show_header=True,
        header_style="bold bright_green",
        border_style="green",
        box=box.ROUNDED,
        title="[bold bright_green] AVAILABLE ALGORITHMS [/]",
    )
    table.add_column("#", style="dim", justify="right", width=3)
    table.add_column("Algorithm", style="bright_green")
    table.add_column("Type", style="bright_cyan")
    table.add_column("Coins", style="dim")
    table.add_column("Efficiency", justify="center")

    for i, (key, algo) in enumerate(ALGORITHMS.items(), 1):
        stars = "★" * algo["efficiency"] + "☆" * (5 - algo["efficiency"])
        table.add_row(str(i), algo["name"], algo["type"], ", ".join(algo["coins"]), stars)

    console.print()
    console.print(table)
    console.print()


def run_benchmark(algo_key: str):
    """Run simulated benchmark for an algorithm."""
    algo = ALGORITHMS.get(algo_key)
    if not algo:
        return None

    console.print()
    print_info(f"Benchmarking [bright_green]{algo['name']}[/]...")
    separator()

    result = benchmark_algorithm(algo_key)

    result_table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.ROUNDED,
        title=f"[bold bright_cyan] BENCHMARK: {result['algorithm'].upper()} [/]",
    )
    result_table.add_column("Metric", style="bright_cyan")
    result_table.add_column("Value", justify="right", style="bright_white")

    result_table.add_row("Hashrate", f"{result['hashrate']} {result['unit']}")
    result_table.add_row("Power Draw", f"{result['power_w']} W")
    result_table.add_row("Temperature", f"{result['temp_c']} °C")
    result_table.add_row("Efficiency", result["efficiency"])
    result_table.add_row("Type", result["type"])

    console.print(result_table)
    console.print()
    return result
