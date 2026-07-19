# Next.js 14 to 15 Migration (breaking changes)

## Async request APIs (breaking)
`cookies()` is now asynchronous and must be awaited: `const cookieStore = await cookies()`.
`headers()` is now asynchronous and must be awaited: `const headersList = await headers()`.
`draftMode()` is now asynchronous and must be awaited: `const { isEnabled } = await draftMode()`.
`params` in `layout.js`, `page.js`, and `route.js` is now a Promise and must be awaited: `const { slug } = await params`.
`searchParams` in `page.js` is now a Promise and must be awaited: `const { query } = await searchParams`.

## Caching defaults changed
`fetch()` requests are no longer cached by default; opt in with `fetch(url, { cache: 'force-cache' })`.
`GET` functions in Route Handlers are no longer cached by default; opt in with `export const dynamic = 'force-static'`.
Page segments are no longer reused from the Client Cache on `<Link>`/`useRouter` navigation by default; configure with `staleTimes`.

## Renames and removals
`useFormState` is deprecated; use `useActionState` from React 19.
The `@next/font` package is removed; import from the built-in `next/font` instead.
`experimental.bundlePagesExternals` is now stable and renamed to `bundlePagesRouterDependencies`.
`experimental.serverComponentsExternalPackages` is now stable and renamed to `serverExternalPackages`.
The `runtime` segment config value `experimental-edge` is removed; use `edge`.
The `geo` and `ip` properties on `NextRequest` are removed; use your host's helpers (e.g. `@vercel/functions` `geolocation`/`ipAddress`).
The minimum React version is now 19.
