# EVIDENT

**Evidence-Grounded Intelligence for Document-Enabled Knowledge Systems**

EVIDENT is a production-grade, secure, evidence-grounded Retrieval-Augmented Generation (RAG) software system designed for mission-critical organizations like ISRO. It answers user queries **only using authorized internal documents**, with explicit source citations, confidence scoring, strict hallucination prevention, role-based access control, and comprehensive audit logging.

## 🎯 Core Philosophy

- **Security > Convenience**: Every access is authenticated, authorized, and audited
- **Correctness > Fluency**: Answers are strictly evidence-based, never fabricated
- **Refusal > Hallucination**: If evidence is insufficient, the system refuses to answer
- **Traceability > Creativity**: Every answer includes source citations and confidence scores

## ✨ Key Features

### 🔐 Security
- JWT-based authentication with refresh tokens
- Role-based access control (Admin, Engineer, Viewer)
- Document-level and chunk-level permissions
- Mission/project scoping for access control
- Comprehensive audit logging

### 🧠 Secure RAG Pipeline
- Semantic document retrieval using FAISS vector search
- Context-locked LLM generation (llama.cpp)
- Confidence scoring and validation
- Hallucination prevention with automatic refusal
- Source citations for every answer

### 📊 Audit & Compliance
- Complete query audit trail
- User activity logging
- System statistics and analytics
- Exportable audit logs

### 🛡️ Hallucination Prevention
- Answer validation against retrieved sources
- Confidence threshold enforcement
- Contradiction detection
- Speculative language detection
- Explicit refusal when evidence is insufficient

## 🏗️ Architecture

```
User Query
  ↓
JWT Authentication
  ↓
Role & Scope Authorization
  ↓
Query Normalization
  ↓
FAISS Vector Retrieval (with access control)
  ↓
Similarity Threshold Check
  ↓
Context Assembly
  ↓
LLM Generation (context-locked)
  ↓
Confidence Calculation
  ↓
Hallucination Validation
  ↓
Source Attachment
  ↓
Persistent Audit Log
  ↓
Structured Response
```

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Vector Store**: FAISS
- **Embeddings**: Sentence Transformers (e5-base)
- **LLM**: llama.cpp (local inference)
- **Authentication**: JWT with bcrypt

### Frontend
- **Framework**: Next.js 14+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL 12+
- Node.js 18+ (for frontend)
- llama.cpp model file (GGUF format)

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone <repository-url>
cd evident
```

### 2. Backend Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# - Set DATABASE_URL
# - Set JWT_SECRET_KEY (generate with: openssl rand -hex 32)
# - Set LLM_MODEL_PATH to your GGUF model file

# Run database migrations (after Phase 2)
# alembic upgrade head

# Start backend server
uvicorn backend.main:app --reload
```

### 3. Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

## 🔒 Security Model

EVIDENT enforces security at multiple levels:

1. **Authentication**: JWT tokens with secure password hashing (bcrypt)
2. **Authorization**: Role-based access control with mission scoping
3. **Access Control**: Document-level and chunk-level permissions
4. **Audit Logging**: Every query is logged with user, timestamp, and results
5. **Data Protection**: All sensitive data is encrypted and access-controlled

## 📚 Documentation

- [Architecture Documentation](docs/ARCHITECTURE.md) - System design and components
- [Security Documentation](docs/SECURITY.md) - Security model and best practices
- [API Documentation](docs/API.md) - API endpoints and usage
- [Setup Guide](docs/SETUP.md) - Detailed setup instructions
- [Deployment Guide](docs/DEPLOYMENT.md) - Production deployment

## 🧪 Development

### Project Structure

```
evident/
├── backend/           # FastAPI backend
│   ├── core/         # Core configuration and database
│   ├── models/       # SQLAlchemy models
│   ├── auth/         # Authentication and authorization
│   ├── rag/          # RAG pipeline components
│   ├── ingestion/    # Document ingestion
│   └── utils/        # Utilities and helpers
├── frontend/         # Next.js frontend
├── data/             # Data storage
│   ├── raw_docs/     # Raw documents
│   └── vector_store/ # FAISS vector store
├── plans/            # Phase-by-phase build plans
└── docs/             # Documentation
```

## 📝 License

[Add your license here]

## 🤝 Contributing

[Add contributing guidelines here]

## 📧 Contact

[Add contact information here]

---

**EVIDENT** - Evidence + Intelligence. Trusted AI for mission-critical systems.
