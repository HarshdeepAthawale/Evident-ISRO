# Phase 3: Core Utilities & Logging

## Overview
Implement structured logging, error handling utilities, and response models. This phase establishes the foundation for consistent logging and error handling across the application.

## Dependencies
- Phase 1: Configuration system must be in place

## Deliverables

### 1. Structured Logging System
- Implement JSON-based structured logging
- Log levels and formatting
- Request/response logging middleware
- Error logging with stack traces

### 2. Error Handling
- Custom exception classes
- Error response models
- Global exception handlers

### 3. Response Models
- Standard API response schemas
- Success/error response formats
- Pydantic models for validation

## Files to Create

### `backend/utils/logger.py`
```python
import logging
import json
from datetime import datetime
from typing import Any

class StructuredLogger:
    def setup_logging()
    def log_request()
    def log_response()
    def log_error()
    def log_audit()
```

### `backend/utils/exceptions.py`
```python
class EVIDENTException(Exception)
class AuthenticationError(EVIDENTException)
class AuthorizationError(EVIDENTException)
class DocumentNotFoundError(EVIDENTException)
class LowConfidenceError(EVIDENTException)
class RefusalError(EVIDENTException)
```

### `backend/utils/responses.py`
```python
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Any (optional)
    error: str (optional)

class QueryResponse(BaseModel):
    answer: str (optional)
    confidence: float (optional)
    sources: List[Source]
    refusal_reason: str (optional)

class Source(BaseModel):
    document_id: str
    document_title: str
    chunk_index: int
    page: int (optional)
    similarity_score: float
```

### `backend/core/middleware.py`
- Request logging middleware
- Response logging middleware
- Error handling middleware
- CORS configuration

## Implementation Details

### Logging Format
Use structured JSON logging:
```json
{
  "timestamp": "2024-01-01T12:00:00Z",
  "level": "INFO",
  "service": "EVIDENT",
  "module": "rag.retriever",
  "message": "Query processed",
  "user_id": "uuid",
  "query_id": "uuid",
  "duration_ms": 150
}
```

### Log Levels
- `DEBUG`: Development details
- `INFO`: Normal operations
- `WARNING`: Potential issues
- `ERROR`: Errors that don't stop execution
- `CRITICAL`: System failures

### Error Response Format
```json
{
  "success": false,
  "error": "Error type",
  "message": "Human-readable message",
  "details": {}
}
```

## Success Criteria
- [ ] Structured logging implemented
- [ ] All log levels working
- [ ] Error handling middleware catches exceptions
- [ ] Response models validate correctly
- [ ] Logs are written to both console and file
- [ ] Request/response logging works

## Notes
- Use Python's `logging` module
- Consider log rotation for production
- Logs should not contain sensitive data (passwords, tokens)
- Use context managers for request tracking
- Add correlation IDs for request tracing
