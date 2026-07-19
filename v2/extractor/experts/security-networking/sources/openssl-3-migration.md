# OpenSSL 1.1.1 to 3.0 Migration (engines→providers, low-level→EVP)

## Engines and custom methods
The ENGINE API is deprecated; use providers instead.
`EVP_MD_meth_new()`, `EVP_CIPHER_meth_new()`, and `EVP_PKEY_meth_new()` are deprecated; implement a provider instead.
`RSA_meth_new()` and `EC_KEY_METHOD_new()` are deprecated; implement a provider instead.
`EVP_PKEY_set1_engine()` is deprecated; use providers.
`FIPS_mode()` and `FIPS_mode_set()` are removed; use `EVP_default_properties_is_fips_enabled()` and the FIPS provider.

## Low-level object creation → EVP_PKEY
`RSA_new()`, `RSA_free()`, and `RSA_up_ref()` are deprecated; use `EVP_PKEY_new()`, `EVP_PKEY_free()`, `EVP_PKEY_up_ref()`.
`DH_new()`, `DSA_new()`, and `EC_KEY_new()` are deprecated; use `EVP_PKEY_new()` and the EVP high-level APIs.

## Low-level cipher/digest → EVP
`AES_encrypt()`, `AES_decrypt()`, and `AES_set_encrypt_key()` are deprecated; use `EVP_EncryptInit_ex()`, `EVP_EncryptUpdate()`, `EVP_EncryptFinal_ex()`.
`DES_encrypt()`, `DES_cbc_encrypt()`, and `DES_ecb_encrypt()` are deprecated; use the EVP cipher functions.
`SHA1_Init()`, `SHA1_Update()`, and `SHA1_Final()` are deprecated; use `EVP_DigestInit_ex()`, `EVP_DigestUpdate()`, `EVP_DigestFinal_ex()`.
`MD5_Init()`, `MD5_Update()`, and `MD5_Final()` are deprecated; use the EVP digest functions or `EVP_Q_digest()`.

## Low-level key parameter access → EVP_PKEY params
`RSA_get0_n()`, `RSA_get0_e()`, and `RSA_get0_d()` are deprecated; use `EVP_PKEY_get_bn_param()` / `EVP_PKEY_get_params()`.
`DH_get0_p()`, `DH_get0_g()`, and `DH_get0_key()` are deprecated; use `EVP_PKEY_get_params()`.
`RSA_set0_key()` is deprecated; use `EVP_PKEY_fromdata()`.

## EVP_PKEY functions returning internal keys
`EVP_PKEY_get0_RSA()` now returns a const pointer to a cached copy of a provider-managed key; treat it as read-only, and changes to the internal key are not reflected in the cached copy.
`EVP_PKEY_get0_EC_KEY()`, `EVP_PKEY_get0_DSA()`, and `EVP_PKEY_get0_DH()` now return const pointers; treat them as read-only.

## Key I/O, generation, sign/verify → EVP / OSSL_DECODER
`d2i_RSAPrivateKey()` and `d2i_RSAPublicKey()` are deprecated; use `OSSL_DECODER_from_bio()`.
`PEM_read_RSAPrivateKey()` is deprecated; use `PEM_read_bio_PrivateKey_ex()`.
`RSA_generate_key()` is deprecated; use `EVP_PKEY_keygen()`.
`EC_KEY_generate_key()` is deprecated; use `EVP_PKEY_generate()`.
`RSA_sign()` and `RSA_verify()` are deprecated; use `EVP_DigestSign()` and `EVP_DigestVerify()`.
`ECDSA_sign()` and `ECDSA_verify()` are deprecated; use `EVP_DigestSign()` and `EVP_DigestVerify()`.
`DH_compute_key()` and `ECDH_compute_key()` are deprecated; use `EVP_PKEY_derive()`.

## MAC and RAND
`HMAC_Init()`, `HMAC_Update()`, and `HMAC_Final()` are deprecated; use `EVP_Q_mac()` or the `EVP_MAC` layer.
`CMAC_Init()`, `CMAC_Update()`, and `CMAC_Final()` are deprecated; use `EVP_MAC_init()`, `EVP_MAC_update()`, `EVP_MAC_final()`.
The `RAND_DRBG` subsystem is removed; use the `EVP_RAND` API instead.
`RAND_bytes()` and `RAND_priv_bytes()` may need a library context; use `RAND_bytes_ex()` and `RAND_priv_bytes_ex()`.

## Miscellaneous
`EVP_PKEY_set_alias_type()` is removed with no replacement.
`BN_is_prime_ex()` and `BN_is_prime_fasttest_ex()` are deprecated; use `BN_check_prime()`.
`EVP_sha256()` and `EVP_aes_256_gcm()` may incur a performance penalty; fetch algorithms with `EVP_MD_fetch()` and `EVP_CIPHER_fetch()`.
`SSL_CTX_new()` may need `SSL_CTX_new_ex()` to pass a library context.
