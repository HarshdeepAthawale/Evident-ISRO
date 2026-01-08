"""
EVIDENT Document Models

This module defines the Document and DocumentChunk models for document storage
and retrieval.
"""

from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, Text, JSON
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import uuid

from backend.core.database import Base


class Document(Base):
    """
    Document model for storing document metadata.
    
    Attributes:
        id: Unique identifier (UUID)
        title: Document title
        file_path: Path to the document file
        file_type: File type/extension
        mission: Mission name (indexed for filtering)
        project: Project name
        uploaded_by: User ID who uploaded the document (FK to User)
        uploaded_at: Timestamp when document was uploaded
        metadata: Additional metadata as JSON
        total_chunks: Total number of chunks in the document
    """
    
    __tablename__ = "documents"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    title = Column(
        String(500),
        nullable=False
    )
    file_path = Column(
        String(1000),
        nullable=False,
        unique=True
    )
    file_type = Column(
        String(50),
        nullable=False
    )
    mission = Column(
        String(255),
        nullable=True,
        index=True
    )
    project = Column(
        String(255),
        nullable=True
    )
    uploaded_by = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    metadata = Column(
        JSON,
        nullable=True,
        default=dict
    )
    total_chunks = Column(
        Integer,
        default=0,
        nullable=False
    )
    
    # Relationships
    uploader = relationship(
        "User",
        back_populates="documents"
    )
    chunks = relationship(
        "DocumentChunk",
        back_populates="document",
        cascade="all, delete-orphan",
        order_by="DocumentChunk.chunk_index"
    )
    permissions = relationship(
        "DocumentPermission",
        back_populates="document",
        cascade="all, delete-orphan"
    )


class DocumentChunk(Base):
    """
    DocumentChunk model for storing text chunks with embeddings.
    
    Attributes:
        id: Unique identifier (UUID)
        document_id: Document ID this chunk belongs to (FK to Document)
        chunk_index: Index of the chunk within the document
        text: The chunk text content
        embedding: Embedding vector reference (for FAISS lookup)
        start_char: Starting character position in original document
        end_char: Ending character position in original document
        created_at: Timestamp when chunk was created
    """
    
    __tablename__ = "document_chunks"
    
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        index=True
    )
    document_id = Column(
        UUID(as_uuid=True),
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    chunk_index = Column(
        Integer,
        nullable=False
    )
    text = Column(
        Text,
        nullable=False
    )
    embedding = Column(
        Text,
        nullable=True,
        comment="Reference to FAISS vector store index"
    )
    start_char = Column(
        Integer,
        nullable=False
    )
    end_char = Column(
        Integer,
        nullable=False
    )
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
    
    # Relationships
    document = relationship(
        "Document",
        back_populates="chunks"
    )
    
    # Unique constraint on document_id and chunk_index
    __table_args__ = (
        {"comment": "Document chunks with embeddings for vector search"}
    )
