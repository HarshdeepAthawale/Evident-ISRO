# Phase 2: Database Models & Schema

## Overview
Create the complete database schema using SQLAlchemy ORM, including all models for users, documents, chunks, audit logs, roles, and permissions. Set up Alembic for database migrations.

## Dependencies
- Phase 1: Project structure and configuration must be complete

## Deliverables

### 1. Database Connection
- Set up PostgreSQL connection in `backend/core/database.py`
- Create database session management
- Implement connection pooling

### 2. SQLAlchemy Models
Create models for:
- `User` - User accounts with roles
- `Document` - Document metadata
- `DocumentChunk` - Text chunks with embeddings
- `AuditLog` - Query and action audit trail
- `Role` - Role definitions
- `Permission` - Permission mappings
- `DocumentPermission` - Document-level access control

### 3. Database Migrations
- Set up Alembic configuration
- Create initial migration
- Define relationships and indexes

## Files to Create

### `backend/core/database.py`
- Database engine creation
- SessionLocal class
- Database dependency for FastAPI
- Connection string from config

### `backend/models/user.py`
```python
class User(Base):
    id: UUID (primary key)
    username: str (unique, indexed)
    email: str (unique, indexed)
    hashed_password: str
    full_name: str
    role: str (admin, engineer, viewer)
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

### `backend/models/document.py`
```python
class Document(Base):
    id: UUID (primary key)
    title: str
    file_path: str
    file_type: str
    mission: str (indexed)
    project: str
    uploaded_by: UUID (FK to User)
    uploaded_at: datetime
    metadata: JSON
    total_chunks: int
    
class DocumentChunk(Base):
    id: UUID (primary key)
    document_id: UUID (FK to Document)
    chunk_index: int
    text: text
    embedding: vector (for FAISS reference)
    start_char: int
    end_char: int
    created_at: datetime
```

### `backend/models/audit_log.py`
```python
class AuditLog(Base):
    id: UUID (primary key)
    user_id: UUID (FK to User)
    query_text: text
    retrieved_documents: JSON
    answer: text (nullable)
    confidence_score: float (nullable)
    refusal_reason: str (nullable)
    sources: JSON
    timestamp: datetime (indexed)
    response_time_ms: int
```

### `backend/models/role.py`
```python
class Role(Base):
    id: UUID (primary key)
    name: str (unique)
    description: str
    permissions: JSON

class DocumentPermission(Base):
    id: UUID (primary key)
    document_id: UUID (FK to Document)
    user_id: UUID (FK to User, nullable)
    role: str (nullable)
    permission_type: str (read, write, delete)
    created_at: datetime
```

### `alembic.ini`
Alembic configuration file

### `alembic/env.py`
Alembic environment setup

### `alembic/versions/001_initial_schema.py`
Initial migration with all tables

## Implementation Details

### Database Relationships
- User → Documents (one-to-many)
- Document → DocumentChunks (one-to-many)
- User → AuditLogs (one-to-many)
- Document → DocumentPermissions (one-to-many)
- User → DocumentPermissions (many-to-many)

### Indexes to Create
- `users.username` (unique)
- `users.email` (unique)
- `documents.mission` (for filtering)
- `audit_logs.timestamp` (for queries)
- `audit_logs.user_id` (for filtering)
- `document_chunks.document_id` (for lookups)

### Database Initialization
- Create function to initialize database
- Create default admin user (if needed)
- Seed initial roles

## Success Criteria
- [ ] All models defined with proper relationships
- [ ] Alembic migrations set up
- [ ] Initial migration creates all tables
- [ ] Database connection works
- [ ] Indexes created for performance
- [ ] Foreign key constraints in place

## Notes
- Use UUID for primary keys (security)
- Add soft delete support where needed
- Use JSON fields for flexible metadata
- Consider adding full-text search indexes later
- All timestamps should use UTC
