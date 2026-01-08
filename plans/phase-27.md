# Phase 27: Frontend Testing

## Overview
Write component tests, integration tests, and end-to-end tests for the frontend. This phase ensures the UI works correctly and prevents regressions.

## Dependencies
- Phase 25: Backend-frontend integration must be complete

## Deliverables

### 1. Component Tests
- React component tests
- UI interaction tests
- Form validation tests

### 2. Integration Tests
- Page flow tests
- API integration tests
- Authentication flow tests

### 3. End-to-End Tests
- Critical user flows
- Admin flows
- Error scenarios

## Files to Create

### `frontend/tests/` directory structure
```
tests/
├── setup.ts
├── utils/
│   ├── testUtils.tsx
│   └── mockApi.ts
├── components/
│   ├── LoginForm.test.tsx
│   ├── QueryInput.test.tsx
│   ├── QueryResult.test.tsx
│   └── DocumentList.test.tsx
├── pages/
│   ├── login.test.tsx
│   ├── query.test.tsx
│   └── dashboard.test.tsx
└── e2e/
    ├── auth.spec.ts
    ├── query.spec.ts
    └── admin.spec.ts
```

### `frontend/jest.config.js`
Jest configuration

### `frontend/.testing-library/`
Testing utilities

## Implementation Details

### Component Tests
Use React Testing Library:
- Test component rendering
- Test user interactions
- Test form submissions
- Test error states
- Test loading states

### Integration Tests
- Test page navigation
- Test API calls
- Test state management
- Test context providers

### End-to-End Tests
Use Playwright or Cypress:
- **Auth Flow**: Login → Dashboard
- **Query Flow**: Enter query → Submit → View results
- **Document Upload**: Upload → View in list
- **Admin Flow**: Manage users → View audit logs

### Mock API
- Mock all API endpoints
- Return realistic responses
- Simulate errors
- Test loading states

### Test Scenarios

**Login Tests:**
- Valid login
- Invalid credentials
- Network error
- Token storage

**Query Tests:**
- Submit query
- View results
- View sources
- Handle refusal
- Error handling

**Admin Tests:**
- User management
- Document management
- Audit log viewing
- Statistics display

## Success Criteria
- [ ] Component tests pass
- [ ] Integration tests pass
- [ ] E2E tests pass
- [ ] Test coverage is adequate
- [ ] Tests are maintainable
- [ ] Tests run in CI (future)

## Notes
- Use React Testing Library
- Use MSW for API mocking
- Use Playwright for E2E
- Add visual regression testing (future)
- Test accessibility
- Test responsive design
