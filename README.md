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
 - Keeping passwords as encrypted values on the filesystem, in the environment, or in S3 objects

Some secrets may be different from passwords, and so we are agnostic, at lesat
in the lower-end code, and also support encrypted YAML or JSON.

## API Ideas

We could make this more complicated by integrating with 3rd party solutions such as S3, HashiCorp vault,
or we could provide some simpler utilities.

How about this:
  - Confsecrets looks for a configuration file with three fallbacks:
      * CONFSECRETS_CONFIG - if defined, and the file exists, this is the configuration.
      * $HOME/.confsecrets - if exists, then is the configuration

  - This file defines the following configuration:
      * salt = string that is the salt, and is interpreted as a binary dump
      * key = the key itself
      * vault = a path to the vault

  - These can all be overridden with environment variables (these take priority):
      * CONFSECRETS_SALT
      * CONFSECRETS_KEY
      * CONFSECRETS_VAULT

Without any of these, the salt must be provided, and the key must be provided.

Confsecrets can the provide a command-line to populate the vault:

  * confsecrets config - writes $HOME/.confsecrets, options are: --salt (will be generated), --key (will be generated), --vault (will be generated)
  * confsecrets key check
  * confsecrets key generate
  * confsecrets vault init <key> - creates a vault, options are --key, --salt, --vault
  * confsecrets vault decrypt - decrypts a vault to a YAML file, options are --key, --salt, and --vault
  * confsecrets set <name> [--value <value>] - typical options, uses value if present, otherwise uses stdin
  * confsecrets get <name> - typical options, outputs the secret to the stdout
  * confsecrets remove <name> - removes an encrypted value from the vault

Within Django or Flask configuration, the secrets can be obtained as follows:

  ES_PASSWORD = Secret('name')

To access it, you can use:

  from django.conf import settings
  from confsecrets import Vault;

  settings.ES_PASSWORD.decrypt()
  
This will fail unless the key and vault are both accessible. It will also fail if that key is not in the vault.

Vault would then know how to deal with the operations described above.


## Development Plan

- Create `confsecrets/vault.py` with a vault object:

```
    Vault(salt=, path=, key=)
```

- Enhance to have configuration by providing a `VaultFactory` that uses a configuration file and/or environment.

- Create a defaultVault() classmethod on VaultFactory that lazily creates the default vault, using another method,
  The internal method first uses the CONFSECRETS_CONFIG, then $HOME/.confsecrets, and then overrides with 
  environment variables.

- Create the `Secret` object that points to a vault, and uses VaultFactory if none is provided.

- Create a `confsecrets/cli.py` that implements the CLI.

- Packaging

## Roadmap

Add support for placing the vault in an URL, by trying to interpret the vault as an URL.  If the URL has a scheme, then 
Vault becomes polymorphic because we implement a __new__ method that can return a LocalVault, an AmazonS3Vault, or a GoogleCloudStorageVault

This is a roadmap item.

## Status

The only facility so far available is Password Based Encryption (PBE) on the filesystem or in the environment.

