"""
EVIDENT Audit Log Model

This module defines the AuditLog model for tracking all queries and actions.
"""

from sqlalchemy import Column, String, Integer, Float, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from backend.core.database import Base


class AuditLog(Base):
    """
    AuditLog model for tracking queries and system actions.
    
    Attributes:
        id: Unique identifier (UUID)
        user_id: User ID who made the query (FK to User)
        query_text: The original query text
        retrieved_documents: JSON array of retrieved document IDs and scores
        answer: The generated answer (nullable if refused)
        confidence_score: Confidence score of the answer (nullable)
        refusal_reason: Reason for refusal if answer was refused (nullable)
        sources: JSON array of source citations
        timestamp: Timestamp when query was made (indexed)
        response_time_ms: Response time in milliseconds
    """
    
    __tablename__ = "audit_logs"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    query_text = Column(
        Text,
        nullable=False
    )
    retrieved_documents = Column(
        JSON,
        nullable=True,
        default=list,
        comment="Array of {document_id, chunk_id, score} objects"
    )
    answer = Column(
        Text,
        nullable=True,
        comment="Generated answer or null if refused"
    )
    confidence_score = Column(
        Float,
        nullable=True,
        comment="Confidence score between 0 and 1"
    )
    refusal_reason = Column(
        String(500),
        nullable=True,
        comment="Reason for refusing to answer"
    )
    sources = Column(
        JSON,
        nullable=True,
        default=list,
        comment="Array of source citations"
    )
    timestamp = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
        index=True
    )
    response_time_ms = Column(
        Integer,
        nullable=False,
        default=0,
        comment="Response time in milliseconds"
    )
    
    # Relationships
    user = relationship(
        "User",
        back_populates="audit_logs"
    )
