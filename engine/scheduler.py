# -*- coding: utf-8 -*-
"""Mining scheduler — schedule management, resource allocation, and auto-pause."""

import random
from datetime import datetime

from rich.table import Table
from rich.panel import Panel
from rich import box

from engine.ui import console, print_info, print_success, print_warning, separator


def get_schedule_status(cfg: dict) -> dict:
    """Get current mining schedule status."""
    res = cfg.get("resources", {})
    schedule = res.get("schedule", {})

    now = datetime.now()
    current_hour = now.hour

    enabled = schedule.get("enabled", False)
    active_hours = schedule.get("active_hours", "00:00-08:00")

    try:
        start_str, end_str = active_hours.split("-")
        start_h = int(start_str.split(":")[0])
        end_h = int(end_str.split(":")[0])
        if start_h <= end_h:
            in_active_window = start_h <= current_hour < end_h
        else:
            in_active_window = current_hour >= start_h or current_hour < end_h
    except (ValueError, AttributeError):
        in_active_window = True

    return {
        "enabled": enabled,
        "active_hours": active_hours,
        "timezone": schedule.get("timezone", "UTC"),
        "in_active_window": in_active_window,
        "should_mine": (not enabled) or in_active_window,
    }


def show_schedule_config(cfg: dict):
    """Display current schedule configuration."""
    res = cfg.get("resources", {})
    schedule = res.get("schedule", {})
    status = get_schedule_status(cfg)

    table = Table(
        show_header=True,
        header_style="bold bright_yellow",
        border_style="yellow",
        box=box.ROUNDED,
        title="[bold bright_yellow] SCHEDULE CONFIGURATION [/]",
    )
    table.add_column("Setting", style="bright_yellow")
    table.add_column("Value", justify="right", style="bright_white")
    table.add_column("Description", style="dim")

    table.add_row(
        "Enabled",
        f"[bright_green]Yes[/]" if schedule.get("enabled") else "[dim]No[/]",
        "Restrict mining to specific hours",
    )
    table.add_row("Active Hours", schedule.get("active_hours", "00:00-08:00"), "Mining window (HH:MM-HH:MM)")
    table.add_row("Timezone", schedule.get("timezone", "UTC"), "Schedule timezone")
    table.add_row(
        "Current Status",
        f"[bright_green]Active[/]" if status["should_mine"] else "[red]Paused[/]",
        "Based on current time",
    )

    console.print()
    console.print(table)
    console.print()


def get_resource_limits(cfg: dict) -> dict:
    """Get current resource limits from config."""
    res = cfg.get("resources", {})
    mining = cfg.get("mining", {})

    return {
        "max_cpu_temp": res.get("max_cpu_temp", 85),
        "max_gpu_temp": res.get("max_gpu_temp", 80),
        "max_memory_mb": res.get("max_memory_mb", 2048),
        "power_limit_w": res.get("power_limit_w", 0),
        "threads": mining.get("threads", 0),
        "intensity": mining.get("intensity", 80),
        "gpu_enabled": mining.get("gpu_enabled", True),
        "pause_on_battery": mining.get("pause_on_battery", True),
        "pause_on_activity": mining.get("pause_on_activity", False),
        "activity_threshold": mining.get("activity_threshold", 30),
    }


def show_resource_limits(cfg: dict):
    """Display current resource limits."""
    limits = get_resource_limits(cfg)

    table = Table(
        show_header=True,
        header_style="bold bright_magenta",
        border_style="magenta",
        box=box.ROUNDED,
        title="[bold bright_magenta] RESOURCE LIMITS [/]",
    )
    table.add_column("Parameter", style="bright_magenta")
    table.add_column("Value", justify="right", style="bright_white")
    table.add_column("Description", style="dim")

    table.add_row("Max CPU Temp", f"{limits['max_cpu_temp']} °C", "Pause mining above this")
    table.add_row("Max GPU Temp", f"{limits['max_gpu_temp']} °C", "Pause mining above this")
    table.add_row("Max Memory", f"{limits['max_memory_mb']} MB", "RAM allocation limit")
    table.add_row("Power Limit", f"{limits['power_limit_w']} W" if limits['power_limit_w'] else "Unlimited", "GPU power cap")
    table.add_row("Threads", "Auto" if limits["threads"] == 0 else str(limits["threads"]), "Mining threads (0=auto)")
    table.add_row("Intensity", f"{limits['intensity']}%", "CPU/GPU utilization target")
    table.add_row("GPU Mining", f"[bright_green]Enabled[/]" if limits["gpu_enabled"] else "[dim]Disabled[/]", "GPU mining toggle")
    table.add_row("Battery Saver", f"[bright_green]Yes[/]" if limits["pause_on_battery"] else "[dim]No[/]", "Pause on battery power")
    table.add_row("Stealth Mode", f"[bright_green]Active[/]" if limits["pause_on_activity"] else "[dim]Inactive[/]", "Pause on system activity")
    table.add_row("Activity Threshold", f"{limits['activity_threshold']}%", "CPU usage to trigger pause")

    console.print()
    console.print(table)
    console.print()
