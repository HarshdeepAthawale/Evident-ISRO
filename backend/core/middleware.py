"""
EVIDENT Middleware

This module contains FastAPI middleware for request/response logging,
error handling, CORS configuration, and request correlation IDs.
"""

import time
import uuid
from typing import Callable
from fastapi import Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from backend.core.config import settings
from backend.utils.logger import StructuredLogger, get_request_id, set_request_id
from backend.utils.exceptions import EVIDENTException
from backend.utils.responses import APIResponse


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging HTTP requests and responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and log request/response.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/handler to call
            
        Returns:
            FastAPI response object
        """
        # Generate or get request ID
        request_id = get_request_id()
        request.state.request_id = request_id
        
        # Set request ID in logger context
        set_request_id(request_id)
        
        # Extract user ID from request state (set by auth middleware)
        user_id = getattr(request.state, "user_id", None)
        
        # Log request
        StructuredLogger.log_request(
            method=request.method,
            path=request.url.path,
            headers=dict(request.headers),
            query_params=dict(request.query_params),
            user_id=str(user_id) if user_id else None
        )
        
        # Measure response time
        start_time = time.time()
        
        try:
            # Process request
            response = await call_next(request)
            
            # Calculate duration
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Add request ID to response headers
            response.headers["X-Request-ID"] = request_id
            
            # Log response
            StructuredLogger.log_response(
                method=request.method,
                path=request.url.path,
                status_code=response.status_code,
                duration_ms=duration_ms,
                user_id=str(user_id) if user_id else None
            )
            
            return response
            
        except Exception as e:
            # Calculate duration even on error
            duration_ms = int((time.time() - start_time) * 1000)
            
            # Log error
            StructuredLogger.log_error(
                error=e,
                context={
                    "method": request.method,
                    "path": request.url.path,
                    "duration_ms": duration_ms,
                },
                user_id=str(user_id) if user_id else None
            )
            
            # Re-raise to be handled by exception handler
            raise


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for handling exceptions and converting them to proper responses.
    """
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        """
        Process request and handle exceptions.
        
        Args:
            request: FastAPI request object
            call_next: Next middleware/handler to call
            
        Returns:
            FastAPI response object
        """
        try:
            return await call_next(request)
        except EVIDENTException as e:
            # Handle custom EVIDENT exceptions
            error_response = APIResponse.error_response(
                message=e.message,
                error=e.error_code,
                details=e.details
            )
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=error_response.model_dump()
            )
        except Exception as e:
            # Handle unexpected exceptions
            StructuredLogger.log_error(
                error=e,
                context={
                    "method": request.method,
                    "path": request.url.path,
                }
            )
            
            error_response = APIResponse.error_response(
                message="An unexpected error occurred",
                error="INTERNAL_SERVER_ERROR",
                details={
                    "error_type": type(e).__name__,
                } if settings.debug else {}
            )
            
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
            return JSONResponse(
                status_code=status_code,
                content=error_response.model_dump()
            )


def setup_cors_middleware(app):
    """
    Set up CORS middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


def setup_middleware(app):
    """
    Set up all middleware for the FastAPI application.
    
    Middleware order (FastAPI processes in reverse order):
    1. Error handling (innermost, added first) - catches exceptions
    2. Request logging (middle, added second) - logs requests/responses
    3. CORS (outermost, added last) - handles CORS headers
    
    Args:
        app: FastAPI application instance
    """
    # Add error handling middleware first (innermost)
    app.add_middleware(ErrorHandlingMiddleware)
    
    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Add CORS middleware last (outermost, handles preflight requests)
    setup_cors_middleware(app)
