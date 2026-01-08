# Phase 6: Role-Based Access Control (RBAC)

## Overview
Implement comprehensive role-based access control with middleware, decorators, and permission checking. This phase enforces authorization at the API level and supports role-based document access.

## Dependencies
- Phase 5: Authentication endpoints must be working

## Deliverables

### 1. RBAC Middleware
- Role checking middleware
- Permission decorators
- Route protection utilities

### 2. Permission System
- Role definitions (admin, engineer, viewer)
- Permission checking logic
- Mission/project scoping

### 3. Admin Endpoints
- Role management endpoints
- Permission assignment

## Files to Create

### `backend/auth/permissions.py`
```python
from functools import wraps
from typing import List

def require_roles(*roles: str)
def require_permission(permission: str)
def require_admin()
def require_engineer_or_admin()
def check_mission_access(mission: str, user: User) -> bool
```

### `backend/auth/middleware.py`
```python
async def role_check_middleware(request: Request, call_next)
async def permission_middleware(request: Request, call_next)
```

### `backend/core/rbac.py`
```python
class RoleChecker:
    def has_role(user: User, role: str) -> bool
    def has_any_role(user: User, roles: List[str]) -> bool
    def has_permission(user: User, permission: str) -> bool
    def can_access_mission(user: User, mission: str) -> bool
```

### `backend/auth/routes.py` (update)
Add admin endpoints:
```python
@router.get("/admin/roles")
@require_admin
async def list_roles() -> List[Role]

@router.post("/admin/users/{user_id}/role")
@require_admin
async def assign_role(user_id: str, role: str)
```

## Implementation Details

### Role Hierarchy
- `admin`: Full access, user management, all documents
- `engineer`: Read/write access to assigned missions
- `viewer`: Read-only access to assigned missions

### Permission Decorators
```python
@router.get("/api/documents")
@require_roles("admin", "engineer", "viewer")
async def list_documents():
    pass

@router.post("/api/documents")
@require_roles("admin", "engineer")
async def upload_document():
    pass

@router.delete("/api/documents/{id}")
@require_admin
async def delete_document():
    pass
```

### Mission Scoping
- Users can be assigned to specific missions
- Documents belong to missions
- Queries filter by user's accessible missions

### Permission Checks
- Document-level: Check user's role and mission access
- Endpoint-level: Decorator-based checks
- Resource-level: Inline checks for fine-grained control

## Success Criteria
- [ ] Role decorators work correctly
- [ ] Middleware enforces permissions
- [ ] Admin-only endpoints are protected
- [ ] Mission scoping works
- [ ] Permission checks are consistent
- [ ] Error messages are clear (403 Forbidden)

## Notes
- Always check permissions at both endpoint and resource level
- Log all permission denials
- Consider caching role checks for performance
- Support for custom roles in future
- Document all permission requirements
