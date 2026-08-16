# ci-tests

Reusable CI action for building and pushing container images with Podman on
self-hosted GitHub Actions runners.

## Contents

| Path | Type | Purpose |
| ---- | ---- | ------- |
| `.github/actions/podman-build-push/action.yml` | Composite action | Build an image with `podman build` and push it with `podman push` |
| `.github/workflows/build-runpod-bench.yaml` | Workflow | Builds and pushes `algovectra/runpod-bench:testing-ci` |
| `test/Dockerfile` | Dockerfile | Minimal sample image used by the test workflow |

## Usage

```yaml
jobs:
  build-and-push:
    runs-on: docker
    steps:
      - uses: actions/checkout@v4

      - uses: Algovectra/ci-tests/.github/actions/podman-build-push@main
        with:
          image: quay.io/myorg/app:v1
          tags: quay.io/myorg/app:latest
          dockerfile: Dockerfile   # default
          context: .               # default
          build-args: |
            VERSION=1.2.3
          labels: |
            org.opencontainers.image.source=myorg/app
          push: "true"             # default
          memory: "8g"              # build-container memory limit
          cpus: "4"                 # build-container CPU quota
```

## Inputs

| Input | Required | Default | Description |
| ----- | -------- | ------- | ----------- |
| `image` | yes | — | Primary image tag, including registry host (e.g. `quay.io/org/app:tag`) |
| `tags` | no | `""` | Additional tags to apply and push, one per line or comma-separated |
| `dockerfile` | no | `Dockerfile` | Path to the Dockerfile/Containerfile relative to `context` |
| `context` | no | `.` | Build context directory |
| `build-args` | no | `""` | Build-time variables, one `KEY=VALUE` per line or comma-separated |
| `labels` | no | `""` | Image labels, one `KEY=VALUE` per line or comma-separated |
| `platforms` | no | `""` | Target platform(s), e.g. `linux/amd64,linux/arm64` |
| `push` | no | `true` | Push after building; set to `false` to build only |
| `memory` | no | `""` | Memory limit for the build container (e.g. `8g`, `512m`) |
| `cpus` | no | `""` | CPU quota for the build container (e.g. `4`, `0.5`); applied via `--cpu-period`/`--cpu-quota` |
| `tls-verify` | no | `true` | Require HTTPS + verify certs on push; `false` allows insecure registries |
| `extra-args` | no | `""` | Additional flags forwarded to `podman build` |
| `cleanup` | no | `true` | Remove the built image(s) from the runner afterward to save disk space |

### Registry authentication

The runner must already be authenticated to the target registry (e.g.
`podman login` or a pre-seeded `/run/user/0/containers/auth.json`). The
action itself does not handle credentials.

## How it works

1. Builds the image: `podman build -f <dockerfile> -t <image> [flags] <context>`
2. Tags it for each entry in `tags` (if any).
3. When `push` is `true`, pushes the primary image and every additional tag.
4. When `cleanup` is `true` (default), removes all local copies of the image(s)
   so the runner doesn't run out of disk space. This step always runs, even if
   the push step failed.

All shell steps run with `set -euo pipefail`, so any failure stops the job.
