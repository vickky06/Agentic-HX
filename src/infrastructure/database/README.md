# Database Infrastructure

## Role
Database configuration, models, and connection management.

## What to Add Here
- Database configuration and connection setup
- SQLAlchemy models (database representations)
- Database migrations and schema management

## Example
```python
class UserModel(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(UUID(as_uuid=False), primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
```

## Connections
- **Implements**: Database persistence
- **Used by**: Repository implementations
- **Maps to/from**: Domain entities
- **Example**: `UserRepositoryImpl` → `UserModel` (database) ↔ `User` (domain)
