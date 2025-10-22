# Unit Tests

## Role
Test individual components in isolation with mocked dependencies.

## What to Add Here
- Domain entity tests
- Value object tests
- Domain service tests
- Individual component tests

## Example
```python
def test_create_user(self):
    email = Email.from_string("test@example.com")
    user = User(email=email, first_name="John", last_name="Doe")
    assert user.email == email
    assert user.full_name == "John Doe"
```

## Connections
- **Tests**: Domain entities, value objects, domain services
- **Uses**: Mocked dependencies
- **Example**: `test_user_entity.py` → `User` entity, `test_email_value_object.py` → `Email` value object
