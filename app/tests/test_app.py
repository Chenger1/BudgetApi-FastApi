import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from typing import Generator

from tortoise.contrib.test import finalizer, initializer

from routers import users, categories, transactions
from authentication import router as auth_router

from db.models import Transaction

from datetime import datetime

user_data = {
    'username': 'test_user',
    'password': 'test_password'
}

app = FastAPI()  # Second app because tortoise_register cant switch to test db if it declares in main.py
app.include_router(users.router)
app.include_router(auth_router)
app.include_router(categories.router)
app.include_router(transactions.router)


@pytest.fixture(scope='module', autouse=True)
def client() -> Generator:
    initializer(['db.models'], db_url='sqlite:///:memory')
    with TestClient(app) as c:
        yield c
    finalizer()


@pytest.fixture
def get_token(client: TestClient):
    response = client.post('/token/', data=user_data)
    token = response.json().get('access_token')
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture()
def create_transactions(client: TestClient, get_token):
    for index in range(5):
        data = {
            'name': f'Test transaction={index}',
            'category': 1,
            'sum': 1000,
            'type': True
        }
        client.post('/transactions/create', json=data, headers=get_token)


def test_create_user(client: TestClient):
    response = client.post('/token/sign-up', json=user_data)
    assert response.status_code == 200
    assert 'access_token' in response.json().keys()


def test_authorization_error(client: TestClient):
    response = client.get('/users/detail/1')
    assert response.status_code == 401


def test_wrong_login_credentials(client: TestClient):
    data = {
        'username': 'test_user',
        'password': 'wrong_passoword'
    }
    response = client.post('/token/', data=data)
    assert response.status_code == 401


def test_success_login(client: TestClient):
    response = client.post('/token/', data=user_data)
    assert response.status_code == 200
    assert 'access_token' in response.json().keys()


def test_get_detail(get_token, client: TestClient):
    response = client.get('/users/detail/1', headers=get_token)
    assert response.status_code == 200
    assert response.json().get('username') == 'test_user'


def test_edit_user(get_token, client: TestClient):
    data = {
        'use_fixed_balance': True,
        'fixed_balance': 100000
    }
    response = client.patch('/users/detail/1', json=data, headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['fixed_balance'] == 100000
    assert response_data['use_fixed_balance'] is True


def test_create_category(get_token, client: TestClient):
    data = {
        'name': 'Test category'
    }
    response = client.post('/categories/create', json=data, headers=get_token)
    assert response.status_code == 200
    assert 'name' in response.json()


def test_edit_category(get_token, client: TestClient):
    data = {'name': 'Edited test category'}
    response = client.patch('/categories/detail/1/edit', json=data, headers=get_token)
    assert response.status_code == 200
    assert response.json().get('name') == 'Edited test category'


def test_list_of_categories(get_token, client: TestClient):
    for index in range(5):
        data = {
            'name': f'Test category-{index}'
        }
        client.post('/categories/create', json=data, headers=get_token)

    response = client.get('/categories/all', headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data.get('categories')) == 6


def test_create_transaction(get_token, client: TestClient):
    data = {
        'name': 'Test transaction',
        'category': 1,
        'sum': 1000,
        'type': True
    }
    response = client.post('/transactions/create', json=data, headers=get_token)
    assert response.status_code == 200
    data = response.json()
    assert 'number' in data.keys()
    assert data['sum'] == 1000


def test_edit_transactions(get_token, client: TestClient):
    data = {'sum': 2000}
    response = client.patch('/transactions/detail/1/edit', json=data, headers=get_token)
    assert response.status_code == 200
    assert response.json().get('sum') == 2000


def test_list_of_transactions(get_token, client: TestClient, create_transactions):
    response = client.get('/transactions/all', headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data.get('transactions')) == 6


def test_delete_transaction(get_token, client: TestClient):
    response = client.delete('/transactions/detail/1/delete', headers=get_token)
    assert response.status_code == 200


@pytest.mark.skip(reason='Sqlite and Tortoise don`t support date period lookups')
def test_list_of_transactions_by_period(get_token, client: TestClient, create_transactions):
    """ There is a problem with testing filtering by period. Sqlite and Tortoise
        don`t support date period lookups. Only with postgres.
     """
    event_loop = client.task.get_loop()

    async def change_transaction_data():
        transaction_to_edit = await Transaction.first()
        transaction_to_edit.created = datetime(2021, 7, 21)
        await transaction_to_edit.save()
    event_loop.run_until_complete(change_transaction_data())

    response = client.get('/transactions/all/statistic/month/7', headers=get_token)
    assert response.status_code == 200
    assert len(response.json()['transactions']) == 1


def test_list_of_transactions_by_type(get_token, client: TestClient, create_transactions):
    event_loop = client.task.get_loop()

    async def change_transactions_type():
        transaction_to_edit = await Transaction.first()
        transaction_to_edit.type = False
        await transaction_to_edit.save()
    event_loop.run_until_complete(change_transactions_type())

    response = client.get('/transactions/all/false', headers=get_token)
    assert response.status_code == 200
    assert len(response.json()['transactions']) == 1


def test_user_balance(get_token, client: TestClient, create_transactions):
    response = client.get('/users/detail/1', headers=get_token)
    assert response.status_code == 200
    assert response.json()['balance'] != 0


def test_user_fixed_balance(get_token, client: TestClient):
    edit_user_data = {
        'use_fixed_balance': True,
        'fixed_balance': 1000
    }
    data = {
        'name': 'Test transaction',
        'category': 1,
        'sum': 1001,
        'type': True
    }
    user_edit_response = client.patch('/users/detail/1', json=edit_user_data, headers=get_token)
    assert user_edit_response.status_code == 200

    response = client.post('/transactions/create', json=data, headers=get_token)
    assert response.status_code == 200

    response_user_messages = client.get('/users/detail/1/messages', headers=get_token)
    assert response_user_messages.status_code == 200
    assert len(response_user_messages.json()['messages']) == 1


def test_transaction_by_category(get_token, client: TestClient, create_transactions):
    response = client.get('/transactions/all/by_category/1', headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert response_data['transactions'][0]['category_id'] == 1


def test_transactions_by_category_with_type(get_token, client: TestClient, create_transactions):
    # Start prepare
    data = {
        'name': 'Second category'
    }
    client.post('/categories/create', json=data, headers=get_token)
    data = {
        'name': 'With second category',
        'category': 2,
        'sum': 5,
        'type': True
    }
    client.post('/transactions/create', json=data, headers=get_token)
    data['type'] = False
    client.post('/transactions/create', json=data, headers=get_token)
    # End prepare
    response_all = client.get('/transactions/all/by_category/2', headers=get_token)
    assert response_all.status_code == 200
    assert len(response_all.json()['transactions']) == 2
    response = client.get('/transactions/all/by_category/2', headers=get_token, params={'transaction_type': True})
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data['transactions']) == 1
    assert response_data['transactions'][0]['category_id'] == 2

    response_false = client.get('/transactions/all/by_category/2', headers=get_token,
                                params={'transaction_type': False})
    assert response_false.status_code == 200
    response_false_data = response_false.json()
    assert len(response_false_data['transactions']) == 1
    assert response_false_data['transactions'][0]['category_id'] == 2
    assert response_false_data['transactions'][0]['type'] is False


def test_delete_category(get_token, client: TestClient):
    response = client.delete('/categories/detail/1/delete', headers=get_token)
    assert response.status_code == 200
