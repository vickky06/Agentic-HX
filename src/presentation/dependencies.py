"""Dependency injection for FastAPI."""

from functools import lru_cache
from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.services.user_service import UserService
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.user_domain_service import UserDomainService
from src.infrastructure.adapters.user_repository_impl import UserRepositoryImpl
from src.infrastructure.database.connection import DatabaseConnection
from src.infrastructure.database.config import DatabaseConfig


@lru_cache()
def get_database_config() -> DatabaseConfig:
    """Get database configuration."""
    return DatabaseConfig()


@lru_cache()
def get_database_connection(config: DatabaseConfig = Depends(get_database_config)) -> DatabaseConnection:
    """Get database connection."""
    return DatabaseConnection(config)


async def get_db_session(
    db_connection: DatabaseConnection = Depends(get_database_connection),
) -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with db_connection.async_session_factory() as session:
        try:
            yield session
        finally:
            await session.close()


def get_user_repository(
    session: AsyncSession = Depends(get_db_session),
) -> UserRepository:
    """Get user repository."""
    return UserRepositoryImpl(session)


def get_user_domain_service(
    user_repository: UserRepository = Depends(get_user_repository),
) -> UserDomainService:
    """Get user domain service."""
    return UserDomainService(user_repository)


def get_user_service(
    user_repository: UserRepository = Depends(get_user_repository),
    user_domain_service: UserDomainService = Depends(get_user_domain_service),
) -> UserService:
    """Get user service."""
    return UserService(user_repository, user_domain_service)
