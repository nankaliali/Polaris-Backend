from sqlalchemy.orm import Session

from models.drive_data_model import User
def get_user_by_username(db: Session, username: str) -> User | None:
    return db.query(User).filter(User.username == username).first()

def get_user_by_device_id(db: Session, device_id: str) -> User | None:
    """Get user by device_id"""
    return db.query(User).filter(User.device_id == device_id).first()

def create_user(
    db: Session,
    username: str,
    hashed_password: str,
    device_id: str
) -> User:
    """
    Create a new user, including their unique device_id.
    """
    db_user = User(
        username=username,
        password=hashed_password,
        device_id=device_id
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_password(
    db: Session,
    username: str,
    new_hashed_password: str
) -> User | None:
    user = get_user_by_username(db, username)
    if user:
        user.password = new_hashed_password
        db.commit()
        db.refresh(user)
        return user
    return None

