"""Main application entry point."""

import asyncio
# import json
import uvicorn
from contextlib import asynccontextmanager
from socketio import asgi
from src.domain.enums.agent_enum_builder import build_agent_type_enum
from src.infrastructure.configs.config_init import ConfigInit
# from src.infrastructure.database.databaseConnection import DatabaseConnection
# from src.infrastructure.database.config import DatabaseConfig
# from src.infrastructure.database.factory.db_factory import DBFactory, test_db_in_mem, test_db_pgsql
from src.presentation.langgraph_main import lang_graph_main
from src.presentation.rest.api.app import create_app
from src.presentation.websockets.websocket_server import sio
# from src.infrastructure.configs.loggers import print  # or your overridden print


@asynccontextmanager
async def lifespan(app):
    """Application lifespan events."""
    # Startup
    _config = ConfigInit()
    AgentType = build_agent_type_enum(_config.config)

    # print("Application configuration loaded:", json.dumps( _config.config['agent_types'],indent=2))
    # Initialize database
    # print("testing faCtory")
    
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
    print("Application configuration loaded:", type(_config.config['agent_types']))
    uvicorn_config = _config.uvicorn_config
    uvicorn.run(
        "main:app",
        **uvicorn_config,
    )

if __name__ == "__main__":
    asyncio.run( lang_graph_main())
    main()
