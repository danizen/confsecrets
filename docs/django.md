---
title: confsecrets | Django Integration
---

## Secrets

Secrets are the primary way that confsecrets integrates with web frameworks like Django. These secrets are typically declared as static objects in your settings, like this:

        from confsecrets import Secret
        
        ...
        
        SOCK_COLOR = Secret('sockcolor')
        UNDERWEAR = Secret('has_underwear')

Secrets behave like strings under the appropriate circumstance:

        print('His socks are %s' % settings.SOCK_COLOR)
        

Secrets behave like booleans under the appropriate circumstance:

        print('He wears underwear' if settings.UNDERWEAR else 'He has no underwear')

Unless you pass a vault, secrets use the DefaultVault.


## Initializing the Vault


By default, the vault takes its configuration from environment variables, however, if you place 'confsecrets.django' in your installed apps, 
then you can specify the vault's configuratio in your settings:

        INSTALLED_APPS = [
            'confsecrets.django',
        ]

        CONFSECRETS_SALT = b'\xde\x0f9\xb7\xbd1\x13\xdc'
        CONFSECRETS_PATH = '/var/lib/mydjangoapp/secrets.yaml'


!!! Note
    Putting the encrypted material (vault file), salt, and clear text key in the
    same git repository is no more than obfuscation.  For best security, these should
    only come together on the developer's desktop, in continuous integration (Jenkins),
    and on deployed servers.


## Management Commands

`confsecrets` has a management command that mirrors the console command `confsecrets`.  The only difference is that
the management command can take part of its configuration from settings.

## Common Errors

If you use a secret that does not exist in the vault, you will get a `KeyError`, just as if you were accessing a value that is not present in a dictionary.
