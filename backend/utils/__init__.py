"""
EVIDENT Utilities Package

This package contains utility modules for logging, error handling,
and response formatting.
"""

from backend.utils.logger import (
    StructuredLogger,
    setup_logging,
    get_request_id,
    set_request_id,
)
from backend.utils.exceptions import (
    EVIDENTException,
    AuthenticationError,
    AuthorizationError,
    DocumentNotFoundError,
    LowConfidenceError,
    RefusalError,
    ValidationError,
    DatabaseError,
    VectorStoreError,
    LLMError,
)
from backend.utils.responses import (
    APIResponse,
    QueryResponse,
    Source,
    PaginatedResponse,
)

__all__ = [
    "StructuredLogger",
    "setup_logging",
    "get_request_id",
    "set_request_id",
    "EVIDENTException",
    "AuthenticationError",
    "AuthorizationError",
    "DocumentNotFoundError",
    "LowConfidenceError",
    "RefusalError",
    "ValidationError",
    "DatabaseError",
    "VectorStoreError",
    "LLMError",
    "APIResponse",
    "QueryResponse",
    "Source",
    "PaginatedResponse",
]
