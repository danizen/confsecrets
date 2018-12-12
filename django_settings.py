import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '98o09e8cueuonehunthoehu0oe8u09eo80'

CONFSECRETS_SALT = b'abcd1234'
CONFSECRETS_PATH = os.path.join(BASE_DIR, '.vault')
CONFSECRETS_KEY = 'Not a good password'

INSTALLED_APPS = (
    'djsecrets',
)
