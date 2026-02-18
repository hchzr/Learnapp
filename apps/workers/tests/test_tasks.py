from __future__ import annotations

from celery.exceptions import Retry

from workers.jobs import HelloWorldJob


class _FakeRequest:
    def __init__(self, retries: int) -> None:
        self.retries = retries


class _RetryTaskContext:
    def __init__(self, retries: int = 0) -> None:
        self.request = _FakeRequest(retries=retries)

    def retry(self, *, exc: Exception, countdown: int) -> None:
        raise Retry(str(exc))


def test_hello_world_job_executes_and_returns_run_id() -> None:
    result = HelloWorldJob.execute(task_ctx=_RetryTaskContext())
    assert result["result"]["message"] == "hello world"
    assert isinstance(result["run_id"], str)
    assert len(result["run_id"]) > 10


def test_base_job_retries_on_failure() -> None:
    class _AlwaysFailJob(HelloWorldJob):
        name = "always_fail"

        def run(self, *args: object, run_id: str, **kwargs: object) -> dict[str, str]:
            raise RuntimeError("boom")

    try:
        _AlwaysFailJob.execute(task_ctx=_RetryTaskContext(retries=0))
        assert False, "expected retry to be raised"
    except Retry:
        assert True
