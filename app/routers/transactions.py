from fastapi import APIRouter, Depends, Request, HTTPException, BackgroundTasks

from utils.authentication import get_current_user

from db.schema import TransactionList, CreateTransaction, Transaction_Schema, EditTransaction
from db import crud
from db.models import Transaction

from app.dependencies import get_user_fixed_balance
from utils.send_mail import send_message

from typing import Optional


router = APIRouter(
    prefix='/transactions',
    tags=['transactions'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Transaction_Schema)
async def create_transaction_handler(request: Request, transaction: CreateTransaction,
                                     background_tasks: BackgroundTasks,
                                     fixed_balance: float = Depends(get_user_fixed_balance),):
    user = request.state.user
    data = transaction.dict()
    if fixed_balance and data['sum'] >= fixed_balance:  #: User has to confirm that he use fixed balance
        await send_message(user.id, 'You have reached your balance', background_tasks)

    data['number'] = await Transaction.get_next_transaction_number(user.id)
    data['user'] = user
    data['category'] = await crud.get_object_by_id(transaction.category, 'Category')
    instance = await crud.create_instance(data, 'Transaction')
    if not data['planned']:  #: Planned transaction will be added to balance later
        if instance.type:
            user.balance += instance.sum
        else:
            user.balance -= instance.sum
        await user.save()
    return await Transaction_Schema.from_tortoise_orm(instance)


@router.get('/all', response_model=TransactionList)
async def get_transaction_list(request: Request):
    user = request.state.user
    transactions = await crud.get_instances_by_user_id(user.id, 'Transaction')
    return {'user_id': user.id, 'username': user.username, 'transactions': transactions}


@router.get('/all/statistic/{period}/{number}', response_model=TransactionList)
async def get_transaction_statistic(period: str, request: Request, number: int = None):
    if period not in ('day', 'month', 'year'):
        raise HTTPException(status_code=404,
                            detail='Wrong period name')
    user = request.state.user
    instances = await Transaction.get_transactions_by_period(user_id=user.id, period=period, number=number)
    return {'user_id': user.id, 'username': user.username, 'transactions': instances}


@router.get('/all/{type}/', response_model=TransactionList)
async def get_transactions_by_type(type: bool, request: Request):
    user = request.state.user
    instances = await Transaction.get_transaction_by_type(user.id, type)
    return {'user_id': user.id, 'username': user.username, 'transactions': instances}


@router.get('/all/by_category/{category_id}', response_model=TransactionList)
async def get_transactions_by_category(request: Request, category_id: int, transaction_type: Optional[bool] = None):
    user = request.state.user
    instances = await Transaction.get_transactions_by_category(user.id, category_id, transaction_type)
    return {'user_id': user.id, 'username': user.username, 'transactions': instances}


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
