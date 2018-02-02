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

## Status

The only facility so far available is Password Based Encryption (PBE) on the filesystem
or in the environment.

