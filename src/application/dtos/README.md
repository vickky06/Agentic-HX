# Data Transfer Objects (DTOs)

## Role
Objects for data transfer between layers. API request/response models.

## What to Add Here
- Request DTOs for API inputs
- Response DTOs for API outputs
- Validation and serialization logic

## Example
```python
class CreateUserRequest(BaseModel):
    email: str = Field(..., min_length=1, max_length=255)
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

class UserResponse(BaseModel):
    id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    is_active: bool
```

## Connections
- **Implements**: API contracts and data validation
- **Used by**: Presentation handlers, application services
- **Maps to/from**: Domain entities
- **Example**: `UserHandler` → `CreateUserRequest` → `UserService` → `UserResponse`
