from .base import *  # noqa: F401, F403

PIVOTALTRACKER_TOKEN_API = 'r5lhdmdz9c6efake'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'circle_test',
        'USER': 'circleci',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
    }
}
