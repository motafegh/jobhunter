from urllib.parse import parse_qs, urlsplit

import pytest

from jobhunter.search_registry import (
    BUILTIN_SEARCH_PACKS,
    build_jobinja_keyword_url,
    expand_keyword_searches,
    normalize_search_term,
    resolve_pack_names,
)


def test_normalizes_persian_variants_and_zero_width_joiners() -> None:
    assert normalize_search_term("  امنيت\u200cسايبری  ") == normalize_search_term(
        "امنیت سایبری"
    )
    assert normalize_search_term("PYTHON") == "python"


def test_builds_encoded_jobinja_keyword_url() -> None:
    url = build_jobinja_keyword_url("مهندس هوش مصنوعی")
    parsed = urlsplit(url)

    assert parsed.scheme == "https"
    assert parsed.netloc == "jobinja.ir"
    assert parsed.path == "/jobs"
    assert parse_qs(parsed.query) == {
        "filters[keywords][0]": ["مهندس هوش مصنوعی"]
    }


def test_expands_profile_with_persian_and_english_terms_and_deduplicates() -> None:
    searches = expand_keyword_searches(profile_names=("ai-security-python",))
    terms = {search.term for search in searches}

    assert "هوش مصنوعی" in terms
    assert "Artificial Intelligence" in terms
    assert "Python" in terms
    assert "پایتون" in terms
    assert "AI Security" in terms
    assert "امنیت هوش مصنوعی" in terms
    assert len(terms) == len(searches)


def test_broad_profile_interleaves_all_selected_packs_in_first_window() -> None:
    searches = expand_keyword_searches(profile_names=("ai-security-python",))
    first_window_origins = {search.origin for search in searches[:12]}

    assert first_window_origins == {
        "pack:ai-ml",
        "pack:llm-applications",
        "pack:python-data",
        "pack:defensive-security",
        "pack:ai-security",
        "pack:network-platform",
    }


def test_custom_terms_are_deduplicated_against_persian_variants() -> None:
    searches = expand_keyword_searches(
        extra_terms=("امنیت\u200cسایبری", "امنيت سایبری", "Cybersecurity"),
    )

    assert [search.term for search in searches] == [
        "امنیت\u200cسایبری",
        "Cybersecurity",
    ]


def test_excluded_terms_remove_pack_entries() -> None:
    searches = expand_keyword_searches(
        pack_names=("python-data",),
        excluded_terms=("python", "پایتون"),
    )

    assert "Python" not in {search.term for search in searches}
    assert "پایتون" not in {search.term for search in searches}


def test_unknown_profiles_and_packs_are_rejected() -> None:
    with pytest.raises(ValueError, match="Unknown Jobinja search profile"):
        resolve_pack_names(profile_names=("unknown",))
    with pytest.raises(ValueError, match="Unknown Jobinja search pack"):
        resolve_pack_names(pack_names=("unknown",))


def test_builtin_packs_have_unique_normalized_terms_within_each_pack() -> None:
    for pack in BUILTIN_SEARCH_PACKS.values():
        normalized = [normalize_search_term(term) for term in pack.terms]
        assert len(normalized) == len(set(normalized)), pack.name
