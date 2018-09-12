---
title: Django Integration
---

## Settings

The `djsecrets` module supports the following settings:

* `CONFSECRETS_SALT` - This must be a binary value at least 8-bytes long, and should be unique between projects.
* `CONFSECRETS_PATH` - The path where this module will look for your secrets.
* `CONFSECRETS_KEY` - This is a clear text key.

Environment variables for all settings are supported; the django settings apply only to `djsecrets` whereas the 
environment variables are implemented in `confsecrets`.

!!! Note
    Putting the encrypted material (vault file), salt, and clear text key in the
    same git repository is no more than obfuscation.  For best security, these should
    only come together on the developer's desktop, in continuous integration (Jenkins),
    and on deployed servers.

## Secrets

Secrets are typically declared as static objects in your settings, like this:

        from djsecrets import Secret
        
        ...
        
        SOCK_COLOR = Secret('sockcolor')
        UNDERWEAR = Secret('has_underwear')

Secrets behave like strings under the appropriate circumstance:

        print('His socks are %s' % settings.SOCK_COLOR)
        
Secrets behave like booleans under the appropriate circumstance:

        print('He wears underwear' if settings.UNDERWEAR else 'He has no underwear')

## Management Commands

`djsecrets` supports the following management commands:

* `newsalt` - Generates a new salt using a secure PRNG 
* `listsecrets` - Lists secrets and their values in the vault
* `getsecret` - Gets the value of a secret from the vault
* `putsecret` - Puts a new value for a secret into the vault
* `rmsecret` - Removes a secret from a vault

## Common Errors

If you use a secret that does not exist in the vault, you will get a `KeyError`, just as if you were accessing 
a value that is not present in a dictionary.
