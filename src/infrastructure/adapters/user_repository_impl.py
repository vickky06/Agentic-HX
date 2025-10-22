"""User repository implementation."""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId
from src.infrastructure.database.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    """User repository implementation using SQLAlchemy."""

    def __init__(self, session: AsyncSession):
        """Initialize with database session."""
        self._session = session

    async def save(self, user: User) -> User:
        """Save a user."""
        # Check if user exists
        existing_user = await self._session.get(UserModel, str(user.id))
        
        if existing_user:
            # Update existing user
            existing_user.email = str(user.email)
            existing_user.first_name = user.first_name
            existing_user.last_name = user.last_name
            existing_user.is_active = user.is_active
            existing_user.updated_at = user.updated_at
            await self._session.commit()
            await self._session.refresh(existing_user)
            return self._to_entity(existing_user)
        else:
            # Create new user
            user_model = UserModel(
                id=str(user.id),
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                is_active=user.is_active,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
            self._session.add(user_model)
            await self._session.commit()
            await self._session.refresh(user_model)
            return self._to_entity(user_model)

    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """Find user by ID."""
        user_model = await self._session.get(UserModel, str(user_id))
        return self._to_entity(user_model) if user_model else None

    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email."""
        stmt = select(UserModel).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        user_model = result.scalar_one_or_none()
        return self._to_entity(user_model) if user_model else None

    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Find all users with pagination."""
        stmt = select(UserModel).offset(skip).limit(limit).order_by(UserModel.created_at.desc())
        result = await self._session.execute(stmt)
        user_models = result.scalars().all()
        return [self._to_entity(user_model) for user_model in user_models]

    async def delete(self, user_id: UserId) -> bool:
        """Delete a user by ID."""
        user_model = await self._session.get(UserModel, str(user_id))
        if user_model:
            await self._session.delete(user_model)
            await self._session.commit()
            return True
        return False

    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email."""
        stmt = select(UserModel.id).where(UserModel.email == str(email))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none() is not None

    def _to_entity(self, user_model: UserModel) -> User:
        """Convert database model to domain entity."""
        return User(
            id=UserId.from_string(user_model.id),
            email=Email.from_string(user_model.email),
            first_name=user_model.first_name,
            last_name=user_model.last_name,
            is_active=user_model.is_active,
            created_at=user_model.created_at,
            updated_at=user_model.updated_at,
        )
