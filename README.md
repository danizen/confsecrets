# confsecrets

## Summary

Simple utilities/modules to encrypt/decrypt application configuration secrets flexibly.

## Description

It is often difficult for developers to manage passwords for databases, search
engines, directory services, etc.  Security wishes to make sure these secrets
are centralized, but this adds a dependency on an external service, not to
mention code complexity.

Several solutions exist, but these are often silos without any abstraction built
around them.

The goal of this project is to provide APIs that wrap the simplest solutions that
are actually solutions, namely:
 - Keeping passwords as encrypted values on the filesystem, in the code, or in S3 objects

Some secrets may be different from passwords, but that is the blue sky future.

## API Ideas

The goal here is to reach the point where we can keep multiple secrets in the same 
encrypted wodge, decrypted with the same passwords, and provide some command-line over 
them that is easily integrated into Django.  We want to act locally but think globally.

How about this:
  - implement `confsecrets\vault.py` which contains a `Vault` class that is a subclass of UserDict, maybe OrderedDict.
  - The vault has the following init:

          Vault(key=, salt=, path=, encoder=, decoder=)

  - It implements it encrypts using the the salt and key to base64.
  - Encrypting immediately flushes the file that has been loaded
  - On decrypt, it checks to see if the file has changed, and reloads the underlying data in that case.
  - On decrypt, it reverses the process.

There is a concept of a "default vault" whose configuration is controlled by environment variables or through the API.
The "default vault" is is a singleton.   

Django integration is provided via a `confsecrets.django` application that allows the configuration to be provided by settings:

    CONFSECRETS_SALT = b'89982hto'
    CONFSECRETS_KEY = 'This is not an example'
    CONFSECRETS_VAULT = os.path.join(BASE_DIR, 'vault.yaml')

This initializes the default vault during configuration freeze.   Otherwise, the default vault's configuration is controlled by th
environment variables.

This is secure as long as the vault file is not stored in git, and then it becomes obfuscation.  However, it is easy to change the salt
as long as you aren't saving too many secrets in it.


Saving secrets becomes easy through a management command to populate the vault:

  * `decryptsecrets` - decrypts a vault to stdout
  * `encryptsecrets`- encrypts a vault from stdin
  * `listsecrets` - lists the secrets stored in the vault
  * `putsecret <name> [--value <value>]` - uses value if present, otherwise uses stdin
  * `getsecret <name>` - typical options, outputs the secret to the stdout
  * `rmsecret <name>` - removes an encrypted value from the vault

With the system configured, dealing with the vault becomes as easy as using Secret objects:

    ES_PASSWORD = Secret('name')

To access it, you can treat it like a string:

    from django.conf import settings

    settings.ES_PASSWORD.decrypt()

The secret also acts like a string:

    int(str(settings.ES_PASSWORD))

or:

    auth_string = "%s:%s" % (username, settings.ES_PASSWORD)
  
This will fail for a number of reasons with clear exceptions:
   - If  the configuration is not available via settings or environment variables
   - If the vault is not-present
   - If the vault doesn't have that key in it

Vault would then know how to deal with the operations described above.

## Development Plan

- Create `confsecrets/vault.py` with a `Vault` and `DefaultVault` class:

    - `Vault(salt=, path=, key=)` - you have to provide all of these
    - `DefaultVault()` - this is a vault that is a singleton.   It also looks at the environment variables, but still accepts salt, path, key

- Create `confsecrets\secrets.py` with a `BaseSecret` and `Secret` class.

   - `BaseSecret` has a vault, which is either provided via initializations or is the `DefaultVault`
   - `Secret` acts like a string.

- Create a `confsecrets/django.py` that implements the settings, and creates the `DefaultVault`

- Create the management commands.

## Roadmap

Not sure on the priority of these:

- Add supoprt for placing the vault in S3 or elsewhere, by trying to interpret the vault as an URL.  Vault becomes polymorphic because
  if path is an URL, then we will create a different sub-class of `Vault` using an override of `__new__`.   A local path vault is still
  standard.

- Provide non-string secrets, which sub-class `BaseSecret` but like like other Python objects.  For dict/sequence types, avoid pickle 
  for interoperation with Java.  Uses JSON, but allow the Vault to be initialized with a specific encoder/decoder.

- Add support for placing the key in a file or on S3, and provide a command to rotate keys.  This requires a `Key` class which knows
  how to get itself from wherever, or rotate itself.

- Support usage without Django by providing a confsecrets console-script and a configuration file that influences the default vault.


## Status

The only facility so far available is Password Based Encryption (PBE) on the filesystem or in the environment.

