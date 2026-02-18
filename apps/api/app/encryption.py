import base64
import hashlib
from functools import lru_cache

from cryptography.fernet import Fernet, InvalidToken
from sqlalchemy.types import String, TypeDecorator

from app.settings import get_settings


@lru_cache
def _fernet() -> Fernet:
    raw_key = get_settings().encryption_key.encode("utf-8")
    derived_key = base64.urlsafe_b64encode(hashlib.sha256(raw_key).digest())
    return Fernet(derived_key)


def encrypt_value(value: str) -> str:
    return _fernet().encrypt(value.encode("utf-8")).decode("utf-8")


def decrypt_value(value: str) -> str:
    try:
        return _fernet().decrypt(value.encode("utf-8")).decode("utf-8")
    except InvalidToken as exc:
        raise ValueError("Unable to decrypt value with the configured key") from exc


class EncryptedString(TypeDecorator[str]):
    impl = String
    cache_ok = True

    def process_bind_param(self, value: str | None, dialect: object) -> str | None:
        if value is None:
            return None
        return encrypt_value(value)

    def process_result_value(self, value: str | None, dialect: object) -> str | None:
        if value is None:
            return None
        return decrypt_value(value)
