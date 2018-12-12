import os
try:
    from django.conf import settings
    have_django = True
except ImportError:
    have_django = False

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

settings_dict = {
    'BASE_DIR': BASE_DIR,
    'SECRET_KEY': '98o09e8cueuonehunthoehu0oe8u09eo80',
    'CONFSECRETS_SALT': b'abcd1234',
    'CONFSECRETS_PATH': os.path.join(BASE_DIR, '.vault'),
    'CONFSECRETS_KEY': 'Not a good password',
    'INSTALLED_APPS': (
        'djsecrets',
    )
}

def pytest_configure():
    if have_django:
        settings.configure(**settings_dict)

