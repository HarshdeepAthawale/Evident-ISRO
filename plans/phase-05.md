# Phase 5: Authentication Endpoints

## Overview
Create all authentication-related API endpoints: login, token refresh, logout, user registration (admin-only), and password reset. This phase makes the authentication system accessible via REST API.

## Dependencies
- Phase 4: Security foundation (JWT, password hashing) must be complete

## Deliverables

### 1. Authentication Endpoints
- POST `/api/auth/login` - User login
- POST `/api/auth/refresh` - Refresh access token
- POST `/api/auth/logout` - Logout (invalidate token)
- POST `/api/auth/register` - User registration (admin-only)
- POST `/api/auth/reset-password` - Password reset request
- POST `/api/auth/reset-password/confirm` - Confirm password reset

### 2. Request/Response Models
- Login request/response
- Token refresh request/response
- Registration request/response
- Password reset models

### 3. Integration
- Connect to database
- Use security utilities
- Implement proper error handling

## Files to Create

### `backend/auth/routes.py`
```python
@router.post("/login")
async def login(credentials: LoginRequest) -> LoginResponse

@router.post("/refresh")
async def refresh_token(refresh_token: str) -> TokenResponse

@router.post("/logout")
async def logout(current_user: User)

@router.post("/register")
async def register(user_data: RegisterRequest, current_user: User) -> UserResponse

@router.post("/reset-password")
async def request_password_reset(email: str)

@router.post("/reset-password/confirm")
async def confirm_password_reset(token: str, new_password: str)
```

### `backend/auth/schemas.py`
```python
class LoginRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: UserInfo

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: str

class UserInfo(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
```

### `backend/main.py` (update)
- Include auth router
- Set up CORS
- Add authentication middleware

## Implementation Details

### Login Flow
1. Validate credentials
2. Check if user is active
3. Verify password
4. Generate access and refresh tokens
5. Log login event
6. Return tokens and user info

### Token Refresh Flow
1. Validate refresh token
2. Check if token is not expired
3. Generate new access token
4. Return new access token

### Registration Flow (Admin Only)
1. Verify current user is admin
2. Validate input data
3. Check username/email uniqueness
4. Hash password
5. Create user in database
6. Return user info

### Password Reset Flow
1. Generate reset token
2. Store token with expiry
3. Send email (or log for now)
4. Validate token on confirmation
5. Update password

### Error Handling
- Invalid credentials → 401
- Inactive user → 403
- Duplicate username/email → 409
- Invalid token → 401
- Missing permissions → 403

## Success Criteria
- [ ] Login endpoint works
- [ ] Token refresh works
- [ ] Logout endpoint exists
- [ ] Registration requires admin role
- [ ] Password reset flow works
- [ ] All endpoints return proper status codes
- [ ] Error messages are clear
- [ ] Tokens are properly formatted

## Notes
- Use HTTP-only cookies for tokens (optional enhancement)
- Implement rate limiting on login
- Log all authentication events
- Consider 2FA for future phases
- Password reset tokens should expire quickly (1 hour)
