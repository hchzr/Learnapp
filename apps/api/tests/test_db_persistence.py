import os
import uuid
from collections.abc import Iterator

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

os.environ.setdefault("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/learnapp_test")
os.environ.setdefault("ENCRYPTION_KEY", "test-encryption-key")

from app.db import SessionLocal, engine
from app.models import Base, ExternalAccount, Provider, User


@pytest.fixture(scope="session", autouse=True)
def prepare_test_db() -> Iterator[None]:
    import psycopg

    db_url = os.environ["DATABASE_URL"]
    admin_url = "postgresql://postgres:postgres@localhost:5432/postgres"
    db_name = db_url.rsplit("/", maxsplit=1)[-1]
    with psycopg.connect(admin_url, autocommit=True) as conn:
        with conn.cursor() as cur:
            cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
            cur.execute(f"CREATE DATABASE {db_name}")
    yield


@pytest.fixture(autouse=True)
async def reset_schema() -> Iterator[None]:
    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)
    yield


@pytest.mark.asyncio
async def test_create_user() -> None:
    async with SessionLocal() as session:
        user = User(email="db-user@example.com")
        session.add(user)
        await session.commit()
        await session.refresh(user)

        assert user.id is not None
        assert user.timezone == "UTC"


@pytest.mark.asyncio
async def test_encrypted_token_roundtrip() -> None:
    async with SessionLocal() as session:
        user = User(email="token-user@example.com")
        session.add(user)
        await session.flush()

        account = ExternalAccount(
            user_id=user.id,
            provider=Provider.NOTION,
            access_token="secret-access-token",
            refresh_token="secret-refresh-token",
            scope="read:all",
        )
        session.add(account)
        await session.commit()

        encrypted_access = (
            await session.execute(
                text("SELECT access_token FROM external_accounts WHERE id = :id"),
                {"id": str(account.id)},
            )
        ).scalar_one()

        assert encrypted_access != "secret-access-token"

    async with SessionLocal() as session:
        persisted = await session.get(ExternalAccount, account.id)
        assert persisted is not None
        assert persisted.access_token == "secret-access-token"
        assert persisted.refresh_token == "secret-refresh-token"


@pytest.mark.asyncio
async def test_external_account_unique_constraint() -> None:
    async with SessionLocal() as session:
        user = User(email=f"duplicate-{uuid.uuid4()}@example.com")
        session.add(user)
        await session.flush()

        one = ExternalAccount(
            user_id=user.id,
            provider=Provider.TODOIST,
            access_token="token-1",
            refresh_token=None,
            scope="tasks:read",
        )
        duplicate = ExternalAccount(
            user_id=user.id,
            provider=Provider.TODOIST,
            access_token="token-2",
            refresh_token=None,
            scope="tasks:write",
        )
        session.add(one)
        await session.flush()
        session.add(duplicate)

        with pytest.raises(IntegrityError):
            await session.commit()
