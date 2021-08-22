from fastapi import FastAPI, Request, Response, Depends
from typing import List
from sqlalchemy.orm import Session

from db.database import SessionLocal, engine
from db.models import Base
from db.schema import User


Base.metadata.create_all(bind=engine)


app = FastAPI()


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


def get_db(request: Request):
    return request.state.db


@app.get('/users/')
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return 200
