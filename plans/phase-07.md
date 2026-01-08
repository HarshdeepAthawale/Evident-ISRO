# Phase 7: Document Access Control

## Overview
Implement document-level and chunk-level access control. This phase ensures users can only access documents and chunks they are authorized to view, with filtering at the query level.

## Dependencies
- Phase 6: RBAC system must be complete
- Phase 2: Document and DocumentPermission models must exist

## Deliverables

### 1. Document-Level Access Control
- Permission checking for documents
- Document ownership logic
- Document sharing functionality

### 2. Chunk-Level Filtering
- Filter chunks by user permissions
- Mission-based filtering
- Role-based filtering

### 3. Query-Time Access Filtering
- Filter retrieved documents by permissions
- Apply access control in RAG pipeline
- Prevent unauthorized document access

## Files to Create

### `backend/core/document_access.py`
```python
def check_document_access(user: User, document_id: str) -> bool
def get_accessible_documents(user: User, mission: str = None) -> List[Document]
def filter_chunks_by_access(user: User, chunks: List[DocumentChunk]) -> List[DocumentChunk]
def can_user_read_document(user: User, document: Document) -> bool
```

### `backend/core/document_sharing.py`
```python
def share_document(document_id: str, user_id: str, permission: str)
def revoke_document_access(document_id: str, user_id: str)
def get_document_permissions(document_id: str) -> List[DocumentPermission]
```

### `backend/rag/access_filter.py`
```python
def filter_retrieved_documents(user: User, documents: List[Document]) -> List[Document]
def apply_access_control_to_chunks(user: User, chunks: List[DocumentChunk]) -> List[DocumentChunk]
```

## Implementation Details

### Access Control Rules
1. Admin: Access to all documents
2. Engineer: Access to documents in assigned missions
3. Viewer: Read-only access to documents in assigned missions
4. Document owner: Full access to own documents
5. Explicit permissions: Override default role permissions

### Permission Types
- `read`: Can view document and chunks
- `write`: Can modify document metadata
- `delete`: Can delete document

### Filtering Strategy
- Pre-filter: Filter documents before vector search
- Post-filter: Filter chunks after retrieval
- Metadata filter: Use FAISS metadata filtering

### Mission Scoping
- Documents belong to missions
- Users are assigned to missions
- Queries automatically filter by user's missions

## Success Criteria
- [ ] Document access checks work correctly
- [ ] Chunks are filtered by permissions
- [ ] Query-time filtering prevents unauthorized access
- [ ] Document sharing works
- [ ] Mission scoping is enforced
- [ ] Admin bypass works correctly

## Notes
- Always check permissions, even for admins (for audit)
- Cache permission checks for performance
- Log all access denials
- Support inheritance (mission → document → chunk)
- Consider row-level security in database
