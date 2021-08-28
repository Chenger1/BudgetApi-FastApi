from fastapi import APIRouter, Depends, Request

from utils.authentication import get_current_user

from db.schema import Category_Schema, CategoryList, CreateCategory, EditCategory
from db import crud


router = APIRouter(
    prefix='/categories',
    tags=['categories'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Category_Schema)
async def create_category_handler(request: Request, category: CreateCategory):
    user = request.state.user
    data = category.dict()
    data['user'] = user
    return await crud.create_instance(data, 'Category')


@router.get('/all', response_model=CategoryList)
async def get_categories_list(request: Request):
    user = request.state.user
    categories = await crud.get_instances_by_user_id(user.id, 'Category')
    return {'user_id': user.id, 'username': user.username, 'categories': categories}


@router.get('/detail/{category_id}', response_model=Category_Schema)
async def get_category(category_id: int):
    return await crud.get_object_by_id(category_id, 'Category')


@router.patch('/detail/{category_id}/edit', response_model=Category_Schema)
async def edit_category(category_id: int, category: EditCategory):
    return await crud.update_instance(category, category_id, 'Category')


@router.delete('/detail/{category_id}/delete')
async def delete_category(category_id: int):
    success, message = await crud.delete_instance(category_id, 'Category')
    return {'status': 204 if success else 500, 'message': message}
