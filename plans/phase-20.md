# Phase 20: Query Workspace UI

## Overview
Build the query workspace interface where users can submit queries, view loading states, and see query history. This phase creates the main user interaction point.

## Dependencies
- Phase 19: Dashboard layout must be complete

## Deliverables

### 1. Query Interface
- Query input form
- Submit button
- Loading states
- Query history sidebar

### 2. Query Submission
- Form validation
- API integration
- Error handling

### 3. Query History
- Recent queries list
- Click to re-run
- Clear history

## Files to Create

### `frontend/app/query/page.tsx`
Main query workspace page

### `frontend/components/query/QueryInput.tsx`
Query input form component

### `frontend/components/query/QueryHistory.tsx`
Query history sidebar component

### `frontend/components/query/QueryForm.tsx`
Complete query form with submission

### `frontend/hooks/useQuery.ts`
Custom hook for query operations

## Implementation Details

### Query Input
- Large textarea for query
- Character counter (optional)
- Submit button
- Clear button
- Example queries (helpful hints)

### Query Submission Flow
1. User enters query
2. Validate (not empty, max length)
3. Show loading state
4. Call `/api/query` endpoint
5. Display results (Phase 21)
6. Add to history
7. Handle errors

### Loading States
- Spinner during query
- Disable form during processing
- Show "Processing query..." message
- Estimated time (if available)

### Query History
- Store in localStorage or context
- Show last 10 queries
- Click to re-run query
- Clear all history
- Persist across sessions

### Error Handling
- Network errors → Show error message
- Validation errors → Show inline errors
- API errors → Display error from backend
- Timeout → Show timeout message

### UI Features
- Auto-focus on input
- Keyboard shortcut (Ctrl+Enter to submit)
- Query suggestions (future)
- Save favorite queries (future)

## Success Criteria
- [ ] Query input works
- [ ] Form validation works
- [ ] Query submission works
- [ ] Loading states display
- [ ] Query history works
- [ ] Error handling works
- [ ] UI is responsive

## Notes
- Use React Hook Form
- Add debouncing for suggestions (future)
- Support query templates
- Add query export (future)
- Consider voice input (future)
- Add query sharing (future)
