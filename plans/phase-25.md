# Phase 25: Backend-Frontend Integration

## Overview
Complete the integration between backend and frontend, ensuring all API endpoints are connected, error handling is consistent, and loading states are properly managed. This phase makes the full-stack application functional.

## Dependencies
- Phase 14: Query API must be complete
- Phase 21: Results display must be complete

## Deliverables

### 1. API Integration
- Connect all frontend components to backend APIs
- Handle authentication tokens
- Implement error handling
- Add loading states

### 2. Error Handling
- Consistent error messages
- Network error handling
- Validation error display
- Timeout handling

### 3. End-to-End Testing
- Test complete query flow
- Test authentication flow
- Test admin functions
- Verify error scenarios

## Files to Update/Create

### `frontend/lib/api.ts` (update)
Complete API client with all endpoints:
- Auth endpoints
- Query endpoint
- Document endpoints
- Admin endpoints

### `frontend/lib/errorHandler.ts`
Centralized error handling

### `frontend/components/common/ErrorBoundary.tsx`
React error boundary component

### `frontend/components/common/LoadingSpinner.tsx`
Loading spinner component

### `frontend/hooks/useApi.ts`
Custom hook for API calls with error handling

## Implementation Details

### API Client Updates
- Add all endpoint methods
- Implement request interceptors (add token)
- Implement response interceptors (handle errors, refresh token)
- Add retry logic for failed requests
- Add request cancellation

### Error Handling Strategy
- **Network Errors**: Show "Connection failed" message
- **401 Unauthorized**: Redirect to login, clear tokens
- **403 Forbidden**: Show "Access denied" message
- **404 Not Found**: Show "Resource not found"
- **500 Server Error**: Show "Server error, please try again"
- **Validation Errors**: Show field-specific errors

### Loading States
- Show spinner during API calls
- Disable forms during submission
- Show skeleton loaders for lists
- Add progress indicators for uploads

### Token Management
- Auto-refresh expired tokens
- Handle token refresh failures
- Clear tokens on 401
- Store tokens securely

### End-to-End Flow Testing
1. **Login Flow**: Login → Dashboard → Query → Results
2. **Query Flow**: Enter query → Submit → View results → Check sources
3. **Document Upload**: Upload → View in list → Edit → Delete
4. **Admin Flow**: View users → Edit user → View audit logs → View stats

## Success Criteria
- [ ] All API endpoints are connected
- [ ] Authentication flow works end-to-end
- [ ] Query flow works completely
- [ ] Error handling is consistent
- [ ] Loading states work
- [ ] Token refresh works
- [ ] All user flows are functional

## Notes
- Add request/response logging (dev only)
- Implement request queuing (future)
- Add offline support detection
- Consider request caching
- Add API response time monitoring
- Support request cancellation
