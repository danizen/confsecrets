#!/usr/bin/env python
import os
import subprocess

from setuptools import setup, find_packages


def get_version():
    """
    Determine a version string using git or a file VERSION.txt
    """
    # VERSION.txt is not added to git, it can be generated manually or by CI/CD
    version = '0.0.1'
    if os.path.isfile('VERSION.txt'):
        with open('VERSION.txt', 'r') as f:
            version = f.read().strip()
    return version


def get_readme():
    """
    Open and read the readme. This would be the place to convert to RST, but we no longer have to.
    """
    with open('README.md') as f:
        return f.read()


setup(
    name='confsecrets',
    version=get_version(),
    description='Simple utilities/modules to encrypt/decrypt application configuration secrets flexibly.',
    long_description=get_readme(),
    long_description_content_type='text/markdown; charset=UTF-8; variant=CommonMark',
    author='Dan Davis',
    author_email='daniel.davis@nih.gov',
    url='https://git-scm.nlm.nih.gov/projects/PYTHON/repos/confsecrets/',
    packages=[
        'confsecrets',
    ],
    #entry_points={
    #    'console_scripts': [
    #        'pbetool=confsecrets.pbetool:main',
    #    ]
    #},
    tests_require=['nose', 'rednose', 'tox', 'PyCrypto', 'six'],
    install_requires=['PyCrypto', 'six'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: Public Domain',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Mocrosoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Security :: Cryptography',
        'Topic :: Software Development',
        'Topic :: Utilities',
    ]
)

