from .base import *


ALLOWED_HOSTS = [
    '0.0.0.0',
    '127.0.0.1',
]


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'i)34=z)*k0@#2poya4%)(9+u-6f=azndpp@q+lrdlgncq^4+f1'
DEBUG = True

INSTALLED_APPS += ("debug_toolbar", )

MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware', )
