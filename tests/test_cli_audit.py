from pathlib import Path

from jobhunter.cli import main


def test_audit_command_handles_empty_local_database(
    tmp_path: Path,
    monkeypatch,
    capsys,
) -> None:
    monkeypatch.chdir(tmp_path)

    exit_code = main(["jobs", "audit"])
    output = capsys.readouterr().out

    assert exit_code == 0
    assert "Jobs audited: 0" in output
    assert "No matching audit entries." in output
