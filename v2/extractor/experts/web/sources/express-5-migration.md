# Express 4 to Express 5 Migration (breaking changes)

## Removed methods / signatures
`app.del()` is removed; use `app.delete()`.
`req.acceptsCharset()` is renamed to `req.acceptsCharsets()`.
`req.acceptsEncoding()` is renamed to `req.acceptsEncodings()`.
`req.acceptsLanguage()` is renamed to `req.acceptsLanguages()`.
`req.param(name)` is removed; use `req.params`, `req.body`, or `req.query` explicitly.
`res.json(obj, status)` is removed; use `res.status(status).json(obj)`.
`res.jsonp(obj, status)` is removed; use `res.status(status).jsonp(obj)`.
`res.send(body, status)` is removed; use `res.status(status).send(body)`.
`res.send(status)` with a numeric status is removed; use `res.sendStatus(status)`.
`res.redirect(url, status)` is removed; use `res.redirect(status, url)`.
`res.redirect('back')` is removed; use `res.redirect(req.get('Referrer') || '/')`.
`res.sendfile()` is removed; use `res.sendFile()` (camelCase).
The `hidden` and `from` options of `res.sendFile()` and `express.static()` are removed; use `dotfiles` and `root`.
`express.static.mime` is removed; use the `mime-types` package.
`app.param(fn)` and `router.param(fn)` (passing a function) are removed.

## Changed behavior
Path route matching: the bare `*` wildcard is removed; use a named wildcard like `/*splat`.
Path route matching: `:param?` optional parameters are removed; use `/:param{:ext}` syntax.
Path route matching: regexp special characters in strings are no longer supported; use an array of paths.
Rejected promises returned from middleware and handlers are now automatically forwarded to the error handler, so `async`/`await` no longer needs a manual `.catch(next)`.
`express.urlencoded()` now defaults `extended` to `false` (was `true`).
`express.static()` now defaults `dotfiles` to `"ignore"` (dotfiles were served by default before).
`req.body` now returns `undefined` when the body is unparsed (was `{}`).
`req.host` now includes the port number (the port was previously stripped).
`req.query` is no longer a writable property and its default parser changed to "simple".
`res.status()` now only accepts integers in the range 100–999.
`res.clearCookie()` now ignores the `maxAge` and `expires` options.
`res.vary()` now throws when the `field` argument is missing.
