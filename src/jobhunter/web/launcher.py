"""Launch the local JobHunter browser interface."""

from __future__ import annotations

import argparse
import ipaddress
import os
import shutil
import subprocess
import sys
import threading
from pathlib import Path

import httpx
import uvicorn
from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings
from jobhunter.web.app import create_app
from jobhunter.web.capability import register_capability_routes


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="jobhunter-app",
        description="Launch the local JobHunter web application",
    )
    parser.add_argument("--config", type=Path, default=None)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.add_argument("--no-browser", action="store_true")
    parser.add_argument(
        "--allow-network",
        action="store_true",
        help="Allow binding outside loopback; use only on a trusted network",
    )
    parser.add_argument(
        "--install-desktop",
        action="store_true",
        help="Install a Linux application-menu launcher and exit",
    )
    return parser


def _is_loopback(host: str) -> bool:
    if host.casefold() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def _is_wsl() -> bool:
    if os.environ.get("WSL_INTEROP") or os.environ.get("WSL_DISTRO_NAME"):
        return True
    try:
        release = Path("/proc/sys/kernel/osrelease").read_text().casefold()
    except OSError:
        return False
    return "microsoft" in release or "wsl" in release


def _run_opener(command: list[str]) -> bool:
    try:
        result = subprocess.run(
            command,
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=3.0,
        )
    except (OSError, subprocess.TimeoutExpired):
        return False
    return result.returncode == 0


def _open_browser(url: str) -> bool:
    """Open the local UI without leaking platform-opener diagnostics to the terminal."""

    if _is_wsl():
        command = shutil.which("cmd.exe")
        fallback = Path("/mnt/c/Windows/System32/cmd.exe")
        if not command and fallback.exists():
            command = str(fallback)
        if command and _run_opener([command, "/c", "start", "", url]):
            return True

    if sys.platform == "darwin":
        opener = shutil.which("open")
        return bool(opener and _run_opener([opener, url]))

    if sys.platform.startswith("win"):
        command = shutil.which("cmd.exe") or "cmd.exe"
        return _run_opener([command, "/c", "start", "", url])

    opener = shutil.which("xdg-open")
    return bool(opener and _run_opener([opener, url]))


def _open_or_report(url: str) -> None:
    if not _open_browser(url):
        print(
            f"Could not open a browser automatically. Open this address manually: {url}",
            file=sys.stderr,
        )


def _desktop_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _install_linux_desktop_launcher(
    config_path: Path | None,
    *,
    home: Path | None = None,
) -> Path:
    selected_config = (config_path or Path("jobhunter.toml")).expanduser().resolve()
    if not selected_config.exists():
        raise FileNotFoundError(
            f"Cannot install launcher because configuration does not exist: {selected_config}"
        )

    home_dir = home or Path.home()
    applications_dir = home_dir / ".local/share/applications"
    icon_dir = home_dir / ".local/share/icons/hicolor/scalable/apps"
    applications_dir.mkdir(parents=True, exist_ok=True)
    icon_dir.mkdir(parents=True, exist_ok=True)

    source_icon = Path(__file__).resolve().parent / "static/icon.svg"
    installed_icon = icon_dir / "jobhunter.svg"
    shutil.copyfile(source_icon, installed_icon)

    executable = shutil.which("jobhunter-app")
    if executable:
        executable_part = _desktop_quote(executable)
    else:
        executable_part = f"{_desktop_quote(sys.executable)} -m jobhunter.web.launcher"
    exec_line = f"{executable_part} --config {_desktop_quote(str(selected_config))}"

    desktop_path = applications_dir / "jobhunter.desktop"
    desktop_path.write_text(
        "\n".join(
            [
                "[Desktop Entry]",
                "Type=Application",
                "Name=JobHunter",
                "Comment=Local-first career intelligence",
                f"Exec={exec_line}",
                f"Path={selected_config.parent}",
                f"Icon={installed_icon}",
                "Terminal=false",
                "Categories=Utility;Development;",
                "StartupNotify=true",
                "",
            ]
        ),
        encoding="utf-8",
    )
    desktop_path.chmod(0o755)
    return desktop_path


def _existing_jobhunter(url: str) -> bool:
    try:
        response = httpx.get(url, timeout=0.35)
    except httpx.HTTPError:
        return False
    return response.status_code == 200 and "JobHunter" in response.text


def build_runtime_app(settings: Settings):
    """Build the normal web app plus bounded capability-intelligence review routes."""

    app = create_app(settings)
    register_capability_routes(app, settings)
    return app


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    if arguments.install_desktop:
        try:
            desktop_path = _install_linux_desktop_launcher(arguments.config)
        except OSError as exc:
            raise SystemExit(f"Desktop launcher installation failed: {exc}") from exc
        print(f"Installed JobHunter application launcher: {desktop_path}")
        return 0

    if not 1 <= arguments.port <= 65535:
        raise SystemExit("Port must be between 1 and 65535")
    if not _is_loopback(arguments.host) and not arguments.allow_network:
        raise SystemExit(
            "Refusing non-loopback bind. Pass --allow-network only when LAN exposure "
            "is intentional."
        )

    try:
        settings = Settings.load(arguments.config)
    except (ConfigLoadError, ValidationError, ValueError) as exc:
        raise SystemExit(f"Configuration error: {exc}") from exc

    url_host = "127.0.0.1" if arguments.host in {"0.0.0.0", "::"} else arguments.host
    url = f"http://{url_host}:{arguments.port}/"
    if _is_loopback(arguments.host) and _existing_jobhunter(url):
        print(f"JobHunter is already running: {url}")
        if not arguments.no_browser:
            _open_or_report(url)
        return 0

    if not arguments.no_browser:
        threading.Timer(0.8, _open_or_report, args=(url,)).start()

    print(f"JobHunter app: {url}")
    print("Press Ctrl+C to stop the local app server.")
    uvicorn.run(
        build_runtime_app(settings),
        host=arguments.host,
        port=arguments.port,
        log_level=settings.log_level.casefold(),
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
