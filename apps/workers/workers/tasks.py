from __future__ import annotations

from typing import cast

from celery import Task

from workers.celery_app import celery_app
from workers.jobs import CleanupOldJobsJob, HelloWorldJob


@celery_app.task(bind=True, name="workers.hello_world")  # type: ignore[misc]
def hello_world(self: Task) -> dict[str, object]:
    return cast(dict[str, object], HelloWorldJob.execute(task_ctx=self))


@celery_app.task(bind=True, name="workers.cleanup_old_jobs")  # type: ignore[misc]
def cleanup_old_jobs(self: Task) -> dict[str, object]:
    return cast(dict[str, object], CleanupOldJobsJob.execute(task_ctx=self))


@celery_app.task(bind=True, name="workers.retryable_hello")  # type: ignore[misc]
def retryable_hello(self: Task, fail_until_retry: int = 1) -> dict[str, object]:
    current_retries = int(self.request.retries)
    if current_retries < fail_until_retry:
        raise self.retry(exc=RuntimeError("forced retry"), countdown=0)
    return cast(dict[str, object], HelloWorldJob.execute(task_ctx=self))
