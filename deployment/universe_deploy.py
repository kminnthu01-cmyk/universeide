#!/usr/bin/env python3
"""
Universe IDE - Docker Integration

Docker deployment for Universe IDE.
"""

import os
import subprocess


# ============================================================================
# DOCKERFILE
# ============================================================================

DOCKERFILE = '''
FROM python:3.11-slim

WORKDIR /workspace

# Install system deps
RUN apt-get update && apt-get install -y \\
    git curl docker.io \\
    && rm -rf /var/lib/apt/lists/*

# Install Python deps
COPY pyproject.toml .
RUN pip install --no-cache-dir -e .

# Copy application
COPY . .

# Expose port
EXPOSE 8080

# Run command
CMD ["python", "-m", "universe_ide", "serve"]
'''


# ============================================================================
# DOCKER COMPOSE
# ============================================================================

DOCKER_COMPOSE = '''
version: "3.8"

services:
  universe-ide:
    build: .
    ports:
      - "8080:8080"
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./workspace:/workspace
    deploy:
      resources:
        limits:
          cpus: "4"
          memory: 8G
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]

  universe-worker:
    build: .
    command: ["python", "-m", "universe_ide", "worker"]
    environment:
      - ANTHROPIC_API_KEY=${ANTHROPIC_API_KEY}
    deploy:
      replicas: 3
      resources:
        limits:
          cpus: "2"
          memory: 4G
'''


# ============================================================================
# KUBERNETES
# ============================================================================

KUBERNETES = '''
apiVersion: apps/v1
kind: Deployment
metadata:
  name: universe-ide
  labels:
    app: universe-ide
spec:
  replicas: 3
  selector:
    matchLabels:
      app: universe-ide
  template:
    metadata:
      labels:
        app: universe-ide
    spec:
      containers:
      - name: universe
        image: universe-ide:latest
        ports:
        - containerPort: 8080
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: universe-secrets
              key: api-key
        resources:
          limits:
            cpu: "4"
            memory: 8Gi
          requests:
            cpu: "2"
            memory: 4Gi
        livenessProbe:
          httpGet:
            path: /api/health
            port: 8080
          initialDelaySeconds: 30
        readinessProbe:
          httpGet:
            path: /api/health
            port: 8080
          initialDelaySeconds: 10
---
apiVersion: v1
kind: Service
metadata:
  name: universe-ide
spec:
  selector:
    app: universe-ide
  ports:
  - port: 80
    targetPort: 8080
  type: LoadBalancer
'''


# ============================================================================
# HELM CHART
# ============================================================================

HELM_VALUES = '''
replicaCount: 3

image:
  repository: universe-ide
  tag: latest
  pullPolicy: IfNotPresent

service:
  type: LoadBalancer
  port: 80
  targetPort: 8080

resources:
  limits:
    cpu: 4
    memory: 8Gi
  requests:
    cpu: 2
    memory: 4Gi

autoscaling:
  enabled: true
  minReplicas: 2
  maxReplicas: 10
  targetCPUUtilizationPercentage: 70

config:
  model: claude-sonnet-4-20250505
  max_agents: 1000
'''


def write_deployment_files():
    """Write deployment files"""
    with open("deployment/Dockerfile", "w") as f:
        f.write(DOCKERFILE)
        
    with open("deployment/docker-compose.yml", "w") as f:
        f.write(DOCKER_COMPOSE)
        
    with open("deployment/kubernetes.yml", "w") as f:
        f.write(KUBERNETES)
        
    with open("deployment/helm/values.yaml", "w") as f:
        f.write(HELM_VALUES)
        
    print("✓ Deployment files written")


if __name__ == "__main__":
    write_deployment_files()