## Installation

confsecrets is best installed from your Python Package repository:

        pip install confsecrets

This provides two top-level packages:

* `confsecrets` - general support for secrets management
* `djsecrets` - Django integration

### Integration with Django

Integration with Django requires that you add the app to your Django apps:

        INSTALLED_APPS = [
            ...
            'djsecrets',
        ]

Once you have done that, you should acquire a salt unique to your project:

        ./manage.py newsalt
        
Then, configure the salt and the secrets path:
            
        CONFSECRETS_SALT = b'abcd1234'
        CONFSECRETS_PATH = os.path.join(BASE_DIR, 'mysecrets.json')
        
For more information, see the [Django Integration](django.md) section.
