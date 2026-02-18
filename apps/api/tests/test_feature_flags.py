import pytest

from app.feature_flags import FEATURE_FLAG_NAMES, is_feature_enabled, list_feature_flags
from app.models import FeatureFlag


class FakeResult:
    def __init__(self, values: list[FeatureFlag]):
        self._values = values

    def scalars(self) -> "FakeResult":
        return self

    def all(self) -> list[FeatureFlag]:
        return self._values


class FakeSession:
    def __init__(self, flags: dict[str, bool]):
        self._flags = flags

    async def get(self, _model, name: str):
        if name not in self._flags:
            return None
        return FeatureFlag(name=name, enabled=self._flags[name])

    async def execute(self, _query):
        values = [FeatureFlag(name=name, enabled=enabled) for name, enabled in self._flags.items()]
        return FakeResult(values)


@pytest.mark.asyncio
async def test_is_feature_enabled_returns_false_for_unknown_flag() -> None:
    session = FakeSession({"anki": True})

    assert await is_feature_enabled(session, "not_a_flag") is False


@pytest.mark.asyncio
async def test_list_feature_flags_returns_all_supported_flags() -> None:
    session = FakeSession({"anki": True, "planner": True})

    flags = await list_feature_flags(session)

    assert set(flags.keys()) == set(FEATURE_FLAG_NAMES)
    assert flags["anki"] is True
    assert flags["planner"] is True
    assert flags["exercises"] is False
