"""
EVIDENT Structured Logging System

This module provides structured JSON logging for the application,
including request/response logging, error logging, and audit logging.
"""

import logging
import json
import sys
from datetime import datetime
from typing import Any, Optional, Dict
from pathlib import Path
import uuid
from contextvars import ContextVar
from logging.handlers import RotatingFileHandler

from backend.core.config import settings

# Context variable for request correlation ID
request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)


class JSONFormatter(logging.Formatter):
    """
    Custom JSON formatter for structured logging.
    """
    
    def format(self, record: logging.LogRecord) -> str:
        """
        Format log record as JSON.
        
        Args:
            record: Log record to format
            
        Returns:
            JSON string representation of the log record
        """
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "service": settings.app_name,
            "module": record.module,
            "function": record.funcName,
            "message": record.getMessage(),
        }
        
        # Add request ID if available
        request_id = request_id_var.get()
        if request_id:
            log_data["request_id"] = request_id
        
        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
            log_data["exception_type"] = record.exc_info[0].__name__ if record.exc_info[0] else None
        
        # Add extra fields from record
        if hasattr(record, "user_id"):
            log_data["user_id"] = str(record.user_id)
        if hasattr(record, "query_id"):
            log_data["query_id"] = str(record.query_id)
        if hasattr(record, "duration_ms"):
            log_data["duration_ms"] = record.duration_ms
        if hasattr(record, "document_id"):
            log_data["document_id"] = str(record.document_id)
        if hasattr(record, "extra_data"):
            log_data.update(record.extra_data)
        
        return json.dumps(log_data, ensure_ascii=False)


class StructuredLogger:
    """
    Structured logging utility for EVIDENT application.
    """
    
    _logger: Optional[logging.Logger] = None
    _file_handler: Optional[RotatingFileHandler] = None
    
    @classmethod
    def setup_logging(cls, log_file: Optional[Path] = None) -> None:
        """
        Set up structured logging for the application.
        
        Args:
            log_file: Optional path to log file. If None, logs only to console.
        """
        logger = logging.getLogger(settings.app_name)
        logger.setLevel(logging.DEBUG if settings.debug else logging.INFO)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG if settings.debug else logging.INFO)
        console_handler.setFormatter(JSONFormatter())
        logger.addHandler(console_handler)
        
        # File handler (with rotation)
        if log_file:
            log_file.parent.mkdir(parents=True, exist_ok=True)
            cls._file_handler = RotatingFileHandler(
                log_file,
                maxBytes=10 * 1024 * 1024,  # 10MB
                backupCount=5,
                encoding='utf-8'
            )
            cls._file_handler.setLevel(logging.INFO)
            cls._file_handler.setFormatter(JSONFormatter())
            logger.addHandler(cls._file_handler)
        
        # Prevent propagation to root logger
        logger.propagate = False
        
        cls._logger = logger
    
    @classmethod
    def get_logger(cls) -> logging.Logger:
        """
        Get the application logger instance.
        
        Returns:
            Logger instance
        """
        if cls._logger is None:
            cls.setup_logging()
        return cls._logger
    
    @classmethod
    def log_request(
        cls,
        method: str,
        path: str,
        headers: Optional[Dict[str, Any]] = None,
        query_params: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log HTTP request.
        
        Args:
            method: HTTP method
            path: Request path
            headers: Request headers (sensitive data will be filtered)
            query_params: Query parameters
            user_id: User ID if authenticated
        """
        logger = cls.get_logger()
        
        # Filter sensitive headers
        safe_headers = {}
        if headers:
            for key, value in headers.items():
                if key.lower() in ['authorization', 'cookie', 'x-api-key']:
                    safe_headers[key] = "***REDACTED***"
                else:
                    safe_headers[key] = value
        
        extra = {
            "type": "request",
            "method": method,
            "path": path,
            "headers": safe_headers,
            "query_params": query_params,
        }
        
        if user_id:
            extra["user_id"] = user_id
        
        logger.info(f"{method} {path}", extra=extra)
    
    @classmethod
    def log_response(
        cls,
        method: str,
        path: str,
        status_code: int,
        duration_ms: int,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log HTTP response.
        
        Args:
            method: HTTP method
            path: Request path
            status_code: Response status code
            duration_ms: Response duration in milliseconds
            user_id: User ID if authenticated
        """
        logger = cls.get_logger()
        
        level = logging.INFO
        if status_code >= 500:
            level = logging.ERROR
        elif status_code >= 400:
            level = logging.WARNING
        
        extra = {
            "type": "response",
            "method": method,
            "path": path,
            "status_code": status_code,
            "duration_ms": duration_ms,
        }
        
        if user_id:
            extra["user_id"] = user_id
        
        logger.log(
            level,
            f"{method} {path} - {status_code} ({duration_ms}ms)",
            extra=extra
        )
    
    @classmethod
    def log_error(
        cls,
        error: Exception,
        context: Optional[Dict[str, Any]] = None,
        user_id: Optional[str] = None
    ) -> None:
        """
        Log error with full stack trace.
        
        Args:
            error: Exception to log
            context: Additional context information
            user_id: User ID if available
        """
        logger = cls.get_logger()
        
        extra = {
            "type": "error",
            "error_type": type(error).__name__,
            "error_message": str(error),
        }
        
        if context:
            extra.update(context)
        
        if user_id:
            extra["user_id"] = user_id
        
        logger.exception(
            f"Error: {type(error).__name__} - {str(error)}",
            extra=extra,
            exc_info=error
        )
    
    @classmethod
    def log_audit(
        cls,
        action: str,
        details: Dict[str, Any],
        user_id: Optional[str] = None
    ) -> None:
        """
        Log audit event.
        
        Args:
            action: Action being audited
            details: Additional details about the action
            user_id: User ID performing the action
        """
        logger = cls.get_logger()
        
        extra = {
            "type": "audit",
            "action": action,
            **details,
        }
        
        if user_id:
            extra["user_id"] = user_id
        
        logger.info(f"Audit: {action}", extra=extra)
    
    @classmethod
    def debug(cls, message: str, **kwargs) -> None:
        """Log debug message."""
        cls.get_logger().debug(message, extra=kwargs)
    
    @classmethod
    def info(cls, message: str, **kwargs) -> None:
        """Log info message."""
        cls.get_logger().info(message, extra=kwargs)
    
    @classmethod
    def warning(cls, message: str, **kwargs) -> None:
        """Log warning message."""
        cls.get_logger().warning(message, extra=kwargs)
    
    @classmethod
    def error(cls, message: str, **kwargs) -> None:
        """Log error message."""
        cls.get_logger().error(message, extra=kwargs)
    
    @classmethod
    def critical(cls, message: str, **kwargs) -> None:
        """Log critical message."""
        cls.get_logger().critical(message, extra=kwargs)


def setup_logging(log_file: Optional[Path] = None) -> None:
    """
    Set up application logging.
    
    Args:
        log_file: Optional path to log file
    """
    StructuredLogger.setup_logging(log_file)


def get_request_id() -> str:
    """
    Get or create request correlation ID.
    
    Returns:
        Request ID string
    """
    request_id = request_id_var.get()
    if request_id is None:
        request_id = str(uuid.uuid4())
        request_id_var.set(request_id)
    return request_id


def set_request_id(request_id: str) -> None:
    """
    Set request correlation ID.
    
    Args:
        request_id: Request ID to set
    """
    request_id_var.set(request_id)
