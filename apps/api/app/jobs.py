from __future__ import annotations

from celery import Celery

from app.settings import get_settings

settings = get_settings()

celery_client = Celery("life_learn_api", broker=settings.redis_url, backend=settings.redis_url)


def enqueue_hello_world() -> str:
    task = celery_client.send_task("workers.hello_world")
    return str(task.id)
