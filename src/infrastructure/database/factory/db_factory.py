from src.infrastructure.database.base.DB_service import DBInstance
from src.infrastructure.database.implementations.in_memory import InMemoryDB
from src.infrastructure.database.implementations.pgsql import PostgresDB


class DBFactory:
    @staticmethod
    async def get_db(db_type: str,config:dict)->DBInstance:
        if db_type == "postgresql":
            return await PostgresDB(config).connect()
        # elif db_type == "sqlite":
        #     pass
        elif db_type == "inmemory":
            return await InMemoryDB(config).connect()
        else:
            raise ValueError(f"Unsupported database type: {db_type}")
        
async def test_db_in_mem():
    print("testing in memory db.")
    """Quick test of DBFactory"""
    db = await DBFactory.get_db("inmemory", {"name": "test_db_in_mem"})
    await db.connect()

    async with db.session() as session:
        await session.insert("users", "u1", {"name": "Vivek"})
        user = await session.fetch_one("users", "u1")
        print("✅ User fetched from InMemory DB:", user)

    await db.close()


async def test_db_pgsql():
    print("🧪 Testing PostgreSQL DB connection...")
    
    config = {
        "host": "db",   # or "db" if running inside Docker container
        "port": 5432,
        "database": "agentic_db",
        "user": "viveksingh",
        "password": "password",
        # "echo": True,
    }

    db = await DBFactory.get_db("postgresql", config)
    print("✅ Connected to PostgreSQL DB!")

    # Run a simple query
    async with db.session() as session:
        result = await session.execute("SELECT NOW()")
        timestamp = result[0]['now'] if isinstance(result[0], dict) else result[0][0]
        print(f"⏱ Current DB Time: {timestamp}")

    await db.close()
    print("🔒 Connection closed,.")
    