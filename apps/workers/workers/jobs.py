from __future__ import annotations

import uuid
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any

from celery.utils.log import get_task_logger

logger = get_task_logger("workers.jobs")


@dataclass(frozen=True)
class RetryConfig:
    max_retries: int = 3
    countdown_seconds: int = 1


class BaseJob(ABC):
    name: str
    retry_config = RetryConfig()

    @classmethod
    def execute(cls, *args: Any, **kwargs: Any) -> Any:
        run_id = kwargs.pop("run_id", str(uuid.uuid4()))
        task_ctx = kwargs.pop("task_ctx", None)

        logger.info(
            "job-start name=%s run_id=%s args=%s kwargs=%s",
            cls.name,
            run_id,
            args,
            kwargs,
        )

        try:
            result = cls().run(*args, run_id=run_id, **kwargs)
        except Exception as exc:
            logger.exception("job-failed name=%s run_id=%s", cls.name, run_id)
            if task_ctx is not None:
                retries = int(getattr(task_ctx.request, "retries", 0))
                if retries < cls.retry_config.max_retries:
                    raise task_ctx.retry(exc=exc, countdown=cls.retry_config.countdown_seconds)
            raise

        logger.info("job-success name=%s run_id=%s", cls.name, run_id)
        return {"run_id": run_id, "result": result}

    @abstractmethod
    def run(self, *args: Any, run_id: str, **kwargs: Any) -> Any:
        raise NotImplementedError


class HelloWorldJob(BaseJob):
    name = "hello_world"

    def run(self, *args: Any, run_id: str, **kwargs: Any) -> dict[str, str]:
        return {"message": "hello world", "run_id": run_id}


class CleanupOldJobsJob(BaseJob):
    name = "cleanup_old_jobs"

    def run(self, *args: Any, run_id: str, **kwargs: Any) -> dict[str, str]:
        cutoff = datetime.now(timezone.utc) - timedelta(days=7)
        return {
            "status": "completed",
            "deleted_before": cutoff.isoformat(),
            "run_id": run_id,
        }


class JobRegistry:
    def __init__(self) -> None:
        self._jobs: dict[str, type[BaseJob]] = {}

    def register(self, job_class: type[BaseJob]) -> None:
        self._jobs[job_class.name] = job_class

    def get(self, name: str) -> type[BaseJob]:
        if name not in self._jobs:
            raise KeyError(f"Unknown job: {name}")
        return self._jobs[name]

    def names(self) -> list[str]:
        return sorted(self._jobs.keys())


def with_retry(job_class: type[BaseJob]) -> Callable[..., Any]:
    def _runner(*args: Any, **kwargs: Any) -> Any:
        return job_class.execute(*args, **kwargs)

    return _runner


job_registry = JobRegistry()
job_registry.register(HelloWorldJob)
job_registry.register(CleanupOldJobsJob)
