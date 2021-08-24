from fastapi import FastAPI, Request, Response

from db.database import SessionLocal, engine
from db.models import Base

from routers import users
from authentication import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(users.router)
app.include_router(auth_router)


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response
