from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from db.schema import User
from db import crud

from dependecies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/detail/{user_id}', response_model=User)
async def get_user_handler(user_id: int, db: Session = Depends(get_db)):
    return await crud.get_user(db, user_id)
