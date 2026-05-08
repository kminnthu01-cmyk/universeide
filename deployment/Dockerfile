
FROM python:3.13-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy files
COPY . .

# Install deps
RUN uv sync

# Expose
EXPOSE 8080

# Run API server
CMD ["python", "universe_server.py"]
