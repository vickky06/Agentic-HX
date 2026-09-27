#!/bin/bash

echo "🐘 Setting up PostgreSQL for Hexagonal Architecture"
echo "=================================================="

# --- 1. Load .env file ---
if [ ! -f .env ]; then
    echo "❌ .env file not found!"
    exit 1
fi

echo "📄 Loading environment variables from .env..."

# Load environment variables safely
while IFS='=' read -r key value; do
    [[ "$key" =~ ^#.*$ ]] && continue  # skip comments
    [[ -z "$key" ]] && continue        # skip empty lines

    # Clean up value
    value=$(echo "$value" | sed -e 's/^"//' -e 's/"$//' -e "s/^'//" -e "s/'$//" -e 's/\r$//')

    export "$key=$value"
    echo "   Loaded: $key=$value"
done < .env

echo ""

# --- 2. Validate required variables ---
REQUIRED_VARS=("DB_HOST" "DB_PORT" "DB_NAME" "DB_USER" "DB_PASSWORD")
for var in "${REQUIRED_VARS[@]}"; do
    if [ -z "${!var}" ]; then
        echo "❌ Missing required variable: $var"
        exit 1
    fi
done

# --- 3. Show configuration ---
CONTAINER_NAME="hexagonal-postgres"
DB_HOST="${DB_HOST:-localhost}"

echo "✅ Using configuration:"
echo "   Host: $DB_HOST"
echo "   Port: $DB_PORT"
echo "   Database: $DB_NAME"
echo "   User: $DB_USER"
echo ""

# --- 4. Check Docker ---
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"

# --- 5. Start PostgreSQL container ---
echo "🔄 Creating PostgreSQL container..."
docker rm -f $CONTAINER_NAME > /dev/null 2>&1

docker run -d \
  --name "$CONTAINER_NAME" \
  -e POSTGRES_DB="$DB_NAME" \
  -e POSTGRES_USER="$DB_USER" \
  -e POSTGRES_PASSWORD="$DB_PASSWORD" \
  -p "$DB_PORT:5432" \
  postgres:15

# --- 6. Wait for PostgreSQL to start ---
echo "⏳ Waiting for PostgreSQL to start..."
sleep 10

# --- 7. Verify container is running ---
if docker ps | grep -q "$CONTAINER_NAME"; then
    echo "✅ PostgreSQL container is running"
else
    echo "❌ Failed to start PostgreSQL container"
    exit 1
fi

# --- 8. Test connection ---
echo "🔄 Testing database connection..."
docker exec "$CONTAINER_NAME" psql -U "$DB_USER" -d "$DB_NAME" -c "SELECT version();" > /dev/null

if [ $? -eq 0 ]; then
    echo "✅ Database connection successful!"
    echo ""
    echo "🎉 PostgreSQL is ready!"
    echo "Database: $DB_NAME"
    echo "User: $DB_USER"
    echo "Host: $DB_HOST"
    echo "Port: $DB_PORT"
    echo ""
    echo "Next steps:"
    echo "1. Run: uv run alembic upgrade head"
    echo "2. Run: uv run python main.py"
else
    echo "❌ Database connection failed"
    exit 1
fi
