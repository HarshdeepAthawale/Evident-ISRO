# Phase 29: Docker Setup

## Overview
Create Docker configuration for containerized deployment. This phase enables easy deployment and development environment setup using Docker.

## Dependencies
- Phase 25: Backend-frontend integration must be complete

## Deliverables

### 1. Dockerfiles
- Backend Dockerfile
- Frontend Dockerfile
- Multi-stage builds for optimization

### 2. Docker Compose
- Complete docker-compose.yml
- PostgreSQL service
- Volume configurations
- Environment variables

### 3. Docker Configuration
- .dockerignore files
- Docker networking
- Health checks

## Files to Create

### `backend/Dockerfile`
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `frontend/Dockerfile`
```dockerfile
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./
CMD ["npm", "start"]
```

### `docker-compose.yml`
```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: evident
      POSTGRES_USER: evident
      POSTGRES_PASSWORD: ${DB_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://evident:${DB_PASSWORD}@postgres:5432/evident
    depends_on:
      - postgres
    volumes:
      - ./data:/app/data
  
  frontend:
    build: ./frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
    depends_on:
      - backend
```

### `backend/.dockerignore`
Ignore unnecessary files in Docker build

### `frontend/.dockerignore`
Ignore unnecessary files in Docker build

### `docker-compose.prod.yml`
Production docker-compose configuration

## Implementation Details

### Backend Dockerfile
- Use Python 3.10 slim image
- Install dependencies
- Copy application code
- Expose port 8000
- Set working directory
- Add health check

### Frontend Dockerfile
- Multi-stage build
- Build stage: Install and build
- Production stage: Copy built files
- Use Node.js Alpine for smaller size
- Expose port 3000

### Docker Compose Services
- **PostgreSQL**: Database service
- **Backend**: FastAPI application
- **Frontend**: Next.js application
- **Volumes**: Persistent data storage

### Volume Mounts
- `postgres_data`: Database data
- `./data/raw_docs`: Document storage
- `./data/vector_store`: Vector store

### Environment Variables
- Use `.env` file
- Set in docker-compose.yml
- Document all variables

### Health Checks
- Backend: `/health` endpoint
- Frontend: Root endpoint
- PostgreSQL: pg_isready

## Success Criteria
- [ ] Backend Dockerfile builds
- [ ] Frontend Dockerfile builds
- [ ] Docker Compose works
- [ ] All services start
- [ ] Services communicate
- [ ] Data persists
- [ ] Health checks work

## Notes
- Use multi-stage builds
- Optimize image sizes
- Use .dockerignore
- Add build caching
- Support development and production
- Document Docker commands
- Add docker-compose override for dev
