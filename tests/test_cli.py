from pathlib import Path

from jobhunter.cli import main


def test_init_creates_configuration_and_local_directories(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["init"])

    assert exit_code == 0
    assert (tmp_path / "jobhunter.toml").is_file()
    assert (tmp_path / "data").is_dir()
    assert (tmp_path / "data" / "evidence").is_dir()


def test_init_refuses_to_replace_existing_configuration(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)
    config_path = tmp_path / "jobhunter.toml"
    config_path.write_text("existing", encoding="utf-8")

    exit_code = main(["init"])

    assert exit_code == 1
    assert config_path.read_text(encoding="utf-8") == "existing"


def test_discovery_requires_configured_or_command_line_search(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "discover"]) == 2


def test_discovery_rejects_non_jobinja_command_line_url(
    tmp_path: Path, monkeypatch
) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "discover", "--url", "https://example.com/jobs"]) == 2


def test_fetch_requires_a_previously_discovered_job(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobinja", "fetch", "missing"]) == 1


def test_show_requires_a_local_detail_version(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)

    assert main(["jobs", "show", "missing"]) == 1
