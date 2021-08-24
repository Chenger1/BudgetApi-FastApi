from .models import User, Base, Category, Transaction
from db import schema
from sqlalchemy.orm import Session

from typing import Optional, Union


models = {
    'Category': Category,
    'EditCategory': Category,
    'UserCreate': User,
    'User': User,
    'CreateTransaction': Transaction,
    'Transaction': Transaction,
    'EditTransaction': Transaction
}


async def get_object_by_id(db: Session, instance_id: int, model_name: str) -> Base:
    model = models[model_name]
    return db.query(model).filter(model.id == instance_id).first()


async def get_user_by_username(db: Session, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


async def get_instances_by_user_id(db: Session, user_id: int, model_name: str) -> list[Optional[Base]]:
    model = models[model_name]
    return db.query(model).filter(model.user_id == user_id).all()


async def update_instance(db: Session, data: Union[schema.BaseModel, schema.BaseCategory, dict],
                          instance_id: int) -> Base:
    instance = await get_object_by_id(db, instance_id, data.__class__.__name__)
    for key, value in data.dict().items():
        if value is not None:
            setattr(instance, key, value)
    db.commit()
    return instance


async def create_instance(db: Session, data: schema.BaseModel) -> Base:
    model = models[data.__class__.__name__]
    instance = model(**data.dict())
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance


async def delete_instance(db: Session, obj_id: int, model_name: str) -> tuple[bool, str]:
    model = models[model_name]
    instance = db.query(model).filter(model.id == obj_id).first()
    try:
        db.delete(instance)
        db.commit()
        return True, 'OK. Deleted'
    except Exception as e:
        return False, str(e)
