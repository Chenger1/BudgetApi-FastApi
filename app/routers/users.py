from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from db.schema import User, UserCreate
from db import crud

from dependecies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/detail/{user_id}', response_model=User)
async def get_user_handler(user_id: int, db: Session = Depends(get_db)):
    return await crud.get_user(db, user_id)


@router.post('/create/')
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return await crud.create_user(db, user)
