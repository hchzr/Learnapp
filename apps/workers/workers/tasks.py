import logging
import uuid

from workers.celery_app import celery_app

logger = logging.getLogger("workers")


@celery_app.task(name="workers.hello_world")
def hello_world() -> str:
    run_id = str(uuid.uuid4())
    logger.info("hello_world task executed run_id=%s", run_id)
    return run_id
