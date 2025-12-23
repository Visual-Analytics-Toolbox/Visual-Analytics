FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim AS builder
COPY ./ .
WORKDIR /django
RUN uv sync --no-dev --frozen && uv run manage.py collectstatic

FROM ghcr.io/astral-sh/uv:python3.14-trixie-slim

LABEL maintainer="Stella Alice Schlotter"

# show the stdout and stderr streams right in the command line instead of getting buffered.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY ./ .

WORKDIR /django

COPY --from=builder /django/staticfiles /django/staticfiles
RUN uv sync --no-dev --frozen
EXPOSE 8000

CMD ["uv", "run", "--no-sync", "gunicorn", "core.wsgi:application", "--workers=2", "--threads=4", "--worker-class", "gthread", "--bind", "0.0.0.0:8000"]
