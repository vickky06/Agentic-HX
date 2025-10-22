# Repository Interfaces (Ports)

## Role
Contracts for data access. Define what the domain needs from data layer.

## What to Add Here
- Abstract repository interfaces
- Domain-specific data access contracts
- Port definitions for external dependencies

## Example
```python
class UserRepository(ABC):
    @abstractmethod
    async def save(self, user: User) -> User:
        pass
    
    @abstractmethod
    async def find_by_id(self, user_id: UserId) -> Optional[User]:
        pass
```

## Connections
- **Implements**: Data access contracts (ports)
- **Implemented by**: Infrastructure adapters
- **Used by**: Domain services, application services
- **Example**: `UserDomainService` → `UserRepository` (interface) ← `UserRepositoryImpl` (infrastructure)
