import pytest
from base64 import b64decode
import re

try:
    from django.core.management import call_command, CommandError
    have_django = True
except ImportError:
    have_django = False


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_new_salt_raw(capsys):
    call_command('newsalt')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    new_salt = eval(captured.out)
    assert isinstance(new_salt, bytes)
    assert len(new_salt) == 8


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_new_salt_encoded(capsys):
    call_command('newsalt', '--encode')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    new_salt = b64decode(captured.out)
    assert isinstance(new_salt, bytes)
    assert len(new_salt) == 8


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_listsecrets_empty(capsys):
    call_command('listsecrets')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    message = captured.out.strip()
    assert message == 'No secrets'


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_putsecret(capsys):
    call_command('putsecret', 'foo', 'bar')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    message = captured.out.strip()
    assert message == 'Updated "foo" in vault'


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_listsecrets_withfoo(capsys):
    call_command('listsecrets')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    lines = captured.out.split('\n')
    assert lines[0] == 'Secrets:'
    assert re.match(r'^\s+foo = bar', lines[1])


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_getsecret_foo(capsys):
    call_command('getsecret', 'foo')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    message = captured.out.strip()
    assert message == 'bar'


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_getsecret_notfound():
    with pytest.raises(CommandError) as err:
        call_command('getsecret', 'bar')


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_rmsecret_notfound():
    with pytest.raises(CommandError) as err:
        call_command('rmsecret', 'bar')


@pytest.mark.skipif(not have_django, reason='Django is not installed')
def test_rmsecret_foo(capsys):
    call_command('rmsecret', 'foo')
    captured = capsys.readouterr()
    assert len(captured.err) == 0
    message = captured.out.strip()
    assert message == 'Removed "foo" from vault'

