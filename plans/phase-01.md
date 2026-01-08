# Phase 1: Project Structure & Configuration

## Overview
Set up the foundational project structure, configuration management, and dependency management for EVIDENT. This phase establishes the directory layout, Python environment setup, and core configuration system.

## Dependencies
None - This is the starting phase.

## Deliverables

### 1. Directory Structure
Create the following directory structure:
```
evident/
├── backend/
│   ├── core/
│   ├── models/
│   ├── auth/
│   ├── rag/
│   ├── ingestion/
│   └── utils/
├── frontend/
├── data/
│   ├── raw_docs/
│   └── vector_store/
├── plans/
└── docs/
```

### 2. Python Environment Setup
- Create `requirements.txt` with all backend dependencies
- Create `.env.example` template file
- Create `.gitignore` file

### 3. Configuration System
- Create `backend/core/config.py` with environment-based configuration
- Support for database, JWT, and application settings

### 4. Documentation
- Create initial `README.md` with project overview
- Document setup instructions

## Files to Create

### `requirements.txt`
```python
# Web Framework
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.23
alembic==1.12.1
psycopg2-binary==2.9.9

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0

# Vector Store & Embeddings
faiss-cpu==1.7.4
sentence-transformers==2.2.2
numpy==1.24.3

# LLM
llama-cpp-python==0.2.11

# Document Processing
PyPDF2==3.0.1
pdfplumber==0.10.3

# Utilities
pydantic==2.5.0
pydantic-settings==2.1.0
```

### `backend/core/config.py`
- Load environment variables
- Database connection settings
- JWT secret and algorithm
- Application settings (host, port, debug)
- Vector store paths
- LLM model paths

### `.env.example`
Template with all required environment variables:
- `DATABASE_URL`
- `JWT_SECRET_KEY`
- `JWT_ALGORITHM`
- `JWT_ACCESS_TOKEN_EXPIRE_MINUTES`
- `VECTOR_STORE_PATH`
- `LLM_MODEL_PATH`
- etc.

### `.gitignore`
Standard Python/Node.js gitignore patterns

### `README.md`
- Project name: EVIDENT
- One-line description
- Architecture overview
- Setup instructions
- Security model summary

## Implementation Details

### Configuration Class Structure
```python
# backend/core/config.py structure
class Settings:
    # Database
    database_url: str
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_access_token_expire_minutes: int
    # Application
    app_name: str = "EVIDENT"
    debug: bool = False
    # Paths
    vector_store_path: str
    raw_docs_path: str
    llm_model_path: str
```

## Success Criteria
- [ ] All directories created
- [ ] `requirements.txt` includes all dependencies
- [ ] `.env.example` has all required variables
- [ ] Configuration loads from environment variables
- [ ] `README.md` provides clear project overview
- [ ] `.gitignore` excludes sensitive files

## Notes
- Use Python 3.10+ for compatibility
- Configuration should use `pydantic-settings` for validation
- All paths should be configurable via environment variables
- Keep sensitive values out of version control
