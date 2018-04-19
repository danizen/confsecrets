from django.apps import AppConfig
from django.conf import settings

from confsecrets.config import Config


class ConfsecretsConfig(AppConfig):
    name = 'confsecrets'
    verbose_name = 'Configuration Secrets Vault'

