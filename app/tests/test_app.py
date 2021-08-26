import pytest
from fastapi.testclient import TestClient
from fastapi import FastAPI

from typing import Generator

from tortoise.contrib.test import finalizer, initializer

from routers import users, categories, transactions
from authentication import router as auth_router

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
        'sum': 1000
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


def test_list_of_transactions(get_token, client: TestClient):
    for index in range(5):
        data = {
            'name': f'Test transaction-{index}',
            'category': 1,
            'sum': 1000
        }
        client.post('/transactions/create', json=data, headers=get_token)

    response = client.get('/transactions/all', headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data.get('transactions')) == 6


def test_delete_transaction(get_token, client: TestClient):
    response = client.delete('/transactions/detail/1/delete', headers=get_token)
    assert response.status_code == 200


def test_delete_category(get_token, client: TestClient):
    response = client.delete('/categories/detail/1/delete', headers=get_token)
    assert response.status_code == 200
