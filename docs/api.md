---
title: confsecrets | API Reference
---

## `confsecrets.pbe`

Provides secure, symmetric encryption without much around it.

Includes these exceptions:

- `confsecrets.pbe.InvalidSalt` - raised for an invalid salt
- `confsecrets.pbe.MessageTooShort` - raised when attempting to decrypt a message that has no room for IV, ciphertext, and MAC
- `confsecrets.pbe.InvalidMessageAuthenticationCode` - raised when decrypting a message with an invalid MAC
- `confsecrets.pbe.PasswordTooSimple` - raised when `PasswordUtil` receives a password that is not complex enough.
- `confsecrets.pbe.PasswordNotShellSafe` - raised when `PasswordUtil` receives a password that must be escaped from a Linux shell. 

Includes these types:

- `confsecrets.pbe.PasswordUtil`:
    - `PasswordUtil.check` - a static method that checks a password for length, complexity, and shell safety.
    - `PasswordUtil.generate` - a static method that generates a password matching above rules 
- `confsecrets.pbe.PBEUtil` - This is the heart of the module, providing secure, symmetric encryption.

## `confsecrets.vault`

Implements a file-based container of encrypted material.  Each piece of encrypted material is accessed via a key.

Includes these exceptions:

- `confsecrets.vault.VaultPathMissing` - raised when no path has been provided
- `confsecrets.vault.VaultNotFound` - raised for operating systems errors accessing the vault 
- `confsecrets.vault.VaultFormatError` - raised when the vault is in an invalid format

Includes these types:

- `confsecrets.vault.Vault` - A dictionary type that stores its values as encrypted, base64 encoded messages within a JSON or YAML file. 
- `confsecrets.vault.DefaultVault` - A vault with global parameters that functions as a singleton

## `confsecrets.secrets`

Provides objects that behave like strings or other types, which are backed by the vault.

Includes these types:

- `confsecrets.secrets.BaseSecret` - A base secret simply knows how to set and get its value from a vault. If no vault is provided, it uses the `DefaultVault`.
- `confsecrets.secrets.Secret` - A secret that behaves like a string in string contexts, a bool in bool contexts, and so on.
