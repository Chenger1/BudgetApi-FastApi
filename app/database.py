import config

from tortoise.contrib.fastapi import register_tortoise



TORTOISE_ORM = {
    'connections': {'default': {
        'engine': 'tortoise.backends.asyncpg',
        'credentials': {
            'database': config.DB_NAME,
            'host': config.DB_HOST,
            'password': config.DB_PASSWORD,
            'port': '5432',
            'user': config.DB_USER
        }
    }},
    'apps': {
        'models': {
            'models': ['db.models', 'aerich.models'],
            'default_connection': 'default'
        }
    }
}

# register_tortoise(
#     app=app,
#     config=TORTOISE_ORM,
#     generate_schemas=True,
#     add_exception_handlers=True
# )
