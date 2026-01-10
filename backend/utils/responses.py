"""
EVIDENT Response Models

This module defines Pydantic models for API responses,
ensuring consistent response formatting across the application.
"""

from pydantic import BaseModel, Field
from typing import Any, Optional, List
from datetime import datetime


class APIResponse(BaseModel):
    """
    Standard API response model.
    
    Attributes:
        success: Whether the request was successful
        message: Human-readable message
        data: Response data (optional)
        error: Error code (optional, present if success is False)
        details: Additional error details (optional)
        timestamp: Response timestamp
    """
    
    success: bool = Field(description="Whether the request was successful")
    message: str = Field(description="Human-readable message")
    data: Optional[Any] = Field(default=None, description="Response data")
    error: Optional[str] = Field(default=None, description="Error code if failed")
    details: Optional[dict] = Field(default=None, description="Additional error details")
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Response timestamp"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Operation completed successfully",
                "data": {},
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }
    
    @classmethod
    def success_response(
        cls,
        message: str = "Operation completed successfully",
        data: Any = None
    ) -> "APIResponse":
        """
        Create a success response.
        
        Args:
            message: Success message
            data: Response data
            
        Returns:
            APIResponse instance
        """
        return cls(
            success=True,
            message=message,
            data=data
        )
    
    @classmethod
    def error_response(
        cls,
        message: str,
        error: str,
        details: Optional[dict] = None
    ) -> "APIResponse":
        """
        Create an error response.
        
        Args:
            message: Error message
            error: Error code
            details: Additional error details
            
        Returns:
            APIResponse instance
        """
        return cls(
            success=False,
            message=message,
            error=error,
            details=details
        )


class Source(BaseModel):
    """
    Source citation model for query responses.
    
    Attributes:
        document_id: UUID of the source document
        document_title: Title of the source document
        chunk_index: Index of the chunk within the document
        page: Page number (optional, if applicable)
        similarity_score: Similarity score for this source
        text_snippet: Excerpt from the source (optional)
    """
    
    document_id: str = Field(description="UUID of the source document")
    document_title: str = Field(description="Title of the source document")
    chunk_index: int = Field(description="Index of the chunk within the document")
    page: Optional[int] = Field(default=None, description="Page number if applicable")
    similarity_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Similarity score between 0 and 1"
    )
    text_snippet: Optional[str] = Field(
        default=None,
        description="Excerpt from the source text"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "document_id": "123e4567-e89b-12d3-a456-426614174000",
                "document_title": "Mission Specification Document",
                "chunk_index": 5,
                "page": 12,
                "similarity_score": 0.85,
                "text_snippet": "The mission objectives include..."
            }
        }


class QueryResponse(BaseModel):
    """
    Response model for query/answer endpoints.
    
    Attributes:
        answer: Generated answer (optional, None if refused)
        confidence: Confidence score of the answer (0-1, optional)
        sources: List of source citations
        refusal_reason: Reason for refusal if answer is None (optional)
        query_id: Unique identifier for this query
        response_time_ms: Response time in milliseconds
    """
    
    answer: Optional[str] = Field(
        default=None,
        description="Generated answer, or None if refused"
    )
    confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Confidence score between 0 and 1"
    )
    sources: List[Source] = Field(
        default_factory=list,
        description="List of source citations"
    )
    refusal_reason: Optional[str] = Field(
        default=None,
        description="Reason for refusal if answer is None"
    )
    query_id: Optional[str] = Field(
        default=None,
        description="Unique identifier for this query"
    )
    response_time_ms: int = Field(
        default=0,
        description="Response time in milliseconds"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "Based on the mission specification document...",
                "confidence": 0.87,
                "sources": [
                    {
                        "document_id": "123e4567-e89b-12d3-a456-426614174000",
                        "document_title": "Mission Specification Document",
                        "chunk_index": 5,
                        "page": 12,
                        "similarity_score": 0.85,
                        "text_snippet": "The mission objectives include..."
                    }
                ],
                "refusal_reason": None,
                "query_id": "123e4567-e89b-12d3-a456-426614174001",
                "response_time_ms": 150
            }
        }
    
    @classmethod
    def refused_response(
        cls,
        refusal_reason: str,
        sources: Optional[List[Source]] = None,
        query_id: Optional[str] = None,
        response_time_ms: int = 0
    ) -> "QueryResponse":
        """
        Create a refused response.
        
        Args:
            refusal_reason: Reason for refusal
            sources: Retrieved sources (optional)
            query_id: Query ID (optional)
            response_time_ms: Response time in milliseconds
            
        Returns:
            QueryResponse instance with answer=None
        """
        return cls(
            answer=None,
            confidence=None,
            sources=sources or [],
            refusal_reason=refusal_reason,
            query_id=query_id,
            response_time_ms=response_time_ms
        )
    
    @classmethod
    def success_response(
        cls,
        answer: str,
        confidence: float,
        sources: List[Source],
        query_id: Optional[str] = None,
        response_time_ms: int = 0
    ) -> "QueryResponse":
        """
        Create a successful response with answer.
        
        Args:
            answer: Generated answer
            confidence: Confidence score
            sources: List of source citations
            query_id: Query ID (optional)
            response_time_ms: Response time in milliseconds
            
        Returns:
            QueryResponse instance with answer
        """
        return cls(
            answer=answer,
            confidence=confidence,
            sources=sources,
            refusal_reason=None,
            query_id=query_id,
            response_time_ms=response_time_ms
        )


class PaginatedResponse(BaseModel):
    """
    Paginated response model for list endpoints.
    
    Attributes:
        items: List of items in the current page
        total: Total number of items
        page: Current page number (1-indexed)
        page_size: Number of items per page
        total_pages: Total number of pages
    """
    
    items: List[Any] = Field(description="List of items in the current page")
    total: int = Field(ge=0, description="Total number of items")
    page: int = Field(ge=1, description="Current page number (1-indexed)")
    page_size: int = Field(ge=1, description="Number of items per page")
    total_pages: int = Field(ge=0, description="Total number of pages")
    
    class Config:
        json_schema_extra = {
            "example": {
                "items": [],
                "total": 100,
                "page": 1,
                "page_size": 20,
                "total_pages": 5
            }
        }
    
    @classmethod
    def create(
        cls,
        items: List[Any],
        total: int,
        page: int,
        page_size: int
    ) -> "PaginatedResponse":
        """
        Create a paginated response.
        
        Args:
            items: List of items for current page
            total: Total number of items
            page: Current page number (1-indexed)
            page_size: Number of items per page
            
        Returns:
            PaginatedResponse instance
        """
        total_pages = (total + page_size - 1) // page_size if total > 0 else 0
        
        return cls(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages
        )
