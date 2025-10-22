"""User DTOs for application layer."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateUserRequest(BaseModel):
    """Request DTO for creating a user."""

    email: str = Field(..., min_length=1, max_length=255)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)


class UpdateUserRequest(BaseModel):
    """Request DTO for updating a user."""

    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[str] = Field(None, min_length=1, max_length=255)


class UserResponse(BaseModel):
    """Response DTO for user data."""

    id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        """Pydantic configuration."""
        from_attributes = True


class UserListResponse(BaseModel):
    """Response DTO for user list."""

    users: list[UserResponse]
    total: int
    skip: int
    limit: int
