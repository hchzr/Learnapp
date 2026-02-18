import os
import subprocess
import sys


def main() -> int:
    app = "workers.celery_app:celery_app"
    cmd = [
        sys.executable,
        "-m",
        "celery",
        "-A",
        app,
        "worker",
        "--loglevel",
        os.getenv("WORKER_LOGLEVEL", "info"),
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
