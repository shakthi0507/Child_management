from datetime import datetime, timedelta, timezone

import os

from passlib.context import CryptContext

from jose import jwt


_DEVELOPMENT_SECRET = "child-development-dev-secret-change-in-production"
_APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
_CONFIGURED_SECRET = os.getenv("JWT_SECRET_KEY")
_SECRET_PLACEHOLDER_MARKERS = ("replace-with", "change-me", "changeme")

if _APP_ENV in {"prod", "production"} and (
    not _CONFIGURED_SECRET
    or len(_CONFIGURED_SECRET) < 32
    or _CONFIGURED_SECRET == _DEVELOPMENT_SECRET
    or any(
        marker in _CONFIGURED_SECRET.lower()
        for marker in _SECRET_PLACEHOLDER_MARKERS
    )
):
    raise RuntimeError(
        "Production requires a unique JWT_SECRET_KEY of at least 32 characters; "
        "template placeholder values are not allowed."
    )

SECRET_KEY = _CONFIGURED_SECRET or _DEVELOPMENT_SECRET

ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = 60



pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)



def hash_password(password: str):

    return pwd_context.hash(password)



def verify_password(
    plain_password: str,
    hashed_password: str
):

    return pwd_context.verify(
        plain_password,
        hashed_password
    )



def create_access_token(
    data: dict
):

    to_encode = data.copy()


    expire = datetime.now(
        timezone.utc
    ) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )


    to_encode.update(
        {
            "exp": expire
        }
    )


    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )
