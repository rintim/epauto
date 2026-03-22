FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock,relabel=shared \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml,relabel=shared \
    set -eux \
    && uv sync --locked --no-install-project --no-editable

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux \
    && uv sync --locked --no-editable

FROM python:3.14-slim
COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

CMD ["epauto", "-c", "config.toml"]
