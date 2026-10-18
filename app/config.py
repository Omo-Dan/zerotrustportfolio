import os
from dataclasses import dataclass

ALLOWED_ENVIRONMENTS = ("development", "production")


class ConfigError(RuntimeError):
    """Raised when the configuration is missing or unsafe."""


@dataclass(frozen=True)
class Settings:
    env: str
    # Debug mode shows tracebacks to visitors, so it is never switched on.
    debug: bool = False


def load_settings() -> Settings:
    env = os.environ.get("APP_ENV")
    if env not in ALLOWED_ENVIRONMENTS:
        raise ConfigError(
            "APP_ENV must be one of: " + ", ".join(ALLOWED_ENVIRONMENTS)
        )
    return Settings(env=env)