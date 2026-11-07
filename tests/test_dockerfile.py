from pathlib import Path

DOCKERFILE = Path("Dockerfile").read_text(encoding="utf-8")


def test_base_image_is_pinned_by_digest():
    assert "FROM python:3.14-slim@sha256:" in DOCKERFILE


def test_temporary_package_upgrades_are_documented_and_clean():
    if "--only-upgrade" in DOCKERFILE:
        assert "Remove when" in DOCKERFILE
        assert "rm -rf /var/lib/apt/lists/*" in DOCKERFILE


def test_package_upgrades_run_before_the_unprivileged_user_is_set():
    if "--only-upgrade" in DOCKERFILE:
        assert DOCKERFILE.index("--only-upgrade") < DOCKERFILE.index("USER 10001")
