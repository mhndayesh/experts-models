# PyMongo 3 to 4 Migration (removed / renamed / behavior changes)

## Removed collection methods
`Collection.insert()` is removed; use `insert_one()` or `insert_many()`.
`Collection.save()` is removed; use `insert_one()` for new documents or `update_one()` for existing.
`Collection.update()` is removed; use `update_one()` or `update_many()`.
`Collection.remove()` is removed; use `delete_one()` or `delete_many()`.
`Collection.find_and_modify()` is removed; use `find_one_and_update()`, `find_one_and_replace()`, or `find_one_and_delete()`.
`Collection.count()` and `Cursor.count()` are removed; use `count_documents()` or `estimated_document_count()`.
`Collection.ensure_index()` is removed; use `create_index()` or `create_indexes()`.
`Collection.initialize_ordered_bulk_op()` and `initialize_unordered_bulk_op()` are removed; use `bulk_write()`.
`Collection.group()` is removed; use `aggregate()` with `$group`.
`Collection.map_reduce()` and `inline_map_reduce()` are removed; use `aggregate()` or `db.command('mapReduce', ...)`.
`Collection.reindex()` is removed; use `db.command('reIndex', 'collection_name')`.
`Collection.parallel_scan()` is removed with no replacement.

## Removed database / client methods
`Database.collection_names()` is removed; use `list_collection_names()`.
`Database.authenticate()` and `Database.logout()` are removed; create separate `MongoClient` instances with credentials.
`Database.eval()`, `Database.system_js`, `Database.error()`, `Database.last_status()`, and `Database.previous_error()` are removed.
`Database.current_op()` is removed; use `database.aggregate([{'$currentOp': {}}])`.
`Database.add_user()` and `remove_user()` are removed; use `db.command("createUser", ...)` and `db.command("dropUser", ...)`.
`MongoReplicaSetClient` is removed; use `MongoClient`.
`MongoClient.database_names()` is removed; use `list_database_names()`.
`MongoClient.fsync()` and `unlock()` are removed; use `client.admin.command('fsync', lock=True)` and `('fsyncUnlock')`.
`IsMaster` is renamed to `Hello`; `NotMasterError` is renamed to `NotPrimaryError`.

## Renamed connection parameters
`ssl_ca_certs` is renamed to `tlsCAFile`; `ssl_certfile`+`ssl_keyfile` are combined into `tlsCertificateKeyFile`.
`ssl_pem_passphrase` is renamed to `tlsCertificateKeyFilePassword`; `ssl_crlfile` to `tlsCRLFile`.
The write-concern option `j` is renamed to `journal`; `wtimeout` is renamed to `wTimeoutMS`.

## Behavior changes
`directConnection` now defaults to `False` instead of `None`.
The default `uuid_representation` changed from `PYTHON_LEGACY` to `UNSPECIFIED`.
`Collection.find()` with an empty projection `{}` now returns the entire document instead of just `_id`.
The `hint` parameter is now required when using `min`/`max` queries.
The `modifiers` parameter is removed from `find()`/`find_one()`; pass options directly.
`bson.binary.UUIDLegacy` is removed; use `Binary.from_uuid()`.
