from core.security import hash_password
from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.drive_data_model import User

def create_test_user():
    db: Session = SessionLocal()

    test_user = User(
        user_id ="1",
        username="testuser",
        password=hash_password("1234")

    )

    db.add(test_user)
    db.commit()
    db.close()
    print(" Test user created")

if __name__ == "__main__":
    create_test_user()
