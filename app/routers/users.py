from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from db.schema import User
from db import crud

from dependecies import get_db
from authentication import get_current_user

router = APIRouter(
    prefix='/users',
    tags=['users'],
    dependencies=[Depends(get_current_user)]
)


@router.get('/detail/{user_id}', response_model=User)
async def get_user_handler(user_id: int, db: Session = Depends(get_db)):
    return await crud.get_object_by_id(db, user_id, 'User')
