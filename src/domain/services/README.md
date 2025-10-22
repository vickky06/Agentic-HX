# Domain Services

## Role
Business logic that doesn't belong to a single entity. Complex domain operations.

## What to Add Here
- Business logic spanning multiple entities
- Domain validation and rules
- Complex business operations

## Example
```python
class UserDomainService:
    async def is_email_unique(self, email: Email, exclude_user_id: Optional[UserId] = None) -> bool:
        existing_user = await self._user_repository.find_by_email(email)
        return existing_user is None
```

## Connections
- **Implements**: Complex business logic
- **Used by**: Application services
- **Uses**: Repository interfaces, domain entities
- **Example**: `UserService` → `UserDomainService` → `UserRepository`
