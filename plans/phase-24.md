# Phase 24: Admin - User & Audit Management UI

## Overview
Create admin interfaces for user management and audit log viewing. This phase enables administrators to manage users and monitor system activity.

## Dependencies
- Phase 19: Dashboard layout must be complete
- Phase 16: Admin API must be working

## Deliverables

### 1. User Management UI
- List all users
- Create/edit users
- Assign roles
- Activate/deactivate users

### 2. Audit Log Viewer
- View all audit logs
- Filter by user, date, role
- Search functionality
- Export to CSV

### 3. System Statistics Dashboard
- User statistics
- Document statistics
- Query statistics
- Visual charts

## Files to Create

### `frontend/app/admin/users/page.tsx`
User management page

### `frontend/components/admin/UserList.tsx`
List of users component

### `frontend/components/admin/UserForm.tsx`
User create/edit form

### `frontend/components/admin/UserModal.tsx`
User details/edit modal

### `frontend/app/admin/audit/page.tsx`
Audit logs page (if not in Phase 22)

### `frontend/components/admin/AuditLogList.tsx`
Audit log list component

### `frontend/components/admin/AuditLogFilters.tsx`
Audit log filters

### `frontend/app/admin/stats/page.tsx`
System statistics dashboard

### `frontend/components/admin/StatsCards.tsx`
Statistics cards component

### `frontend/components/admin/StatsCharts.tsx`
Charts for statistics

## Implementation Details

### User Management
- Table view with columns: Username, Email, Role, Status, Actions
- Create new user button
- Edit user (click row or button)
- Assign/change role dropdown
- Activate/deactivate toggle
- Delete user (with confirmation)
- Filter by role, status
- Search by username/email

### User Form
- Username (required, unique)
- Email (required, unique, validated)
- Password (required for new, optional for edit)
- Full Name (required)
- Role (dropdown: admin, engineer, viewer)
- Active status (checkbox)

### Audit Log Viewer
- Table with columns: Timestamp, User, Query, Answer Preview, Confidence, Status
- Filter by:
  - User (dropdown)
  - Date range (date picker)
  - Role (dropdown)
  - Refusal status (checkbox)
- Search by query text
- Export to CSV button
- Click row to view full details
- Pagination

### Statistics Dashboard
- **User Stats**: Total users, Active users, Users by role
- **Document Stats**: Total documents, Documents by mission, Documents by type
- **Query Stats**: Total queries, Average confidence, Refusal rate, Queries over time
- **Chunk Stats**: Total chunks, Average chunks per document
- Visual charts (bar, line, pie)
- Time range selector

### Access Control
- All pages require admin role
- Redirect non-admins
- Show admin badge in navigation

## Success Criteria
- [ ] User list displays
- [ ] User creation works
- [ ] User editing works
- [ ] Role assignment works
- [ ] Audit logs display
- [ ] Filtering works
- [ ] Export works
- [ ] Statistics display correctly
- [ ] Charts render

## Notes
- Add user activity timeline
- Support bulk user operations
- Add user import/export
- Implement audit log retention settings
- Add real-time statistics updates
- Support custom date ranges
