from src.application.repositories.state_repository import StateRepository


class CheckpointRepository(StateRepository):
    def __init__(self):
        self._store = {}

    async def save_state(self, run_id, state):
        self._store[run_id] = state.snapshot()

    async def load_state(self, run_id):
        data = self._store.get(run_id)
        return data
