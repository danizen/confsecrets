from django.core.management.base import BaseCommand

from . import VaultConfigMixin


class Command(VaultConfigMixin, BaseCommand):

    def add_arguments(self, parser):
        parser.description = 'Stores a secret value into the vault'
        parser.add_argument('secret', metavar='SECRET', help='The name of the secret you want to remove')
        parser.add_argument('value', metavar='VALUE', help='The value for the secret')
        self.add_vault_config(parser)

    def handle(self, *args, **opts):
        self.configure_vault(**opts)

        secret = opts['secret']
        value = opts['value']
        self.vault[secret] = value

        print('Updated "{}" in vault'.format(secret))
