from .models import User
from db import schema
from sqlalchemy.orm import Session

from typing import Optional


async def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


async def create_user(db: Session, user: schema.UserCreate) -> User:
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
