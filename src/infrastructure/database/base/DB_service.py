from abc import ABC, abstractmethod
from typing import Self, Any, AsyncIterator, Optional
from contextlib import asynccontextmanager


class DBInstance(ABC):
    """
    Abstract base for all database implementations (Postgres, MySQL, InMemory, etc.)
    Defines a minimal async interface for connecting, managing sessions,
    and performing CRUD operations.
    """

    @abstractmethod
    async def connect(self) -> Self:
        """Establish connection to the underlying database (e.g. pool or in-memory setup)."""
        ...
    @abstractmethod
    @asynccontextmanager
    def get_session(self) -> AsyncIterator[Any]:
        """Return a session or connection object that can be used to run queries."""
        ...

    @abstractmethod
    async def close(self) -> None:
        """Gracefully close database connection or release pool."""
        ...

    # --- CRUD-Like API ---

    @abstractmethod
    async def insert(self, table: str, key: Any, value: dict) -> Any:
        """Insert a record into a table or collection."""
        ...

    @abstractmethod
    async def fetch_one(self, table: str, key: Any) -> Optional[dict]:
        """Fetch a single record by key/id."""
        ...

    @abstractmethod
    async def fetch_all(self, table: str) -> list[dict]:
        """Fetch all records from a table."""
        ...

    @abstractmethod
    async def update(self, table: str, key: Any, value: dict) -> Any:
        """Update a record by key/id."""
        ...

    @abstractmethod
    async def delete(self, table: str, key: Any) -> bool:
        """Delete a record by key/id."""
        ...

    # --- Transaction / Context API ---

    @abstractmethod
    @asynccontextmanager
    def session(self) -> AsyncIterator[Any]:
        """
        Provide an async context manager for a DB session/transaction.

        Example:
            async with db.session() as s:
                await s.execute(...)
        """
        ...
