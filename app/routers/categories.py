from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session

from dependecies import get_db
from authentication import get_current_user

from db.schema import Category, CategoryList
from db.crud import create_instance, get_categories_by_user_id, get_object_by_id


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Category)
async def create_category_handler(category: Category, db: Session = Depends(get_db)):
    return await create_instance(db, category)


@router.get('/all', response_model=CategoryList)
async def get_categories_list(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    categories = await get_categories_by_user_id(db, user.id)
    return {'id': user.id, 'username': user.username, 'categories': categories}


@router.get('/detail/{category_id}', response_model=Category)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    return await get_object_by_id(db, category_id, 'Category')
