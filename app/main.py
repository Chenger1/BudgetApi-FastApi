from fastapi import FastAPI
import uvicorn

from routers import users, categories, transactions, admin
from utils.authentication import router as auth_router, get_password_hash

from tortoise.contrib.fastapi import register_tortoise
from utils.database import TORTOISE_ORM
from logger import log

from db.models import User
import config

app = FastAPI()
app.include_router(users.router)
app.include_router(auth_router)
app.include_router(categories.router)
app.include_router(transactions.router)
app.include_router(admin.router)

register_tortoise(
    app=app,
    config=TORTOISE_ORM,
    generate_schemas=True,
    add_exception_handlers=True
)


@app.on_event('startup')
async def startup_event():
    password = get_password_hash(config.ADMIN_PASSWORD)
    _ = await User.get_or_create(
        username=config.ADMIN_USERNAME,
        defaults={'email': config.ADMIN_EMAIL, 'is_admin': True,
                  'password': password}
    )


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
    log.info('App started')
