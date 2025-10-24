#!/bin/bash

echo "🐘 Setting up PostgreSQL for Hexagonal Architecture"
echo "=" * 50

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# Create PostgreSQL container
echo "🔄 Creating PostgreSQL container..."
docker run -d \
  --name hexagonal-postgres \
  -e POSTGRES_DB=hexagonal_db \
  -e POSTGRES_USER=viveksingh \
  -e POSTGRES_PASSWORD=password \
  -p 5432:5432 \
  postgres:15

# Wait for PostgreSQL to start
echo "⏳ Waiting for PostgreSQL to start..."
sleep 10

# Check if container is running
if docker ps | grep -q hexagonal-postgres; then
    echo "✅ PostgreSQL container is running"
else
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi

# Test connection
echo "🔄 Testing database connection..."
docker exec hexagonal-postgres psql -U viveksingh -d hexagonal_db -c "SELECT version();"

if [ $? -eq 0 ]; then
    echo "✅ Database connection successful!"
    echo ""
    echo "🎉 PostgreSQL is ready!"
    echo "Database: hexagonal_db"
    echo "User: viveksingh"
    echo "Password: (empty)"
    echo "Host: localhost"
    echo "Port: 5432"
    echo ""
    echo "Next steps:"
    echo "1. Run: uv run alembic upgrade head"
    echo "2. Run: uv run python main.py"
else
    echo "❌ Database connection failed"
    exit 1
fi
