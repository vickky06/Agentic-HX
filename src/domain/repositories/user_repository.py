"""User repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.user import User
from ..value_objects.email import Email
from ..value_objects.user_id import UserId


class UserRepository(ABC):
    """Abstract user repository interface."""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save a user."""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        """Find user by ID."""
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email."""
        pass

    @abstractmethod
    async def find_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Find all users with pagination."""
        pass

    @abstractmethod
    async def delete(self, user_id: UserId) -> bool:
        """Delete a user by ID."""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email."""
        pass
