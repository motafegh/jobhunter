"""Launch the local JobHunter browser interface."""

from __future__ import annotations

import argparse
import ipaddress
import threading
import webbrowser
from pathlib import Path

import uvicorn
from pydantic import ValidationError

from jobhunter.config import ConfigLoadError, Settings
from jobhunter.web.app import create_app


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
    return parser


def _is_loopback(host: str) -> bool:
    if host.casefold() == "localhost":
        return True
    try:
        return ipaddress.ip_address(host).is_loopback
    except ValueError:
        return False


def main(argv: list[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
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
    if not arguments.no_browser:
        threading.Timer(0.8, webbrowser.open, args=(url,)).start()

    print(f"JobHunter app: {url}")
    print("Press Ctrl+C to stop the local app server.")
    uvicorn.run(
        create_app(settings),
        host=arguments.host,
        port=arguments.port,
        log_level=settings.log_level.casefold(),
        access_log=False,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
