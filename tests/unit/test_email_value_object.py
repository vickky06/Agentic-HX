"""Unit tests for Email value object."""

import pytest

from src.domain.value_objects.email import Email


class TestEmailValueObject:
    """Test cases for Email value object."""

    def test_create_valid_email(self):
        """Test creating a valid email."""
        email = Email.from_string("test@example.com")
        assert email.value == "test@example.com"

    def test_email_normalization(self):
        """Test email normalization (lowercase and trim)."""
        email = Email.from_string("  TEST@EXAMPLE.COM  ")
        assert email.value == "test@example.com"

    def test_invalid_email_format(self):
        """Test invalid email format."""
        with pytest.raises(ValueError, match="Invalid email format"):
            Email.from_string("invalid-email")

    def test_empty_email(self):
        """Test empty email."""
        with pytest.raises(ValueError, match="Email cannot be empty"):
            Email.from_string("")

    def test_email_equality(self):
        """Test email equality."""
        email1 = Email.from_string("test@example.com")
        email2 = Email.from_string("test@example.com")
        email3 = Email.from_string("other@example.com")
        
        assert email1 == email2
        assert email1 != email3

    def test_email_hash(self):
        """Test email hash."""
        email1 = Email.from_string("test@example.com")
        email2 = Email.from_string("test@example.com")
        
        assert hash(email1) == hash(email2)

    def test_email_string_representation(self):
        """Test email string representation."""
        email = Email.from_string("test@example.com")
        assert str(email) == "test@example.com"
