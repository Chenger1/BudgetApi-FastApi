import environs


env = environs.Env()
env.read_env()

DB_NAME = env.str('DB_NAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')
