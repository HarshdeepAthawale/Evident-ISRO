"""
EVIDENT RBAC Middleware

This module provides middleware for role-based access control.
Note: Most RBAC is handled via decorators and dependencies.
This middleware can be used for global role/permission checks if needed.
"""

from fastapi import Request, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from typing import Callable

from backend.utils.logger import StructuredLogger

logger = StructuredLogger.get_logger()


class RBACMiddleware(BaseHTTPMiddleware):
    """
    Middleware for role-based access control.
    
    This middleware can perform global permission checks before
    requests reach route handlers. Most RBAC is handled via
    decorators and dependencies, but this can be useful for
    path-based access control.
    """
    
    def __init__(
        self,
        app: Callable,
        protected_paths: list = None,
        admin_only_paths: list = None
    ):
        """
        Initialize RBAC middleware.
        
        Args:
            app: ASGI application
            protected_paths: List of path prefixes that require authentication
            admin_only_paths: List of path prefixes that require admin role
        """
        super().__init__(app)
        self.protected_paths = protected_paths or ["/api/"]
        self.admin_only_paths = admin_only_paths or ["/api/admin/"]
    
    async def dispatch(self, request: Request, call_next: Callable):
        """
        Process request through RBAC middleware.
        
        Note: This is a basic implementation. Most RBAC checks
        should be done via decorators and dependencies in route handlers.
        """
        # Skip RBAC checks for public endpoints
        if request.url.path in ["/", "/health", "/docs", "/openapi.json", "/redoc"]:
            return await call_next(request)
        
        # Check if path requires authentication
        requires_auth = any(
            request.url.path.startswith(path) for path in self.protected_paths
        )
        
        if requires_auth:
            # Check if path requires admin
            requires_admin = any(
                request.url.path.startswith(path) for path in self.admin_only_paths
            )
            
            if requires_admin:
                # Admin-only paths are checked in route handlers via decorators
                # This middleware just logs the attempt
                logger.debug(
                    f"Admin-only path accessed: {request.url.path}",
                    extra={
                        "path": request.url.path,
                        "method": request.method,
                        "event": "admin_path_access"
                    }
                )
        
        # Continue to next middleware/route handler
        # Actual RBAC checks happen in route handlers via decorators
        response = await call_next(request)
        return response


def setup_rbac_middleware(app, **kwargs):
    """
    Set up RBAC middleware for FastAPI application.
    
    Args:
        app: FastAPI application instance
        **kwargs: Additional arguments for RBACMiddleware
    """
    app.add_middleware(RBACMiddleware, **kwargs)
