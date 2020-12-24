import os
from base64 import b64decode
from django.apps import AppConfig
from django.conf import settings

from confsecrets.vault import DefaultVault
from confsecrets.config import Config


# Default configuration
for item in Config:
    if not hasattr(settings, item.value):
        if item == Config.SALT:
            setattr(settings, item.value, b64decode(os.environ.get(item.value, None)))
        else:
            setattr(settings, item.value, os.environ.get(item.value, None))


class SecretsAppConfig(AppConfig):
    name = 'confsecrets'
    verbose_name = 'confsecrets.django'

    def ready(self):
        DefaultVault.init(
            settings.CONFSECRETS_SALT,
            settings.CONFSECRETS_KEY,
            settings.CONFSECRETS_PATH
        )
