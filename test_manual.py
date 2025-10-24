#!/usr/bin/env python3
"""Manual testing script for the hexagonal architecture application."""

import asyncio
import sys
from datetime import datetime

from src.domain.entities.user import User
from src.domain.value_objects.email import Email
from src.domain.value_objects.user_id import UserId


def test_domain_entities():
    """Test domain entities and value objects."""
    print("🧪 Testing Domain Entities...")
    print("=" * 40)
    
    # Test Email value object
    try:
        email = Email.from_string("test@example.com")
        print(f"✅ Email created: {email}")
        
        # Test email validation
        try:
            invalid_email = Email.from_string("invalid-email")
            print("❌ Invalid email should have failed")
        except ValueError as e:
            print(f"✅ Email validation works: {e}")
        
        # Test email normalization
        normalized_email = Email.from_string("  TEST@EXAMPLE.COM  ")
        print(f"✅ Email normalized: {normalized_email}")
        
    except Exception as e:
        print(f"❌ Email test failed: {e}")
    
    # Test UserId value object
    try:
        user_id = UserId.generate()
        print(f"✅ UserId generated: {user_id}")
        
        user_id_from_string = UserId.from_string(str(user_id))
        print(f"✅ UserId from string: {user_id_from_string}")
        
    except Exception as e:
        print(f"❌ UserId test failed: {e}")
    
    # Test User entity
    try:
        email = Email.from_string("john.doe@example.com")
        user = User(
            email=email,
            first_name="John",
            last_name="Doe"
        )
        print(f"✅ User created: {user}")
        print(f"   Full name: {user.full_name}")
        print(f"   Is active: {user.is_active}")
        
        # Test user methods
        user.activate()
        print(f"✅ User activated: {user.is_active}")
        
        user.update_name("Jane", "Smith")
        print(f"✅ User name updated: {user.full_name}")
        
        new_email = Email.from_string("jane.smith@example.com")
        user.update_email(new_email)
        print(f"✅ User email updated: {user.email}")
        
    except Exception as e:
        print(f"❌ User test failed: {e}")
    
    print("=" * 40)


def test_application_services():
    """Test application services (without database)."""
    print("🧪 Testing Application Services...")
    print("=" * 40)
    
    try:
        from src.application.dtos.user_dto import CreateUserRequest, UserResponse
        
        # Test DTOs
        request = CreateUserRequest(
            email="test@example.com",
            first_name="John",
            last_name="Doe"
        )
        print(f"✅ CreateUserRequest: {request}")
        
        # Test response DTO
        response = UserResponse(
            id="123e4567-e89b-12d3-a456-426614174000",
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            full_name="John Doe",
            is_active=True,
            created_at=datetime.now()
        )
        print(f"✅ UserResponse: {response}")
        
    except Exception as e:
        print(f"❌ Application services test failed: {e}")
    
    print("=" * 40)


def test_infrastructure():
    """Test infrastructure components."""
    print("🧪 Testing Infrastructure...")
    print("=" * 40)
    
    try:
        from src.infrastructure.database.config import DatabaseConfig
        
        # Test database configuration
        config = DatabaseConfig()
        print(f"✅ Database config created")
        print(f"   Host: {config.host}")
        print(f"   Port: {config.port}")
        print(f"   Database: {config.name}")
        print(f"   URL: {config.url}")
        
    except Exception as e:
        print(f"❌ Infrastructure test failed: {e}")
    
    print("=" * 40)


def test_presentation():
    """Test presentation layer."""
    print("🧪 Testing Presentation Layer...")
    print("=" * 40)
    
    try:
        from src.presentation.rest.api.app import create_app
        
        # Test FastAPI app creation
        app = create_app()
        print(f"✅ FastAPI app created")
        print(f"   Title: {app.title}")
        print(f"   Version: {app.version}")
        print(f"   Routes: {len(app.routes)}")
        
        # List available routes
        for route in app.routes:
            if hasattr(route, 'path') and hasattr(route, 'methods'):
                print(f"   Route: {route.methods} {route.path}")
        
    except Exception as e:
        print(f"❌ Presentation test failed: {e}")
    
    print("=" * 40)


def main():
    """Run all manual tests."""
    print("🚀 Starting Manual Tests for Hexagonal Architecture")
    print("=" * 60)
    
    test_domain_entities()
    test_application_services()
    test_infrastructure()
    test_presentation()
    
    print("🏁 Manual Tests completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
