import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CHECKLIST = ROOT / "docs" / "security" / "mfa-checklist.md"

ACCOUNTS = ("GitHub", "Render", "Registrar", "AWS")
SECTIONS = ("## Accounts", "## Commits and tokens", "## Next review")
DATE = re.compile(r"\d{4}-\d{2}-\d{2}")


def _text() -> str:
    assert CHECKLIST.is_file(), "docs/security/mfa-checklist.md is missing"
    return CHECKLIST.read_text(encoding="utf-8")


def _section(text: str, heading: str) -> str:
    assert heading in text, f"missing section: {heading}"
    return text.split(heading, 1)[1].split("\n## ", 1)[0]


def test_checklist_cites_its_requirements() -> None:
    text = _text()
    assert "HE-05" in text
    assert "S2-10" in text


def test_checklist_has_every_section() -> None:
    text = _text()
    for heading in SECTIONS:
        assert heading in text, f"missing section: {heading}"


def test_every_account_is_confirmed_or_marked_not_applicable() -> None:
    accounts = _section(_text(), "## Accounts")
    rows = [line for line in accounts.splitlines() if line.startswith("|")]
    for name in ACCOUNTS:
        matching = [row for row in rows if row.startswith(f"| {name}")]
        assert matching, f"no row for {name}"
        row = matching[0]
        assert DATE.search(row) or "Not applicable yet" in row, (
            f"{name} needs a confirmation date or 'Not applicable yet'"
        )


def test_next_review_has_a_date() -> None:
    review = _section(_text(), "## Next review")
    assert DATE.search(review), "the next review needs a date"
