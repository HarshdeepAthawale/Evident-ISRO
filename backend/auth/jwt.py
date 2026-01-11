"""
EVIDENT JWT Token Management

This module provides JWT token generation, validation, decoding,
and related utilities for authentication.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional
from jose import JWTError, jwt
from uuid import UUID

from backend.core.config import settings
from backend.utils.exceptions import AuthenticationError


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: Dictionary containing token payload (should include 'sub', 'username', 'role')
        expires_delta: Optional timedelta for expiration (defaults to configured access token expiry)
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "access"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def create_refresh_token(data: dict) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: Dictionary containing token payload (should include 'sub', 'username', 'role')
        
    Returns:
        Encoded JWT refresh token string
    """
    to_encode = data.copy()
    
    expire = datetime.utcnow() + timedelta(days=settings.jwt_refresh_token_expire_days)
    
    to_encode.update({
        "exp": expire,
        "iat": datetime.utcnow(),
        "type": "refresh"
    })
    
    encoded_jwt = jwt.encode(
        to_encode,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    
    return encoded_jwt


def verify_token(token: str, token_type: str = "access") -> dict:
    """
    Verify and decode a JWT token.
    
    Args:
        token: JWT token string to verify
        token_type: Expected token type ("access" or "refresh")
        
    Returns:
        Decoded token payload as dictionary
        
    Raises:
        AuthenticationError: If token is invalid, expired, or wrong type
    """
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            raise AuthenticationError(
                message=f"Invalid token type. Expected {token_type}, got {payload.get('type')}"
            )
        
        # Check if token has required fields
        if "sub" not in payload:
            raise AuthenticationError(
                message="Token missing required 'sub' field"
            )
        
        return payload
        
    except JWTError as e:
        raise AuthenticationError(
            message=f"Invalid token: {str(e)}"
        )


def decode_token(token: str) -> dict:
    """
    Decode a JWT token without verification (use with caution).
    
    This function does not verify the token signature and should only
    be used when verification is not required (e.g., debugging).
    
    Args:
        token: JWT token string to decode
        
    Returns:
        Decoded token payload as dictionary
        
    Raises:
        AuthenticationError: If token cannot be decoded
    """
    try:
        payload = jwt.decode(
            token,
            options={"verify_signature": False}
        )
        return payload
    except JWTError as e:
        raise AuthenticationError(
            message=f"Token decode failed: {str(e)}"
        )


def get_user_id_from_token(token: str) -> UUID:
    """
    Extract user ID from a JWT token.
    
    Args:
        token: JWT token string
        
    Returns:
        User ID as UUID
        
    Raises:
        AuthenticationError: If token is invalid or user ID is missing
    """
    payload = verify_token(token)
    user_id_str = payload.get("sub")
    
    if not user_id_str:
        raise AuthenticationError(
            message="Token missing user ID (sub field)"
        )
    
    try:
        return UUID(user_id_str)
    except (ValueError, TypeError) as e:
        raise AuthenticationError(
            message=f"Invalid user ID in token: {str(e)}"
        )
