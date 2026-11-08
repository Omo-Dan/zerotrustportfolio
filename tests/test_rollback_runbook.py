from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "runbooks" / "rollback.md"

SECTIONS = (
    "## When to roll back",
    "## Standard path",
    "## Fast path",
    "## Verify",
    "## Drill log",
)


def _text() -> str:
    assert RUNBOOK.is_file(), "docs/runbooks/rollback.md is missing"
    return RUNBOOK.read_text(encoding="utf-8")


def test_runbook_cites_its_requirements() -> None:
    text = _text()
    assert "HE-06" in text
    assert "AC-15" in text


def test_runbook_has_every_section() -> None:
    text = _text()
    for heading in SECTIONS:
        assert heading in text, f"missing section: {heading}"


def test_standard_path_goes_through_the_pipeline() -> None:
    text = _text()
    standard = text.split("## Standard path", 1)[1].split("## Fast path", 1)[0]
    assert "git revert" in standard
    assert "pull request" in standard.lower()


def test_fast_path_states_the_autodeploy_consequence() -> None:
    text = _text()
    fast = text.split("## Fast path", 1)[1].split("## Verify", 1)[0]
    assert "autodeploy" in fast.lower()
    assert "revert" in fast.lower()


def test_verify_uses_the_version_endpoint() -> None:
    text = _text()
    verify = text.split("## Verify", 1)[1].split("## Drill log", 1)[0]
    assert "/version" in verify
    assert "/healthz" in verify
