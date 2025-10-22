"""User application service (use cases)."""

from typing import List, Optional

from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.user_domain_service import UserDomainService
from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId
from src.application.dtos.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse


class UserService:
    """User application service containing use cases."""

    def __init__(
        self,
        user_repository: UserRepository,
        user_domain_service: UserDomainService,
    ):
        """Initialize with dependencies."""
        self._user_repository = user_repository
        self._user_domain_service = user_domain_service

    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        """Create a new user."""
        email = Email.from_string(request.email)
        
        # Validate using domain service
        await self._user_domain_service.validate_user_creation(
            email, request.first_name, request.last_name
        )
        
        # Create user entity
        user = User(
            email=email,
            first_name=request.first_name,
            last_name=request.last_name,
        )
        
        # Save user
        saved_user = await self._user_repository.save(user)
        
        return self._to_user_response(saved_user)

    async def get_user_by_id(self, user_id: str) -> Optional[UserResponse]:
        """Get user by ID."""
        user_id_obj = UserId.from_string(user_id)
        user = await self._user_repository.find_by_id(user_id_obj)
        
        if user is None:
            return None
        
        return self._to_user_response(user)

    async def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """Get user by email."""
        email_obj = Email.from_string(email)
        user = await self._user_repository.find_by_email(email_obj)
        
        if user is None:
            return None
        
        return self._to_user_response(user)

    async def get_users(self, skip: int = 0, limit: int = 100) -> UserListResponse:
        """Get list of users with pagination."""
        users = await self._user_repository.find_all(skip=skip, limit=limit)
        
        user_responses = [self._to_user_response(user) for user in users]
        
        return UserListResponse(
            users=user_responses,
            total=len(user_responses),
            skip=skip,
            limit=limit,
        )

    async def update_user(self, user_id: str, request: UpdateUserRequest) -> Optional[UserResponse]:
        """Update user."""
        user_id_obj = UserId.from_string(user_id)
        user = await self._user_repository.find_by_id(user_id_obj)
        
        if user is None:
            return None
        
        # Update fields if provided
        if request.first_name is not None or request.last_name is not None:
            first_name = request.first_name or user.first_name
            last_name = request.last_name or user.last_name
            user.update_name(first_name, last_name)
        
        if request.email is not None:
            email = Email.from_string(request.email)
            # Check if email is unique (excluding current user)
            if not await self._user_domain_service.is_email_unique(email, user_id_obj):
                raise ValueError("Email already exists")
            user.update_email(email)
        
        # Save updated user
        updated_user = await self._user_repository.save(user)
        
        return self._to_user_response(updated_user)

    async def delete_user(self, user_id: str) -> bool:
        """Delete user."""
        user_id_obj = UserId.from_string(user_id)
        
        # Check if user can be deleted
        if not await self._user_domain_service.can_user_be_deleted(user_id_obj):
            raise ValueError("User cannot be deleted")
        
        return await self._user_repository.delete(user_id_obj)

    async def activate_user(self, user_id: str) -> Optional[UserResponse]:
        """Activate user."""
        user_id_obj = UserId.from_string(user_id)
        user = await self._user_repository.find_by_id(user_id_obj)
        
        if user is None:
            return None
        
        user.activate()
        updated_user = await self._user_repository.save(user)
        
        return self._to_user_response(updated_user)

    async def deactivate_user(self, user_id: str) -> Optional[UserResponse]:
        """Deactivate user."""
        user_id_obj = UserId.from_string(user_id)
        user = await self._user_repository.find_by_id(user_id_obj)
        
        if user is None:
            return None
        
        user.deactivate()
        updated_user = await self._user_repository.save(user)
        
        return self._to_user_response(updated_user)

    def _to_user_response(self, user: User) -> UserResponse:
        """Convert User entity to UserResponse DTO."""
        return UserResponse(
            id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
