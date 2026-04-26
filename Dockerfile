# ── Stage 1: Builder ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install node and npm
RUN apt-get update && apt-get install -y nodejs npm && rm -rf /var/lib/apt/lists/*

# Install uv for fast dependency resolution
RUN pip install --no-cache-dir uv==0.4.18

# Copy dependency files first (layer caching)
COPY pyproject.toml ./
COPY uv.lock* ./
COPY package.json package-lock.json ./

# Install Python dependencies into a virtual environment
RUN uv venv /app/.venv && \
    uv pip install --python /app/.venv/bin/python \
        fastapi>=0.110.0 \
        uvicorn[standard]>=0.29.0 \
        pydantic>=2.0.0 \
        openai>=1.0.0 \
        httpx>=0.27.0 \
        openenv-core>=0.2.0

# Install frontend dependencies and build
RUN npm ci && npm run build

# ── Stage 2: Runtime ─────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

# Non-root user for security
RUN useradd --create-home --shell /bin/bash appuser

WORKDIR /app

# Copy virtual environment from builder
COPY --from=builder /app/.venv /app/.venv

# Copy application code
COPY --chown=appuser:appuser . .

# Copy built frontend
COPY --from=builder --chown=appuser:appuser /app/dist ./dist

# Make sure server package dir exists
RUN mkdir -p server && \
    touch server/__init__.py

# Activate venv
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app"
ENV PYTHONUNBUFFERED=1
ENV PORT=7860

# Switch to non-root user
USER appuser

EXPOSE 7860

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:7860/health')" || exit 1

# Start the FastAPI server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860", "--workers", "1"]
