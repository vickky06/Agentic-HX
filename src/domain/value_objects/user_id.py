"""User ID value object."""

from __future__ import annotations

import uuid
from typing import Any

from pydantic import BaseModel, Field, field_validator


class UserId(BaseModel):
    """User ID value object."""

    value: str = Field(..., min_length=1)

    @field_validator("value")
    @classmethod
    def validate_uuid(cls, v: str) -> str:
        """Validate UUID format."""
        try:
            uuid.UUID(v)
            return v
        except ValueError:
            raise ValueError("Invalid UUID format")

    def __str__(self) -> str:
        """String representation."""
        return self.value

    def __eq__(self, other: Any) -> bool:
        """Equality comparison."""
        if not isinstance(other, UserId):
            return False
        return self.value == other.value

    def __hash__(self) -> int:
        """Hash for use in sets and dicts."""
        return hash(self.value)

    @classmethod
    def generate(cls) -> UserId:
        """Generate a new UserId."""
        return cls(value=str(uuid.uuid4()))

    @classmethod
    def from_string(cls, user_id_str: str) -> UserId:
        """Create UserId from string."""
        return cls(value=user_id_str)
