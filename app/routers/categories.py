from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session

from dependecies import get_db
from authentication import get_current_user

from db.schema import Category, CategoryList, EditCategory
from db import crud


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Category)
async def create_category_handler(category: Category, db: Session = Depends(get_db)):
    return await crud.create_instance(db, category)


@router.get('/all', response_model=CategoryList)
async def get_categories_list(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    categories = await crud.get_instances_by_user_id(db, user.id, 'Category')
    return {'id': user.id, 'username': user.username, 'categories': categories}


@router.get('/detail/{category_id}', response_model=Category)
async def get_category(category_id: int, db: Session = Depends(get_db)):
    return await crud.get_object_by_id(db, category_id, 'Category')


@router.patch('/detail/{category_id}/edit', response_model=EditCategory)
async def edit_category(category_id: int, category: EditCategory, db: Session = Depends(get_db)):
    return await crud.update_instance(db, category, category_id)


@router.delete('/detail/{category_id}/delete')
async def delete_category(category_id: int, db: Session = Depends(get_db)):
    success, message = await crud.delete_instance(db, category_id, 'Category')
    return {'status': 204 if success else 500, 'message': message}
