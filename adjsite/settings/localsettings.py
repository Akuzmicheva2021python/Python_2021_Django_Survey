from .basesettings import *
# import django_on_heroku
import dj_database_url

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('DJANGO_SECRET_KEY', default='django-insecure-^v$#^hk1zqvp25(ot!pp343b$ga7%xvno8l#$#u$!&dzaf%6h^')

DEBUG = env.bool('DJANGO_DEBUG', True)

ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

INTERNAL_IPS = []
    # '127.0.0.1',]
# django_on_heroku.settings(locals())

db_from_env = dj_database_url.config(conn_max_age=500, ssl_require=False)
DATABASES['default'].update(db_from_env)

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# DEVEL_APPS = [
#     'debug_toolbar',
# ]

# DEBUG_TOOLBAR_CONFIG = {
#     "SHOW_TOOLBAR_CALLBACK": lambda x: True,
# }
