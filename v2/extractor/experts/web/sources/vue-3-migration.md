# Vue 2 to Vue 3 Migration Guide (breaking changes)

## Global API
The global Vue API changed to use an application instance: `new Vue()` is replaced with `createApp()`.
Global and internal APIs have been restructured to be tree-shakable; global functions like `Vue.nextTick`, `Vue.observable` moved.

## Template directives
`v-model` usage on components has been reworked, replacing `v-bind.sync`.
The `key` usage on `<template v-for>` and on non-`v-for` nodes has changed.
`v-if` and `v-for` precedence when used on the same element has changed; `v-if` now has higher priority.
`v-bind="object"` is now order-sensitive.
The `v-on:event.native` modifier has been removed.
`keyCode` support as `v-on` modifiers has been removed.

## Components
Functional components can only be created using a plain function; the `functional` attribute on SFC `<template>` and the `functional` component option are deprecated.
Async components now require the `defineAsyncComponent` method to be created.
Component events should now be declared with the `emits` option.

## Render function and slots
The render function API changed.
`$scopedSlots` is removed; all slots are exposed via `$slots` as functions.
`$listeners` has been removed and merged into `$attrs`.
`$attrs` now includes `class` and `style` attributes.

## Lifecycle
The `destroyed` lifecycle hook is renamed to `unmounted`.
The `beforeDestroy` lifecycle hook is renamed to `beforeUnmount`.

## Other changes
Props `default` factory function no longer has access to `this` context.
The custom directive API changed to align with component lifecycle; `binding.expression` is removed.
The `data` option should always be declared as a function.
The `data` option from mixins is now merged shallowly.
`<TransitionGroup>` now renders no wrapper element by default.
When watching an array, the callback only triggers when the array is replaced.

## Removed APIs
The `$on`, `$off` and `$once` instance methods are removed.
Filters are removed.
Inline template attributes are removed.
The `$children` instance property is removed.
The `propsData` option is removed.
The `$destroy` instance method is removed.
The global `Vue.set` and `Vue.delete`, and instance methods `$set` and `$delete`, are removed.
