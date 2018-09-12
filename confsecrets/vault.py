"""
Implement a generic Vault class and encode concept of a DefaultVaault in a singleton.
"""
import os
from threading import Lock
from collections import UserDict, OrderedDict
from .config import Config
from .pbe import PBEUtil
import json

__all__ = ('VAULT_MAGIC', 'VaultPathMissing', 'VaultNotFound', 'VaultFormatError', 'Vault', 'DefaultVault',)


VAULT_MAGIC = 5986667612


class VaultPathMissing(Exception):
    """
    A path for the vault is required
    """
    pass


class VaultNotFound(Exception):
    """
    The vault does not exist and is not writable
    """
    pass


class VaultFormatError(Exception):
    """
    The vault has an invalid format
    """
    pass


class Vault(UserDict):
    """
    A vault is a dict whose items are stored encrypted in memory and mirrored onto the disk.
    """

    def __init__(self, salt=None, key=None, path=None):
        self.pbe = PBEUtil(key, salt)
        if path is None:
            raise VaultPathMissing()
        self.path = path
        self.data = {}
        self.last_status = None
        self.lock = Lock()
        self.freshen()

    def status(self):
        try:
            return os.stat(self.path)
        except FileNotFoundError:
            return None

    def __read_local(self):
        with open(self.path, 'r') as f:
            new_data = json.load(f)
            if not isinstance(new_data, dict):
                raise VaultFormatError()
            if 'magic' not in new_data:
                raise VaultFormatError()
            if new_data['magic'] != VAULT_MAGIC:
                raise VaultFormatError()
            self.data = new_data['data']

    def __write_local(self):
        vault_data = {
            'magic': VAULT_MAGIC,
            'data': OrderedDict(sorted(self.data.items(), key=lambda item: item[0]))
        }
        with open(self.path, 'w') as f:
            json.dump(vault_data, f)
            f.flush()

    def read(self):
        self.lock.acquire()
        try:
            self.__read_local()
        finally:
            self.lock.release()

    def write(self):
        self.lock.acquire()
        try:
            self.__write_local()
        finally:
            self.lock.release()

    def freshen(self):
        current_status = self.status()
        if current_status != self.last_status:
            self.read()
            self.last_status = current_status

    def __getitem__(self, name):
        self.freshen()
        encrypted_value = super().__getitem__(str(name))
        return self.pbe.decrypt(encrypted_value)

    def __setitem__(self, name, value):
        self.freshen()
        encrypted_value = self.pbe.encrypt(value).decode('utf-8')
        retval = super().__setitem__(str(name), encrypted_value)
        self.write()
        return retval

    def keys(self):
        self.freshen()
        return self.data.keys()

    def __delitem__(self, name):
        self.freshen()
        return super().__delitem__(str(name))

    def __repr__(self):
        return '<Vault object path=%s>' % self.path


class DefaultVault(Vault):
    """
    A singleton vault whose parameters come from the environment by default
    The parameters can be initialized by calling `init` classmethod before instantiating
    """
    __instance = None
    __salt = os.environ.get(Config.SALT.value, None)
    __key = os.environ.get(Config.KEY.value, None)
    __path = os.environ.get(Config.PATH.value, None)

    def __new__(cls):
        if cls.__instance is None:
            DefaultVault.__instance = object.__new__(cls)
        return DefaultVault.__instance

    def __init__(self):
        salt = DefaultVault.__salt
        key = DefaultVault.__key
        path = DefaultVault.__path
        super().__init__(salt, key, path)

    @classmethod
    def init(cls, salt=None, key=None, path=None):
        """
        Change the defaults before the vault is initialized, or it has no affect
        """
        DefaultVault.__salt = salt
        DefaultVault.__key = key
        DefaultVault.__path = path
