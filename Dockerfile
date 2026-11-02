FROM python3.14@sha256:7bd9bc5a5ebfe5f5cae5419bbb7fceee8b74d6049893fc39549ebfdcb0a5151d as builder
COPY --from=ghcr.io/astral-sh/uv@sha256:9f130421e930bfbdc563c00740466603f8723158e90297d07957c2294640262b /uv /bin/

WORKDIR /app

COPY pyproject.toml uv.lock ./

RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked

FROM python3.14@sha256:7bd9bc5a5ebfe5f5cae5419bbb7fceee8b74d6049893fc39549ebfdcb0a5151d as runner

WORKDIR /app
 
ENV PYTHONUNBUFFERED=1

COPY --from=builder /app/.venv .venv
ENV PATH="/app/.venv/bin:$PATH"

RUN ["addgroup", "--system", "appgroup"]
RUN ["adduser", "--system", "--ingroup", "appgroup", "appuser"]

USER appuser

COPY src/app ./app
COPY src/alembic ./alembic
COPY alembic.ini ./
COPY deploy/entrypoint.sh ./

RUN ["chown", "-R", "appuser:appgroup", "/app"]
RUN ["chmod", "+x", "entrypoint.sh"]

ENTRYPOINT ["entrypoint.sh"]