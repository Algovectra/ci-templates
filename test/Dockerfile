FROM python:3.12-slim

ARG BUILD_DATE
ARG REVISION

LABEL org.opencontainers.image.title="runpod-bench"
LABEL org.opencontainers.image.description="Sample benchmark image for RunPod built via ci-tests"
LABEL org.opencontainers.image.created="${BUILD_DATE}"
LABEL org.opencontainers.image.revision="${REVISION}"
LABEL org.opencontainers.image.source="Algovectra/ci-tests"

WORKDIR /app

RUN apt-get update \
    && apt-get install --no-install-recommends -y stress-ng=1.* \
    && rm -rf /var/lib/apt/lists/*

COPY benchmark.py .

RUN chmod +x benchmark.py

ENTRYPOINT ["python3", "/app/benchmark.py"]
