# Phase 11: LLM Integration (llama.cpp)

## Overview
Integrate llama.cpp for local LLM inference with strict context-locked generation. This phase enables the AI to generate answers strictly from retrieved documents.

## Dependencies
- Phase 10: RAG retrieval system must be complete

## Deliverables

### 1. LLM Setup
- Load llama.cpp model
- Configure generation parameters
- Model initialization

### 2. Context-Locked Generation
- Strict prompt templates
- Context-only answer generation
- Refusal instructions

### 3. Generation Control
- Temperature settings
- Token limits
- Stop sequences

## Files to Create

### `backend/rag/generator.py`
```python
from llama_cpp import Llama

class LLMGenerator:
    def __init__(self, model_path: str)
    def generate(context: str, query: str, max_tokens: int = 500) -> str
    def create_prompt(context: str, query: str) -> str
    def validate_answer(answer: str, context: str) -> bool
```

### `backend/rag/prompts.py`
```python
SYSTEM_PROMPT = """You are EVIDENT, a secure AI assistant for ISRO.
You must answer questions ONLY using the provided context documents.
If the answer is not in the context, you MUST refuse to answer.
Never make up information or use external knowledge."""

def create_rag_prompt(context: str, query: str) -> str
def create_refusal_prompt(query: str) -> str
```

### `backend/core/llm_config.py`
```python
class LLMConfig:
    model_path: str
    n_ctx: int = 4096
    n_threads: int = 4
    temperature: float = 0.1
    top_p: float = 0.9
    max_tokens: int = 500
```

## Implementation Details

### Model Configuration
- Use quantized models (Q4_K_M or Q5_K_M)
- Context window: 4096 tokens
- Temperature: 0.1 (low for deterministic answers)
- Top-p: 0.9 (nucleus sampling)

### Prompt Template
```
System: {SYSTEM_PROMPT}

Context Documents:
{document_1}
---
{document_2}
---
...

User Query: {query}

Answer (ONLY from context, refuse if not found):
```

### Generation Parameters
- `max_tokens`: 500 (limit answer length)
- `stop`: ["\n\nContext:", "User Query:", "---"]
- `repeat_penalty`: 1.1 (reduce repetition)
- `top_k`: 40 (diversity)

### Context Assembly
- Combine retrieved chunks
- Add document citations
- Limit total context to model's window
- Prioritize higher-scoring chunks

### Refusal Handling
- If no context → return refusal
- If low confidence → return refusal
- Explicit refusal message format

## Success Criteria
- [ ] Model loads successfully
- [ ] Generation works with context
- [ ] Answers are context-locked
- [ ] Refusal works when appropriate
- [ ] Token limits are enforced
- [ ] Performance is acceptable

## Notes
- Support multiple model formats (GGUF)
- Consider GPU acceleration
- Monitor memory usage
- Cache model loading
- Support model switching
- Add fallback for model errors
