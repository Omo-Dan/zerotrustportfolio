from pathlib import Path

ZAP = Path(".github/workflows/zap-baseline.yml").read_text(encoding="utf-8")


def test_zap_image_is_pinned_by_digest():
    assert "ghcr.io/zaproxy/zaproxy@sha256:" in ZAP


def test_zap_image_is_not_pulled_by_a_moving_tag():
    assert "zaproxy/zaproxy:stable" not in ZAP
    assert "zaproxy/zaproxy:latest" not in ZAP


def rules() -> str:
    return Path(".zap/rules.tsv").read_text(encoding="utf-8")


def rule_lines() -> list[tuple[int, str]]:
    lines = rules().splitlines()
    return [
        (index, line)
        for index, line in enumerate(lines)
        if line and not line.startswith("#")
    ]


def test_zap_rules_file_accepts_cacheable_content_only():
    ids = [line.split("\t")[0] for _, line in rule_lines()]
    assert ids == ["10049"]


def test_every_accepted_zap_rule_has_a_written_reason():
    lines = rules().splitlines()
    for index, line in rule_lines():
        assert index > 0 and lines[index - 1].startswith("#"), line


def test_zap_rules_are_tab_separated():
    for _, line in rule_lines():
        assert len(line.split("\t")) >= 3, "rule lines need tab separators"


def test_zap_scan_uses_the_rules_file():
    assert ".zap/rules.tsv" in ZAP
    assert "-c rules.tsv" in ZAP
