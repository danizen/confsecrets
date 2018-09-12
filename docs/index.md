---
title: Getting Started
---

## Summary

confsecrets is a library providing secure symmetric cryptography based on PyCrypto or cryptodome 
to any Python project.  A set of secrets are collected into a "vault" which is stored as a JSON
or YAML file.   All secrets share the same salt and binary key.  The binary key is derived from a
clear text key via PBKDF2.

## Installation

confsecrets is best installed from your Python Package repository:

        pip install confsecrets

This provides two top-level packages:

* `confsecrets` - general support for secrets management
* `djsecrets` - Django integration

## Integration with Django

Integration with Django requires that you add the app to your Django apps:

        INSTALLED_APPS = [
            ...
            'djsecrets',
        ]

To determine a new random salt which will be specific to your project, use the following management command:

        ./manage.py newsalt

Then, configure the salt and the secrets path in your Django settings:
            
        CONFSECRETS_SALT = b'abcd1234'
        CONFSECRETS_PATH = os.path.join(BASE_DIR, 'mysecrets.json')

For more information, see the [Django Integration](django.md) section.
