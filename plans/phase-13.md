# Phase 13: Hallucination Prevention

## Overview
Implement comprehensive hallucination prevention that validates answers against sources, detects contradictions, and enforces strict refusal when evidence is insufficient.

## Dependencies
- Phase 12: Confidence scoring must be complete

## Deliverables

### 1. Answer Validation
- Source verification checks
- Contradiction detection
- Fact validation

### 2. Refusal System
- Refusal reasons
- Refusal response format
- Refusal logging

### 3. Hallucination Detection
- Pattern detection
- Speculative language detection
- External knowledge detection

## Files to Create

### `backend/rag/refusal.py`
```python
class RefusalHandler:
    def should_refuse(answer: str, sources: List[RetrievedChunk], confidence: float) -> Tuple[bool, str]
    def validate_against_sources(answer: str, sources: List[RetrievedChunk]) -> bool
    def detect_contradictions(answer: str, sources: List[RetrievedChunk]) -> bool
    def detect_speculative_language(answer: str) -> bool
    def create_refusal_response(reason: str) -> dict
```

### `backend/rag/validation.py`
```python
def verify_facts_in_sources(answer: str, sources: List[str]) -> bool
def check_key_claims(answer: str, sources: List[str]) -> List[bool]
def detect_hallucination_patterns(answer: str) -> bool
def extract_claims(answer: str) -> List[str]
```

### `backend/rag/refusal_reasons.py`
```python
class RefusalReason(Enum):
    NO_DOCUMENTS = "No relevant documents found"
    LOW_SIMILARITY = "Retrieved documents have low similarity to query"
    LOW_CONFIDENCE = "Answer confidence below threshold"
    CONTRADICTORY_SOURCES = "Sources contain conflicting information"
    INSUFFICIENT_EVIDENCE = "Insufficient evidence to answer question"
    SPECULATIVE_ANSWER = "Answer contains speculative or unverified claims"
```

## Implementation Details

### Validation Checks
1. **Source Verification**: All key claims must be in sources
2. **Contradiction Detection**: Check for conflicting information
3. **Speculative Language**: Detect phrases like "probably", "might", "could be"
4. **External Knowledge**: Flag information not in sources
5. **Confidence Check**: Verify confidence meets threshold

### Refusal Triggers
- No documents retrieved
- Similarity score < threshold
- Confidence score < threshold
- Contradictory sources
- Speculative language detected
- Key claims not in sources

### Refusal Response Format
```json
{
    "answer": null,
    "confidence": 0.0,
    "sources": [],
    "refusal_reason": "LOW_CONFIDENCE",
    "refusal_message": "Insufficient evidence to provide a reliable answer. Confidence score: 0.65 (threshold: 0.70)"
}
```

### Hallucination Patterns
- Generic statements without source support
- Specific numbers/dates not in sources
- Technical terms not mentioned in context
- Causal relationships not stated
- Comparisons not in sources

### Validation Methods
- **Claim Extraction**: Extract factual claims from answer
- **Source Matching**: Match claims to source text
- **Coverage Check**: Verify sufficient source coverage
- **Consistency Check**: Ensure no contradictions

## Success Criteria
- [ ] Answer validation works
- [ ] Contradictions are detected
- [ ] Speculative language is flagged
- [ ] Refusal responses are clear
- [ ] All refusal reasons are handled
- [ ] Validation is accurate

## Notes
- Be conservative (refuse when uncertain)
- Log all refusals with reasons
- Support configurable strictness
- Consider fine-tuning validation
- Add explanation for refusals
- Monitor false positive rate
