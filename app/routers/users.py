from fastapi import APIRouter

router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/detail/{user_id}')
async def create_user(user_id: int):
    return {'user_id': user_id}
