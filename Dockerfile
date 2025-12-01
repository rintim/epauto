FROM python:3.14-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

ENV UV_LINK_MODE=copy

WORKDIR /opt/epauto

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    set -eux \
    && uv sync --locked --no-install-project --no-editable

ADD . /opt/epauto

RUN --mount=type=cache,target=/root/.cache/uv \
    set -eux \
    && uv sync --locked --no-editable

FROM python:3.14-slim
COPY --from=builder /opt/epauto/.venv /opt/epauto/.venv

RUN set -eux \
    && groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 -m appuser \
    && chown -R appuser:nonroot /opt/epauto/ \
    && mkdir -p /etc/opt \
    && touch /etc/opt/epauto.toml \
    && chown -R appuser:nonroot /etc/opt/epauto.toml

USER appuser
WORKDIR /opt/epauto

CMD ["/opt/epauto/.venv/bin/epauto", "--config", "/etc/opt/epauto.toml"]
