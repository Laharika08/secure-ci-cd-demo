"""FastAPI Secure Build Info API.

This module defines a minimal FastAPI application that exposes two endpoints:

* `/` – health check endpoint returning a simple status JSON.  This endpoint is
  useful for Kubernetes liveness and readiness probes.
* `/build-info` – returns build metadata such as version, build ID,
  environment, security validation status and build timestamp.  Values are
  populated from environment variables to allow the CI/CD pipeline to inject
  metadata at build or deployment time.
"""

import os
from datetime import datetime
from fastapi import FastAPI

app = FastAPI(title="FastAPI Secure Build Info API")


@app.get("/")
def health_check() -> dict[str, str]:
    """Return a basic health status used for readiness probes."""
    return {"status": "ok"}


@app.get("/build-info")
def build_info() -> dict[str, str]:
    """Return build metadata for the current deployment.

    The CI/CD pipeline can set the following environment variables to
    propagate build information into the running container:

    * **APP_VERSION** – semantic version of the application (default: `0.1.0`).
    * **BUILD_ID** – unique identifier for the build (e.g. commit SHA).
    * **DEPLOYMENT_ENV** – deployment environment (e.g. `dev`, `staging`, `prod`).
    * **SECURITY_STATUS** – indicates whether security validations passed (e.g. `pass` or `fail`).
    * **BUILD_TIMESTAMP** – ISO8601 timestamp of when the build was created.
    """
    return {
        "version": os.getenv("APP_VERSION", "0.1.0"),
        "build_id": os.getenv("BUILD_ID", "unknown"),
        "environment": os.getenv("DEPLOYMENT_ENV", "dev"),
        "security_validation": os.getenv("SECURITY_STATUS", "unknown"),
        "build_timestamp": os.getenv("BUILD_TIMESTAMP", datetime.utcnow().isoformat()),
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
