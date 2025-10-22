"""SMTP email service implementation."""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Any

from .email_service import EmailService


class SMTPEmailService(EmailService):
    """SMTP email service implementation."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        username: str,
        password: str,
        from_email: str,
    ):
        """Initialize SMTP email service."""
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.from_email = from_email

    async def send_email(self, to: str, subject: str, body: str, **kwargs: Any) -> bool:
        """Send an email via SMTP."""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False

    async def send_welcome_email(self, user_email: str, user_name: str) -> bool:
        """Send welcome email to new user."""
        subject = "Welcome to our platform!"
        body = f"""
        <html>
        <body>
            <h2>Welcome {user_name}!</h2>
            <p>Thank you for joining our platform. We're excited to have you on board!</p>
            <p>If you have any questions, feel free to reach out to our support team.</p>
            <br>
            <p>Best regards,<br>The Team</p>
        </body>
        </html>
        """
        return await self.send_email(user_email, subject, body)

    async def send_password_reset_email(self, user_email: str, reset_token: str) -> bool:
        """Send password reset email."""
        subject = "Password Reset Request"
        body = f"""
        <html>
        <body>
            <h2>Password Reset Request</h2>
            <p>You have requested to reset your password.</p>
            <p>Click the link below to reset your password:</p>
            <a href="https://yourapp.com/reset-password?token={reset_token}">Reset Password</a>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
            <br>
            <p>Best regards,<br>The Team</p>
        </body>
        </html>
        """
        return await self.send_email(user_email, subject, body)
