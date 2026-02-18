import logging

from workers.tasks import hello_world


def test_task_logs_include_run_id(caplog) -> None:
    with caplog.at_level(logging.INFO):
        run_id = hello_world.run()

    task_logs = [record for record in caplog.records if record.name == "workers"]

    assert task_logs
    task_log = task_logs[-1]
    assert getattr(task_log, "run_id", "-") == run_id
    assert task_log.getMessage() == "hello_world task executed"
