from pathlib import Path

ZAP = Path(".github/workflows/zap-baseline.yml").read_text(encoding="utf-8")


def test_zap_image_is_pinned_by_digest():
    assert "ghcr.io/zaproxy/zaproxy@sha256:" in ZAP


def test_zap_image_is_not_pulled_by_a_moving_tag():
    assert "zaproxy/zaproxy:stable" not in ZAP
    assert "zaproxy/zaproxy:latest" not in ZAP
