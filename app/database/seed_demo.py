"""Initialize a new demo database without risking an existing database.

This wrapper reuses the repository's reset fixture only after verifying every
application table is empty. Demo passwords must be supplied in the process
environment and are never printed.
"""

import contextlib
import io
import os
from pathlib import Path

from sqlalchemy import inspect, text

from app.core.security import hash_password
from app.database.base import Base
from app.database.import_assessment_docx import import_assessments
from app.database.session import engine

# Importing the fixture registers its models and functions but does not run it.
import seed as fixture_seed


ROOT = Path(__file__).resolve().parents[2]
ASSESSMENT_DOCUMENT = ROOT / "001 Assessment - initial.docx"


def _demo_passwords() -> tuple[str, str, str]:
    values = (
        os.getenv("DEMO_ADMIN_PASSWORD", ""),
        os.getenv("DEMO_PARENT_PASSWORD", ""),
        os.getenv("DEMO_THERAPIST_PASSWORD", ""),
    )
    if any(len(password) < 16 for password in values):
        raise RuntimeError(
            "Set DEMO_ADMIN_PASSWORD, DEMO_PARENT_PASSWORD, and "
            "DEMO_THERAPIST_PASSWORD to unique values of at least 16 characters."
        )
    if len(set(values)) != len(values):
        raise RuntimeError("Each demo role must have a different password.")
    return values


def _ensure_empty_database() -> None:
    # Check before creating anything. In particular, this must not silently add
    # tables to an existing application database and then claim it is fresh.
    existing_tables = set(inspect(engine).get_table_names())
    known_tables = set(Base.metadata.tables)
    unknown_tables = existing_tables - known_tables
    if unknown_tables:
        raise RuntimeError(
            "Refusing to run the reset-based demo fixture because the database "
            "contains tables not owned by this application: "
            + ", ".join(sorted(unknown_tables))
        )

    with engine.connect() as connection:
        populated = []
        for table_name in sorted(existing_tables):
            count = connection.execute(
                text(f'SELECT COUNT(*) FROM "{table_name}"')
            ).scalar_one()
            if count:
                populated.append(table_name)
    if populated:
        raise RuntimeError(
            "Refusing to run the reset-based demo fixture because the database "
            "already contains data. Populated tables: " + ", ".join(populated)
        )


def seed_demo_database() -> tuple[int, int]:
    passwords = _demo_passwords()
    if not ASSESSMENT_DOCUMENT.is_file():
        raise FileNotFoundError(
            f"Required assessment document is missing: {ASSESSMENT_DOCUMENT.name}"
        )

    _ensure_empty_database()

    role_passwords = iter(
        [passwords[0], *([passwords[1]] * 3), *([passwords[2]] * 3)]
    )

    def hash_demo_password(_fixture_password: str) -> str:
        try:
            password = next(role_passwords)
        except StopIteration as exc:
            raise RuntimeError(
                "Demo fixture user ordering changed; review seed_demo.py."
            ) from exc
        return hash_password(password)

    fixture_seed.hash_password = hash_demo_password
    # Silence fixture progress output in deployment logs.
    with contextlib.redirect_stdout(io.StringIO()):
        fixture_seed.main()

    created_assessments, created_questions = import_assessments(
        ASSESSMENT_DOCUMENT
    )
    return created_assessments, created_questions


if __name__ == "__main__":
    assessment_count, question_count = seed_demo_database()
    print(
        "Demo fixture initialized. Imported "
        f"{assessment_count} assessment templates and {question_count} questions."
    )
    print("Demo passwords are managed outside source code and were not printed.")
