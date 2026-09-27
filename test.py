from app.database.session import engine

with engine.connect() as conn:
    conn.execute(
        """
        ALTER TABLE assessment_responses
        ADD COLUMN created_at DATETIME
        """
    )

    conn.commit()