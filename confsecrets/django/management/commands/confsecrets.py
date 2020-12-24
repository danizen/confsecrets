from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'The confsecrets CLI with Django configuration'

    def handle(self, *args, **options):
        print('Not yet implemented')
