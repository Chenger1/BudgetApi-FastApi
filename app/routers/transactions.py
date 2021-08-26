from fastapi import APIRouter, Depends, Request

from authentication import get_current_user

from db.schema import TransactionList, CreateTransaction, Transaction_Schema, EditTransaction
from db import crud
from db.models import Transaction


router = APIRouter(
    prefix='/transactions',
    tags=['transactions'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Transaction_Schema)
async def create_transaction_handler(request: Request, transaction: CreateTransaction):
    user = request.state.user
    data = transaction.dict()
    data['number'] = await Transaction.get_next_transaction_number(user.id)
    data['user'] = user
    data['category'] = await crud.get_object_by_id(transaction.category, 'Category')
    instance = await crud.create_instance(data, 'Transaction')
    return await Transaction_Schema.from_tortoise_orm(instance)


@router.get('/all', response_model=TransactionList)
async def get_transaction_list(request: Request):
    user = request.state.user
    transactions = await crud.get_instances_by_user_id(user.id, 'Transaction')
    return {'user_id': user.id, 'username': user.username, 'transactions': transactions}


@router.get('/detail/{transaction_id}', response_model=Transaction_Schema)
async def get_transaction(transaction_id: int):
    instance = await crud.get_object_by_id(transaction_id, 'Transaction')
    return await Transaction_Schema.from_tortoise_orm(instance)


@router.patch('/detail/{transaction_id}/edit', response_model=Transaction_Schema)
async def edit_transaction(transaction_id: int, data: EditTransaction):
    instance = await crud.update_instance(data, transaction_id, 'Transaction')
    return await Transaction_Schema.from_tortoise_orm(instance)


@router.delete('/detail/{transaction_id}/delete')
async def delete_transaction(transaction_id: int):
    success, message = await crud.delete_instance(transaction_id, 'Transaction')
    return {'status': 201 if success else 500, 'message': message}
