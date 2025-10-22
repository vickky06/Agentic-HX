#!/usr/bin/env python3
"""Comprehensive test runner for the hexagonal architecture application."""

import subprocess
import sys
from pathlib import Path


def run_command(command: str, description: str) -> bool:
    """Run a command and return success status."""
    print(f"\n🔄 {description}...")
    print(f"Command: {command}")
    print("-" * 50)
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed:")
        print("STDOUT:", e.stdout)
        print("STDERR:", e.stderr)
        return False


def main():
    """Run all tests."""
    print("🧪 Hexagonal Architecture - Comprehensive Testing")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("pyproject.toml").exists():
        print("❌ Please run this script from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not run_command("uv sync --extra dev", "Installing dependencies"):
        print("❌ Failed to install dependencies")
        sys.exit(1)
    
    # Run unit tests
    if not run_command("uv run pytest tests/unit/ -v", "Running unit tests"):
        print("❌ Unit tests failed")
        sys.exit(1)
    
    # Run integration tests
    if not run_command("uv run pytest tests/integration/ -v", "Running integration tests"):
        print("❌ Integration tests failed")
        sys.exit(1)
    
    # Run manual tests
    if not run_command("uv run python test_manual.py", "Running manual tests"):
        print("❌ Manual tests failed")
        sys.exit(1)
    
    # Run all tests with coverage
    if not run_command("uv run pytest tests/ --cov=src --cov-report=term-missing", "Running all tests with coverage"):
        print("❌ Coverage tests failed")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 All tests completed successfully!")
    print("=" * 60)
    
    print("\n📊 Test Summary:")
    print("✅ Unit tests - Domain entities and value objects")
    print("✅ Integration tests - Application services with mocked dependencies")
    print("✅ Manual tests - All layers without database")
    print("✅ Coverage report - Code coverage analysis")
    
    print("\n🚀 Next Steps:")
    print("1. To test with database: Set up PostgreSQL and run migrations")
    print("2. To test API endpoints: Start the app with 'uv run python main.py'")
    print("3. To run API tests: Use 'uv run python test_api.py'")
    print("4. To view coverage report: Open htmlcov/index.html")


if __name__ == "__main__":
    main()
