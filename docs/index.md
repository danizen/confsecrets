---
title: confsecrets | Getting Started
---

## Summary

confsecrets is a library providing secure symmetric cryptography based on PyCrypto, pycryptodome, or pycryptodomex to any Python project.  A set of secrets are collected into a "vault" which is stored as a JSON file.  All secrets share the same salt and binary key.  The binary key is derived from a
clear text key via PBKDF2.

## Installation

confsecrets is best installed from your Python Package repository:

        pip install confsecrets

This provides one top-level packages:

* `confsecrets` - general support for secrets management

There is also a `confsecrets` command that you can use to create a new salt, manage the vault, etc.

## Environment Variables

`confsecrets.vault.DefaultVault` and the command-line, use the following environment variables:

* `CONFSECRETS_SALT` - a base64 encoded, 8-byte salt
* `CONFSECRETS_KEY` - a plain text password or passphrase from which the binary key is derived
* `CONFSECSETS_PATH` - The path to a JSON-encoded vault file, which will be initialized if needed

## Console Comands

* `confsecrets newsalt` - creates a new, base-64 encoded salt.  
   The `--raw` argument causes this to be printed as python code, to be copied into a file.

* `confsecrets list` - lists all secrets in a vault.

* `confsecrets get <secret>` - gets a single secret.

* `confsecrets put <secret> <value>` - updates a secret to the given value

* `confsecrets rm <secret>` - removes a secret from a vault
