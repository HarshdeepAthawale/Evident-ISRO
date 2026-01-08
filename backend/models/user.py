"""
EVIDENT User Model

This module defines the User model for authentication and authorization.
"""

from sqlalchemy import Column, String, Boolean, DateTime, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from backend.core.database import Base


class UserRole(str, enum.Enum):
    """User role enumeration."""
    ADMIN = "admin"
    ENGINEER = "engineer"
    VIEWER = "viewer"


class User(Base):
    """
    User model for authentication and authorization.
    
    Attributes:
        id: Unique identifier (UUID)
        username: Unique username (indexed)
        email: Unique email address (indexed)
        hashed_password: Bcrypt hashed password
        full_name: User's full name
        role: User role (admin, engineer, viewer)
        is_active: Whether the user account is active
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    
    __tablename__ = "users"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    username = Column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )
    email = Column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    hashed_password = Column(
        String(255),
        nullable=False
    )
    full_name = Column(
        String(255),
        nullable=False
    )
    role = Column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.VIEWER
    )
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False
    )
    
    # Relationships
    documents = relationship(
        "Document",
        back_populates="uploader",
        cascade="all, delete-orphan"
    )
    audit_logs = relationship(
        "AuditLog",
        back_populates="user",
        cascade="all, delete-orphan"
    )
    document_permissions = relationship(
        "DocumentPermission",
        back_populates="user",
        cascade="all, delete-orphan"
    )
