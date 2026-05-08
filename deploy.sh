#!/bin/bash
# Universe IDE - One-Click Docker Deployment

set -e

echo "🪐 Universe IDE - Docker Deployment"
echo "=================================="

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Installing..."
    # Install Docker based on OS
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew install docker
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        curl -fsSL https://get.docker.com | sh
    fi
fi

echo "✅ Docker found"

# Build image
echo "📦 Building Universe IDE..."
docker build -t universe-ide:latest -f deployment/Dockerfile .

echo "✅ Image built: universe-ide:latest"

# Run container
echo "🚀 Starting Universe IDE..."
docker run -d --name universe-ide -p 8080:8080 universe-ide:latest

echo ""
echo "✅ Universe IDE running!"
echo ""
echo "🌐 Open: http://localhost:8080"
echo "📝 Docs: https://github.com/kminnthu01-cmyk/universeide"
echo ""
echo "Commands:"
echo "  docker stop universe-ide   # Stop"
echo "  docker start universe-ide  # Start"
echo "  docker logs -f universe-ide  # View logs"