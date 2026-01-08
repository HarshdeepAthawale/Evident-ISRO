# Phase 21: Results Display Component

## Overview
Create the results display component that shows answers with confidence indicators, source citations, refusal messages, and copy/share functionality. This phase completes the query result presentation.

## Dependencies
- Phase 20: Query workspace must be complete
- Phase 14: Query API must be working

## Deliverables

### 1. Result Display
- Answer text display
- Confidence indicator
- Source citations
- Refusal message display

### 2. Source Citations
- Document titles
- Chunk text preview
- Similarity scores
- Page numbers (if available)

### 3. Interactive Features
- Copy answer
- Share query
- Expand/collapse sources
- View full source text

## Files to Create

### `frontend/components/query/QueryResult.tsx`
Main result display component

### `frontend/components/query/AnswerDisplay.tsx`
Answer text with confidence indicator

### `frontend/components/query/SourceList.tsx`
List of source citations

### `frontend/components/query/SourceCard.tsx`
Individual source citation card

### `frontend/components/query/RefusalMessage.tsx`
Refusal message display

### `frontend/components/ui/ConfidenceBadge.tsx`
Confidence score visual indicator

## Implementation Details

### Answer Display
- Show answer text in readable format
- Highlight key information (future)
- Format markdown if present
- Show confidence badge

### Confidence Indicator
- Color-coded badge:
  - Green: High (>= 0.8)
  - Yellow: Medium (0.7-0.8)
  - Red: Low (< 0.7) or refused
- Show percentage
- Tooltip with explanation

### Source Citations
- List all sources used
- Show document title
- Show chunk preview (first 200 chars)
- Show similarity score
- Link to full document (future)
- Expand to see full chunk text

### Refusal Message
- Clear refusal reason
- Explanation of why refused
- Suggestions for better query
- Link to help/documentation

### Interactive Features
- **Copy Answer**: Copy to clipboard
- **Share Query**: Generate shareable link
- **Export**: Export as PDF/Markdown
- **Feedback**: Like/dislike answer (future)

### Visual Design
- Clean, readable typography
- Proper spacing
- Color coding for confidence
- Icons for actions
- Smooth animations

## Success Criteria
- [ ] Answer displays correctly
- [ ] Confidence indicator works
- [ ] Sources are listed
- [ ] Citations are clickable
- [ ] Refusal messages are clear
- [ ] Copy functionality works
- [ ] UI is polished

## Notes
- Use markdown renderer for formatting
- Add syntax highlighting for code
- Support dark mode
- Add print styles
- Consider accessibility
- Add loading skeleton
