"""Main application entry point."""

import sys, builtins
import uvicorn
from contextlib import asynccontextmanager
from socketio import asgi
from src.infrastructure.configs.config_init import ConfigInit
from src.infrastructure.database.databaseConnection import DatabaseConnection
from src.infrastructure.database.config import DatabaseConfig
from src.infrastructure.database.factory.db_factory import DBFactory, test_db_in_mem, test_db_pgsql
from src.presentation.rest.api.app import create_app
from src.presentation.websockets.websocket_server import sio
from src.infrastructure.configs.loggers import logger, print  # or your overridden print


@asynccontextmanager
async def lifespan(app):
    """Application lifespan events."""
    # Startup
    print("Starting up...")
    # Initialize database
    print("testing faCtory")
    
    # try:
    #     await db_connection.create_tables_async()
    #     print("Database tables created successfully",level="INFO")
    # except Exception as e:
    #     print(f"Failed to create database tables: {e}")
    
    yield
    
    # Shutdown
    print("Shutting down...")


# Create the FastAPI app instance
fastapi_app = create_app()

# Set the lifespan context
fastapi_app.router.lifespan_context = lifespan

# Combine FastAPI + Socket.IO
app = asgi.ASGIApp(sio, other_asgi_app=fastapi_app)

def main():
    """Main function to run the application."""
    _config = ConfigInit()
    uvicorn_config = _config.uvicorn_config
    uvicorn.run(
        "main:app",
        **uvicorn_config,
    )

if __name__ == "__main__":
    main()
