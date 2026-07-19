# cryptography library — removals, deprecations, and behavior changes

## Removed
The type aliases `PUBLIC_KEY_TYPES`, `PRIVATE_KEY_TYPES`, `CERTIFICATE_PRIVATE_KEY_TYPES`, `CERTIFICATE_ISSUER_PUBLIC_KEY_TYPES`, and `CERTIFICATE_PUBLIC_KEY_TYPES` are removed; use `PublicKeyTypes`, `PrivateKeyTypes`, `CertificateIssuerPrivateKeyTypes`, `CertificateIssuerPublicKeyTypes`, and `CertificatePublicKeyTypes`.
The `CFB`, `OFB`, and `CFB8` cipher modes are removed from the standard module; they moved to `cryptography.hazmat.decrepit`.
The `Camellia` cipher is removed from the standard module; it moved to `cryptography.hazmat.decrepit`.
The `CAST5`, `SEED`, `IDEA`, and `Blowfish` cipher classes are removed; they moved to `cryptography.hazmat.decrepit`.
The `TripleDES` and `ARC4` ciphers are removed from the standard module; they moved to decrepit.
The `get_attribute_for_oid` method on `CertificateSigningRequest` is removed; use `request.attributes.get_attribute_for_oid()`.
The `encode_point` and `from_encoded_point` methods on `EllipticCurvePublicNumbers` are removed; use `EllipticCurvePublicKey.public_bytes()` and `EllipticCurvePublicKey.from_encoded_point()`.
The `signer` and `verifier` methods on key classes are removed; use `sign` and `verify`.
Support for binary elliptic curves (the `SECT*` classes) is removed.
Support for OpenSSL 1.1.x is removed; OpenSSL 3.0.0 or later is now required.
Support for using MD5 or SHA1 in certificate builders is removed.
Support for Python 3.6, 3.7, and 3.8 is removed.

## Deprecated
Passing 64-bit and 128-bit keys to `TripleDES` is deprecated; only 192-bit keys will be accepted.
DSA key support in SSH loading functions is deprecated.
OpenSSH serialization support for DSA keys is deprecated.
The `not_valid_before`, `not_valid_after`, `revocation_date`, `next_update`, and `last_update` properties that return a naive datetime are deprecated; use the `_utc` variants (`not_valid_before_utc`, etc.).
The `subject`, `verification_time`, and `max_chain_depth` properties on `ClientVerifier` and `ServerVerifier` are deprecated; use the `policy` property.

## Behavior changes
`ChaCha20` now treats the first 4 bytes of the nonce as a 32-bit little-endian block counter (RFC 7539) and raises an error on counter overflow.
Loading an X.509 CRL with mismatched signature algorithms now raises `ValueError` during parsing instead of only during validation.
Loading certificates with ECDSA/DSA NULL parameters in the signature now raises `ValueError` instead of a deprecation warning.
`load_ssh_private_key()` now raises `TypeError` if an unencrypted key is given a password, and `TypeError` if an encrypted key is given no password.
`public_bytes` and `private_bytes` now raise `TypeError` instead of `ValueError` for an invalid encoding.
Loading a PKCS7 structure with no content field now raises `ValueError` instead of returning an empty list.
`rfc4514_string()` now formats email addresses with the standard `emailAddress` attribute instead of the nonstandard `E`.
Loading keys with unsupported algorithms now raises `UnsupportedAlgorithm` instead of `ValueError`.
