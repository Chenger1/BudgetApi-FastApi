from fastapi import APIRouter, Depends, Request

from db.schema import User_Schema, EditUser, MessageList
from db import crud
from db.models import Message

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


@router.patch('/detail/{user_id}', response_model=User_Schema)
async def edit_user_data(user_id: int, data: EditUser):
    return await crud.update_instance(data, user_id, 'User')


@router.get('/detail/{user_id}/messages', response_model=MessageList)
async def get_user_messages(request: Request, user_id: int):
    user = request.state.user
    instances = await Message.get_messages(user_id)
    return {'user_id': user_id, 'username': user.username, 'messages': instances}
