# Secure CI/CD Pipeline Project

This repository demonstrates a complete secure CI/CD pipeline for a lightweight Python service.  The pipeline automatically enforces security gates, signs container images, and deploys the application to Kubernetes.  This folder contains the application source code, deployment configuration, policy rules and instructions for running a live demo.

## Repository structure

| Path | Purpose |
| --- | --- |
| `app/main.py` | FastAPI service exposing health and build‑info endpoints. |
| `requirements.txt` | Python dependencies for the FastAPI application. |
| `Dockerfile` | Container build instructions for the FastAPI service. |
| `policy/latest-tag.rego` | OPA/Conftest policy that blocks Kubernetes workloads using the `:latest` image tag.  Conftest will fail if the policy denies the manifest.  `deny` rules cause Conftest to exit with a non‑zero code【71470937592858†L71-L87】. |
| `config/deployment.yaml` | Sample Kubernetes deployment and service manifest for the FastAPI application. |
| `demo_instructions.md` | Step‑by‑step guide to run the pipeline and demonstrate the secure CI/CD workflow. |

## Application overview

The FastAPI Secure Build Info API is designed to demonstrate the secure pipeline.  It is built with Python and FastAPI and containerized using Docker.  When deployed, it exposes two core endpoints:

* `/` – Health check endpoint that returns a simple status.  This can be used by Kubernetes liveness/readiness probes.
* `/build-info` – Returns metadata about the build, including the application version, build ID, deployment environment, security validation status and build timestamp.  These values are read from environment variables at runtime and allow the pipeline to propagate build metadata into the running service.

For additional context on Conftest policies and how they are evaluated, see the official documentation which explains that policies should be placed in a `policy` directory and that `deny` rules produce failures during evaluation【71470937592858†L71-L87】.

## Requirements

* Docker (≥20.10) to build and run the container locally.
* kubectl configured to point at a Kubernetes cluster for deployment testing.
* Python 3.10+ if you wish to run the service locally without Docker.
* Conftest (optional) if you want to run the policy tests manually.

## Getting started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the service locally**

   ```bash
   export APP_VERSION=0.1.0
   export BUILD_ID=local
   export DEPLOYMENT_ENV=dev
   export SECURITY_STATUS=pass
   export BUILD_TIMESTAMP=$(date -Iseconds)
   uvicorn app.main:app --reload --port 8000
   ```

3. **Build and run the container**

   ```bash
   docker build -t fastapi-secure-demo:0.1.0 .
   docker run --rm -p 8000:8000 \
     -e APP_VERSION=0.1.0 \
     -e BUILD_ID=$(git rev-parse --short HEAD) \
     -e DEPLOYMENT_ENV=local \
     -e SECURITY_STATUS=pass \
     -e BUILD_TIMESTAMP=$(date -Iseconds) \
     fastapi-secure-demo:0.1.0
   ```

4. **Deploy to Kubernetes**

   Adjust the image reference in `config/deployment.yaml` to point at your signed image in GitHub Container Registry, then apply the manifest:

   ```bash
   kubectl apply -f config/deployment.yaml
   ```

Refer to `demo_instructions.md` for a full end‑to‑end demonstration using the GitHub Actions pipeline and Cosign for signing container images.
