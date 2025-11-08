from contextlib import asynccontextmanager
from typing import AsyncIterator, Optional
from src.infrastructure.database.base.DB_service import DBInstance

# Shared global in-memory storage (simulate DB)
_GLOBAL_INMEMORY_STORAGE = {}

class InMemoryDBManager:
    def __init__(self, config: Optional[dict] = None):
        if not config or not isinstance(config, dict):
            raise ValueError("InMemoryDB requires a valid config dict.")

        name = config.get("name")
        if not name:
            raise ValueError("InMemoryDB config must include a non-empty 'name' key.")

        # Initialize namespace for this DB name if not exists
        if name not in _GLOBAL_INMEMORY_STORAGE:
            _GLOBAL_INMEMORY_STORAGE[name] = {}

        # Reference to the namespace
        self.storage = _GLOBAL_INMEMORY_STORAGE[name]


class InMemoryDB(DBInstance):
    def __init__(self, config: dict):
        self.db_name = config.get("name", "default")
        self.manager = InMemoryDBManager(config)
        self.storage = self.manager.storage

    async def connect(self):
        # In-memory DB doesn't need real connection setup
        return self

    @asynccontextmanager
    async def get_session(self) -> AsyncIterator["InMemoryDB"]:
        """Simulates a DB session context"""
        try:
            yield self
        finally:
            # In-memory DBs usually don't persist state between runs,
            # so you could add cleanup here if desired
            pass

    async def close(self):
        """Optional cleanup if you want to clear all data for this DB"""
        self.storage.clear()

    # ----------------
    # CRUD Operations
    # ----------------
    async def insert(self, table: str, key: str, value: dict) -> dict:
        self.storage.setdefault(table, {})[key] = value
        return value

    async def fetch_one(self, table: str, key: str) -> Optional[dict]:
        return self.storage.get(table, {}).get(key)

    async def fetch_all(self, table: str) -> list[dict]:
        return list(self.storage.get(table, {}).values())

    async def update(self, table: str, key: str, value: dict) -> Optional[dict]:
        if table in self.storage and key in self.storage[table]:
            self.storage[table][key] = value
            return value
        return None

    async def delete(self, table: str, key: str) -> bool:
        if table in self.storage and key in self.storage[table]:
            del self.storage[table][key]
            return True
        return False

    # ----------------
    # Transaction API
    # ----------------
    @asynccontextmanager
    async def session(self) -> AsyncIterator["InMemoryDB"]:
        """Simulate a transactional block"""
        try:
            # Could clone state here if we wanted rollback ability
            yield self
        finally:
            # Commit/rollback not needed since it's in-memory
            pass
