from httpx import AsyncClient
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient

from db.database import Base
from dependecies import get_db

from app.main import app

import contextlib


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


user_data = {
    'username': 'test_user',
    'password': 'test_password'
}


def override_get_db():
    """ Use test db instead of real """
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def drop_db():
    meta = Base.metadata
    with contextlib.closing(engine.connect()) as conn:
        trans = conn.begin()
        for table in reversed(meta.sorted_tables):
            conn.execute(table.delete())
        trans.commit()


@pytest.fixture(scope='session', autouse=True)
def teardown(request):
    request.addfinalizer(drop_db)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


@pytest.fixture
def get_token():
    response = client.post('/token/', data=user_data)
    token = response.json().get('access_token')
    return {'Authorization': f'Bearer {token}'}


#  Just learn how to write async tests
@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post('/token/sign-up', json=user_data)
        assert response.status_code == 200
        assert 'access_token' in response.json().keys()


def test_authorization_error():
    response = client.get('/users/detail/1')
    assert response.status_code == 401


def test_wrong_login_credentials():
    data = {
        'username': 'test_user',
        'password': 'wrong_passoword'
    }
    response = client.post('/token/', data=data)
    assert response.status_code == 401


def test_success_login():
    response = client.post('/token/', data=user_data)
    assert response.status_code == 200
    assert 'access_token' in response.json().keys()


def test_get_detail(get_token):
    response = client.get('/users/detail/1', headers=get_token)
    assert response.status_code == 200
    assert response.json().get('username') == 'test_user'


def test_create_category(get_token):
    data = {
        'name': 'Test category',
        'user_id': 1
    }
    response = client.post('/categories/create', json=data, headers=get_token)
    assert response.status_code == 200
    assert 'name' in response.json()


def test_edit_category(get_token):
    data = {'name': 'Edited test category'}
    response = client.patch('/categories/detail/1/edit', json=data, headers=get_token)
    assert response.status_code == 200
    assert response.json().get('name') == 'Edited test category'


def test_list_of_categories(get_token):
    for index in range(5):
        data = {
            'name': f'Test category-{index}',
            'user_id': 1
        }
        client.post('/categories/create', json=data, headers=get_token)

    response = client.get('/categories/all', headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data.get('categories')) == 6


def test_delete_category(get_token):
    response = client.delete('/categories/detail/1/delete', headers=get_token)
    assert response.status_code == 200


def test_create_transaction(get_token):
    data = {
        'name': 'Test transaction',
        'user_id': 1,
        'category_id': 1,
        'sum': 1000
    }
    response = client.post('/transactions/create', json=data, headers=get_token)
    assert response.status_code == 200
    data = response.json()
    assert 'number' in data.keys()
    assert data['sum'] == 1000


def test_edit_transactions(get_token):
    data = {'sum': 2000}
    response = client.patch('/transactions/detail/1/edit', json=data, headers=get_token)
    assert response.status_code == 200
    assert response.json().get('sum') == 2000


def test_list_of_transactions(get_token):
    for index in range(5):
        data = {
            'name': f'Test transaction-{index}',
            'user_id': 1,
            'category_id': 1,
            'sum': 1000
        }
        client.post('/transactions/create', json=data, headers=get_token)

    response = client.get('/transactions/all', headers=get_token)
    assert response.status_code == 200
    response_data = response.json()
    assert len(response_data.get('transactions')) == 6


def test_delete_transaction(get_token):
    response = client.delete('/transactions/detail/1/delete', headers=get_token)
    assert response.status_code == 200
