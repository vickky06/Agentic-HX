# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

# Install uv and Postgres client (for pg_isready)
RUN apt-get update && apt-get install -y postgresql-client && pip install uv && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-cache

COPY . .

EXPOSE 8000

CMD bash -c "uv run alembic upgrade head && uv run python main.py"