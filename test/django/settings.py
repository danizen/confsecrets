from confsecrets import Secret


SECRET_KEY = 'eq3e9rklb)q5k@!@d^^94l4ldut)uev3#axpj_3j62&$upocex'

INSTALLED_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.auth',
    'confsecrets.django',
]

ASECRET = Secret('ASECRET')
