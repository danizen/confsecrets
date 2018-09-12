import sys
from django.core.management.base import BaseCommand, CommandError

from . import VaultConfigMixin


class Command(VaultConfigMixin, BaseCommand):

    def add_arguments(self, parser):
        parser.description = 'Retrieves a single secret from the vault'
        parser.add_argument('secret', metavar='SECRET', help='The name of the secret you want to remove')
        self.add_vault_config(parser)

    def handle(self, *args, **opts):
        self.configure_vault(**opts)

        secret = opts['secret']
        try:
            del self.vault[secret]
            print('Removed "{}" from vault'.format(secret))
        except KeyError:
            sys.stderr.write('There is no secret "{}" in the vault\n'.format(secret))
            sys.exit(1)
