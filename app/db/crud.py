from .models import User, Base, Category
from db import schema
from sqlalchemy.orm import Session

from typing import Optional


models = {
    'Category': Category,
    'UserCreate': User,
    'User': User
}


async def get_object_by_id(db: Session, instance_id: int, model_name: str) -> Base:
    model = models[model_name]
    return db.query(model).filter(model.id == instance_id).first()


async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


async def get_categories_by_user_id(db: Session, user_id: int) -> list[Optional[Category]]:
    return db.query(Category).filter(Category.user_id == user_id).all()


async def create_instance(db: Session, data: schema.BaseModel) -> Base:
    model = models[data.__class__.__name__]
    instance = model(**data.dict())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance
