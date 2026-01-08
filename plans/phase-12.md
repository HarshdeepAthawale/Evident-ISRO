# Phase 12: Confidence Scoring System

## Overview
Implement confidence scoring that measures how well the generated answer aligns with retrieved sources. This phase adds quality assurance to prevent low-confidence answers.

## Dependencies
- Phase 11: LLM generation must be working

## Deliverables

### 1. Confidence Calculation
- Answer-source alignment scoring
- Semantic similarity between answer and sources
- Overall confidence score

### 2. Threshold Logic
- Configurable confidence threshold
- Refusal based on low confidence
- Confidence-based filtering

### 3. Scoring Methods
- Multiple scoring approaches
- Weighted combination
- Validation against sources

## Files to Create

### `backend/rag/confidence.py`
```python
class ConfidenceScorer:
    def calculate_confidence(answer: str, sources: List[RetrievedChunk], embedding_model: EmbeddingModel) -> float
    def answer_source_alignment(answer: str, source_text: str) -> float
    def semantic_similarity(text1: str, text2: str) -> float
    def validate_answer_against_sources(answer: str, sources: List[RetrievedChunk]) -> bool
    def should_refuse(confidence: float, threshold: float = 0.7) -> bool
```

### `backend/rag/scoring_methods.py`
```python
def cosine_similarity_score(answer_embedding: np.ndarray, source_embeddings: List[np.ndarray]) -> float
def keyword_overlap_score(answer: str, sources: List[str]) -> float
def ngram_overlap_score(answer: str, sources: List[str]) -> float
def combined_confidence_score(scores: dict, weights: dict) -> float
```

## Implementation Details

### Confidence Calculation
1. Embed answer and source texts
2. Calculate cosine similarity between answer and each source
3. Take maximum similarity as base score
4. Calculate keyword overlap
5. Combine scores with weights
6. Return final confidence (0.0 - 1.0)

### Scoring Components
- **Semantic Similarity** (weight: 0.6): Embedding-based similarity
- **Keyword Overlap** (weight: 0.2): Shared important terms
- **N-gram Overlap** (weight: 0.1): Phrase matching
- **Source Coverage** (weight: 0.1): How many sources support answer

### Confidence Thresholds
- **High**: >= 0.8 → Accept answer
- **Medium**: 0.7 - 0.8 → Accept with warning
- **Low**: < 0.7 → Refuse answer
- Configurable per query type

### Refusal Logic
- If confidence < threshold → refuse
- If no sources support answer → refuse
- If conflicting sources → refuse
- Log refusal reason

### Validation
- Check answer doesn't contradict sources
- Verify key claims are in sources
- Detect hallucination patterns
- Flag speculative language

## Success Criteria
- [ ] Confidence scores are calculated
- [ ] Scores range from 0.0 to 1.0
- [ ] Threshold logic works
- [ ] Low confidence triggers refusal
- [ ] Scoring is consistent
- [ ] Performance is acceptable

## Notes
- Cache embeddings for efficiency
- Tune weights based on testing
- Consider learning-based scoring (future)
- Log all confidence scores
- Support per-query thresholds
- Add confidence explanation
