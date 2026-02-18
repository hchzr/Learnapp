from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import FeatureFlag

FEATURE_FLAG_NAMES: tuple[str, ...] = (
    "notion_sync",
    "todoist_sync",
    "drive_ingestion",
    "anki",
    "exercises",
    "planner",
)
FEATURE_FLAG_NAME_SET = set(FEATURE_FLAG_NAMES)


async def is_feature_enabled(session: AsyncSession, name: str) -> bool:
    if name not in FEATURE_FLAG_NAME_SET:
        return False

    feature_flag = await session.get(FeatureFlag, name)
    if feature_flag is None:
        return False
    return feature_flag.enabled


async def list_feature_flags(session: AsyncSession) -> dict[str, bool]:
    results = await session.execute(select(FeatureFlag).order_by(FeatureFlag.name.asc()))
    flags = {feature_flag.name: feature_flag.enabled for feature_flag in results.scalars().all()}
    return {name: flags.get(name, False) for name in FEATURE_FLAG_NAMES}


def validate_feature_flag_name(name: str) -> bool:
    return name in FEATURE_FLAG_NAME_SET
