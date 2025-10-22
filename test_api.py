#!/usr/bin/env python3
"""API testing script for the hexagonal architecture application."""

import asyncio
import json
import sys
from typing import Dict, Any

import httpx


class APITester:
    """Simple API tester for the hexagonal architecture application."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = httpx.AsyncClient()
    
    async def test_health_endpoint(self) -> bool:
        """Test the health endpoint."""
        try:
            response = await self.client.get(f"{self.base_url}/health")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Health check: {data}")
                return True
            else:
                print(f"❌ Health check failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Health check error: {e}")
            return False
    
    async def test_root_endpoint(self) -> bool:
        """Test the root endpoint."""
        try:
            response = await self.client.get(f"{self.base_url}/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Root endpoint: {data}")
                return True
            else:
                print(f"❌ Root endpoint failed: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Root endpoint error: {e}")
            return False
    
    async def test_create_user(self, user_data: Dict[str, Any]) -> bool:
        """Test user creation."""
        try:
            response = await self.client.post(
                f"{self.base_url}/users/",
                json=user_data
            )
            if response.status_code == 201:
                data = response.json()
                print(f"✅ User created: {data}")
                return True
            else:
                print(f"❌ User creation failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ User creation error: {e}")
            return False
    
    async def test_get_users(self) -> bool:
        """Test getting users list."""
        try:
            response = await self.client.get(f"{self.base_url}/users/")
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Users list: {data}")
                return True
            else:
                print(f"❌ Get users failed: {response.status_code}")
                print(f"Response: {response.text}")
                return False
        except Exception as e:
            print(f"❌ Get users error: {e}")
            return False
    
    async def run_all_tests(self) -> None:
        """Run all API tests."""
        print("🧪 Starting API Tests...")
        print("=" * 50)
        
        # Test basic endpoints
        await self.test_health_endpoint()
        await self.test_root_endpoint()
        
        # Test user operations
        user_data = {
            "email": "test@example.com",
            "first_name": "John",
            "last_name": "Doe"
        }
        
        await self.test_create_user(user_data)
        await self.test_get_users()
        
        print("=" * 50)
        print("🏁 API Tests completed!")
    
    async def close(self):
        """Close the HTTP client."""
        await self.client.aclose()


async def main():
    """Main function to run API tests."""
    tester = APITester()
    
    try:
        await tester.run_all_tests()
    finally:
        await tester.close()


if __name__ == "__main__":
    asyncio.run(main())
