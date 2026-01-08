# Phase 15: Document Management API

## Overview
Create CRUD API endpoints for document management: upload, list, retrieve, update, and delete documents. This phase enables document administration through the API.

## Dependencies
- Phase 8: Document ingestion must be complete

## Deliverables

### 1. Document Endpoints
- POST `/api/documents` - Upload document
- GET `/api/documents` - List documents
- GET `/api/documents/{id}` - Get document details
- PUT `/api/documents/{id}` - Update document metadata
- DELETE `/api/documents/{id}` - Delete document

### 2. Upload Handling
- File upload processing
- Validation
- Ingestion trigger

### 3. Access Control
- Role-based endpoint protection
- Document-level permissions
- Mission scoping

## Files to Create

### `backend/api/documents.py`
```python
@router.post("/documents", dependencies=[Depends(require_roles("admin", "engineer"))])
async def upload_document(
    file: UploadFile,
    metadata: DocumentMetadata,
    current_user: User
) -> DocumentResponse

@router.get("/documents")
async def list_documents(
    mission: str = None,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> List[DocumentResponse]

@router.get("/documents/{document_id}")
async def get_document(
    document_id: str,
    current_user: User = Depends(get_current_active_user)
) -> DocumentResponse

@router.put("/documents/{document_id}")
async def update_document(
    document_id: str,
    metadata: DocumentUpdate,
    current_user: User = Depends(require_roles("admin", "engineer"))
) -> DocumentResponse

@router.delete("/documents/{document_id}")
async def delete_document(
    document_id: str,
    current_user: User = Depends(require_admin)
) -> DeleteResponse
```

### `backend/api/document_schemas.py`
```python
class DocumentMetadata(BaseModel):
    title: str
    mission: str
    project: str = None
    document_type: str = None

class DocumentResponse(BaseModel):
    id: str
    title: str
    mission: str
    project: str
    document_type: str
    uploaded_by: str
    uploaded_at: datetime
    total_chunks: int
    file_path: str
```

## Implementation Details

### Upload Flow
1. Validate file (PDF, size limits)
2. Save file to `data/raw_docs/`
3. Extract metadata
4. Create document record
5. Trigger ingestion pipeline
6. Generate embeddings
7. Add to vector store
8. Return document info

### File Validation
- Allowed types: PDF only
- Max file size: 50MB (configurable)
- Virus scanning (future)
- Content validation

### List Documents
- Filter by mission (user's accessible missions)
- Pagination support
- Sort by upload date
- Search by title (future)

### Delete Document
- Remove from database
- Delete file from disk
- Remove from vector store
- Delete all chunks
- Log deletion

### Access Control
- Upload: Admin or Engineer
- List: All authenticated users (filtered by access)
- View: Based on document permissions
- Update: Admin or Engineer (owner)
- Delete: Admin only

## Success Criteria
- [ ] Documents can be uploaded
- [ ] Documents are listed correctly
- [ ] Document details are retrieved
- [ ] Metadata can be updated
- [ ] Documents can be deleted
- [ ] Access control is enforced
- [ ] File validation works

## Notes
- Support batch upload (future)
- Add document versioning (future)
- Support other file types (future)
- Add document preview
- Implement soft delete
- Add restore functionality
