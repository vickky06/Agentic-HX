"""External email service interface."""

from abc import ABC, abstractmethod
from typing import Dict, Any


class EmailService(ABC):
    """Abstract email service interface."""

    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str, **kwargs: Any) -> bool:
        """Send an email."""
        pass

    @abstractmethod
    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user."""
        pass

    @abstractmethod
    async def send_password_reset_email(self, user_email: str, reset_token: str) -> bool:
        """Send password reset email."""
        pass
