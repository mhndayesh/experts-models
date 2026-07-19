# React 19 Upgrade Guide (breaking changes, removed APIs, deprecations)

## Errors in render are not re-thrown
Old: errors thrown during render were caught and rethrown, and in DEV logged to `console.error`, causing duplicate logs. New: uncaught errors are reported to `window.reportError`; errors caught by an Error Boundary are reported to `console.error`. New root options `onUncaughtError` and `onCaughtError` are available on `createRoot`.

## Removed: propTypes and defaultProps for functions
`PropTypes` checks are removed from the React package and are silently ignored. `defaultProps` is removed from function components; use ES6 default parameters instead. Class components continue to support `defaultProps`.

## Removed: Legacy Context (contextTypes and getChildContext)
Legacy Context using `contextTypes` and `getChildContext` is removed. Use `React.createContext()` and `static contextType` instead.

## Removed: string refs
String refs like `ref='input'` are removed. Use a callback ref: `ref={input => this.input = input}`.

## Removed: Module pattern factories
Module pattern factory components (returning an object with a `render` method) are removed; return JSX directly.

## Removed: React.createFactory
`React.createFactory` is removed; use JSX instead, e.g. `<button />`.

## Removed: react-test-renderer/shallow
`react-test-renderer/shallow` is removed; install `react-shallow-renderer` and import `ShallowRenderer` from `react-shallow-renderer`.

## Removed: react-dom/test-utils
`act` is removed from `react-dom/test-utils`; import `act` from `react` instead. All other `test-utils` functions have been removed.

## Removed: ReactDOM.render
`ReactDOM.render` is removed. Use `createRoot` from `react-dom/client`: `const root = createRoot(container); root.render(<App />)`.

## Removed: ReactDOM.hydrate
`ReactDOM.hydrate` is removed. Use `hydrateRoot` from `react-dom/client`: `hydrateRoot(container, <App />)`.

## Removed: unmountComponentAtNode
`unmountComponentAtNode` is removed; use `root.unmount()` instead.

## Removed: ReactDOM.findDOMNode
`ReactDOM.findDOMNode` is removed; use refs (`useRef`) instead.

## Deprecated: element.ref
Accessing `element.ref` is deprecated in favor of `element.props.ref`; `ref` is now a regular prop.

## Deprecated: react-test-renderer
`react-test-renderer` is deprecated in favor of `@testing-library/react`; it logs a deprecation warning and switched to concurrent rendering in React 19.

## TypeScript: ref callbacks must not return a value
A ref callback with an implicit return like `ref={current => (instance = current)}` is now rejected by TypeScript; use a block body: `ref={current => {instance = current}}`.

## TypeScript: useRef requires an argument
`useRef()` now requires an argument; call `useRef(undefined)`. All refs are now mutable, and `MutableRefObject` is deprecated in favor of a single `RefObject` type.

## TypeScript: ReactElement props default to unknown
The `props` of React elements now default to `unknown` instead of `any`.

## TypeScript: JSX namespace
The global `JSX` namespace is replaced; use `React.JSX` and wrap module augmentation inside `declare module "react"`.

## react-dom: removed unstable APIs
`react-dom` removes `unstable_flushControlled`, `unstable_createEventHandle`, `unstable_renderSubtreeIntoContainer`, and `unstable_runWithPriority`. `errorInfo.digest` is removed from `onRecoverableError`. JavaScript URLs in `src` and `href` now error.

## UMD builds removed
UMD builds are no longer produced; use an ESM-based CDN such as esm.sh.

## New JSX transform is now required
The new JSX transform (2020) is now required; React 19 features like `ref` as a prop require it. A warning is shown if the outdated transform is used.

## StrictMode changes
In development double-render, `useMemo` and `useCallback` reuse the memoized results from the first render during the second render. Ref callbacks are double-invoked on initial mount.
