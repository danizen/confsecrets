from Crypto import Random
from Crypto.Hash.HMAC import HMAC
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from base64 import b64encode, b64decode
import string
from enum import Enum
from six.moves import shlex_quote

__all__ = ['MessageTooShort','InvalidMessageAuthenticationCode', 'PasswordTooSimple','PasswordNotShellSafe', 'PasswordUtil', 'PBEUtil', 'CClass',]


class MessageTooShort(Exception):
    """
    Encrypted message/password too short; the encrypted message must be at least 48 bytes.
    """
    pass


class InvalidMessageAuthenticationCode(Exception):
    """
    Message authentication code invalid; the encrypted message must have been created by different software or with a different password.
    """
    pass


class PasswordTooSimple(Exception):
    """
    The password must be at least 12 characters long and include an uppercase letter,
    a lower case letter, a symbol, and a digit.
    """
    pass


class PasswordNotShellSafe(Exception):
    """
    This password requires quoting in a bash shell, and thus causes operational risk.
    """
    pass


class CClass(Enum):
    LOWER = 1
    UPPER = 2
    DIGIT = 3
    SYMBOL = 4
    SPACE = 5
    OTHER = 6

    @classmethod
    def classes(cls, password):
        def character2class(c):
            if c in string.ascii_lowercase:
                return cls.LOWER
            elif c in string.ascii_uppercase:
                return cls.UPPER
            elif c in string.digits:
                return cls.DIGIT
            elif c in string.punctuation:
                return cls.SYMBOL
            elif c in string.whitespace:
                return cls.SPACE
            else:
                return cls.OTHER
        return set(map(character2class, password))


class PasswordUtil():

    required_classes = {CClass.LOWER, CClass.UPPER, CClass.DIGIT, CClass.SYMBOL}
    min_length = 12

    """
    The password util provides a mechanism to check and generate passwords
    """
    @classmethod
    def check(cls, password):
        """
        Checks password strength as follows:
            - At least min_length characters
            - At least one lowercase, uppercase, numeric, and symbolic character
            - Safe for the Linux shell, e.g. does not require escaping

        :param password: a password string
        :return: nothing if password is OK, raises if password is not ok
        """
        # Check password length
        if len(password) < cls.min_length:
            raise PasswordTooSimple
        # Map characters to character classes
        classes = CClass.classes(password)
        # Make sure you have needed classes
        if not cls.required_classes.issubset(classes):
            raise PasswordTooSimple()
        # Check if the password is safe for the shell
        if shlex_quote(password) != password:
            raise PasswordNotShellSafe()


class PBEUtil(object):
    """
    A Cryptor handles symmetric encryption using binary keys derived from clear text keys
    The algorithm for key derivation is PBKDF2 with SHA256.
    The algorithm for encryption is AES 256 (key_size==32 bytes).
    By default there are 1007 iterations.
    The message includes the IV and the encrypted data.
    There is no message authentication on these, the HMAC is used only in key derivation.

    See RFC-2898 for a definition of the algorithms.
    """
    salt = b'\xe2\x98\xe5\xdc\xeb\xf5\xcc\xd8'
    iterations = 1007
    key_size = 32

    def __init__(self, password, salt=None):
        if not isinstance(password, bytes):
            password = str(password).encode('utf-8')
        self.password= password
        if salt is not None:
            self.salt = bytes(salt)
        self.__key = None

    @property
    def key(self):
        """
        Compute a derived key based on attributes on this object.
        """
        if self.__key is None:
            def proof(password, salt):
                return HMAC(password, salt, SHA256).digest()
            self.__key = PBKDF2(self.password, self.salt, self.key_size, self.iterations, prf=proof)
        return self.__key

    def encrypt_guts(self, cleartext):
        """
        Encrypt some clear text and return and encrypted message bytes

        :param cleartext: a str
        :return: encrypted message including the IV and the ciphertext
        """
        if isinstance(cleartext, str):
            cleartext = cleartext.encode('utf-8')
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        ciphertext = cipher.encrypt(cleartext)
        return iv + ciphertext

    def decrypt_guts(self, message):
        """
        Decrypt a message using an IV and some encrypted bytes

        :param: message: must be bytes including iv and ciphertext
        :return: A clear text string
        """
        iv = message[0:16]
        ciphertext = message[16:]
        cipher = AES.new(self.key, AES.MODE_CFB, iv)
        return cipher.decrypt(ciphertext)

    def encrypt(self, cleartext):
        """
        Encrypt some clear text, returning a Base64 message including mac, an iv, and ciphertext

        :param cleartext: a str
        :return: Base64 encoded encrypted bytes with a mac
        """
        message_bytes = self.encrypt_guts(cleartext)
        mac = HMAC(self.key, message_bytes, SHA256).digest()
        return b64encode(mac + message_bytes)

    def decrypt(self, message):
        """
        Decrypt a message that is encoded in Base64 consisting of a mac, an iv, and ciphertext

        :param: message: must be a base64 encoded string
        :return: A clear text string
        """
        message_bytes = b64decode(message)
        if len(message_bytes) < 48:
            raise MessageTooShort()
        expect_mac = message_bytes[0:32]
        actual_mac = HMAC(self.key, message_bytes[32:], SHA256).digest()
        if actual_mac != expect_mac:
            raise InvalidMessageAuthenticationCode()
        clear_bytes = self.decrypt_guts(message_bytes[32:])
        return clear_bytes.decode('utf-8')
