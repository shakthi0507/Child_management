from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os


APP_ENV = os.getenv("APP_ENV", "development").strip().lower()
_CONFIGURED_DATABASE_URL = os.getenv("DATABASE_URL")

if APP_ENV in {"prod", "production"} and not _CONFIGURED_DATABASE_URL:
    raise RuntimeError("Production requires DATABASE_URL to be configured.")

DATABASE_URL = _CONFIGURED_DATABASE_URL or "sqlite:///./child_development.db"

if (
    APP_ENV in {"prod", "production"}
    and DATABASE_URL.startswith("sqlite:")
    and not DATABASE_URL.startswith("sqlite:////")
):
    raise RuntimeError(
        "Production SQLite DATABASE_URL must use an absolute persistent path."
    )


connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
