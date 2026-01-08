# Phase 23: Admin - Document Management UI

## Overview
Build the admin document management interface for uploading, listing, editing, and deleting documents. This phase enables document administration through the UI.

## Dependencies
- Phase 19: Dashboard layout must be complete
- Phase 15: Document management API must be working

## Deliverables

### 1. Document List
- Display all documents
- Filter by mission, type
- Search functionality
- Pagination

### 2. Document Upload
- File upload interface
- Metadata form
- Upload progress
- Success/error handling

### 3. Document Management
- Edit metadata
- Delete documents
- View document details
- Permission management

## Files to Create

### `frontend/app/admin/documents/page.tsx`
Document management page

### `frontend/components/admin/DocumentList.tsx`
List of documents component

### `frontend/components/admin/DocumentUpload.tsx`
File upload component

### `frontend/components/admin/DocumentForm.tsx`
Metadata form component

### `frontend/components/admin/DocumentCard.tsx`
Individual document card

### `frontend/components/admin/DocumentModal.tsx`
Document details/edit modal

## Implementation Details

### Document List
- Table or card view
- Columns: Title, Mission, Type, Upload Date, Uploader, Actions
- Sortable columns
- Filter by mission, type, date
- Search by title

### Upload Interface
- Drag-and-drop file upload
- File browser button
- File validation (PDF only, size limit)
- Metadata form:
  - Title (required)
  - Mission (required)
  - Project (optional)
  - Document Type (optional)
- Upload progress bar
- Success notification

### Document Actions
- **View**: Show document details
- **Edit**: Update metadata
- **Delete**: Remove document (with confirmation)
- **Download**: Download original file
- **Permissions**: Manage access (future)

### Document Details
- Full metadata
- Upload information
- Chunk count
- Access permissions
- Query statistics (future)

### Access Control
- Show only for admin/engineer roles
- Hide delete for non-admins
- Filter documents by user's accessible missions

## Success Criteria
- [ ] Document list displays
- [ ] Upload works
- [ ] Metadata form works
- [ ] Edit functionality works
- [ ] Delete works with confirmation
- [ ] Filtering and search work
- [ ] Access control is enforced

## Notes
- Add bulk upload (future)
- Support document preview
- Add version history (future)
- Implement soft delete
- Add document analytics
- Support document tags
