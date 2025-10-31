from pathlib import Path
import os

from src.infrastructure.database.config import DatabaseConfig

def test_me():
# Debug script
    print("=" * 50)
    print("DEBUGGING ENV LOADING")
    print("=" * 50)

    print(f"\n1. Working directory: {os.getcwd()}")
    print(f"2. .env exists: {Path('.env').exists()}")
    print(f"3. .env absolute path: {Path('.env').absolute()}")

    if Path(".env").exists():
        print("\n4. .env file contents:")
        with open(".env") as f:
            for line in f:
                if line.strip():
                    print(f"   {line.rstrip()}")

    print("\n5. Environment variables:")
    for key in ["DB_HOST", "DB_PORT", "DB_NAME", "DB_USER", "DB_PASSWORD"]:
        print(f"   {key} = {os.getenv(key, 'NOT SET')}")

    print("\n6. Testing DatabaseConfig:")
    # from  import DatabaseConfig
    config = DatabaseConfig()
    print(f"   config.host = {config.host}")
    print(f"   config.port = {config.port}")
    print(f"   config.name = {config.name}")
    print(f"   config.user = {config.user}")