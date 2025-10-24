"""Main application entry point."""

import asyncio
import uvicorn
from contextlib import asynccontextmanager
from socketio import ASGIApp
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.config import DatabaseConfig
from src.presentation.rest.api.app import create_app
from src.presentation.websockets.websocket_server import sio


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
fastapi_app = create_app()

# Set the lifespan context
fastapi_app.router.lifespan_context = lifespan

# Combine FastAPI + Socket.IO
app = ASGIApp(sio, other_asgi_app=fastapi_app)


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
