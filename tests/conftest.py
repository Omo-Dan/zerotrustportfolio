import os

# Tests run as the development environment unless a test overrides it.
os.environ.setdefault("APP_ENV", "development")
