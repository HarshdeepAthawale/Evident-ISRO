"""
EVIDENT Authentication Routes

This module defines all authentication-related API endpoints.
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.core.database import get_db
from backend.core.security import (
    hash_password,
    verify_password,
    validate_password_strength_with_error,
    generate_password_reset_token
)
from backend.auth.jwt import create_access_token, create_refresh_token, verify_token
from backend.auth.dependencies import get_current_active_user, security
from backend.auth.schemas import (
    LoginRequest,
    LoginResponse,
    TokenRefreshRequest,
    TokenResponse,
    RegisterRequest,
    UserResponse,
    PasswordResetRequest,
    PasswordResetConfirmRequest,
    MessageResponse,
    UserInfo,
    RoleInfo,
    RoleListResponse,
    AssignRoleRequest,
    AssignRoleResponse
)
from backend.auth.password_reset import password_reset_store
from backend.auth.permissions import require_admin
from backend.models.user import User, UserRole
from backend.models.role import Role
from backend.utils.exceptions import AuthenticationError, ValidationError, AuthorizationError
from backend.utils.logger import StructuredLogger

router = APIRouter(prefix="/api/auth", tags=["authentication"])
logger = StructuredLogger.get_logger()


@router.post("/login", response_model=LoginResponse, status_code=status.HTTP_200_OK)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
) -> LoginResponse:
    """
    User login endpoint.
    
    Authenticates user and returns access and refresh tokens.
    """
    try:
        # Find user by username
        user = db.query(User).filter(User.username == credentials.username).first()
        
        if user is None:
            logger.warning(f"Login attempt with invalid username: {credentials.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Check if user is active
        if not user.is_active:
            logger.warning(f"Login attempt for inactive user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is inactive"
            )
        
        # Verify password
        if not verify_password(credentials.password, user.hashed_password):
            logger.warning(f"Login attempt with invalid password for user: {user.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid username or password"
            )
        
        # Generate tokens
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value
        }
        
        access_token = create_access_token(data=token_data)
        refresh_token = create_refresh_token(data=token_data)
        
        # Log successful login
        logger.info(
            f"User logged in: {user.username}",
            extra={
                "user_id": str(user.id),
                "username": user.username,
                "event": "login"
            }
        )
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type="bearer",
            user=UserInfo(
                id=str(user.id),
                username=user.username,
                email=user.email,
                full_name=user.full_name,
                role=user.role.value,
                is_active=user.is_active
            )
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during login"
        )


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(
    request: TokenRefreshRequest,
    db: Session = Depends(get_db)
) -> TokenResponse:
    """
    Refresh access token using refresh token.
    """
    try:
        # Verify refresh token
        payload = verify_token(request.refresh_token, token_type="refresh")
        
        user_id = payload.get("sub")
        user = db.query(User).filter(User.id == user_id).first()
        
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token"
            )
        
        # Generate new access token
        token_data = {
            "sub": str(user.id),
            "username": user.username,
            "role": user.role.value
        }
        
        access_token = create_access_token(data=token_data)
        
        logger.info(
            f"Token refreshed for user: {user.username}",
            extra={
                "user_id": str(user.id),
                "event": "token_refresh"
            }
        )
        
        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )
        
    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.message)
        )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during token refresh"
        )


@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def logout(
    current_user: User = Depends(get_current_active_user)
) -> MessageResponse:
    """
    Logout endpoint.
    
    Note: Token invalidation (blacklisting) is not implemented in this phase.
    For full logout functionality, implement token blacklisting in future phases.
    """
    logger.info(
        f"User logged out: {current_user.username}",
        extra={
            "user_id": str(current_user.id),
            "username": current_user.username,
            "event": "logout"
        }
    )
    
    return MessageResponse(message="Logged out successfully")


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: RegisterRequest,
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
) -> UserResponse:
    """
    User registration endpoint (admin-only).
    
    Allows admin users to create new user accounts.
    """
    # Check if current user is admin
    if current_user.role != UserRole.ADMIN:
        logger.warning(
            f"Non-admin user attempted registration: {current_user.username}",
            extra={
                "user_id": str(current_user.id),
                "event": "unauthorized_registration_attempt"
            }
        )
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Only administrators can register new users"
        )
    
    # Validate password strength
    try:
        validate_password_strength_with_error(user_data.password)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    
    # Validate role
    try:
        role = UserRole(user_data.role.lower())
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid role. Must be one of: {[r.value for r in UserRole]}"
        )
    
    # Create new user
    try:
        hashed_password = hash_password(user_data.password)
        
        new_user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            full_name=user_data.full_name,
            role=role,
            is_active=True
        )
        
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        
        logger.info(
            f"User registered by admin: {new_user.username}",
            extra={
                "user_id": str(new_user.id),
                "username": new_user.username,
                "registered_by": str(current_user.id),
                "event": "user_registration"
            }
        )
        
        return UserResponse(
            id=str(new_user.id),
            username=new_user.username,
            email=new_user.email,
            full_name=new_user.full_name,
            role=new_user.role.value,
            is_active=new_user.is_active,
            created_at=new_user.created_at.isoformat()
        )
        
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        
        if "username" in error_msg.lower() or "unique constraint" in error_msg.lower():
            if "username" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Username already exists"
                )
            elif "email" in error_msg.lower():
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email already exists"
                )
        
        logger.error(f"Registration error: {error_msg}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this username or email already exists"
        )
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Registration error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during registration"
        )


@router.post("/reset-password", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def request_password_reset(
    request: PasswordResetRequest,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Request password reset.
    
    Generates a reset token and stores it (email sending not implemented in this phase).
    """
    # Find user by email
    user = db.query(User).filter(User.email == request.email).first()
    
    # Always return success message (security: don't reveal if email exists)
    if user is None:
        logger.warning(f"Password reset requested for non-existent email: {request.email}")
        return MessageResponse(
            message="If the email exists, a password reset link has been sent"
        )
    
    # Generate reset token
    reset_token = generate_password_reset_token()
    
    # Store token
    password_reset_store.store_token(
        token=reset_token,
        user_id=str(user.id),
        email=user.email
    )
    
    # TODO: Send email with reset link in future phases
    # For now, log the token (in production, this should be sent via email)
    logger.info(
        f"Password reset requested for user: {user.username}",
        extra={
            "user_id": str(user.id),
            "email": user.email,
            "event": "password_reset_requested",
            "reset_token": reset_token  # Remove this in production or send via secure channel
        }
    )
    
    # In production, send email instead of logging
    return MessageResponse(
        message="If the email exists, a password reset link has been sent"
    )


