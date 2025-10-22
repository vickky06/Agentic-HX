"""Unit tests for User entity."""

import pytest
from datetime import datetime

from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId


class TestUserEntity:
    """Test cases for User entity."""

    def test_create_user(self):
        """Test user creation."""
        email = Email.from_string("test@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe",
        )
        
        assert user.email == email
        assert user.first_name == "John"
        assert user.last_name == "Doe"
        assert user.is_active is True
        assert user.full_name == "John Doe"
        assert isinstance(user.id, UserId)
        assert isinstance(user.created_at, datetime)

    def test_activate_user(self):
        """Test user activation."""
        email = Email.from_string("test@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe",
            is_active=False,
        )
        
        user.activate()
        
        assert user.is_active is True
        assert user.updated_at is not None

    def test_deactivate_user(self):
        """Test user deactivation."""
        email = Email.from_string("test@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe",
        )
        
        user.deactivate()
        
        assert user.is_active is False
        assert user.updated_at is not None

    def test_update_name(self):
        """Test name update."""
        email = Email.from_string("test@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe",
        )
        
        user.update_name("Jane", "Smith")
        
        assert user.first_name == "Jane"
        assert user.last_name == "Smith"
        assert user.full_name == "Jane Smith"
        assert user.updated_at is not None

    def test_update_name_with_empty_values(self):
        """Test name update with empty values."""
        email = Email.from_string("test@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe",
        )
        
        with pytest.raises(ValueError, match="First name and last name cannot be empty"):
            user.update_name("", "Smith")

    def test_update_email(self):
        """Test email update."""
        email = Email.from_string("test@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe",
        )
        
        new_email = Email.from_string("new@example.com")
        user.update_email(new_email)
        
        assert user.email == new_email
        assert user.updated_at is not None
