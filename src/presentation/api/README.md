# API Layer

## Role
FastAPI application setup, configuration, and routing.

## What to Add Here
- FastAPI application configuration
- CORS and middleware setup
- Router registration and API documentation

## Example
```python
def create_app() -> FastAPI:
    app = FastAPI(
        title="Hexagonal Architecture API",
        description="A hexagonal architecture implementation in Python",
        version="1.0.0",
    )
    app.add_middleware(CORSMiddleware, allow_origins=["*"])
    app.include_router(user_router)
    return app
```

## Connections
- **Implements**: API application setup
- **Uses**: Handler routers
- **Used by**: Main application entry point
- **Example**: `main.py` → `create_app()` → `user_router`
