import asyncio

from domain.entities.state import State
from application.repositories.state_repository import StateRepository #interface


class StateService:
    def __init__(self, state_repository: StateRepository, lock: asyncio.Lock):
        self.state_repository = state_repository
        self.lock = lock

    async def get_state(self) -> State:
        async with self.lock:
            state_data = await self.state_repository.fetch_state()
            return state_data

    async def update_meta(self, new_meta: dict) -> State:
        async with self.lock:
            state = await self.get_state()
            state.update_meta(new_meta)
            await self.state_repository.save_state(state.model_dump())
            return state

    async def update_nodes_processing(self, new_nodes: dict) -> State:
        async with self.lock:
            state = await self.get_state()
            state.update_nodes_processing(new_nodes)
            await self.state_repository.save_state(state.model_dump())
            return state
        


"""
Example calling code:
# src/presentation/rest/state_controller.py
from fastapi import APIRouter, Depends
import asyncio
from application.services.state_service import StateService
from infrastructure.database.state_repository_impl import StateRepositoryImpl

router = APIRouter()
_lock = asyncio.Lock()  # app-wide lock
_state_repo = StateRepositoryImpl()
_state_service = StateService(_state_repo, _lock)

@router.get("/state")
async def get_state():
    state = await _state_service.get_state()
    return state.model_dump()

@router.post("/state/meta")
async def update_meta(new_meta: dict):
    updated = await _state_service.update_meta(new_meta)
    return updated.model_dump()

@router.post("/state/nodes")
async def update_nodes(new_nodes: dict):
    updated = await _state_service.update_nodes_processing(new_nodes)
    return updated.model_dump()

"""