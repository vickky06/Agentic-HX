# End-to-End Tests

## Role
Test complete user workflows through the entire application stack.

## What to Add Here
- Full API workflow tests
- Database integration tests
- External service integration tests
- Complete user journey tests

## Example
```python
async def test_create_user_workflow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/users/", json={
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        })
        assert response.status_code == 201
        assert response.json()["email"] == "test@example.com"
```

## Connections
- **Tests**: Complete application workflows
- **Uses**: Real database, real external services
- **Example**: HTTP API → Application → Domain → Infrastructure → Database
