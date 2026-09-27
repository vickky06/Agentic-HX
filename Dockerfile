# syntax=docker/dockerfile:1
FROM python:3.13-slim

WORKDIR /app

# Install build dependencies and Postgres client
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libffi-dev \
    postgresql-client \
    && pip install uv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files first (to leverage Docker cache)
COPY pyproject.toml uv.lock README.md ./

# Install project dependencies
RUN uv sync --frozen --no-cache

# Copy project source
COPY . .

EXPOSE 8000

# Run migrations + start app
CMD bash -c "uv run alembic upgrade head && uv run python main.py"