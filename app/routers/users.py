from fastapi import APIRouter, Depends

from db.schema import User_Schema
from db import crud

from authentication import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(get_current_user)]
)


@router.get('/detail/{user_id}', response_model=User_Schema)
async def get_user_handler(user_id: int):
    return await crud.get_object_by_id(user_id, 'User')


@router.delete('/detail/{user_id}')
async def delete_user(user_id: int):
    return await crud.delete_instance(user_id, 'User')
