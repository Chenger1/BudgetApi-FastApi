from app.main import app
from db.models import User
import config
from authentication import get_password_hash


@app.on_event('startup')
async def startup_event():
    password = get_password_hash(config.ADMIN_PASSWORD)
    await User.create(
        username=config.ADMIN_USERNAME,
        password=password,
        email=config.ADMIN_EMAIL,
        is_admin=True
    )
