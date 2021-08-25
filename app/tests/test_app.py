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


#  Just learn how to write async tests
@pytest.mark.asyncio
async def test_create_user():
    data = {
        'username': 'test_user',
        'password': 'test_password'
    }
    async with AsyncClient(app=app, base_url='http://127.0.0.1:8000') as ac:
        response = await ac.post('/token/sign-up', json=data)
        assert response.status_code == 200
        assert 'access_token' in response.json().keys()
