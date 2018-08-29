from django.apps import AppConfig
from django.conf import settings

from confsecrets.vault import DefaultVault

# load default settings
__DEFAULTS = {
    'CONFSECRETS_SALT': None,
    'CONFSECRETS_KEY': None,
    'CONFSECRETS_PATH': None,
}
for key, value in __DEFAULTS.items():
    setattr(settings, key, value)


class ConfsecretsConfig(AppConfig):
    name = 'confsecrets'
    verbose_name = 'Configuration Secrets Vault'

    def ready(self):
        salt = settings.CONFSECRETS_SALT
        key = settings.CONFSECRETS_KEY
        path = settings.CONFSECRETS_PATH

        # DefaultVault.init() is not enough - we have to create the default vault here,
        # because any secrets in settings will instantiate the default vault.
        vault = DefaultVault()
        vault.salt = salt
        vault.key = key
        vault.path = path
