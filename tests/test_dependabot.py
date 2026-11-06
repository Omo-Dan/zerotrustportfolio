from pathlib import Path


def config() -> str:
    return Path(".github/dependabot.yml").read_text(encoding="utf-8")


def test_dependabot_covers_the_three_ecosystems():
    for ecosystem in ("pip", "github-actions", "docker"):
        assert f'package-ecosystem: "{ecosystem}"' in config()


def test_every_ecosystem_is_checked_weekly():
    assert config().count('interval: "weekly"') == 3


def test_every_ecosystem_limits_open_pull_requests():
    assert config().count("open-pull-requests-limit:") == 3
