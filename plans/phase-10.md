# Phase 10: RAG Retrieval System

## Overview
Implement the RAG retrieval system that performs semantic search, applies metadata filtering, and retrieves relevant document chunks. This phase creates the core retrieval functionality.

## Dependencies
- Phase 9: Vector store must be set up
- Phase 7: Document access control must be implemented

## Deliverables

### 1. Query Processing
- Query normalization
- Query embedding generation
- Query expansion (optional)

### 2. Vector Search
- FAISS similarity search
- Top-k retrieval
- Similarity score thresholding

### 3. Metadata Filtering
- Filter by role
- Filter by mission
- Filter by document type
- Apply access control

### 4. Result Ranking
- Score-based ranking
- Diversity in results
- Remove duplicates

## Files to Create

### `backend/rag/retriever.py`
```python
class DocumentRetriever:
    def __init__(self, vector_store: VectorStore, embedding_model: EmbeddingModel)
    def retrieve(query: str, user: User, k: int = 5, threshold: float = 0.7) -> List[RetrievedChunk]
    def normalize_query(query: str) -> str
    def embed_query(query: str) -> np.ndarray
    def search_with_filters(query_vector: np.ndarray, user: User, k: int, filters: dict) -> List[dict]
    def apply_access_control(chunks: List[dict], user: User) -> List[dict]
    def rank_results(chunks: List[dict]) -> List[dict]
```

### `backend/rag/schemas.py`
```python
class RetrievedChunk(BaseModel):
    chunk_id: str
    document_id: str
    document_title: str
    text: str
    similarity_score: float
    chunk_index: int
    page: int (optional)
    metadata: dict
```

### `backend/rag/query_processor.py`
```python
def normalize_query(query: str) -> str
def expand_query(query: str) -> str
def extract_keywords(query: str) -> List[str]
```

## Implementation Details

### Retrieval Flow
1. Normalize user query
2. Generate query embedding with "query: " prefix
3. Perform FAISS search with metadata filters
4. Apply access control filtering
5. Filter by similarity threshold
6. Rank and deduplicate results
7. Return top-k chunks

### Metadata Filters
- `mission`: User's accessible missions
- `role`: User's role requirements
- `document_type`: Optional filter
- `date_range`: Optional filter

### Similarity Threshold
- Default: 0.7 (cosine similarity)
- Configurable per query
- Below threshold → refuse answer
- Log low-similarity queries

### Top-K Selection
- Default k: 5 chunks
- Maximum k: 20 chunks
- Ensure diversity (different documents)
- Prioritize higher scores

### Access Control Integration
- Filter chunks by user permissions
- Check document-level access
- Apply mission scoping
- Log filtered chunks

## Success Criteria
- [ ] Queries are normalized correctly
- [ ] Embeddings are generated for queries
- [ ] FAISS search returns relevant chunks
- [ ] Metadata filtering works
- [ ] Access control is applied
- [ ] Similarity thresholding works
- [ ] Results are ranked properly

## Notes
- Use query prefix for better embeddings
- Consider hybrid search (keyword + semantic)
- Cache frequent queries
- Monitor retrieval performance
- Support reranking (future enhancement)
