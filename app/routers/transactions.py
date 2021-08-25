from fastapi import APIRouter, Depends, Request

from sqlalchemy.orm import Session

from authentication import get_current_user
from dependecies import get_db

from db.schema import Transaction, CreateTransaction, TransactionList, EditTransaction
from db import crud, utils

import datetime


router = APIRouter(
    prefix='/transactions',
    tags=['transactions'],
    dependencies=[Depends(get_current_user)]
)


@router.post('/create', response_model=Transaction)
async def create_transaction_handler(request: Request, data: CreateTransaction, db: Session = Depends(get_db)):
    user = request.state.user
    data.number = await utils.get_next_transaction_number(db, user.id)
    data.created = datetime.date.today()
    return await crud.create_instance(db, data)


@router.get('/all', response_model=TransactionList)
async def get_transaction_list(request: Request, db: Session = Depends(get_db)):
    user = request.state.user
    transactions = await crud.get_instances_by_user_id(db, user.id, 'Transaction')
    return {'id': user.id, 'username': user.username, 'transactions': transactions}


@router.get('/detail/{transaction_id}', response_model=Transaction)
async def get_transaction(transaction_id: int, db: Session = Depends(get_db)):
    instance = await crud.get_object_by_id(db, transaction_id, 'Transaction')
    return {'id': instance.id,
            'number': instance.number,
            'sum': instance.sum,
            'created': instance.created,
            'user_id': instance.user_id,
            'category_id': instance.category_id,
            'category_name': instance.category.name}


@router.patch('/detail/{transaction_id}/edit', response_model=Transaction)
async def edit_transaction(transaction_id: int, data: EditTransaction, db: Session = Depends(get_db)):
    instance = await crud.update_instance(db, data, transaction_id)
    return {'id': instance.id,
            'number': instance.number,
            'sum': instance.sum,
            'created': instance.created,
            'user_id': instance.user_id,
            'category_id': instance.category_id,
            'category_name': instance.category.name if instance.category else None}


@router.delete('/detail/{transaction_id}/delete')
async def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    success, message = await crud.delete_instance(db, transaction_id, 'Transaction')
    return {'status': 201 if success else 500, 'message': message}
