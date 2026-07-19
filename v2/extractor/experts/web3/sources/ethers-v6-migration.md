# ethers.js v5 to v6 Migration (breaking changes)

## BigNumber → native bigint
`BigNumber.from(x)` is replaced by native `BigInt(x)`.
`a.add(b)` is replaced by the `a + b` operator; `a.eq(b)` by `a == b`.

## Providers
`import { providers } from "ethers"` is replaced by direct imports like `import { InfuraProvider } from "ethers"`.
`ethers.providers.Web3Provider` is renamed to `ethers.BrowserProvider`.
`provider.sendTransaction(signedTx)` is renamed to `provider.broadcastTransaction(signedTx)`.
`new StaticJsonRpcProvider(url, network)` is replaced by `new JsonRpcProvider(url, network, { staticNetwork: network })`.
`await provider.getGasPrice()` is replaced by `(await provider.getFeeData()).gasPrice`.

## Contracts
`contract.functions.foo(addr)` is replaced by `contract.foo.staticCallResult(addr)`.
`contract.callStatic.foo(addr)` is replaced by `contract.foo.staticCall(addr)`.
`contract.estimateGas.foo(addr)` is replaced by `contract.foo.estimateGas(addr)`.
`contract.populateTransaction.foo(addr)` is replaced by `contract.foo.populateTransaction(addr)`.

## Utils moved to top level / renamed
`ethers.utils.parseEther` / `formatEther` are now top-level `ethers.parseEther` / `ethers.formatEther`.
`ethers.constants.AddressZero` is renamed to `ethers.ZeroAddress`.
`ethers.constants.HashZero` is renamed to `ethers.ZeroHash`.
`ethers.utils.formatBytes32String()` is renamed to `ethers.encodeBytes32String()`.
`ethers.utils.parseBytes32String()` is renamed to `ethers.decodeBytes32String()`.
`ethers.utils.hexDataSlice()` is renamed to `ethers.dataSlice()`.
`ethers.utils.hexZeroPad()` is renamed to `ethers.zeroPadValue()`.
`ethers.utils.hexlify(number)` is replaced by `ethers.toBeHex(number)`.
`ethers.utils.hexValue(value)` is replaced by `ethers.toQuantity(value)`.
`ethers.utils.arrayify(value)` is renamed to `ethers.getBytes(value)`.
`ethers.utils.solidityPack()` is renamed to `ethers.solidityPacked()`.
`ethers.utils.solidityKeccak256()` is renamed to `ethers.solidityPackedKeccak256()`.
`ethers.utils.soliditySha256()` is renamed to `ethers.solidityPackedSha256()`.
`AbiCoder.defaultAbiCoder` (property) is now a function `AbiCoder.defaultAbiCoder()`.
`splitSignature(sig)` and `joinSignature(sig)` are replaced by `ethers.Signature.from(sig)` and `.serialized`.
`parseTransaction(bytes)` and `serializeTransaction(tx)` are replaced by `Transaction.from(...)` and `.serialized`.
`ethers.utils.defineReadOnly(obj, name, value)` is replaced by `ethers.defineProperties(obj, { name: value })`.
