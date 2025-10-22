"""User domain entity."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict

from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId


class User(BaseModel):
    """User domain entity."""

    id: UserId = Field(default_factory=UserId.generate)
    email: Email
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default=None)

    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"

    def activate(self) -> None:
        """Activate the user."""
        self.is_active = True
        self.updated_at = datetime.now(timezone.utc)

    def deactivate(self) -> None:
        """Deactivate the user."""
        self.is_active = False
        self.updated_at = datetime.now(timezone.utc)

    def update_name(self, first_name: str, last_name: str) -> None:
        """Update user's name."""
        if not first_name or not last_name:
            raise ValueError("First name and last name cannot be empty")
        
        self.first_name = first_name
        self.last_name = last_name
        self.updated_at = datetime.now(timezone.utc)

    def update_email(self, email: Email) -> None:
        """Update user's email."""
        self.email = email
        self.updated_at = datetime.now(timezone.utc)

    def __str__(self) -> str:
        """String representation."""
        return f"User(id={self.id}, email={self.email}, name={self.full_name})"

    model_config = ConfigDict(arbitrary_types_allowed=True)
