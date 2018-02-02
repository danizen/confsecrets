from unittest import TestCase
from confsecrets.pbe import *
from base64 import b64decode, b64encode


class TestPBEUtil(TestCase):

    def testEncryptDecrypt(self):
        """
        Verify that the cryptor can do a roound trip encryption
        """
        expected_text = 'This message must go round a bunch'
        pbe = PBEUtil('This is the password')
        crypt_message = pbe.encrypt(expected_text)
        actual_text = pbe.decrypt(crypt_message)
        self.assertEquals(actual_text, expected_text)

    def testKeyDerivation(self):
        """
        Test that key derived from the same password is the same
        """
        pbe = PBEUtil('This is the password')
        other_pbe = PBEUtil('This is the password')
        self.assertEquals(pbe.key, other_pbe.key)

    def testDifferentPasswordDifferentKey(self):
        """
        Test that changes the password changes the key
        """
        pbe = PBEUtil('This is the password')
        other_pbe = PBEUtil('This is the other password')
        self.assertNotEquals(pbe.key, other_pbe.key)

    def testDifferentSaltDifferentKey(self):
        """
        Test that changing the salt changes the key
        """
        pbe = PBEUtil('This is the password')
        other_pbe = PBEUtil('This is the password', salt= b'\x88\xb0m*\x92\x18\xab\xc3')
        self.assertNotEquals(pbe.key, other_pbe.key)

    def testLengthError(self):
        """
        Test that the length of the message is checked
        """
        pbe = PBEUtil('This is the password')
        message = pbe.encrypt('This is the message')
        message_bytes = b64decode(message)
        truncated_message = b64encode(message_bytes[0:47])
        with self.assertRaises(MessageTooShort):
            pbe.decrypt(truncated_message)

    def testAlteredMACError(self):
        """
        Test that the MAC is checked
        """
        pbe = PBEUtil('This is the password')
        message = pbe.encrypt('This is the message')
        message_bytes = bytearray(b64decode(message))
        # We use XOR here because we need to know it will change
        message_bytes[20] = message_bytes[20] ^ 0xff
        altered_message= b64encode(message_bytes)
        with self.assertRaises(InvalidMessageAuthenticationCode):
            pbe.decrypt(altered_message)


class TestPasswordUtil(TestCase):

    def test_too_short(self):
        with self.assertRaises(PasswordTooSimple):
            PasswordUtil.check('abc')

    def test_too_simple(self):
        with self.assertRaises(PasswordTooSimple):
            PasswordUtil.check('11abcdefghijKLMNOPqrstuv22')

    def test_not_shell_safe(self):
        with self.assertRaises(PasswordNotShellSafe):
            PasswordUtil.check('11abcdefghijKL   -MNOPqrstuv22')
        with self.assertRaises(PasswordNotShellSafe):
            PasswordUtil.check('11abcdefghijKL${HOME}MNOPqrstuv22')

    def test_ok(self):
        PasswordUtil.check('11,abcdefghijKLMNOPqrstuv,22')

    def test_generate(self):
        length = len(PasswordUtil.generate(length=2))
        self.assertEquals(length, PasswordUtil.min_length)
        extra_length = len(PasswordUtil.generate(length=16))
        self.assertEquals(extra_length, 16)
