## Dockerfile for FastAPI Secure Build Info API
#
# This Dockerfile builds a minimal container for the FastAPI service.
# It leverages a slim Python base image to reduce attack surface and size.
# The image exposes port 8000 and runs the app with uvicorn.

FROM python:3.11-slim AS base

# Install system dependencies and create a non‑root user
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install dependencies
WORKDIR /app
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY app /app/app

EXPOSE 8000

# Default environment variables; these can be overridden at runtime
ENV APP_VERSION=0.1.0 \
    BUILD_ID=local \
    DEPLOYMENT_ENV=prod \
    SECURITY_STATUS=unknown \
    BUILD_TIMESTAMP=""

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
