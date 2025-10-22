"""User domain service."""

from typing import Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId


class UserDomainService:
    """User domain service for complex business logic."""

    def __init__(self, user_repository: UserRepository):
        """Initialize with user repository."""
        self._user_repository = user_repository

    async def is_email_unique(self, email: Email, exclude_user_id: Optional[UserId] = None) -> bool:
        """Check if email is unique across all users."""
        existing_user = await self._user_repository.find_by_email(email)
        
        if existing_user is None:
            return True
        
        # If we're updating a user, exclude their own email
        if exclude_user_id and existing_user.id == exclude_user_id:
            return True
        
        return False

    async def can_user_be_deleted(self, user_id: UserId) -> bool:
        """Check if user can be deleted based on business rules."""
        user = await self._user_repository.find_by_id(user_id)
        
        if user is None:
            return False
        
        # Add business rules here, e.g., check if user has active orders, etc.
        # For now, we'll allow deletion of any existing user
        return True

    async def validate_user_creation(self, email: Email, first_name: str, last_name: str) -> None:
        """Validate user creation data."""
        if not first_name or not last_name:
            raise ValueError("First name and last name are required")
        
        if not await self.is_email_unique(email):
            raise ValueError("Email already exists")
