from app.database.session import SessionLocal
from app.models.user import User

db = SessionLocal()

users = db.query(User).all()

for u in users:
    print(
        u.id,
        u.username,
        u.email,
        u.role,
        u.password
    )

db.close()