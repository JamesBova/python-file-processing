FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr for real-time Docker logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies in a separate layer for Docker layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Run as non-root user (production security best practice)
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

CMD ["python", "-m", "src.main"]