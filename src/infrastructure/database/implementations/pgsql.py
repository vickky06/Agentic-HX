import asyncpg
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator, Optional, Self
from src.infrastructure.database.base.DB_service import DBInstance


class PostgresDB(DBInstance):
    def __init__(self, config: dict[str, Any]):
        """
        config example:
        {
            "user": "vivek",
            "password": "secret",
            "database": "wallet",
            "host": "localhost",
            "port": 5432,
            "min_size": 1,
            "max_size": 5
        }
        """
        self.config = config
        self.pool: Optional[asyncpg.Pool] = None

    def check_pool(self) -> bool:
        return self.pool is not None
    # --- Connection Management ---

    async def connect(self) -> Self:
        """Initialize a connection pool."""
        if not self.pool:
            self.pool = await asyncpg.create_pool(**self.config)
        return self

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator[asyncpg.Connection]:
        """
        Acquire a connection from the pool and release it automatically.
        Example:
            async with db.get_session() as conn:
                await conn.execute("SELECT 1")
        """
        if self.pool is None:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")

        conn = await self.pool.acquire()
        try:
            yield conn
        finally:
            await self.pool.release(conn)

    async def close(self) -> None:
        """Gracefully close connection pool."""
        if self.pool:
            await self.pool.close()
            self.pool = None

    # --- CRUD-Like Operations (simplified ORM-less interface) ---

    async def insert(self, table: str, key: str, value: dict) -> Any:
        """
        Insert a row into a table using key/value mapping.
        Assumes `key` corresponds to a column named 'id'.
        """
        
        cols = ", ".join(value.keys())
        placeholders = ", ".join(f"${i+1}" for i in range(len(value)))
        query = f"INSERT INTO {table} ({cols}) VALUES ({placeholders}) RETURNING *"
        if self.pool :
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, *value.values())
                return dict(row)
        else:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")

    async def fetch_one(self, table: str, key: str) -> Optional[dict]:
        """Fetch a single row by `id` column."""
        query = f"SELECT * FROM {table} WHERE id=$1"
        if self.pool :
            
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, key)
                return dict(row) if row else None
        else:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")


    async def fetch_all(self, table: str) -> list[dict]:
        """Fetch all rows from a table."""
        query = f"SELECT * FROM {table}"
        if self.pool:
            async with self.pool.acquire() as conn:
                rows = await conn.fetch(query)
                return [dict(r) for r in rows]
        else:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")

    async def update(self, table: str, key: str, value: dict) -> Any:
        """Update a row by id."""
        set_clause = ", ".join(f"{k}=${i+2}" for i, k in enumerate(value.keys()))
        query = f"UPDATE {table} SET {set_clause} WHERE id=$1 RETURNING *"
        if self.pool :        
            async with self.pool.acquire() as conn:
                row = await conn.fetchrow(query, key, *value.values())
                return dict(row) if row else None
        else:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")

    async def delete(self, table: str, key: str) -> bool:
        """Delete a row by id."""
        query = f"DELETE FROM {table} WHERE id=$1"
        if self.pool:    
            async with self.pool.acquire() as conn:
                result = await conn.execute(query, key)
                return result.endswith("DELETE 1")
        else:
            raise RuntimeError("Database pool is not initialized. Call connect() first.")
    
    #--- Transaction / Context API ---
    @asynccontextmanager
    async def session(self) -> AsyncIterator[asyncpg.Connection]:
        """
        Provide an async context manager for transactional operations.
        Usage:
            async with db.session() as conn:
                await conn.execute(...)
        """
        if not self.pool:
            raise RuntimeError("Database not connected. Call connect() first.")

        conn = await self.pool.acquire()
        txn = conn.transaction()
        await txn.start()

        try:
            yield conn
            await txn.commit()
        except Exception:
            await txn.rollback()
            raise
        finally:
            await self.pool.release(conn)
