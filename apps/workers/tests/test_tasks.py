from workers.tasks import hello_world


def test_hello_world_returns_run_id() -> None:
    run_id = hello_world.run()
    assert isinstance(run_id, str)
    assert len(run_id) > 10
