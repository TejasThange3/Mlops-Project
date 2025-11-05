# Docker Setup Guide

## Prerequisites

- **Docker Desktop** installed (Windows/Mac) or Docker Engine (Linux)
- **Docker Compose** (usually included with Docker Desktop)

## Building the Docker Image

### Build the image locally:

```bash
docker build -t mlops-water-potability:latest .
```

### Check built images:

```bash
docker images | grep mlops
```

## Running with Docker Compose

### Start all services:

```bash
docker-compose up -d
```

This will start:

- **FastAPI Application** (Port 8000)
- **PostgreSQL Database** (Port 5432, internal only)
- **Redis Cache** (Port 6379, internal only)

### View logs:

```bash
docker-compose logs -f app
```

### Stop all services:

```bash
docker-compose down
```

### Remove volumes (clean slate):

```bash
docker-compose down -v
```

## Accessing the Application

Once running, access:

- **Web UI**: http://localhost:8000/
- **API Docs**: http://localhost:8000/docs (Swagger UI)
- **ReDoc**: http://localhost:8000/redoc

## Environment Variables

You can customize the application by creating a `.env` file:

```env
API_HOST=0.0.0.0
API_PORT=8000
MODEL_PATH=/app/models/model.joblib
SCALER_PATH=/app/models/scaler.joblib
DVC_NO_ANALYTICS=1
```

Then use it with docker-compose:

```bash
docker-compose --env-file .env up -d
```

## Pushing to Docker Registry

### Tag the image:

```bash
docker tag mlops-water-potability:latest your-dockerhub-username/mlops-water-potability:latest
```

### Login to Docker Hub:

```bash
docker login
```

### Push the image:

```bash
docker push your-dockerhub-username/mlops-water-potability:latest
```

## Pulling from Registry

```bash
docker pull your-dockerhub-username/mlops-water-potability:latest
docker run -p 8000:8000 your-dockerhub-username/mlops-water-potability:latest
```

## Troubleshooting

### Container won't start

```bash
docker-compose logs app
```

### Port already in use

Change the port in `docker-compose.yml`:

```yaml
ports:
  - "8001:8000" # Use 8001 instead of 8000
```

### Permission issues on Linux

```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Clear Docker resources

```bash
docker system prune -a --volumes
```

## Development Mode

For development with auto-reload:

Create `docker-compose.dev.yml`:

```yaml
version: "3.8"
services:
  app:
    build:
      context: .
      dockerfile: Dockerfile
    volumes:
      - .:/app
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Run:

```bash
docker-compose -f docker-compose.dev.yml up
```

## Health Check

The application includes a health check endpoint:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{ "status": "healthy" }
```

## Performance Tuning

### Increase memory limit

```yaml
services:
  app:
    deploy:
      resources:
        limits:
          memory: 2G
```

### Use multi-stage builds

The provided Dockerfile already uses multi-stage builds for smaller final image size.

### Monitor resource usage

```bash
docker stats mlops-water-potability-app
```
