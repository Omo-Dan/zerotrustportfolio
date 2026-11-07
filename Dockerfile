FROM python:3.14-slim@sha256:af8a5aa14780025dbfbcfbc81bd8a91ebd87711dd5b0f48ed71090949dd7cb1d

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# Temporary: take the zlib security fix (CVE-2026-76844, CVE-2026-85091)
# before the pinned base image includes it.
# Remove when the base image ships zlib1g 1:1.3.dfsg+really1.3.1-1+deb13u1 or later.
RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive apt-get install --yes --no-install-recommends --only-upgrade zlib1g \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN python -m pip install --require-hashes -r requirements.txt \
    && python -m pip uninstall --yes pip

COPY app ./app

RUN groupadd --system --gid 10001 app \
    && useradd --system --uid 10001 --gid app --no-create-home --shell /usr/sbin/nologin app

USER 10001:10001

CMD ["sh", "-c", "exec uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]