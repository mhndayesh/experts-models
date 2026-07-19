# Paramiko — removals, deprecations, and behavior changes

## Removed
DSA/DSS key algorithm support is removed in 4.0.0.
SHA-1 RSA signature verification is removed in 5.0.0.
The SHA-1 key exchange methods `diffie-hellman-group-exchange-sha1`, `diffie-hellman-group14-sha1`, and `diffie-hellman-group1-sha1` are removed in 5.0.0.
GSSAPI support is removed in 5.0.0.
Python 2 and Python < 3.6 support is dropped in 3.0.0.
The `paramiko.py3compat` module is removed in 3.0.0.
`paramiko.common.asbytes` is moved to `paramiko.util.asbytes` in 3.0.0.
The `PKey.__cmp__` ordering comparison is removed in 3.0.0.
`paramiko.util.retry_on_signal` is removed in 3.0.0.
`paramiko.__all__` is removed in 4.0.0.
The `ed25519`, `invoke`, and `all` packaging extras are removed in 4.0.0.

## Behavior changes
The `PKey.from_path` argument is renamed from `passphrase` to `password` in 5.0.0 (backwards incompatible).
`SSHConfig` now preserves `proxycommand` as `None` instead of deleting it in 3.0.0.
The minimum DH group-exchange modulus increased from 1024 to 2048 bits in 5.0.0.
RSA public-key algorithms now prefer SHA2 over SHA1 as of 2.9.0.
`PKey.write_private_key` methods were reorganized in 5.0.0; child classes no longer override them.

## Deprecated / future
The default private-key format will change from PEM to OpenSSH in a future major release (warned in 5.0.0).
