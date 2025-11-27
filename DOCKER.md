# Docker Deployment Guide

This guide explains how to run the Content Journey Finder application using Docker.

## Quick Start

The simplest way to run the application is using Docker Compose:

```bash
docker-compose up --build
```

The application will be available at `http://localhost:8000`

## Docker Setup Details

### Prerequisites

- Docker 20.10 or higher
- Docker Compose v2.0 or higher

### Building the Image

Build the Docker image manually:

```bash
docker build -t content-journey-finder:latest .
```

### Running the Container

Run the container from the built image:

```bash
docker run -p 8000:8000 content-journey-finder:latest
```

With environment variables:

```bash
docker run -p 8000:8000 \
  -e PORT=8000 \
  content-journey-finder:latest
```

### Docker Compose

The `docker-compose.yml` file provides a complete setup:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    volumes:
      - ./app:/app/app  # Mount for development
    restart: unless-stopped
```

#### Development Mode

For development with hot-reload:

```bash
docker-compose up
```

Changes to the `app/` directory will be reflected immediately.

#### Production Mode

For production, remove the volumes section from docker-compose.yml or create a separate `docker-compose.prod.yml`:

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
    restart: always
```

Run with:

```bash
docker-compose -f docker-compose.prod.yml up -d
```

## Environment Variables

Configure the application using environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `PORT` | Application port | `8000` |
| `QDRANT_HOST` | Qdrant server host | `localhost` |
| `QDRANT_PORT` | Qdrant server port | `6333` |
| `TRANSFORMERS_CACHE` | Cache directory for ML models | None |

Example `.env` file:

```bash
PORT=8000
QDRANT_HOST=localhost
QDRANT_PORT=6333
TRANSFORMERS_CACHE=/app/.cache/huggingface
```

Use with Docker Compose:

```bash
docker-compose --env-file .env up
```

## Health Checks

The container includes a health check that verifies the application is running:

```bash
docker ps  # Check HEALTH status column
```

Manual health check:

```bash
curl http://localhost:8000/health
```

Expected response:

```json
{"status": "healthy"}
```

## Logs

View application logs:

```bash
docker-compose logs -f
```

Or for a specific container:

```bash
docker logs -f <container_name>
```

## Troubleshooting

### Container won't start

1. Check if port 8000 is already in use:
   ```bash
   lsof -i :8000  # Linux/Mac
   netstat -ano | findstr :8000  # Windows
   ```

2. Check Docker logs:
   ```bash
   docker-compose logs
   ```

### Model download issues

If the application can't download ML models from HuggingFace:

1. Pre-download models outside Docker
2. Mount the model cache directory:
   ```yaml
   volumes:
     - ~/.cache/huggingface:/root/.cache/huggingface
   ```

### Permission issues

If you encounter permission errors:

```bash
sudo docker-compose up
```

Or add your user to the docker group:

```bash
sudo usermod -aG docker $USER
```

Log out and back in for changes to take effect.

## Performance Optimization

### Multi-stage builds

For smaller images, use multi-stage builds (already implemented in Dockerfile).

### Resource limits

Limit container resources in docker-compose.yml:

```yaml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
```

### Caching

Mount a cache directory for faster startups:

```yaml
volumes:
  - model-cache:/root/.cache/huggingface

volumes:
  model-cache:
```

## Scaling

Run multiple instances with Docker Compose:

```bash
docker-compose up --scale web=3
```

Use a load balancer (nginx, traefik) to distribute traffic.

## Security

### Non-root user

The Dockerfile runs as root by default. For production, add a non-root user:

```dockerfile
RUN useradd -m -u 1000 appuser
USER appuser
```

### Network isolation

Use Docker networks to isolate services:

```yaml
networks:
  frontend:
  backend:

services:
  web:
    networks:
      - frontend
      - backend
```

## Deployment

### Deploy to Docker Hub

```bash
docker tag content-journey-finder:latest yourusername/content-journey-finder:latest
docker push yourusername/content-journey-finder:latest
```

### Deploy to Cloud Platforms

#### AWS ECS

Use the Docker image with AWS ECS task definitions.

#### Google Cloud Run

```bash
gcloud run deploy content-journey-finder \
  --image gcr.io/PROJECT_ID/content-journey-finder \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated
```

#### Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name content-journey-finder \
  --image content-journey-finder:latest \
  --ports 8000
```

## Maintenance

### Update the container

```bash
docker-compose pull
docker-compose up -d
```

### Clean up

Remove stopped containers:

```bash
docker-compose down
```

Remove volumes:

```bash
docker-compose down -v
```

Remove images:

```bash
docker rmi content-journey-finder:latest
```

### Backup

Backup application data and logs:

```bash
docker-compose exec web tar czf /tmp/backup.tar.gz /app/data
docker cp $(docker-compose ps -q web):/tmp/backup.tar.gz ./backup.tar.gz
```
