# Integration Tests

## Role
Test component interactions and application services with real dependencies.

## What to Add Here
- Application service tests
- Repository implementation tests
- Component interaction tests
- Database integration tests

## Example
```python
@pytest.mark.asyncio
async def test_create_user_success(self, user_service, mock_user_repository):
    request = CreateUserRequest(email="test@example.com", first_name="John", last_name="Doe")
    result = await user_service.create_user(request)
    assert result.email == "test@example.com"
```

## Connections
- **Tests**: Application services, repository implementations
- **Uses**: Real or mocked infrastructure dependencies
- **Example**: `test_user_service.py` → `UserService` with mocked `UserRepository`
