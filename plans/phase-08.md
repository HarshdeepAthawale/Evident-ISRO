# Phase 8: Document Ingestion Pipeline

## Overview
Create the document ingestion system that parses PDFs, chunks text, extracts metadata, and prepares documents for vector storage. This phase enables the system to process and store documents.

## Dependencies
- Phase 2: Document and DocumentChunk models must exist

## Deliverables

### 1. PDF Parsing
- PDF text extraction
- Metadata extraction (title, author, date)
- Page-level processing

### 2. Text Chunking
- Intelligent text splitting
- Overlap between chunks
- Chunk size management

### 3. Metadata Extraction
- Document title
- Author/creator
- Creation date
- Mission/project assignment
- Document type classification

### 4. Storage
- Store raw documents
- Save document metadata to database
- Prepare chunks for embedding

## Files to Create

### `backend/ingestion/ingest_docs.py`
```python
class DocumentIngester:
    def ingest_pdf(file_path: str, metadata: dict) -> Document
    def parse_pdf(file_path: str) -> dict
    def chunk_text(text: str, chunk_size: int, overlap: int) -> List[str]
    def extract_metadata(file_path: str) -> dict
    def save_document(document_data: dict) -> Document
```

### `backend/ingestion/parsers.py`
```python
def parse_pdf_pypdf2(file_path: str) -> str
def parse_pdf_pdfplumber(file_path: str) -> str
def extract_pdf_metadata(file_path: str) -> dict
```

### `backend/ingestion/chunking.py`
```python
def chunk_text_by_sentences(text: str, chunk_size: int, overlap: int) -> List[str]
def chunk_text_by_tokens(text: str, max_tokens: int, overlap: int) -> List[str]
def smart_chunk_text(text: str, chunk_size: int) -> List[str]
```

### `backend/ingestion/metadata.py`
```python
def extract_document_metadata(file_path: str) -> dict
def infer_mission_from_content(text: str) -> str
def classify_document_type(text: str) -> str
```

## Implementation Details

### Chunking Strategy
- Default chunk size: 500 tokens
- Overlap: 50 tokens (10%)
- Preserve sentence boundaries
- Handle tables and structured content

### Metadata Fields
- `title`: Document title
- `author`: Creator/author
- `date`: Creation/modification date
- `mission`: Mission assignment
- `project`: Project name
- `document_type`: Report, manual, SOP, etc.
- `pages`: Total page count
- `language`: Document language

### File Storage
- Store in `data/raw_docs/{mission}/{document_id}.pdf`
- Maintain original filename
- Support versioning (future)

### Error Handling
- Invalid PDF → Log error, skip document
- Corrupted file → Handle gracefully
- Missing metadata → Use defaults
- Large files → Process in chunks

## Success Criteria
- [ ] PDFs are parsed correctly
- [ ] Text is chunked with proper overlap
- [ ] Metadata is extracted accurately
- [ ] Documents are stored in database
- [ ] Chunks are created and linked
- [ ] Error handling works for invalid files

## Notes
- Support multiple PDF parsing libraries (fallback)
- Consider OCR for scanned PDFs (future)
- Handle different encodings
- Preserve formatting where possible
- Log all ingestion events
