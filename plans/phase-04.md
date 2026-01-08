# Phase 4: Security Foundation

## Overview
Implement the core security infrastructure: JWT token generation and validation, password hashing with bcrypt, and token refresh logic. This phase establishes authentication capabilities.

## Dependencies
- Phase 2: User model must exist
- Phase 3: Logging and error handling must be in place

## Deliverables

### 1. JWT Token Management
- Token generation (access and refresh)
- Token validation
- Token decoding
- Token expiration handling

### 2. Password Security
- bcrypt password hashing
- Password verification
- Password strength validation

### 3. Security Utilities
- Password validation rules
- Token refresh logic
- Security helpers

## Files to Create

### `backend/auth/jwt.py`
```python
def create_access_token(data: dict, expires_delta: timedelta)
def create_refresh_token(data: dict)
def verify_token(token: str) -> dict
def decode_token(token: str) -> dict
def get_current_user(token: str) -> User
```

### `backend/core/security.py`
```python
def hash_password(password: str) -> str
def verify_password(plain_password: str, hashed_password: str) -> bool
def validate_password_strength(password: str) -> bool
def generate_password_reset_token() -> str
```

### `backend/auth/dependencies.py`
```python
async def get_current_user(token: str) -> User
async def get_current_active_user(current_user: User) -> User
```

## Implementation Details

### JWT Configuration
- Algorithm: HS256
- Access token expiry: 30 minutes (configurable)
- Refresh token expiry: 7 days (configurable)
- Secret key from environment variable

### Password Requirements
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one number
- At least one special character

### Token Payload Structure
```python
{
    "sub": "user_id",
    "username": "username",
    "role": "admin|engineer|viewer",
    "exp": timestamp,
    "iat": timestamp,
    "type": "access|refresh"
}
```

### Password Hashing
- Use bcrypt with cost factor 12
- Salt automatically generated
- Store only hashed passwords

## Success Criteria
- [ ] JWT tokens can be generated
- [ ] Tokens can be validated
- [ ] Password hashing works correctly
- [ ] Password verification works
- [ ] Token expiration is enforced
- [ ] Refresh token logic implemented
- [ ] Password validation rules enforced

## Notes
- Never log passwords or tokens
- Use secure random for token generation
- Implement token blacklisting for logout (optional)
- Consider rate limiting for login attempts
- Store JWT secret securely (never in code)
