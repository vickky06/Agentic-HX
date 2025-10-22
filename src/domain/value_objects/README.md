# Value Objects

## Role
Immutable objects without identity. Represent concepts in the domain.

## What to Add Here
- Immutable objects with validation (e.g., `Email`, `Money`, `Address`)
- Value objects with business rules
- Objects that are equal by value, not identity

## Example
```python
class Email(BaseModel):
    value: str
    
    @field_validator("value")
    def validate_email(cls, v: str) -> str:
        if not re.match(email_pattern, v):
            raise ValueError("Invalid email format")
        return v.lower().strip()
```

## Connections
- **Implements**: Domain validation and business rules
- **Used by**: Domain entities, application DTOs
- **Example**: `User` entity → `Email` value object
