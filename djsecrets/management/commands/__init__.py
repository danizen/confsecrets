from confsecrets.vault import DefaultVault


class VaultConfigMixin:
    """
    Defines arguments to configure the default vault
    """

    def add_vault_config(self, parser):
        parser.add_argument('--salt', metavar='SALT', default=None,
                            help='Salt for confsecrets.vault')
        parser.add_argument('--key', metavar='KEY', default=None,
                            help='Text from which a binary key is derived')
        parser.add_argument('--path', metavar='PATH', default=None,
                            help='PAth to the vault')
        return parser

    def configure_vault(self, **opts):
        salt = opts.get('salt', None)
        key = opts.get('key', None)
        path = opts.get('path', None)
        DefaultVault.init(salt=salt, key=key, path=path)
        self.vault = DefaultVault()
