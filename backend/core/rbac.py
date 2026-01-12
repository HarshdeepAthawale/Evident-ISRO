"""
EVIDENT Role-Based Access Control (RBAC)

This module provides core RBAC functionality for checking roles,
permissions, and mission access.
"""

from typing import List, Optional
from sqlalchemy.orm import Session

from backend.models.user import User, UserRole
from backend.models.document import Document
from backend.models.role import DocumentPermission, PermissionType


class RoleChecker:
    """
    Utility class for role and permission checking.
    """
    
    # Role hierarchy: higher roles inherit permissions of lower roles
    ROLE_HIERARCHY = {
        UserRole.ADMIN: [UserRole.ADMIN, UserRole.ENGINEER, UserRole.VIEWER],
        UserRole.ENGINEER: [UserRole.ENGINEER, UserRole.VIEWER],
        UserRole.VIEWER: [UserRole.VIEWER]
    }
    
    # Permission mappings by role
    ROLE_PERMISSIONS = {
        UserRole.ADMIN: {
            "users:read", "users:write", "users:delete",
            "documents:read", "documents:write", "documents:delete",
            "roles:read", "roles:write", "roles:delete",
            "missions:read", "missions:write", "missions:delete",
            "admin:access"
        },
        UserRole.ENGINEER: {
            "documents:read", "documents:write",
            "missions:read"
        },
        UserRole.VIEWER: {
            "documents:read",
            "missions:read"
        }
    }
    
    @staticmethod
    def has_role(user: User, role: str) -> bool:
        """
        Check if user has a specific role.
        
        Args:
            user: User object
            role: Role name to check
            
        Returns:
            True if user has the role, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        try:
            role_enum = UserRole(role.lower())
            return user.role == role_enum
        except ValueError:
            return False
    
    @staticmethod
    def has_any_role(user: User, roles: List[str]) -> bool:
        """
        Check if user has any of the specified roles.
        
        Args:
            user: User object
            roles: List of role names to check
            
        Returns:
            True if user has any of the roles, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        for role in roles:
            if RoleChecker.has_role(user, role):
                return True
        
        return False
    
    @staticmethod
    def has_permission(user: User, permission: str) -> bool:
        """
        Check if user has a specific permission.
        
        Admins have all permissions. Other roles have permissions
        defined in ROLE_PERMISSIONS.
        
        Args:
            user: User object
            permission: Permission string (e.g., "documents:read")
            
        Returns:
            True if user has the permission, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        # Admins have all permissions
        if user.role == UserRole.ADMIN:
            return True
        
        # Check role permissions
        role_perms = RoleChecker.ROLE_PERMISSIONS.get(user.role, set())
        return permission in role_perms
    
    @staticmethod
    def can_access_mission(user: User, mission: Optional[str], db: Optional[Session] = None) -> bool:
        """
        Check if user can access a specific mission.
        
        - Admins can access all missions (including None)
        - Engineers and viewers can access missions they're assigned to
        - For now, we assume all engineers/viewers can access all missions
          (mission assignment can be added in a future phase)
        
        Args:
            user: User object
            mission: Mission name (can be None)
            db: Optional database session for checking mission assignments
            
        Returns:
            True if user can access the mission, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        # Admins can access all missions
        if user.role == UserRole.ADMIN:
            return True
        
        # If no mission specified, allow access (for non-mission-scoped resources)
        if mission is None:
            return True
        
        # TODO: In future phases, check user's assigned missions
        # For now, engineers and viewers can access all missions
        # This can be extended with a user_missions table or user.missions field
        return True
    
    @staticmethod
    def can_access_document(user: User, document: Document, db: Session) -> bool:
        """
        Check if user can access a specific document.
        
        - Admins can access all documents
        - Check document-level permissions
        - Check mission access
        - Check role-based permissions
        
        Args:
            user: User object
            document: Document object
            db: Database session
            
        Returns:
            True if user can access the document, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        # Admins can access all documents
        if user.role == UserRole.ADMIN:
            return True
        
        # Check mission access
        if not RoleChecker.can_access_mission(user, document.mission, db):
            return False
        
        # Check document-level permissions
        # First check user-specific permissions
        user_permission = db.query(DocumentPermission).filter(
            DocumentPermission.document_id == document.id,
            DocumentPermission.user_id == user.id
        ).first()
        
        if user_permission:
            return user_permission.permission_type in [
                PermissionType.READ,
                PermissionType.WRITE,
                PermissionType.DELETE
            ]
        
        # Check role-based permissions
        role_permission = db.query(DocumentPermission).filter(
            DocumentPermission.document_id == document.id,
            DocumentPermission.role == user.role.value
        ).first()
        
        if role_permission:
            return role_permission.permission_type in [
                PermissionType.READ,
                PermissionType.WRITE,
                PermissionType.DELETE
            ]
        
        # Default: check role permissions
        # Engineers can read/write, viewers can only read
        if user.role == UserRole.ENGINEER:
            return True  # Engineers can read/write documents in their missions
        elif user.role == UserRole.VIEWER:
            return True  # Viewers can read documents in their missions
        
        return False
    
    @staticmethod
    def can_modify_document(user: User, document: Document, db: Session) -> bool:
        """
        Check if user can modify (write/delete) a specific document.
        
        Args:
            user: User object
            document: Document object
            db: Database session
            
        Returns:
            True if user can modify the document, False otherwise
        """
        if not user or not user.is_active:
            return False
        
        # Admins can modify all documents
        if user.role == UserRole.ADMIN:
            return True
        
        # Check mission access
        if not RoleChecker.can_access_mission(user, document.mission, db):
            return False
        
        # Check document-level permissions
        user_permission = db.query(DocumentPermission).filter(
            DocumentPermission.document_id == document.id,
            DocumentPermission.user_id == user.id,
            DocumentPermission.permission_type.in_([
                PermissionType.WRITE,
                PermissionType.DELETE
            ])
        ).first()
        
        if user_permission:
            return True
        
        # Check role-based permissions
        role_permission = db.query(DocumentPermission).filter(
            DocumentPermission.document_id == document.id,
            DocumentPermission.role == user.role.value,
            DocumentPermission.permission_type.in_([
                PermissionType.WRITE,
                PermissionType.DELETE
            ])
        ).first()
        
        if role_permission:
            return True
        
        # Default: engineers can modify, viewers cannot
        return user.role == UserRole.ENGINEER
