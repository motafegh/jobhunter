from pathlib import Path

from jobhunter.web.launcher import _install_linux_desktop_launcher, _is_loopback


def test_web_launcher_accepts_loopback_hosts() -> None:
    assert _is_loopback("127.0.0.1")
    assert _is_loopback("::1")
    assert _is_loopback("localhost")


def test_web_launcher_rejects_non_loopback_hosts() -> None:
    assert not _is_loopback("0.0.0.0")
    assert not _is_loopback("192.168.1.20")
    assert not _is_loopback("example.com")


def test_desktop_launcher_binds_exact_configuration_path(tmp_path: Path) -> None:
    project_dir = tmp_path / "project"
    project_dir.mkdir()
    config_path = project_dir / "jobhunter.toml"
    config_path.write_text("[jobhunter]\n", encoding="utf-8")
    home = tmp_path / "home"

    desktop_path = _install_linux_desktop_launcher(config_path, home=home)
    content = desktop_path.read_text(encoding="utf-8")

    assert desktop_path == home / ".local/share/applications/jobhunter.desktop"
    assert f'--config "{config_path.resolve()}"' in content
    assert f"Path={project_dir.resolve()}" in content
    assert (home / ".local/share/icons/hicolor/scalable/apps/jobhunter.svg").exists()
