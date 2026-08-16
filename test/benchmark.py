#!/usr/bin/env python3
"""Minimal benchmark entrypoint for the runpod-bench sample image.

Runs a short CPU stress workload and prints a summary so the container
produces meaningful output when executed on RunPod (or anywhere else).
"""

import platform
import socket
import subprocess
import sys
import time
from datetime import datetime, timezone


def banner(title: str) -> None:
    line = "=" * 60
    print(f"\n{line}\n{title}\n{line}")


def main() -> int:
    banner("runpod-bench  —  sample benchmark")

    print(f"Host:       {socket.gethostname()}")
    print(f"Platform:   {platform.platform()}")
    print(f"Python:     {sys.version.split()[0]}")
    print(f"Timestamp:  {datetime.now(timezone.utc).isoformat()}")

    banner("CPU stress (10 s)")
    start = time.monotonic()
    result = subprocess.run(
        ["stress-ng", "--cpu", "2", "--timeout", "10s", "--metrics-brief"],
        capture_output=True,
        text=True,
    )
    elapsed = time.monotonic() - start

    if result.stdout:
        print(result.stdout.strip())
    if result.returncode != 0:
        print(f"stress-ng failed (rc={result.returncode})", file=sys.stderr)
        if result.stderr:
            print(result.stderr.strip(), file=sys.stderr)

    banner("Result")
    print(f"Wall-clock elapsed: {elapsed:.2f} s")
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
