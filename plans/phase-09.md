# Phase 9: Vector Store Setup

## Overview
Set up FAISS vector store with sentence transformer embeddings. This phase creates the vector search infrastructure that enables semantic document retrieval.

## Dependencies
- Phase 8: Document ingestion must be complete

## Deliverables

### 1. FAISS Index Management
- Create and manage FAISS index
- Persistent storage to disk
- Index loading and saving
- Incremental updates

### 2. Embedding System
- Sentence transformer model (e5-base)
- Generate embeddings for chunks
- Batch embedding generation

### 3. Vector Store Operations
- Add vectors to index
- Update vectors
- Delete vectors
- Search operations

## Files to Create

### `backend/rag/vector_store.py`
```python
class VectorStore:
    def __init__(self, index_path: str, embedding_model: str)
    def create_index(dimension: int)
    def load_index() -> faiss.Index
    def save_index()
    def add_vectors(vectors: np.ndarray, ids: List[str], metadata: List[dict])
    def search(query_vector: np.ndarray, k: int, filters: dict) -> List[dict]
    def delete_vectors(ids: List[str])
    def update_vector(id: str, vector: np.ndarray)
```

### `backend/rag/embeddings.py`
```python
class EmbeddingModel:
    def __init__(self, model_name: str = "intfloat/e5-base")
    def encode(text: str) -> np.ndarray
    def encode_batch(texts: List[str]) -> np.ndarray
    def get_dimension() -> int
```

### `backend/rag/index_manager.py`
```python
def initialize_vector_store()
def rebuild_index()
def add_document_to_index(document: Document, chunks: List[DocumentChunk])
def remove_document_from_index(document_id: str)
```

## Implementation Details

### FAISS Index Type
- Use `IndexFlatIP` (Inner Product) for cosine similarity
- Normalize vectors for cosine similarity
- Store metadata alongside vectors
- Use ID mapping for chunk references

### Embedding Model
- Model: `intfloat/e5-base` (768 dimensions)
- Query prefix: "query: "
- Document prefix: "passage: "
- Batch size: 32 for efficiency

### Index Structure
- Vector dimension: 768
- Index file: `data/vector_store/index.faiss`
- Metadata file: `data/vector_store/metadata.json`
- ID mapping: `data/vector_store/id_mapping.json`

### Persistence
- Save index after each batch of additions
- Load index on application startup
- Support index rebuilding
- Backup index before major operations

### Metadata Storage
- Store chunk ID, document ID, mission, role requirements
- Enable metadata filtering in search
- Support filtering by mission, document type, etc.

## Success Criteria
- [ ] FAISS index is created
- [ ] Embeddings are generated correctly
- [ ] Vectors are added to index
- [ ] Index persists to disk
- [ ] Index loads on startup
- [ ] Search operations work
- [ ] Metadata filtering works

## Notes
- Use GPU if available (faiss-gpu)
- Consider quantization for large indices
- Monitor index size and performance
- Support index sharding for scale
- Cache embeddings for repeated queries
