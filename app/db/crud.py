from .models import User
from db import schema
from sqlalchemy.orm import Session


async def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


async def create_user(db: Session, user: schema.UserCreate) -> User:
    user = User(**user.dict())
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
