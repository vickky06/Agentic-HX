#!/usr/bin/env python3
"""Setup script for the hexagonal architecture project."""

import asyncio
import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False


def main():
    """Main setup function."""
    print("🚀 Setting up Hexagonal Architecture Project")
    print("=" * 50)
    
    # Check if uv is installed
    if not run_command("uv --version", "Checking uv installation"):
        print("❌ uv is not installed. Please install it first:")
        print("   curl -LsSf https://astral.sh/uv/install.sh | sh")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("uv sync", "Installing dependencies"):
        sys.exit(1)
    
    # Check if .env exists
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Please copy .env.example to .env and configure it:")
        print("   cp .env.example .env")
        print("   # Edit .env with your database credentials")
        return
    
    print("\n🎉 Setup completed successfully!")
    print("\nNext steps:")
    print("1. Configure your database in .env file")
    print("2. Create PostgreSQL database: createdb hexagonal_db")
    print("3. Run migrations: uv run alembic upgrade head")
    print("4. Start the application: uv run python main.py")
    print("5. Visit http://localhost:8000/docs for API documentation")


if __name__ == "__main__":
    main()
