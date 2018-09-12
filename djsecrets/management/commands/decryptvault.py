from django.core.management.base import BaseCommand, CommandError

from . import VaultConfigMixin


class Command(VaultConfigMixin, BaseCommand):

    def add_arguments(self, parser):
        parser.description = 'Decrypts the vault to the console'
        self.add_vault_config(parser)

    def handle(self, *args, **opts):
        self.configure_vault(**opts)
        raise CommandError('Not yet implemented')
