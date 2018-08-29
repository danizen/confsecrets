from django.core.management.base import BaseCommand, CommandError
from confsecrets.config import configure_vault_parser


class Command(BaseCommand):

    def add_arguments(self, parser):
        configure_vault_parser(parser)
        parser.description = 'Stores a secret value into the vault'

    def handle(self, *args, **opts):
        raise CommandError('Not yet implemented')
