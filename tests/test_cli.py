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
