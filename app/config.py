import environs


env = environs.Env()
env.read_env()

DB_NAME = env.str('DB_NAME')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_HOST = env.str('DB_HOST')
DB_USER = env.str('DB_USER')

MAIL_USERNAME = env.str('MAIL_USERNAME')
MAIL_PASSWORD = env.str('MAIL_PASSWORD')
MAIL_FROM = env.str('MAIL_FROM')
MAIL_PORT = env.str('MAIL_PORT')
MAIL_SERVER = env.str('MAIL_SERVER')
MAIL_FROM_NAME = env.str('MAIL_FROM_NAME')
