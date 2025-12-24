from sqlalchemy.orm import Session
from models import User, UserRole
from auth import get_password_hash
from typing import Optional

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, email: str, password: str, full_name: str, 
                role: UserRole = UserRole.CUSTOMER, phone: str = None, 
                address: str = None, latitude: float = None, longitude: float = None):
    hashed_password = get_password_hash(password)
    db_user = User(
        email=email,
        password_hash=hashed_password,
        full_name=full_name,
        role=role,
        phone=phone,
        address=address,
        latitude=latitude,
        longitude=longitude
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_by_role(db: Session, role: UserRole, skip: int = 0, limit: int = 100):
    return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()

def update_user(db: Session, user_id: int, **kwargs):
    user = get_user_by_id(db, user_id)
    if user:
        for key, value in kwargs.items():
            if hasattr(user, key) and value is not None:
                setattr(user, key, value)
        db.commit()
        db.refresh(user)
    return user
