import pytest
from base64 import b64decode

try:
    from django.core.management import call_command
    have_django = True
except ImportError:
    have_django = False


if not have_django:
    pytest.skip('Django is not installed')


def test_new_salt_raw(capsys):
    call_command('newsalt')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    new_salt = eval(captured.out)
    assert isinstance(new_salt, bytes)
    assert len(new_salt) == 8


def test_new_salt_encoded(capsys):
    call_command('newsalt', '--encode')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    new_salt = b64decode(captured.out)
    assert isinstance(new_salt, bytes)
    assert len(new_salt) == 8


