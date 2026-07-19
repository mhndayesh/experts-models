# Svelte 4 to Svelte 5 Migration (runes, breaking changes)

## Reactivity syntax
Top-level `let count = 0` is no longer implicitly reactive; use `let count = $state(0)`.
Reactive derivations `$: double = count * 2` are replaced by `let double = $derived(count * 2)`.
Reactive side-effect blocks `$: { ... }` are replaced by `$effect(() => { ... })`.
`export let prop` is replaced by destructuring `$props()`: `let { prop } = $props()`.

## Event handling
`on:click={handler}` is replaced by the `onclick={handler}` property.
`createEventDispatcher()` is deprecated; accept callback props instead and call them.
Event forwarding via `<button on:click>` is replaced by accepting and passing an `onclick` prop.
Event modifiers like `on:click|preventDefault|once` are removed; handle in the function or use actions.
Multiple handlers `on:click={one} on:click={two}` are disallowed; combine into one handler.

## Slots to snippets
The default `<slot />` is replaced by `let { children } = $props()` and `{@render children?.()}`.
Named slots `<slot name="header" />` are replaced by a `header` prop rendered with `{@render header()}`.
Slot props via `let:item` are replaced by snippets: `{#snippet item(text)}...{/snippet}`.

## Component instantiation
`new Component({ target })` is removed; use `mount(Component, { target })`.
`app.$on('event', cb)` is replaced by the `events` option on `mount` (deprecated) or callback props.
`app.$set({...})` is removed; manipulate the `$state` object directly.
`app.$destroy()` is removed; use `unmount(app)`.
Server-side `App.render({ props })` is replaced by `render(App, { props })`.
Components are now functions, not classes; they no longer have a `.render()` method.
`SvelteComponent` type is replaced by the `Component` type.

## Props and bindings
Props are no longer bindable by default; mark them with `$bindable()`: `let { foo = $bindable() } = $props()`.
The `accessors` compiler option is ignored; use component exports instead.
The `immutable` compiler option is ignored; reactivity is determined by `$state`.

## Dynamic components
`<svelte:component this={Thing} />` is no longer necessary; components are reactive, use `<Thing />`.

## Lifecycle
In runes mode `beforeUpdate` is replaced by `$effect.pre()` and `afterUpdate` by `$effect()`.

## Other
`null` and `undefined` now render as an empty string instead of the text "null"/"undefined".
`ontouchstart` and `ontouchmove` handlers are passive by default; use actions if `preventDefault()` is needed.
String event-attribute values like `onclick="alert('hello')"` are disallowed; use a function.
`import { walk } from 'svelte/compiler'` is removed; import `walk` from `estree-walker`.
The `css: false`, `hydratable`, and `enableSourcemap` compiler options are removed.
Internet Explorer is no longer supported.
