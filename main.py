"""Main application entry point."""

import asyncio
import uvicorn
from contextlib import asynccontextmanager

from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.config import DatabaseConfig
from src.presentation.api.app import create_app


@asynccontextmanager
async def lifespan(app):
    """Application lifespan events."""
    # Startup
    print("Starting up...")
    
    # Initialize database
    config = DatabaseConfig()
    db_connection = DatabaseConnection(config)
    
    try:
        await db_connection.create_tables_async()
        print("Database tables created successfully")
    except Exception as e:
        print(f"Failed to create database tables: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create the FastAPI app instance
app = create_app()

# Set the lifespan context
app.router.lifespan_context = lifespan


def main():
    """Main function to run the application."""
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
