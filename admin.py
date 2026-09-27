import os

from app.database.session import SessionLocal
from app.models.user import User
from app.core.security import hash_password

db = SessionLocal()
admin_password = os.getenv("DEMO_ADMIN_PASSWORD", "")
if len(admin_password) < 16:
    raise RuntimeError("Set DEMO_ADMIN_PASSWORD to a value of at least 16 characters.")

user = User(
    username="admin",
    email="admin@test.com",
    password=hash_password(admin_password),
    role="ADMIN"
)

db.add(user)
db.commit()

db.close()
