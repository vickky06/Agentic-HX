"""Email value object."""

from __future__ import annotations

import re
from typing import Any

from pydantic import BaseModel, Field, field_validator


class Email(BaseModel):
    """Email value object with validation."""

    value: str = Field(..., max_length=255)

    @field_validator("value")
    @classmethod
    def validate_email(cls, v: str) -> str:
        """Validate email format."""
        # Normalize first (trim and lowercase)
        normalized = v.strip().lower()
        
        if not normalized:
            raise ValueError("Email cannot be empty")
        
        # Basic email regex pattern
        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, normalized):
            raise ValueError("Invalid email format")
        
        return normalized

    def __str__(self) -> str:
        """String representation."""
        return self.value

    def __eq__(self, other: Any) -> bool:
        """Equality comparison."""
        if not isinstance(other, Email):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.value)

    @classmethod
    def from_string(cls, email_str: str) -> Email:
        """Create Email from string."""
        return cls(value=email_str)
