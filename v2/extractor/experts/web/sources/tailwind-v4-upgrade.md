# Tailwind CSS v3 → v4 Upgrade Guide (breaking changes)

## Removed @tailwind Directives
Old: `@tailwind base; @tailwind components; @tailwind utilities;`
New: `@import "tailwindcss";`

## Removed Deprecated Utilities
`bg-opacity-*` is removed; use opacity modifiers like `bg-black/50`.
`text-opacity-*` is removed; use opacity modifiers like `text-black/50`.
`border-opacity-*` is removed; use opacity modifiers like `border-black/50`.
`divide-opacity-*` is removed; use opacity modifiers like `divide-black/50`.
`ring-opacity-*` is removed; use opacity modifiers like `ring-black/50`.
`placeholder-opacity-*` is removed; use opacity modifiers like `placeholder-black/50`.
`flex-shrink-*` is renamed to `shrink-*`.
`flex-grow-*` is renamed to `grow-*`.
`overflow-ellipsis` is renamed to `text-ellipsis`.
`decoration-slice` is renamed to `box-decoration-slice`.
`decoration-clone` is renamed to `box-decoration-clone`.

## Renamed Utilities
`shadow-sm` is renamed to `shadow-xs`.
`shadow` is renamed to `shadow-sm`.
`drop-shadow-sm` is renamed to `drop-shadow-xs`.
`drop-shadow` is renamed to `drop-shadow-sm`.
`blur-sm` is renamed to `blur-xs`.
`blur` is renamed to `blur-sm`.
`backdrop-blur-sm` is renamed to `backdrop-blur-xs`.
`backdrop-blur` is renamed to `backdrop-blur-sm`.
`rounded-sm` is renamed to `rounded-xs`.
`rounded` is renamed to `rounded-sm`.
`outline-none` is renamed to `outline-hidden`.
`ring` is renamed to `ring-3`.

## Default Ring Width Change
Old: the `ring` utility added a `3px` ring. New: the `ring` utility adds a `1px` ring; use `ring-3` for the old behavior.

## Space-Between Selector Change
Old CSS: `.space-y-4 > :not([hidden]) ~ :not([hidden]) { margin-top: 1rem; }`. New CSS: `.space-y-4 > :not(:last-child) { margin-bottom: 1rem; }`.

## Divide Selector Change
Old CSS: `.divide-y-4 > :not([hidden]) ~ :not([hidden]) { border-top-width: 4px; }`. New CSS: `.divide-y-4 > :not(:last-child) { border-bottom-width: 4px; }`.

## Using Variants with Gradients
Old behavior: overriding part of a gradient with a variant would reset the entire gradient. New behavior: gradient values are preserved; use `via-none` to unset a three-stop gradient back to a two-stop gradient in a specific state.

## Container Configuration
Old: the `container` utility had configuration options like `center` and `padding`. New: use the `@utility` directive to customize the `container` utility.

## Default Border Color
Old: `border-*` and `divide-*` utilities used your configured `gray-200` color by default. New: `border-*` and `divide-*` utilities use `currentColor`. Specify a color anywhere you are using a `border-*` or `divide-*` utility.

## Default Ring Color
Old: the `ring` utility default color was `blue-500`. New: the `ring` utility default color is `currentColor`. Add `ring-blue-500` anywhere you were depending on the default ring color.

## New Default Placeholder Color
Old: placeholder text used your configured `gray-400` color by default. New: placeholder text uses the current text color at 50% opacity.

## Buttons Use Default Cursor
Old: buttons used `cursor: pointer`. New: buttons use `cursor: default` to match the default browser behavior.

## Dialog Margins Removed
Old: Preflight did not reset margins on `<dialog>` elements. New: Preflight now resets margins on `<dialog>` elements.

## Hidden Attribute Takes Priority
Old: display classes like `block` or `flex` took priority over the `hidden` attribute. New: the `hidden` attribute takes priority; remove the `hidden` attribute if you want an element to be visible.

