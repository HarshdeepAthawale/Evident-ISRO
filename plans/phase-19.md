# Phase 19: Dashboard Layout

## Overview
Create the main dashboard layout with navigation sidebar, user profile display, role-based menu, and responsive design. This phase establishes the application shell.

## Dependencies
- Phase 18: Authentication UI must be complete

## Deliverables

### 1. Dashboard Layout
- Main layout component
- Navigation sidebar
- Header with user info
- Content area

### 2. Navigation
- Role-based menu items
- Active route highlighting
- Collapsible sidebar

### 3. User Profile
- Display user name and role
- Logout button
- User settings (future)

## Files to Create

### `frontend/app/dashboard/layout.tsx`
Dashboard layout with sidebar and header

### `frontend/components/layout/Sidebar.tsx`
Navigation sidebar component

### `frontend/components/layout/Header.tsx`
Header with user profile

### `frontend/components/layout/NavItem.tsx`
Navigation item component

### `frontend/app/dashboard/page.tsx`
Dashboard home page

## Implementation Details

### Layout Structure
```
┌─────────────────────────────────┐
│ Header (User Profile, Logout)   │
├──────────┬──────────────────────┤
│          │                      │
│ Sidebar  │   Main Content      │
│ (Nav)    │   Area              │
│          │                      │
└──────────┴──────────────────────┘
```

### Navigation Items
**All Users:**
- Dashboard (home)
- Query Workspace
- Query History

**Engineers & Admins:**
- Document Management

**Admins Only:**
- User Management
- Audit Logs
- System Statistics

### Sidebar Features
- Collapsible on mobile
- Active route highlighting
- Role-based item visibility
- Icons for each section

### User Profile Display
- User full name
- Role badge (Admin/Engineer/Viewer)
- Logout button
- Dropdown menu (future: settings, profile)

### Responsive Design
- Desktop: Sidebar always visible
- Tablet: Collapsible sidebar
- Mobile: Hamburger menu

## Success Criteria
- [ ] Layout renders correctly
- [ ] Sidebar navigation works
- [ ] Role-based menu items show/hide
- [ ] User profile displays
- [ ] Logout works
- [ ] Responsive design works
- [ ] Active route is highlighted

## Notes
- Use Tailwind for styling
- Add smooth transitions
- Support keyboard navigation
- Add tooltips for icons
- Consider dark mode
- Add loading states
