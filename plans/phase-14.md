# Phase 14: Query API Endpoints

## Overview
Create the main query API endpoint that integrates the complete RAG pipeline: authentication, retrieval, generation, confidence scoring, and refusal handling. This phase exposes the RAG system via REST API.

## Dependencies
- Phase 13: Hallucination prevention must be complete

## Deliverables

### 1. Query Endpoint
- POST `/api/query` - Main query endpoint
- Request/response models
- Error handling

### 2. Pipeline Integration
- Full RAG pipeline execution
- Audit logging
- Response formatting

### 3. API Documentation
- OpenAPI/Swagger documentation
- Request/response examples

## Files to Create

### `backend/api/query.py`
```python
@router.post("/query")
async def query(
    request: QueryRequest,
    current_user: User = Depends(get_current_active_user)
) -> QueryResponse:
    # 1. Validate query
    # 2. Check authorization
    # 3. Retrieve documents
    # 4. Generate answer
    # 5. Calculate confidence
    # 6. Validate and check refusal
    # 7. Log to audit
    # 8. Return response
```

### `backend/api/schemas.py`
```python
class QueryRequest(BaseModel):
    query: str
    k: int = 5
    confidence_threshold: float = 0.7
    mission: str = None

class QueryResponse(BaseModel):
    answer: Optional[str]
    confidence: Optional[float]
    sources: List[Source]
    refusal_reason: Optional[str]
    refusal_message: Optional[str]
    query_id: str
    timestamp: datetime

class Source(BaseModel):
    document_id: str
    document_title: str
    chunk_index: int
    text: str
    similarity_score: float
    page: int = None
```

### `backend/main.py` (update)
- Include query router
- Add OpenAPI documentation
- Configure CORS

## Implementation Details

### Query Flow
1. **Authentication**: Verify JWT token
2. **Authorization**: Check user permissions
3. **Query Normalization**: Clean and normalize query
4. **Retrieval**: Get relevant chunks with access control
5. **Generation**: Generate answer from context
6. **Confidence**: Calculate confidence score
7. **Validation**: Check for hallucinations
8. **Refusal Check**: Determine if answer should be refused
9. **Audit Log**: Log query and response
10. **Response**: Return structured response

### Error Handling
- Invalid query → 400 Bad Request
- Unauthorized → 401 Unauthorized
- Forbidden → 403 Forbidden
- No documents → Refusal response
- Generation error → 500 with error message

### Response Format
```json
{
    "answer": "The pressure drop occurred due to fuel line cavitation.",
    "confidence": 0.91,
    "sources": [
        {
            "document_id": "uuid",
            "document_title": "Engine Analysis Report",
            "chunk_index": 3,
            "text": "...",
            "similarity_score": 0.89,
            "page": 14
        }
    ],
    "refusal_reason": null,
    "refusal_message": null,
    "query_id": "uuid",
    "timestamp": "2024-01-01T12:00:00Z"
}
```

### Audit Logging
- Log every query (success or refusal)
- Include user, query, retrieved docs, answer, confidence
- Store in database for compliance

## Success Criteria
- [ ] Query endpoint works
- [ ] Full pipeline executes
- [ ] Responses are properly formatted
- [ ] Error handling works
- [ ] Audit logging works
- [ ] API documentation is complete

## Notes
- Add rate limiting (future)
- Support streaming responses (future)
- Add query history endpoint
- Support query cancellation
- Monitor API performance
- Add request validation
