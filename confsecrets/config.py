"""
Implements Configuration of confsecrets
"""
from enum import Enum
from argparse import ArgumentParser

__all__ = (
    'Config',
    'configure_vault_parser',
)


class Config(Enum):
    """
    Things that may appear in environment or settings
    """
    SALT = 'CONFSECRETS_SALT'
    KEY = 'CONFSECRETS_KEY'
    PATH = 'CONFSECRETS_PATH'


def configure_vault_parser(parser=None):
    if not parser:
        parser = ArgumentParser()
    parser.add_argument('--salt', metavar='SALT', default=None,
                        help='Salt for confsecrets.vault')
    parser.add_argument('--key', metavar='KEY', default=None,
                        help='Text from which a binary key is derived')
    parser.add_argument('--path', metavar='PATH', default=None,
                        help='PAth to the vault')
    return parser