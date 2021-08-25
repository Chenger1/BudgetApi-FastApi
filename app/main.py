from fastapi import FastAPI
import uvicorn

from db.database import engine
from db.models import Base

from routers import users, categories, transactions
from authentication import router as auth_router


Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(users.router)
app.include_router(auth_router)
app.include_router(categories.router)
app.include_router(transactions.router)


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
