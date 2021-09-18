from Application import db, bcrypt
from Application.models import Admin


hashed_password = bcrypt.generate_password_hash("12345")

admin = Admin(name="Jack John", username="admin",
               email="admin@admin.com", password=hashed_password)

db.session.add(admin)
db.session.commit()

print("Added Admin")