@router.post("/reset-password/confirm", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def confirm_password_reset(
    request: PasswordResetConfirmRequest,
    db: Session = Depends(get_db)
) -> MessageResponse:
    """
    Confirm password reset with token.
    """
    # Validate password strength
    try:
        validate_password_strength_with_error(request.new_password)
    except ValidationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message
        )
    
    # Get token data
    token_data = password_reset_store.get_token_data(request.token)
    
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid or expired reset token"
        )
    
    # Find user
    user = db.query(User).filter(User.id == token_data["user_id"]).first()
    
    if user is None:
        password_reset_store.delete_token(request.token)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid reset token"
        )
    
    # Update password
    try:
        user.hashed_password = hash_password(request.new_password)
        db.commit()
        
        # Mark token as used
        password_reset_store.mark_token_used(request.token)
        
        logger.info(
            f"Password reset completed for user: {user.username}",
            extra={
                "user_id": str(user.id),
                "event": "password_reset_completed"
            }
        )
        
        return MessageResponse(message="Password reset successfully")
        
    except Exception as e:
        db.rollback()
        logger.error(f"Password reset error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error during password reset"
        )


# Admin Endpoints

@router.get("/admin/roles", response_model=RoleListResponse, status_code=status.HTTP_200_OK)
async def list_roles(
    current_user: User = Depends(get_current_active_user),
    _: None = Depends(require_admin()),
    db: Session = Depends(get_db)
) -> RoleListResponse:
    """
    List all available roles (admin-only).
    """
    try:
        roles = db.query(Role).all()
        
        role_list = [
            RoleInfo(
                name=role.name,
                description=role.description or "",
                permissions=role.permissions or {}
            )
            for role in roles
        ]
        
        # Also include built-in roles from UserRole enum
        built_in_roles = [
            RoleInfo(
                name=role.value,
                description=f"Built-in {role.value} role",
                permissions={}
            )
            for role in UserRole
        ]
        
        # Combine and remove duplicates
        all_roles = {role.name: role for role in role_list}
        for role in built_in_roles:
            if role.name not in all_roles:
                all_roles[role.name] = role
        
        logger.info(
            f"Roles listed by admin: {current_user.username}",
            extra={
                "user_id": str(current_user.id),
                "event": "roles_listed"
            }
        )
        
        return RoleListResponse(roles=list(all_roles.values()))
        
    except Exception as e:
        logger.error(f"List roles error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while listing roles"
        )


@router.post("/admin/users/{user_id}/role", response_model=AssignRoleResponse, status_code=status.HTTP_200_OK)
async def assign_role(
    user_id: str,
    request: AssignRoleRequest,
    current_user: User = Depends(get_current_active_user),
    _: None = Depends(require_admin()),
    db: Session = Depends(get_db)
) -> AssignRoleResponse:
    """
    Assign a role to a user (admin-only).
    """
    try:
        # Validate role
        try:
            new_role = UserRole(request.role.lower())
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid role. Must be one of: {[r.value for r in UserRole]}"
            )
        
        # Find target user
        try:
            target_user = db.query(User).filter(User.id == user_id).first()
        except Exception:
            target_user = None
        
        if target_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User not found: {user_id}"
            )
        
        # Prevent self-demotion from admin (safety check)
        if target_user.id == current_user.id and new_role != UserRole.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot remove admin role from yourself"
            )
        
        # Update role
        old_role = target_user.role
        target_user.role = new_role
        db.commit()
        db.refresh(target_user)
        
        logger.info(
            f"Role assigned by admin: {current_user.username} assigned {new_role.value} to {target_user.username}",
            extra={
                "admin_id": str(current_user.id),
                "target_user_id": str(target_user.id),
                "old_role": old_role.value,
                "new_role": new_role.value,
                "event": "role_assigned"
            }
        )
        
        return AssignRoleResponse(
            message=f"Role {new_role.value} assigned successfully",
            user_id=str(target_user.id),
            new_role=new_role.value
        )
        
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        logger.error(f"Assign role error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while assigning role"
        )
