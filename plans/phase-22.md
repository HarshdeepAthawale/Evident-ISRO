# Phase 22: Query History & Audit Logs UI

## Overview
Implement the query history page where users can view their past queries, filter results, and see confidence scores. This phase enables users to review their interaction history.

## Dependencies
- Phase 21: Results display must be complete

## Deliverables

### 1. Query History Page
- List of past queries
- Filtering and search
- Pagination
- Query details view

### 2. History Features
- View query and answer
- See confidence scores
- View sources
- Re-run queries

### 3. Audit Logs (Admin)
- View all user queries
- Filter by user, date, role
- Export functionality

## Files to Create

### `frontend/app/history/page.tsx`
User query history page

### `frontend/components/history/HistoryList.tsx`
List of query history items

### `frontend/components/history/HistoryItem.tsx`
Individual history item component

### `frontend/components/history/HistoryFilters.tsx`
Filter and search component

### `frontend/app/admin/audit/page.tsx`
Admin audit logs page (if not in Phase 24)

### `frontend/hooks/useHistory.ts`
Custom hook for query history

## Implementation Details

### Query History Display
- Show query text (truncated)
- Show answer preview
- Show confidence score
- Show timestamp
- Show number of sources
- Click to expand details

### Filtering Options
- Search by query text
- Filter by date range
- Filter by confidence level
- Filter by refusal status
- Sort by date, confidence

### Pagination
- Show 20 items per page
- Previous/Next buttons
- Page numbers
- Total count display

### Query Details View
- Full query text
- Full answer
- All sources
- Confidence breakdown
- Refusal reason (if applicable)
- Option to re-run

### Admin Audit Logs
- View all users' queries
- Filter by user
- Filter by date range
- Filter by role
- Export to CSV
- View statistics

### Data Source
- Option 1: Store in localStorage (client-side only)
- Option 2: Fetch from `/api/history` endpoint (requires backend)
- Option 3: Fetch from `/api/admin/audit-logs` (admin)

## Success Criteria
- [ ] History page displays queries
- [ ] Filtering works
- [ ] Search works
- [ ] Pagination works
- [ ] Query details expand
- [ ] Re-run functionality works
- [ ] Admin audit logs work

## Notes
- Add date range picker
- Support export to CSV
- Add statistics dashboard
- Consider real-time updates
- Add query analytics
- Support bulk operations
