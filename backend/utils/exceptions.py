"""
EVIDENT Custom Exceptions

This module defines custom exception classes for the application,
providing structured error handling with proper error codes and messages.
"""

from typing import Optional, Dict, Any


class EVIDENTException(Exception):
    """
    Base exception class for all EVIDENT exceptions.
    
    Attributes:
        message: Human-readable error message
        error_code: Error code for programmatic handling
        details: Additional error details
    """
    
    def __init__(
        self,
        message: str,
        error_code: str = "EVIDENT_ERROR",
        details: Optional[Dict[str, Any]] = None
    ):
        """
        Initialize exception.
        
        Args:
            message: Human-readable error message
            error_code: Error code for programmatic handling
            details: Additional error details
        """
        self.message = message
        self.error_code = error_code
        self.details = details or {}
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert exception to dictionary for JSON response.
        
        Returns:
            Dictionary representation of the exception
        """
        return {
            "error": self.error_code,
            "message": self.message,
            "details": self.details,
        }


class AuthenticationError(EVIDENTException):
    """
    Exception raised when authentication fails.
    """
    
    def __init__(
        self,
        message: str = "Authentication failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            details=details
        )


class AuthorizationError(EVIDENTException):
    """
    Exception raised when authorization fails (user lacks permission).
    """
    
    def __init__(
        self,
        message: str = "Access denied",
        resource: Optional[str] = None,
        action: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        error_details = details or {}
        if resource:
            error_details["resource"] = resource
        if action:
            error_details["action"] = action
        
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            details=error_details
        )


class DocumentNotFoundError(EVIDENTException):
    """
    Exception raised when a document is not found.
    """
    
    def __init__(
        self,
        document_id: Optional[str] = None,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        if message is None:
            message = f"Document not found"
            if document_id:
                message = f"Document not found: {document_id}"
        
        error_details = details or {}
        if document_id:
            error_details["document_id"] = document_id
        
        super().__init__(
            message=message,
            error_code="DOCUMENT_NOT_FOUND",
            details=error_details
        )


class LowConfidenceError(EVIDENTException):
    """
    Exception raised when answer confidence is below threshold.
    """
    
    def __init__(
        self,
        confidence: float,
        threshold: float,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        if message is None:
            message = (
                f"Answer confidence ({confidence:.2f}) is below "
                f"threshold ({threshold:.2f})"
            )
        
        error_details = details or {}
        error_details["confidence"] = confidence
        error_details["threshold"] = threshold
        
        super().__init__(
            message=message,
            error_code="LOW_CONFIDENCE",
            details=error_details
        )


class RefusalError(EVIDENTException):
    """
    Exception raised when the system refuses to answer a query.
    """
    
    def __init__(
        self,
        reason: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        if message is None:
            message = f"Query refused: {reason}"
        
        error_details = details or {}
        error_details["refusal_reason"] = reason
        
        super().__init__(
            message=message,
            error_code="REFUSAL_ERROR",
            details=error_details
        )


class ValidationError(EVIDENTException):
    """
    Exception raised when input validation fails.
    """
    
    def __init__(
        self,
        field: str,
        message: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        if message is None:
            message = f"Validation failed for field: {field}"
        
        error_details = details or {}
        error_details["field"] = field
        
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            details=error_details
        )


class DatabaseError(EVIDENTException):
    """
    Exception raised when database operations fail.
    """
    
    def __init__(
        self,
        message: str = "Database operation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="DATABASE_ERROR",
            details=details
        )


class VectorStoreError(EVIDENTException):
    """
    Exception raised when vector store operations fail.
    """
    
    def __init__(
        self,
        message: str = "Vector store operation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="VECTOR_STORE_ERROR",
            details=details
        )


class LLMError(EVIDENTException):
    """
    Exception raised when LLM operations fail.
    """
    
    def __init__(
        self,
        message: str = "LLM operation failed",
        details: Optional[Dict[str, Any]] = None
    ):
        super().__init__(
            message=message,
            error_code="LLM_ERROR",
            details=details
        )
