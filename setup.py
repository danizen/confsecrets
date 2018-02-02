#!/usr/bin/env python
import os
import subprocess

from pip.download import PipSession
from pip.req import parse_requirements

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


def get_dependencies(path):
    """
    Parse requirements files using pip internals and return only the name of the requirement
    """
    return [dep.name for dep in parse_requirements(path, session=PipSession())]


def get_tests_require():
    # tests require everything in requirements.txt
    return get_dependencies('requirements.txt')


def get_install_requires():
    # requirements.txt contains everything to run and test, because that's what CI/CD uses.
    # to build proper install-requires, strip out pytest packages.
    return list(filter(lambda name: not 'nose' in name, get_dependencies('requirements.txt')))



setup(
    name='confsecrets',
    version=get_version(),
    description='Simple utilities/modules to encrypt/decrypt application configuration secrets flexibly.',
    author='Dan Davis',
    author_email='daniel.davis@nih.gov',
    url='https://git-scm.nlm.nih.gov/projects/PYTHON/repos/confsecrets/',
    packages=[
        'confsecrets',
    ],
    entry_points={
        'console_scripts': [
            'pbetool=confsecrets.pbe:main',
        ]
    },
    tests_require=get_tests_require(),
    install_requires=get_install_requires(),
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
