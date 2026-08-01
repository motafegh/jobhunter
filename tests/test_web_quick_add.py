import pytest

from jobhunter.web.quick_add import parse_quick_add_input


def test_quick_add_resolves_direct_job_url() -> None:
    target = parse_quick_add_input(
        "https://jobinja.ir/companies/example-company/jobs/tmW5/example-title"
    )

    assert target.kind == "job"
    assert target.job is not None
    assert target.job.source_job_id == "tmW5"
    assert target.job.company_slug == "example-company"
    assert target.search_url is None


def test_quick_add_resolves_jobinja_search_url() -> None:
    target = parse_quick_add_input(
        "https://jobinja.ir/jobs?filters%5Bkeywords%5D%5B0%5D=Python&page=2"
    )

    assert target.kind == "search-url"
    assert target.job is None
    assert target.search_url is not None
    assert "page=" not in target.search_url
    assert "Python" in target.search_url


def test_quick_add_builds_search_for_persian_or_english_phrase() -> None:
    target = parse_quick_add_input("  امنیت هوش مصنوعی  ")

    assert target.kind == "keyword"
    assert target.display_value == "امنیت هوش مصنوعی"
    assert target.search_url is not None
    assert target.search_url.startswith("https://jobinja.ir/jobs?")


def test_quick_add_rejects_unapproved_external_url() -> None:
    with pytest.raises(ValueError, match="Jobinja URLs only"):
        parse_quick_add_input("https://example.com/jobs/123")
