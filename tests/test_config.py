import pytest

from app.config import ConfigError, load_settings


def test_missing_app_env_refuses_to_start(monkeypatch):
    monkeypatch.delenv("APP_ENV", raising=False)
    with pytest.raises(ConfigError):
        load_settings()


@pytest.mark.parametrize("value", ["", "staging", "PRODUCTION", "prod", "true"])
def test_unknown_app_env_refuses_to_start(monkeypatch, value):
    monkeypatch.setenv("APP_ENV", value)
    with pytest.raises(ConfigError):
        load_settings()


@pytest.mark.parametrize("value", ["development", "production"])
def test_known_app_env_is_accepted(monkeypatch, value):
    monkeypatch.setenv("APP_ENV", value)
    assert load_settings().env == value


@pytest.mark.parametrize("value", ["development", "production"])
def test_debug_is_off_in_every_environment(monkeypatch, value):
    monkeypatch.setenv("APP_ENV", value)
    assert load_settings().debug is False


def test_app_runs_with_debug_off():
    from app.main import app

    assert app.debug is False
