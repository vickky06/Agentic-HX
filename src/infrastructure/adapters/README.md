# Infrastructure Adapters

## Role
Concrete implementations of domain interfaces. Bridge between domain and external systems.

## What to Add Here
- Repository implementations (e.g., `UserRepositoryImpl`)
- External service adapters
- Data mapping between domain and infrastructure

## Example
```python
class UserRepositoryImpl(UserRepository):
    def __init__(self, session: AsyncSession):
        self._session = session
    
    async def save(self, user: User) -> User:
        user_model = UserModel(
            id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
        )
        self._session.add(user_model)
        await self._session.commit()
        return self._to_entity(user_model)
```

## Connections
- **Implements**: Domain repository interfaces
- **Used by**: Application services through dependency injection
- **Uses**: Database models, external APIs
- **Example**: `UserService` → `UserRepository` (interface) ← `UserRepositoryImpl` (adapter)
