from jobhunter.web.launcher import _is_loopback


def test_web_launcher_accepts_loopback_hosts() -> None:
    assert _is_loopback("127.0.0.1")
    assert _is_loopback("::1")
    assert _is_loopback("localhost")


def test_web_launcher_rejects_non_loopback_hosts() -> None:
    assert not _is_loopback("0.0.0.0")
    assert not _is_loopback("192.168.1.20")
    assert not _is_loopback("example.com")
