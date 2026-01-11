"""
EVIDENT Authentication Module

This package provides authentication and authorization functionality,
including JWT token management and FastAPI dependencies.
"""

from backend.auth.jwt import (
    create_access_token,
    create_refresh_token,
    verify_token,
    decode_token,
    get_user_id_from_token,
)
from backend.auth.dependencies import (
    get_current_user,
    get_current_active_user,
    get_optional_current_user,
    security,
)

__all__ = [
    # JWT functions
    "create_access_token",
    "create_refresh_token",
    "verify_token",
    "decode_token",
    "get_user_id_from_token",
    # Dependencies
    "get_current_user",
    "get_current_active_user",
    "get_optional_current_user",
    "security",
]
