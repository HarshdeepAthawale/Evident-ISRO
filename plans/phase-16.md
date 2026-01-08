# Phase 16: Admin & Audit API

## Overview
Create admin API endpoints for user management, audit log viewing, system statistics, and role management. This phase enables administrative functions via API.

## Dependencies
- Phase 6: RBAC must be complete

## Deliverables

### 1. User Management Endpoints
- GET `/api/admin/users` - List users
- GET `/api/admin/users/{id}` - Get user details
- PUT `/api/admin/users/{id}` - Update user
- DELETE `/api/admin/users/{id}` - Delete user
- POST `/api/admin/users/{id}/role` - Assign role

### 2. Audit Log Endpoints
- GET `/api/admin/audit-logs` - List audit logs
- GET `/api/admin/audit-logs/{id}` - Get audit log details
- GET `/api/admin/audit-logs/export` - Export audit logs

### 3. System Statistics
- GET `/api/admin/stats` - System statistics
- GET `/api/admin/stats/users` - User statistics
- GET `/api/admin/stats/documents` - Document statistics
- GET `/api/admin/stats/queries` - Query statistics

### 4. Role Management
- GET `/api/admin/roles` - List roles
- POST `/api/admin/roles` - Create role
- PUT `/api/admin/roles/{id}` - Update role

## Files to Create

### `backend/api/admin.py`
```python
@router.get("/admin/users")
@require_admin
async def list_users(skip: int = 0, limit: int = 100) -> List[UserResponse]

@router.get("/admin/users/{user_id}")
@require_admin
async def get_user(user_id: str) -> UserResponse

@router.put("/admin/users/{user_id}")
@require_admin
async def update_user(user_id: str, user_data: UserUpdate) -> UserResponse

@router.delete("/admin/users/{user_id}")
@require_admin
async def delete_user(user_id: str) -> DeleteResponse

@router.post("/admin/users/{user_id}/role")
@require_admin
async def assign_role(user_id: str, role: str) -> UserResponse

@router.get("/admin/audit-logs")
@require_admin
async def list_audit_logs(
    user_id: str = None,
    start_date: datetime = None,
    end_date: datetime = None,
    skip: int = 0,
    limit: int = 100
) -> List[AuditLogResponse]

@router.get("/admin/stats")
@require_admin
async def get_system_stats() -> SystemStatsResponse
```

### `backend/api/admin_schemas.py`
```python
class UserResponse(BaseModel):
    id: str
    username: str
    email: str
    full_name: str
    role: str
    is_active: bool
    created_at: datetime

class AuditLogResponse(BaseModel):
    id: str
    user_id: str
    username: str
    query_text: str
    answer: Optional[str]
    confidence: Optional[float]
    refusal_reason: Optional[str]
    timestamp: datetime
    response_time_ms: int

class SystemStatsResponse(BaseModel):
    total_users: int
    total_documents: int
    total_queries: int
    total_chunks: int
    average_confidence: float
    refusal_rate: float
```

## Implementation Details

### User Management
- List all users with pagination
- Filter by role, active status
- Update user details (except password)
- Deactivate users (soft delete)
- Assign/change roles
- View user activity

### Audit Log Access
- Filter by user, date range
- Search by query text
- Export to CSV/JSON
- View detailed log entries
- Statistics on queries

### System Statistics
- Total counts (users, documents, queries)
- Average confidence scores
- Refusal rate
- Query volume over time
- Most active users
- Most queried documents

### Role Management
- List all roles
- Create custom roles (future)
- Assign permissions to roles
- View role assignments

### Access Control
- All endpoints require admin role
- Log all admin actions
- Support audit of admin actions

## Success Criteria
- [ ] Users can be listed and managed
- [ ] Audit logs are accessible
- [ ] Statistics are calculated correctly
- [ ] Roles can be managed
- [ ] All endpoints require admin
- [ ] Filtering and pagination work
- [ ] Export functionality works

## Notes
- Add user activity tracking
- Support bulk operations (future)
- Add data export formats
- Implement audit log retention
- Add real-time statistics (future)
- Support role templates
