from django.core.management.base import BaseCommand
from Crypto.Random import get_random_bytes


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.description = 'Generate a new random salt'

    def handle(self, *args, **opts):
        salt = get_random_bytes(8)
        print(salt)
