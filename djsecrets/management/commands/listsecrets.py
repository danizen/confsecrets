from django.core.management.base import BaseCommand, CommandError

from . import VaultConfigMixin


class Command(VaultConfigMixin, BaseCommand):

    def add_arguments(self, parser):
        parser.description = 'Lists secrets in the default vault'
        self.add_vault_config(parser)

    def handle(self, *args, **opts):
        self.configure_vault(**opts)

        if len(self.vault):
            print('Keys:')
            for key in self.vault.keys():
                print('\t{}'.format(key))
        else:
            print('No keys')
