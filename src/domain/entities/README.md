# Domain Entities

## Role
Core business objects with identity and lifecycle. Contain business logic and rules.

## What to Add Here
- Business entities with identity (e.g., `User`, `Order`, `Product`)
- Business methods and validation logic
- State transitions and business rules

## Example
```python
class User(BaseModel):
    id: UserId
    email: Email
    first_name: str
    last_name: str
    is_active: bool
    
    def activate(self) -> None:
        self.is_active = True
```

## Connections
- **Implements**: Business rules and entity behavior
- **Used by**: Application services, domain services
- **Contains**: Value objects (Email, UserId)
- **Example**: `UserService.create_user()` → `User` entity
