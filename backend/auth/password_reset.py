"""
EVIDENT Password Reset Token Storage

This module provides a simple in-memory storage for password reset tokens.
For production, consider using a database table or Redis.
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Any
from threading import Lock


class PasswordResetTokenStore:
    """
    In-memory storage for password reset tokens.
    
    Tokens expire after 1 hour (configurable).
    """
    
    def __init__(self, expiry_hours: int = 1):
        """
        Initialize token store.
        
        Args:
            expiry_hours: Token expiry time in hours (default: 1)
        """
        self._tokens: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()
        self.expiry_hours = expiry_hours
    
    def store_token(self, token: str, user_id: str, email: str) -> None:
        """
        Store a password reset token.
        
        Args:
            token: Reset token
            user_id: User ID
            email: User email
        """
        with self._lock:
            self._tokens[token] = {
                "user_id": user_id,
                "email": email,
                "expires_at": datetime.utcnow() + timedelta(hours=self.expiry_hours),
                "used": False
            }
    
    def get_token_data(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get token data if valid and not expired.
        
        Args:
            token: Reset token
            
        Returns:
            Token data dict with user_id and email, or None if invalid/expired
        """
        with self._lock:
            if token not in self._tokens:
                return None
            
            token_data = self._tokens[token]
            
            # Check if expired
            if datetime.utcnow() > token_data["expires_at"]:
                del self._tokens[token]
                return None
            
            # Check if already used
            if token_data["used"]:
                return None
            
            return token_data
    
    def mark_token_used(self, token: str) -> None:
        """
        Mark a token as used.
        
        Args:
            token: Reset token
        """
        with self._lock:
            if token in self._tokens:
                self._tokens[token]["used"] = True
    
    def delete_token(self, token: str) -> None:
        """
        Delete a token.
        
        Args:
            token: Reset token
        """
        with self._lock:
            if token in self._tokens:
                del self._tokens[token]
    
    def cleanup_expired(self) -> int:
        """
        Remove expired tokens.
        
        Returns:
            Number of tokens removed
        """
        with self._lock:
            now = datetime.utcnow()
            expired_tokens = [
                token for token, data in self._tokens.items()
                if now > data["expires_at"]
            ]
            
            for token in expired_tokens:
                del self._tokens[token]
            
            return len(expired_tokens)


# Global token store instance
password_reset_store = PasswordResetTokenStore(expiry_hours=1)
