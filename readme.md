# Data Curating Function

This is a function to automatically curate data from specific OCI buckets to a
persistence bucket and then create a table in an autonomous database.

## Table of Contents

<!-- vim-markdown-toc GFM -->

* [Prerequisite](#prerequisite)
    * [OCI Components](#oci-components)
    * [Credentials](#credentials)
* [Configuration](#configuration)

<!-- vim-markdown-toc -->

## Prerequisite

### OCI Components

1.  Source and target Buckets
2.  Autonomous Database
3.  Functions
4.  Rules

### Credentials

These credentials are required to be created on Cloud Shell for the function to
work.

To access buckets:

- `.oci/` containing `config` and `oci_api_key.pem`; these are files from an API
key from Oracle user.

To access an autonomous database:

- `wallet/` containing `ewallet.pem` and `tnsnames.ora`; these are wallet files
downloaded from an autonomous database.
- `wallet_password` containing a password created when downloading a wallet.
- `admin_password` containing an admin user's password for an autonomous
database.

To connect an autonomous database with buckets, set connections in the
autonomous database and configure a credential name in [`./config.yaml`][config]
accordingly.

## Configuration

See [`./config.yaml`][config].


<!-- internal -->
[config]: ./config.yaml
