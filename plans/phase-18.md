# Phase 18: Authentication UI

## Overview
Build the authentication user interface: login page, token management, authentication context, and protected route middleware. This phase enables users to authenticate through the frontend.

## Dependencies
- Phase 17: Next.js setup must be complete
- Phase 5: Authentication API must be working

## Deliverables

### 1. Login Page
- Login form with validation
- Error handling
- Loading states

### 2. Authentication Context
- Auth context provider
- Token storage
- User state management

### 3. Protected Routes
- Route protection middleware
- Redirect to login
- Role-based route access

## Files to Create

### `frontend/app/login/page.tsx`
```tsx
export default function LoginPage() {
  // Login form
  // Form validation
  // API call to /api/auth/login
  // Token storage
  // Redirect to dashboard
}
```

### `frontend/components/auth/LoginForm.tsx`
Login form component with validation

### `frontend/contexts/AuthContext.tsx`
```tsx
interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
  isLoading: boolean
}
```

### `frontend/middleware.ts`
Next.js middleware for route protection

### `frontend/lib/auth.ts`
Authentication utilities:
- Token storage (localStorage or httpOnly cookies)
- Token refresh
- Token validation

## Implementation Details

### Login Flow
1. User enters credentials
2. Validate form (client-side)
3. Call `/api/auth/login`
4. Store tokens securely
5. Update auth context
6. Redirect to dashboard

### Token Storage
- Option 1: localStorage (easier, less secure)
- Option 2: httpOnly cookies (more secure, requires backend support)
- Store access token and refresh token
- Implement token refresh logic

### Auth Context
- Provide user state globally
- Handle login/logout
- Auto-refresh tokens
- Check authentication status

### Protected Routes
- Check authentication in middleware
- Redirect to login if not authenticated
- Check roles for admin routes
- Preserve intended destination

### Error Handling
- Invalid credentials → Show error message
- Network errors → Show connection error
- Token expiry → Auto-refresh or redirect
- Clear error messages

## Success Criteria
- [ ] Login page renders correctly
- [ ] Form validation works
- [ ] Login API call succeeds
- [ ] Tokens are stored securely
- [ ] Auth context updates
- [ ] Protected routes work
- [ ] Logout functionality works

## Notes
- Use React Hook Form for forms
- Add loading spinners
- Implement "Remember me" (optional)
- Add password visibility toggle
- Support password reset link
- Add session timeout warning
