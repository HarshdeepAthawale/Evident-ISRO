"""
EVIDENT Permission Decorators and Utilities

This module provides decorators and utilities for enforcing
role-based access control at the endpoint level.
"""

from typing import Any
from fastapi import Depends, HTTPException, status

from backend.auth.dependencies import get_current_active_user
from backend.core.rbac import RoleChecker
from backend.models.user import User
from backend.utils.logger import StructuredLogger

logger = StructuredLogger.get_logger()


def require_roles(*roles: str):
    """
    Create a FastAPI dependency that requires user to have one of the specified roles.
    
    Usage:
        @router.get("/endpoint")
        async def my_endpoint(
            current_user: User = Depends(get_current_active_user),
            _: None = Depends(require_roles("admin", "engineer"))
        ):
            pass
    
    Args:
        *roles: Variable number of role names (e.g., "admin", "engineer", "viewer")
        
    Returns:
        FastAPI dependency function
    """
    def role_check(current_user: User = Depends(get_current_active_user)) -> None:
        if not RoleChecker.has_any_role(current_user, list(roles)):
            logger.warning(
                f"Access denied: User {current_user.username} lacks required roles: {roles}",
                extra={
                    "user_id": str(current_user.id),
                    "username": current_user.username,
                    "required_roles": list(roles),
                    "user_role": current_user.role.value,
                    "event": "authorization_denied"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(roles)}"
            )
        return None
    
    return role_check


def require_permission(permission: str):
    """
    Create a FastAPI dependency that requires user to have a specific permission.
    
    Usage:
        @router.get("/endpoint")
        async def my_endpoint(
            current_user: User = Depends(get_current_active_user),
            _: None = Depends(require_permission("documents:read"))
        ):
            pass
    
    Args:
        permission: Permission string (e.g., "documents:read", "users:write")
        
    Returns:
        FastAPI dependency function
    """
    def permission_check(current_user: User = Depends(get_current_active_user)) -> None:
        if not RoleChecker.has_permission(current_user, permission):
            logger.warning(
                f"Access denied: User {current_user.username} lacks required permission: {permission}",
                extra={
                    "user_id": str(current_user.id),
                    "username": current_user.username,
                    "required_permission": permission,
                    "user_role": current_user.role.value,
                    "event": "authorization_denied"
                }
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required permission: {permission}"
            )
        return None
    
    return permission_check


def require_admin():
    """
    Create a FastAPI dependency that requires admin role.
    
    Usage:
        @router.get("/admin/endpoint")
        async def admin_endpoint(
            current_user: User = Depends(get_current_active_user),
            _: None = Depends(require_admin())
        ):
            pass
    
    Returns:
        FastAPI dependency function
    """
    return require_roles("admin")


def require_engineer_or_admin():
    """
    Create a FastAPI dependency that requires engineer or admin role.
    
    Usage:
        @router.post("/documents")
        async def upload_document(
            current_user: User = Depends(get_current_active_user),
            _: None = Depends(require_engineer_or_admin())
        ):
            pass
    
    Returns:
        FastAPI dependency function
    """
    return require_roles("admin", "engineer")


def check_mission_access(mission: str, user: User, db: Any = None) -> bool:
    """
    Check if user can access a specific mission.
    
    This is a utility function for inline permission checks.
    
    Args:
        mission: Mission name
        user: User object
        db: Optional database session
        
    Returns:
        True if user can access the mission, False otherwise
    """
    return RoleChecker.can_access_mission(user, mission, db)


# Alias for require_roles (for backward compatibility)
get_role_dependency = require_roles
