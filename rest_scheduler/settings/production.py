from .base import *
import dj_database_url


ALLOWED_HOSTS = [
    'afternoon-depths-71837.herokuapp.com',
    'restscheduler.wilsonsantos.pro',
]

DEBUG = False

SECRET_KEY = get_env_variable('DJANGO_SECRET_KEY')

# Heroku: Update database configuration from $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)
