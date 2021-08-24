from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from dependecies import get_db
from authentication import get_current_user

from db.schema import Category
from db.crud import create_instance


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Category)
async def create_category_handler(category: Category, db: Session = Depends(get_db)):
    return await create_instance(db, category)
