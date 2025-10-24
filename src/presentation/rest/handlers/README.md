# Request Handlers

## Role
HTTP request/response handling. Convert HTTP requests to application service calls.

## What to Add Here
- HTTP endpoint handlers
- Request/response mapping
- Error handling and HTTP status codes

## Example
```python
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = await user_service.create_user(request)
        return user
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
```

## Connections
- **Implements**: HTTP endpoints
- **Uses**: Application services through dependency injection
- **Used by**: API layer through router registration
- **Example**: HTTP POST /users → `create_user()` → `UserService.create_user()`
