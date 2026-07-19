# web3.py migration (v5→v6→v7 breaking changes)

## v5 to v6 — class split and renames
The single `Web3` class is split into `Web3` and `AsyncWeb3`; use `Web3(Web3.HTTPProvider(...))` or `AsyncWeb3(AsyncWeb3.AsyncHTTPProvider(...))`.
`SolidityError` is renamed to `ContractLogicError`.
`sha3()` and `soliditySha3()` are renamed to `keccak()` and `solidityKeccak()`.
`InfuraKeyNotFound` is renamed to `InfuraProjectIdNotFound`; the `WEB3_INFURA_API_KEY` env var is renamed to `WEB3_INFURA_PROJECT_ID`.
The IBAN module and the Parity module are removed.
`w3.enable_strict_bytes_checking()` is replaced by the `w3.strict_bytes_type_checking` property (default `True`).

## v6 to v7 — middleware and snake_case
`middlewares` is renamed to `middleware`; middleware moved from a function-based to a class-based model.
`geth_poa_middleware` is renamed to `ExtraDataToPOAMiddleware`; `pythonic_middleware` to `PythonicMiddleware`.
`construct_sign_and_send_raw_middleware(private_key)` is replaced by `SignAndSendRawMiddlewareBuilder.build(private_key)`.
`name_to_address_middleware` is renamed to `ENSNameToAddressMiddleware`.
The filter parameters `fromBlock`, `toBlock`, and `blockHash` are renamed to `from_block`, `to_block`, and `block_hash`.
`WebsocketProviderV2` is renamed to `WebSocketProvider`; `AsyncWeb3.persistent_websocket(...)` is replaced by `AsyncWeb3(WebSocketProvider('...'))`.
`Contract.encodeABI()` is renamed to `Contract.encode_abi()`; the `fn_name` argument becomes `abi_element_identifier`.
JSON-RPC errors now raise `Web3RPCError` instead of `ValueError`; `AssertionError`/`ValueError`/`TypeError` become `Web3AssertionError`/`Web3ValueError`/`Web3TypeError`.
Python 3.7 support is dropped (Python 3.8+ required); the EthPM module, `geth.miner`, and `geth.personal` namespaces are removed.
`CallOverride` is renamed to `StateOverride`.
