"""Integration tests for User service."""

import pytest
from unittest.mock import AsyncMock, Mock

from src.application.dtos.user_dto import CreateUserRequest, UpdateUserRequest
from src.application.services.user_service import UserService
from src.domain.entities.user import User
from src.domain.repositories.user_repository import UserRepository
from src.domain.services.user_domain_service import UserDomainService
from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId


class TestUserService:
    """Integration tests for User service."""

    @pytest.fixture
    def mock_user_repository(self):
        """Mock user repository."""
        return AsyncMock(spec=UserRepository)

    @pytest.fixture
    def mock_user_domain_service(self):
        """Mock user domain service."""
        return AsyncMock(spec=UserDomainService)

    @pytest.fixture
    def user_service(self, mock_user_repository, mock_user_domain_service):
        """User service with mocked dependencies."""
        return UserService(mock_user_repository, mock_user_domain_service)

    @pytest.mark.asyncio
    async def test_create_user_success(self, user_service, mock_user_repository, mock_user_domain_service):
        """Test successful user creation."""
        # Arrange
        request = CreateUserRequest(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        
        created_user = User(
            email=Email.from_string("test@example.com"),
            first_name="John",
            last_name="Doe",
        )
        
        mock_user_domain_service.validate_user_creation.return_value = None
        mock_user_repository.save.return_value = created_user
        
        # Act
        result = await user_service.create_user(request)
        
        # Assert
        assert result.email == "test@example.com"
        assert result.first_name == "John"
        assert result.last_name == "Doe"
        assert result.full_name == "John Doe"
        assert result.is_active is True
        
        mock_user_domain_service.validate_user_creation.assert_called_once()
        mock_user_repository.save.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_user_validation_failure(self, user_service, mock_user_domain_service):
        """Test user creation with validation failure."""
        # Arrange
        request = CreateUserRequest(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
        )
        
        mock_user_domain_service.validate_user_creation.side_effect = ValueError("Email already exists")
        
        # Act & Assert
        with pytest.raises(ValueError, match="Email already exists"):
            await user_service.create_user(request)

    @pytest.mark.asyncio
    async def test_get_user_by_id_found(self, user_service, mock_user_repository):
        """Test getting user by ID when user exists."""
        # Arrange
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        user = User(
            id=UserId.from_string(user_id),
            email=Email.from_string("test@example.com"),
            first_name="John",
            last_name="Doe",
        )
        
        mock_user_repository.find_by_id.return_value = user
        
        # Act
        result = await user_service.get_user_by_id(user_id)
        
        # Assert
        assert result is not None
        assert result.id == user_id
        assert result.email == "test@example.com"

    @pytest.mark.asyncio
    async def test_get_user_by_id_not_found(self, user_service, mock_user_repository):
        """Test getting user by ID when user doesn't exist."""
        # Arrange
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        mock_user_repository.find_by_id.return_value = None
        
        # Act
        result = await user_service.get_user_by_id(user_id)
        
        # Assert
        assert result is None

    @pytest.mark.asyncio
    async def test_update_user_success(self, user_service, mock_user_repository, mock_user_domain_service):
        """Test successful user update."""
        # Arrange
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        request = UpdateUserRequest(
            first_name="Jane",
            last_name="Smith",
        )
        
        existing_user = User(
            id=UserId.from_string(user_id),
            email=Email.from_string("test@example.com"),
            first_name="John",
            last_name="Doe",
        )
        
        updated_user = User(
            id=UserId.from_string(user_id),
            email=Email.from_string("test@example.com"),
            first_name="Jane",
            last_name="Smith",
        )
        
        mock_user_repository.find_by_id.return_value = existing_user
        mock_user_repository.save.return_value = updated_user
        
        # Act
        result = await user_service.update_user(user_id, request)
        
        # Assert
        assert result is not None
        assert result.first_name == "Jane"
        assert result.last_name == "Smith"
        assert result.full_name == "Jane Smith"

    @pytest.mark.asyncio
    async def test_delete_user_success(self, user_service, mock_user_repository, mock_user_domain_service):
        """Test successful user deletion."""
        # Arrange
        user_id = "123e4567-e89b-12d3-a456-426614174000"
        
        mock_user_domain_service.can_user_be_deleted.return_value = True
        mock_user_repository.delete.return_value = True
        
        # Act
        result = await user_service.delete_user(user_id)
        
        # Assert
        assert result is True
        mock_user_domain_service.can_user_be_deleted.assert_called_once()
        mock_user_repository.delete.assert_called_once()
