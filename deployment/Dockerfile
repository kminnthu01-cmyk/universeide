
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

# Run
CMD ["uv", "run", "python", "-c", "from universe_ide import cosmos; print(cosmos(1000))"]