## Using a Prefix
Old: prefixes did not look like variants. New: prefixes now look like variants and are always at the beginning of the class name, e.g. `tw:flex tw:bg-red-500 tw:hover:bg-red-600`.

## The Important Modifier
Old: `!` was placed at the beginning of the utility name after variants: `flex! bg-red-500!`. New: `!` is placed at the very end of the class name: `flex bg-red-500 hover:bg-red-600/50!`.

## Adding Custom Utilities
Old: `@layer utilities { .tab-4 { tab-size: 4; } }`. New: `@utility tab-4 { tab-size: 4; }`.

## Variant Stacking Order
Old: stacked variants applied from right to left: `first:*:pt-0 last:*:pb-0`. New: stacked variants apply left to right: `*:first:pt-0 *:last:pb-0`.

## Variables in Arbitrary Values
Old syntax: `bg-[--brand-color]`. New syntax: `bg-(--brand-color)`.

## Arbitrary Values in Grid and Object-Position Utilities
Old: commas were used in `grid-cols-*`, `grid-rows-*`, and `object-*` utilities: `grid-cols-[max-content,auto]`. New: underscores must be used to represent spaces: `grid-cols-[max-content_auto]`.

## Hover Styles on Mobile
Old: the `hover` variant applied on all devices. New: the `hover` variant only applies when the primary input device supports hover: `@media (hover: hover)`.

## Transitioning Outline-Color
Old: `transition` and `transition-colors` utilities did not include `outline-color`. New: `transition` and `transition-colors` utilities now include the `outline-color` property.

## Individual Transform Properties
Old: `rotate-*`, `scale-*`, and `translate-*` were based on the `transform` property. New: they are based on individual `rotate`, `scale`, and `translate` CSS properties.

## Resetting Transforms
Old: reset via `transform-none`: `scale-150 focus:transform-none`. New: reset individual properties instead: `scale-150 focus:scale-none`.

## Transitions with Individual Transform Properties
Old: `transition-[opacity,transform] hover:scale-150`. New: `transition-[opacity,scale] hover:scale-150`.

## Disabling Core Plugins
Old: the `corePlugins` option was available to disable certain utilities. New: the `corePlugins` option is no longer supported in v4.

## Using the theme() Function
Old: dot notation `theme(colors.red.500)` and `theme(screens.xl)`. New: use CSS variables `var(--color-red-500)` and `theme(--breakpoint-xl)`.

## Using a JavaScript Config File
Old: JavaScript config files were detected automatically. New: JavaScript config files must be loaded explicitly using the `@config` directive: `@config "../../tailwind.config.js";`. The `corePlugins`, `safelist`, and `separator` options from JavaScript config are not supported in v4.0.

## Theme Values in JavaScript
Old: the `resolveConfig` function was exported to turn JavaScript config into a flat object. New: the function is removed; use CSS variables directly or `getComputedStyle` to access theme values.

## Using @apply with Vue, Svelte, or CSS Modules
Old: stylesheets bundled separately had access to theme variables and custom utilities. New: they do not; use `@reference "../../app.css";` or use CSS theme variables directly instead of `@apply`.

## Browser Requirements
Old: supported older browsers. New: Tailwind CSS v4.0 is designed for Safari 16.4+, Chrome 111+, and Firefox 128+.

## PostCSS Plugin Location
Old: the `tailwindcss` package was a PostCSS plugin. New: the PostCSS plugin lives in a dedicated `@tailwindcss/postcss` package.

## Tailwind CLI Package
Old: `npx tailwindcss -i input.css -o output.css`. New: `npx @tailwindcss/cli -i input.css -o output.css`.

## Using Sass, Less, and Stylus
Old: could be used with Tailwind CSS v3. New: Tailwind CSS v4.0 is not designed to be used with CSS preprocessors like Sass, Less, or Stylus.
