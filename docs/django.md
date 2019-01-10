---
title: confsecrets | Django Integration
---

## Secrets

Secrets are the primary way that confsecrets integrates with web frameworks like Django. These secrets are typically declared as static objects in your settings, like this:

        from confsecrets import Secret
        
        ...
        
        SOCK_COLOR = Secret('sockcolor', vault=VAULT)
        UNDERWEAR = Secret('has_underwear', vault=VAULT)

Secrets behave like strings under the appropriate circumstance:

        print('His socks are %s' % settings.SOCK_COLOR)
        

Secrets behave like booleans under the appropriate circumstance:

        print('He wears underwear' if settings.UNDERWEAR else 'He has no underwear')

However, to use secrets, you must first declare a vault.


## Initializing the Vault

You need to create the vault in your settings file:

    from confsecrets.vault import Vault
    from confsecrets.vault import Config

    ...

    VAULT = Vault(
        salt=b'abcd1234',
        key='Every good boy does fine',
        path=os.environ.get(Config.PATH.value)
    )

!!! Note
    Putting the encrypted material (vault file), salt, and clear text key in the
    same git repository is no more than obfuscation.  For best security, these should
    only come together on the developer's desktop, in continuous integration (Jenkins),
    and on deployed servers.


## Management Commands

`confsecrets` has no management commands, because it is not a Django app.
You can use the console command `confsecrets` instead.


## Common Errors

If you use a secret that does not exist in the vault, you will get a `KeyError`, just as if you were accessing a value that is not present in a dictionary.
