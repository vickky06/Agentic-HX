#!/bin/bash
set -e

until pg_isready -h db -U hx_user -d hx_db > /dev/null 2>&1; do
  echo "Waiting for Postgres..."
  sleep 2
done

echo "Postgres is up — running migrations..."
uv run alembic upgrade head
uv run python src/main.py