#!/usr/bin/env python3
"""Simple API test to verify the hexagonal architecture works."""

import asyncio
import json
from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.presentation.rest.api.app import create_app
from src.presentation.dependencies import create_user_service
from src.application.dtos.user_dto import CreateUserRequest


async def test_api_directly():
    """Test the API directly without HTTP."""
    print("🧪 Testing API directly...")
    
    try:
        # Create user service
        user_service = await create_user_service()
        print("✅ User service created")
        
        # Test user creation
        request = CreateUserRequest(
            email="direct@example.com",
            first_name="Direct",
            last_name="Test"
        )
        
        result = await user_service.create_user(request)
        print(f"✅ User created: {result}")
        
        # Test getting users
        users = await user_service.get_users()
        print(f"✅ Users retrieved: {users}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


def test_api_with_testclient():
    """Test the API using FastAPI TestClient."""
    print("🧪 Testing API with TestClient...")
    
    try:
        app = create_app()
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        print(f"✅ Health check: {response.status_code} - {response.json()}")
        
        # Test root endpoint
        response = client.get("/")
        print(f"✅ Root endpoint: {response.status_code} - {response.json()}")
        
        # Test user creation
        user_data = {
            "email": "testclient@example.com",
            "first_name": "TestClient",
            "last_name": "User"
        }
        
        response = client.post("/users/", json=user_data)
        print(f"✅ User creation: {response.status_code}")
        if response.status_code == 201:
            print(f"   Response: {response.json()}")
        else:
            print(f"   Error: {response.text}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


async def main():
    """Run all tests."""
    print("🚀 Testing Hexagonal Architecture API")
    print("=" * 50)
    
    await test_api_directly()
    print()
    test_api_with_testclient()
    
    print("=" * 50)
    print("🏁 Tests completed!")


if __name__ == "__main__":
    asyncio.run(main())
