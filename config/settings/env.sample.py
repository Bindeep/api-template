from .base import *

INSTALLED_APPS += (
    'debug_toolbar',
    'drf_yasg',
    'django_extensions'
)

MIDDLEWARE += (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
)

INTERNAL_IPS = ['127.0.0.1', ]

ALLOWED_HOSTS = ['*']

CORS_ORIGIN_ALLOW_ALL = True
