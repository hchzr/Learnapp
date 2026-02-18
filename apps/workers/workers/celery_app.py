import os

from celery import Celery  # type: ignore[import-untyped]

redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

celery_app = Celery("life_learn_workers", broker=redis_url, backend=redis_url)
celery_app.conf.update(task_serializer="json", result_serializer="json", accept_content=["json"])
