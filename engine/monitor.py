# -*- coding: utf-8 -*-
"""System resource monitor — CPU, GPU, temperature, and power tracking."""

import random
import time
from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.ui import console, print_info, print_success, print_warning, separator


def get_cpu_info() -> dict:
    """Simulate CPU information and current stats."""
    cores = random.choice([4, 6, 8, 12, 16])
    threads = cores * 2
    usage = round(random.uniform(15, 95), 1)
    temp = random.randint(40, 82)
    freq = round(random.uniform(2.4, 4.8), 2)

    return {
        "name": random.choice([
            "AMD Ryzen 9 5900X", "Intel Core i7-12700K",
            "AMD Ryzen 7 5800X", "Intel Core i9-13900K",
        ]),
        "cores": cores,
        "threads": threads,
        "usage_pct": usage,
        "temp_c": temp,
        "freq_ghz": freq,
    }


def get_gpu_info(count: int = None) -> list[dict]:
    """Simulate GPU information and current stats."""
    if count is None:
        count = random.randint(1, 3)

    gpus = []
    models = [
        "NVIDIA RTX 3080", "NVIDIA RTX 3090", "NVIDIA RTX 4070",
        "AMD RX 6800 XT", "AMD RX 7900 XTX",
    ]
    for i in range(count):
        usage = round(random.uniform(60, 100), 1)
        temp = random.randint(55, 82)
        mem_used = round(random.uniform(4.0, 10.0), 1)
        mem_total = random.choice([8, 10, 12, 24])
        power = round(random.uniform(120, 350), 0)
        fan = random.randint(40, 85)

        gpus.append({
            "index": i,
            "name": random.choice(models),
            "usage_pct": usage,
            "temp_c": temp,
            "mem_used_gb": mem_used,
            "mem_total_gb": mem_total,
            "power_w": power,
            "fan_pct": fan,
        })
    return gpus


def show_system_overview():
    """Display complete system resource overview."""
    cpu = get_cpu_info()
    gpus = get_gpu_info()

    cpu_table = Table(
        show_header=True,
        header_style="bold bright_cyan",
        border_style="cyan",
        box=box.ROUNDED,
        title="[bold bright_cyan] CPU STATUS [/]",
    )
    cpu_table.add_column("Property", style="bright_cyan")
    cpu_table.add_column("Value", justify="right", style="bright_white")

    temp_color = "bright_green" if cpu["temp_c"] < 65 else "yellow" if cpu["temp_c"] < 80 else "red"
    cpu_table.add_row("Model", cpu["name"])
    cpu_table.add_row("Cores / Threads", f"{cpu['cores']} / {cpu['threads']}")
    cpu_table.add_row("Usage", f"{cpu['usage_pct']}%")
    cpu_table.add_row("Temperature", f"[{temp_color}]{cpu['temp_c']} °C[/]")
    cpu_table.add_row("Frequency", f"{cpu['freq_ghz']} GHz")

    console.print()
    console.print(cpu_table)

    for gpu in gpus:
        gpu_table = Table(
            show_header=True,
            header_style="bold bright_green",
            border_style="green",
            box=box.ROUNDED,
            title=f"[bold bright_green] GPU {gpu['index']} — {gpu['name']} [/]",
        )
        gpu_table.add_column("Property", style="bright_green")
        gpu_table.add_column("Value", justify="right", style="bright_white")

        temp_color = "bright_green" if gpu["temp_c"] < 65 else "yellow" if gpu["temp_c"] < 80 else "red"
        gpu_table.add_row("Usage", f"{gpu['usage_pct']}%")
        gpu_table.add_row("Temperature", f"[{temp_color}]{gpu['temp_c']} °C[/]")
        gpu_table.add_row("Memory", f"{gpu['mem_used_gb']} / {gpu['mem_total_gb']} GB")
        gpu_table.add_row("Power Draw", f"{gpu['power_w']:.0f} W")
        gpu_table.add_row("Fan Speed", f"{gpu['fan_pct']}%")

        console.print()
        console.print(gpu_table)

    console.print()


def get_mining_stats() -> dict:
    """Simulate current mining statistics."""
    hashrate = round(random.uniform(4000, 9000), 0)
    shares_accepted = random.randint(50, 500)
    shares_rejected = random.randint(0, 5)
    uptime_sec = random.randint(3600, 86400)
    earnings_xmr = round(random.uniform(0.001, 0.05), 6)
    earnings_usd = round(earnings_xmr * random.uniform(150, 200), 2)

    hours = uptime_sec // 3600
    minutes = (uptime_sec % 3600) // 60

    return {
        "hashrate": hashrate,
        "unit": "H/s",
        "shares_accepted": shares_accepted,
        "shares_rejected": shares_rejected,
        "uptime": f"{hours}h {minutes}m",
        "earnings_xmr": earnings_xmr,
        "earnings_usd": earnings_usd,
        "difficulty": random.randint(200000, 500000),
    }
