# Application Services (Use Cases)

## Role
Application-specific business logic and use cases. Orchestrate domain objects.

## What to Add Here
- Use case implementations (e.g., `CreateUser`, `UpdateUser`, `DeleteUser`)
- Application workflows and business processes
- Coordination between domain objects

## Example
```python
class UserService:
    async def create_user(self, request: CreateUserRequest) -> UserResponse:
        email = Email.from_string(request.email)
        await self._user_domain_service.validate_user_creation(email, request.first_name, request.last_name)
        user = User(email=email, first_name=request.first_name, last_name=request.last_name)
        saved_user = await self._user_repository.save(user)
        return self._to_user_response(saved_user)
```

## Connections
- **Implements**: Use cases and application workflows
- **Uses**: Domain services, entities, repository interfaces
- **Used by**: Presentation handlers
- **Example**: `UserHandler.create_user()` → `UserService.create_user()`
