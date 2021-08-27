from .models import User, Category, Transaction
from db import schema

from typing import Optional, Union


models = {
    'Category': Category,
    'User': User,
    'Transaction': Transaction
}


async def create_instance(data: dict, model_name: str) -> Union[User, Category, Transaction]:
    model = models[model_name]
    instance = await model.create(**data)
    return instance


async def update_instance(data: schema.BaseModel, instance_id: int, model_name: str) -> \
        Union[User, Category, Transaction]:
    instance = await get_object_by_id(instance_id, model_name)
    for key, value in data.dict().items():
        if value is not None:
            setattr(instance, key, value)
    await instance.save()
    return instance


async def delete_instance(obj_id: int, model_name: str) -> tuple[bool, str]:
    model = models[model_name]
    instance = await model.get_or_none(id=obj_id)
    try:
        await instance.delete()
        return True, 'OK. Deleted'
    except Exception as e:
        return False, str(e)


async def get_object_by_id(instance_id: int, model_name: str) -> Union[User, Category, Transaction]:
    model = models[model_name]
    return await model.get_or_none(id=instance_id)


async def get_user_by_username(username: str) -> Optional[User]:
    return await User.get_or_none(username=username)


async def get_instances_by_user_id(user_id: int, model_name: str) -> list[Optional[Union[Category, Transaction]]]:
    model = models[model_name]
    return await model.filter(user__id=user_id)
