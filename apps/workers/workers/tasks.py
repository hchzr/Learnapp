import logging
import uuid

from workers.celery_app import celery_app
from workers.logging_utils import RunIdLoggerAdapter, setup_logging

setup_logging()
logger = logging.getLogger("workers")


@celery_app.task(name="workers.hello_world")  # type: ignore[misc]
def hello_world() -> str:
    run_id = str(uuid.uuid4())
    run_logger = RunIdLoggerAdapter(logger, {"run_id": run_id})
    run_logger.info("hello_world task executed")
    return run_id
