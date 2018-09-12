from base64 import b64encode

from django.core.management.base import BaseCommand
from Crypto.Random import get_random_bytes


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.description = 'Generate a new random salt'
        parser.add_argument('--encode', action='store_true', default=False,
                            help='Encode as Base64, rather than print as Python')

    def handle(self, *args, **opts):
        salt = get_random_bytes(8)
        if opts['encode']:
            salt = b64encode(salt).decode('utf-8')
        print(salt)

