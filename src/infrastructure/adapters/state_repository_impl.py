from domain.entities.state import State
from application.repositories.state_repository import StateRepository

class StateRepositoryImpl(StateRepository):
    def __init__(self, db_session):
        self.db_session = db_session

    async def fetch_state(self) -> State:
        # Implementation to fetch state from the database
        result = await self.db_session.execute("SELECT meta, nodes_processing FROM state_table LIMIT 1")
        row = result.fetchone()
        if row:
            return State(meta=row['meta'], nodes_processing=row['nodes_processing'])
        return State()

    async def save_state(self, state_data: dict) -> None:
        # Implementation to save state to the database
        await self.db_session.execute(
            "INSERT INTO state_table (meta, nodes_processing) VALUES (:meta, :nodes_processing) "
            "ON CONFLICT (id) DO UPDATE SET meta = :meta, nodes_processing = :nodes_processing",
            state_data
        )
        await self.db_session.commit()