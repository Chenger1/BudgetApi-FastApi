from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from db.schema import User
from db.crud import get_user

from dependecies import get_db

router = APIRouter(
    prefix='/users',
    tags=['users'],
)


@router.get('/detail/{user_id}', response_model=User)
async def create_user(user_id: int, db: Session = Depends(get_db)):
    return await get_user(db, user_id)
