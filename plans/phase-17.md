# Phase 17: Next.js Setup & Configuration

## Overview
Set up the Next.js frontend application with TypeScript, Tailwind CSS, and project structure. This phase establishes the frontend foundation.

## Dependencies
None - Frontend can be developed in parallel

## Deliverables

### 1. Next.js Application
- Initialize Next.js 14+ with App Router
- TypeScript configuration
- Tailwind CSS setup

### 2. Project Structure
- App directory structure
- Components directory
- Utilities and lib directories

### 3. Configuration
- Environment variables
- API client setup
- Type definitions

## Files to Create

### `frontend/package.json`
```json
{
  "name": "evident-frontend",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "react-dom": "^18.0.0",
    "typescript": "^5.0.0",
    "tailwindcss": "^3.3.0",
    "axios": "^1.6.0"
  }
}
```

### `frontend/tsconfig.json`
TypeScript configuration

### `frontend/tailwind.config.js`
Tailwind CSS configuration

### `frontend/next.config.js`
Next.js configuration

### `frontend/app/layout.tsx`
Root layout component

### `frontend/lib/api.ts`
API client utilities

### `frontend/lib/types.ts`
TypeScript type definitions

### `frontend/.env.example`
Environment variables template

## Implementation Details

### Directory Structure
```
frontend/
├── app/
│   ├── layout.tsx
│   ├── page.tsx
│   ├── login/
│   ├── dashboard/
│   ├── query/
│   └── admin/
├── components/
│   ├── ui/
│   └── common/
├── lib/
│   ├── api.ts
│   ├── types.ts
│   └── utils.ts
└── styles/
    └── globals.css
```

### API Client
- Axios instance with base URL
- Request interceptors (add auth token)
- Response interceptors (handle errors)
- Type-safe API calls

### Environment Variables
- `NEXT_PUBLIC_API_URL`: Backend API URL
- `NEXT_PUBLIC_APP_NAME`: Application name

### Type Definitions
- User types
- Query types
- Document types
- API response types

### Styling
- Tailwind CSS for styling
- Custom color scheme
- Responsive design utilities
- Dark mode support (optional)

## Success Criteria
- [ ] Next.js app runs
- [ ] TypeScript compiles
- [ ] Tailwind CSS works
- [ ] Project structure is set up
- [ ] API client is configured
- [ ] Environment variables load

## Notes
- Use App Router (not Pages Router)
- Enable strict TypeScript
- Set up ESLint and Prettier
- Configure path aliases
- Add error boundaries
- Set up testing framework (future)
