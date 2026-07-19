# urllib3 v1 to v2 Migration (breaking changes)

## Removed
Support for non-OpenSSL TLS libraries (LibreSSL, wolfSSL) is removed.
Support for OpenSSL versions older than 1.1.1 is removed.
Support for Python 2.7 and Python 3.5–3.9 is removed; Python 3.10 or later is required.
Support for non-CPython/PyPy3 implementations (Google App Engine, Jython) is removed.
The `urllib3.contrib.ntlmpool` module is removed.
The `urllib3.contrib.securetransport` module is removed.
The `urllib3[secure]` extra is removed.
The `HTTPResponse.strict` attribute and the `strict` parameter are removed (unneeded on Python 3).
`VerifiedHTTPSConnection` is no longer importable from `urllib3.connectionpool`; use `HTTPSConnection` from `urllib3.connection`.

## Changed defaults and behavior
The default minimum TLS version changed from TLS 1.0 to TLS 1.2.
The default request body encoding changed from ISO-8859-1 to UTF-8.
Certificate hostname verification via `commonName` is removed; only `subjectAltName` is used.
The default set of TLS ciphers is removed; urllib3 now uses the system-configured cipher list.
URLs without a scheme are deprecated and will raise errors in a future version.
