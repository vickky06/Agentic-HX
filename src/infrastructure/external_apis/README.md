# External APIs

## Role
Interfaces and implementations for external service integrations.

## What to Add Here
- External service interfaces (e.g., email, payment, notification services)
- Service implementations (SMTP, REST APIs, message queues)
- External API clients and adapters

## Example
```python
class EmailService(ABC):
    @abstractmethod
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        pass

class SMTPEmailService(EmailService):
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        # SMTP implementation
```

## Connections
- **Implements**: External service contracts
- **Used by**: Application services, domain services
- **Uses**: External systems (SMTP, REST APIs)
- **Example**: `UserService` → `EmailService` → `SMTPEmailService`
