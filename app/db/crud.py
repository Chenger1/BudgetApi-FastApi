from .models import User
from sqlalchemy.orm import Session


async def get_user(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()
