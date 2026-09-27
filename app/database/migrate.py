from sqlalchemy import inspect, text

from app.database.session import engine


VOICE_COLUMNS = {
    "ai_summary": "TEXT",
    "ai_suggestion": "TEXT",
    "review_status": "VARCHAR DEFAULT 'PENDING'",
    "therapist_comment": "TEXT",
}


def migrate_voice_notes() -> None:
    inspector = inspect(engine)
    if "voice_notes" not in inspector.get_table_names():
        return

    existing = {column["name"] for column in inspector.get_columns("voice_notes")}
    with engine.begin() as connection:
        for name, definition in VOICE_COLUMNS.items():
            if name not in existing:
                connection.execute(
                    text(f"ALTER TABLE voice_notes ADD COLUMN {name} {definition}")
                )


if __name__ == "__main__":
    migrate_voice_notes()
    print("Voice-note migration completed")
