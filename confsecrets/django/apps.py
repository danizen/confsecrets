import os
from base64 import b64decode
from django.apps import AppConfig
from django.conf import settings

from confsecrets.vault import DefaultVault
from confsecrets.config import Config

# Default configuration
for item in Config:
    if not hasattr(settings, item.value):
        value = os.environ.get(item.value, None)
        if item == Config.SALT and value:
            value = b64decode(value)
        setattr(settings, item.value, value)


class SecretsAppConfig(AppConfig
    ):
    name = 'confsecrets'
    verbose_name = 'confsecrets.django'

    def ready(self):
        DefaultVault.init(
            settings.CONFSECRETS_SALT,
            settings.CONFSECRETS_KEY,
            settings.CONFSECRETS_PATH
        )
