"""
EVIDENT Security Utilities

This module provides password hashing, verification, validation,
and other security-related utilities.
"""

import re
import secrets
from passlib.context import CryptContext
from typing import Optional

from backend.utils.exceptions import ValidationError

# Create password context with bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__rounds=12)


def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Args:
        password: Plain text password to hash
        
    Returns:
        Hashed password string
        
    Raises:
        ValueError: If password is empty
    """
    if not password:
        raise ValueError("Password cannot be empty")
    
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to verify against
        
    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def validate_password_strength(password: str) -> bool:
    """
    Validate password strength according to requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    
    Args:
        password: Password to validate
        
    Returns:
        True if password meets requirements, False otherwise
    """
    if len(password) < 8:
        return False
    
    if not re.search(r'[A-Z]', password):
        return False
    
    if not re.search(r'[a-z]', password):
        return False
    
    if not re.search(r'\d', password):
        return False
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    
    return True


def validate_password_strength_with_error(password: str) -> None:
    """
    Validate password strength and raise ValidationError if invalid.
    
    Args:
        password: Password to validate
        
    Raises:
        ValidationError: If password does not meet strength requirements
    """
    if not password:
        raise ValidationError(
            field="password",
            message="Password is required"
        )
    
    if len(password) < 8:
        raise ValidationError(
            field="password",
            message="Password must be at least 8 characters long"
        )
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            field="password",
            message="Password must contain at least one uppercase letter"
        )
    
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            field="password",
            message="Password must contain at least one lowercase letter"
        )
    
    if not re.search(r'\d', password):
        raise ValidationError(
            field="password",
            message="Password must contain at least one number"
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(
            field="password",
            message="Password must contain at least one special character"
        )


def generate_password_reset_token() -> str:
    """
    Generate a secure random token for password reset.
    
    Returns:
        Secure random token string (32 bytes, URL-safe base64 encoded)
    """
    return secrets.token_urlsafe(32)
