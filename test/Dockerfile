FROM python:3.12-slim

ARG BUILD_DATE
ARG REVISION

LABEL org.opencontainers.image.title="runpod-bench"
LABEL org.opencontainers.image.description="Sample benchmark image for RunPod built via ci-tests"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${REVISION}"
LABEL org.opencontainers.image.source="Algovectra/ci-tests"

WORKDIR /app
