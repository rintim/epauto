FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    set -eux \
    && uv sync --locked --no-install-project --no-editable

ADD . /app

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux \
    && uv sync --locked --no-editable

FROM python:3.14-slim
COPY --from=builder /app/.venv /app/.venv

RUN set -eux \
    && groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 -m appuser \
    && chown -R appuser:nonroot /app

USER appuser
WORKDIR /app

CMD ["/app/.venv/bin/epauto"]
