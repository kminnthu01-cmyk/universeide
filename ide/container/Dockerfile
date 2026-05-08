# Universe IDE - Multi-stage Dockerfile
# Production-ready container

FROM python:3.13-slim AS base
WORKDIR /app

# Install system deps
RUN apt-get update && apt-get install -y \
    git curl wget build-essential \
    && rm -rf /var/lib/apt/lists/*

# Python
FROM base AS python-deps
COPY pyproject.toml uv.lock ./
RUN pip install uv && uv sync

# Application
FROM python-deps AS app
COPY universe/ ./universe/
COPY ide/ ./ide/

# Ports
EXPOSE 8080

# Run
ENV PYTHONUNBUFFERED=1
ENV OPENHANDS_SUPPRESS_BANNER=1

CMD ["python", "-m", "uvicorn", "ide.backend.api.main:app", "--host", "0.0.0.0", "--port", "8080"]