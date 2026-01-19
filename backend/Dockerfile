# Start from a lightweight Python 3.13 image (Critical for ARM64 stability)
FROM python:3.13-slim

WORKDIR /app

# Install system dependencies (OpenBLAS is key for ARM64 math stability)
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    curl \
    libopenblas-dev \
    --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install uv (Package Manager)
RUN curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv \
    && mv /root/.local/bin/uvx /usr/local/bin/uvx

# Copy dependency files
COPY pyproject.toml .

# Install dependencies using uv
# --system installs into the system python environment, avoiding venv complexity in Docker
RUN uv pip install -r pyproject.toml --system && \
    uv pip install pytest pytest-asyncio --system

ENV PYTHONPATH=/app

# Copy application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
