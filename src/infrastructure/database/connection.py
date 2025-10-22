"""Database connection setup."""

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from .config import DatabaseConfig


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


class DatabaseConnection:
    """Database connection manager."""

    def __init__(self, config: DatabaseConfig):
        """Initialize database connection."""
        self.config = config
        self._engine = None
        self._async_engine = None
        self._session_factory = None
        self._async_session_factory = None

    @property
    def engine(self):
        """Get synchronous engine."""
        if self._engine is None:
            self._engine = create_engine(
                self.config.url,
                echo=self.config.echo,
                pool_pre_ping=True,
            )
        return self._engine

    @property
    def async_engine(self):
        """Get asynchronous engine."""
        if self._async_engine is None:
            async_url = self.config.url.replace("postgresql://", "postgresql+asyncpg://")
            self._async_engine = create_async_engine(
                async_url,
                echo=self.config.echo,
                pool_pre_ping=True,
            )
        return self._async_engine

    @property
    def session_factory(self):
        """Get session factory."""
        if self._session_factory is None:
            self._session_factory = sessionmaker(
                bind=self.engine,
                autocommit=False,
                autoflush=False,
            )
        return self._session_factory

    @property
    def async_session_factory(self):
        """Get async session factory."""
        if self._async_session_factory is None:
            self._async_session_factory = async_sessionmaker(
                bind=self.async_engine,
                class_=AsyncSession,
                autocommit=False,
                autoflush=False,
            )
        return self._async_session_factory

    def create_tables(self):
        """Create all tables."""
        Base.metadata.create_all(bind=self.engine)

    async def create_tables_async(self):
        """Create all tables asynchronously."""
        async with self.async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
