"""User HTTP handlers."""

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.application.dtos.user_dto import CreateUserRequest, UpdateUserRequest, UserResponse, UserListResponse
from src.application.services.user_service import UserService
from src.presentation.dependencies import get_user_service

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    request: CreateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Create a new user."""
    try:
        user = await user_service.create_user(request)
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Get user by ID."""
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.get("/", response_model=UserListResponse)
async def get_users(
    skip: int = 0,
    limit: int = 100,
    user_service: UserService = Depends(get_user_service),
) -> UserListResponse:
    """Get list of users with pagination."""
    if skip < 0 or limit <= 0 or limit > 1000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid pagination parameters",
        )
    
    users = await user_service.get_users(skip=skip, limit=limit)
    return users


@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    request: UpdateUserRequest,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Update user."""
    try:
        user = await user_service.update_user(user_id, request)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> JSONResponse:
    """Delete user."""
    try:
        success = await user_service.delete_user(user_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )
        return JSONResponse(content=None, status_code=status.HTTP_204_NO_CONTENT)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )


@router.post("/{user_id}/activate", response_model=UserResponse)
async def activate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Activate user."""
    user = await user_service.activate_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user


@router.post("/{user_id}/deactivate", response_model=UserResponse)
async def deactivate_user(
    user_id: str,
    user_service: UserService = Depends(get_user_service),
) -> UserResponse:
    """Deactivate user."""
    user = await user_service.deactivate_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    return user
