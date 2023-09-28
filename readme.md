# Data Curating Function

This is a function to automatically curate data from specific OCI buckets to a
persistence bucket and then create a table in an autonomous database.

### Required Credentials

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
