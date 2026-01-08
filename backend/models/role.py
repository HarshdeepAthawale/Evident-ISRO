"""
EVIDENT Role and Permission Models

This module defines the Role and DocumentPermission models for access control.
"""

from sqlalchemy import Column, String, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid
import enum

from backend.core.database import Base


class PermissionType(str, enum.Enum):
    """Permission type enumeration."""
    READ = "read"
    WRITE = "write"
    DELETE = "delete"


class Role(Base):
    """
    Role model for role-based access control.
    
    Attributes:
        id: Unique identifier (UUID)
        name: Role name (unique)
        description: Role description
        permissions: JSON object with permission mappings
    """
    
    __tablename__ = "roles"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    name = Column(
        String(100),
        unique=True,
        nullable=False
    )
    description = Column(
        String(500),
        nullable=True
    )
    permissions = Column(
        JSON,
        nullable=False,
        default=dict,
        comment="JSON object with permission mappings"
    )


class DocumentPermission(Base):
    """
    DocumentPermission model for document-level access control.
    
    Attributes:
        id: Unique identifier (UUID)
        document_id: Document ID (FK to Document)
        user_id: User ID (FK to User, nullable if role-based)
        role: Role name (nullable if user-based)
        permission_type: Type of permission (read, write, delete)
        created_at: Timestamp when permission was created
    """
    
    __tablename__ = "document_permissions"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    role = Column(
        String(50),
        nullable=True,
        comment="Role name if permission is role-based"
    )
    permission_type = Column(
        Enum(PermissionType),
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    document = relationship(
        "Document",
        back_populates="permissions"
    )
    user = relationship(
        "User",
        back_populates="document_permissions"
    )
    
    # Ensure either user_id or role is set
    __table_args__ = (
        {"comment": "Document-level permissions for users or roles"}
    )
