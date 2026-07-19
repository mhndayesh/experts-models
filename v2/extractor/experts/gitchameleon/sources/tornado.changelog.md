
# ===== SOURCE: https://raw.githubusercontent.com/tornadoweb/tornado/master/docs/releases/v5.0.0.rst =====

What's new in Tornado 5.0
=========================

Mar 5, 2018
-----------

Highlights
~~~~~~~~~~

- The focus of this release is improving integration with `asyncio`.
  On Python 3, the `.IOLoop` is always a wrapper around the `asyncio`
  event loop, and `asyncio.Future` and `asyncio.Task` are used instead
  of their Tornado counterparts. This means that libraries based on
  `asyncio` can be mixed relatively seamlessly with those using
  Tornado. While care has been taken to minimize the disruption from
  this change, code changes may be required for compatibility with
  Tornado 5.0, as detailed in the following section.
- Tornado 5.0 supports Python 2.7.9+ and 3.4+. Python 2.7 and 3.4 are
  deprecated and support for them will be removed in Tornado 6.0,
  which will require Python 3.5+.

Backwards-compatibility notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 3.3 is no longer supported.
- Versions of Python 2.7 that predate the `ssl` module update are no
  longer supported. (The `ssl` module was updated in version 2.7.9,
  although in some distributions the updates are present in builds
  with a lower version number. Tornado requires `ssl.SSLContext`,
  `ssl.create_default_context`, and ``ssl.match_hostname``)
- Versions of Python 3.5 prior to 3.5.2 are no longer supported due to
  a change in the async iterator protocol in that version.
- The ``trollius`` project (`asyncio` backported to Python 2) is no
  longer supported.
- `tornado.concurrent.Future` is now an alias for `asyncio.Future`
  when running on Python 3. This results in a number of minor
  behavioral changes:

    - `.Future` objects can only be created while there is a current
      `.IOLoop`
    - The timing of callbacks scheduled with
      ``Future.add_done_callback`` has changed.
      `tornado.concurrent.future_add_done_callback` can be used to
      make the behavior more like older versions of Tornado (but not
      identical). Some of these changes are also present in the Python
      2 version of `tornado.concurrent.Future` to minimize the
      difference between Python 2 and 3.
    - Cancellation is now partially supported, via
      `asyncio.Future.cancel`. A canceled `.Future` can no longer have
      its result set. Applications that handle `~asyncio.Future`
      objects directly may want to use
      `tornado.concurrent.future_set_result_unless_cancelled`. In
      native coroutines, cancellation will cause an exception to be
      raised in the coroutine.
    - The ``exc_info`` and ``set_exc_info`` methods are no longer
      present. Use `tornado.concurrent.future_set_exc_info` to replace
      the latter, and raise the exception with
      `~asyncio.Future.result` to replace the former.
- ``io_loop`` arguments to many Tornado functions have been removed.
  Use `.IOLoop.current()` instead of passing `.IOLoop` objects
  explicitly.
- On Python 3, `.IOLoop` is always a wrapper around the `asyncio`
  event loop. ``IOLoop.configure`` is effectively removed on Python 3
  (for compatibility, it may be called to redundantly specify the
  `asyncio`-backed `.IOLoop`)
- `.IOLoop.instance` is now a deprecated alias for `.IOLoop.current`.
  Applications that need the cross-thread communication behavior
  facilitated by `.IOLoop.instance` should use their own global variable
  instead.


Other notes
~~~~~~~~~~~

- The ``futures`` (`concurrent.futures` backport) package is now required
  on Python 2.7.
- The ``certifi`` and ``backports.ssl-match-hostname`` packages are no
  longer required on Python 2.7.
- Python 3.6 or higher is recommended, because it features more
  efficient garbage collection of `asyncio.Future` objects.

`tornado.auth`
~~~~~~~~~~~~~~

- `.GoogleOAuth2Mixin` now uses a newer set of URLs.

`tornado.autoreload`
~~~~~~~~~~~~~~~~~~~~

- On Python 3, uses ``__main__.__spec`` to more reliably reconstruct
  the original command line and avoid modifying ``PYTHONPATH``.
- The ``io_loop`` argument to `tornado.autoreload.start` has been removed.

`tornado.concurrent`
~~~~~~~~~~~~~~~~~~~~

- `tornado.concurrent.Future` is now an alias for `asyncio.Future`
  when running on Python 3. See "Backwards-compatibility notes" for
  more.
- Setting the result of a ``Future`` no longer blocks while callbacks
  are being run. Instead, the callbacks are scheduled on the next
  `.IOLoop` iteration.
- The deprecated alias ``tornado.concurrent.TracebackFuture`` has been
  removed.
- `tornado.concurrent.chain_future` now works with all three kinds of
  ``Futures`` (Tornado, `asyncio`, and `concurrent.futures`)
- The ``io_loop`` argument to `tornado.concurrent.run_on_executor` has
  been removed.
- New functions `.future_set_result_unless_cancelled`,
  `.future_set_exc_info`, and `.future_add_done_callback` help mask
  the difference between `asyncio.Future` and Tornado's previous
  ``Future`` implementation.

`tornado.curl_httpclient`
~~~~~~~~~~~~~~~~~~~~~~~~~

- Improved debug logging on Python 3.
- The ``time_info`` response attribute now includes ``appconnect`` in
  addition to other measurements.
- Closing a `.CurlAsyncHTTPClient` now breaks circular references that
  could delay garbage collection.
- The ``io_loop`` argument to the `.CurlAsyncHTTPClient` constructor
  has been removed.

`tornado.gen`
~~~~~~~~~~~~~

- ``tornado.gen.TimeoutError`` is now an alias for
  `tornado.util.TimeoutError`.
- Leak detection for ``Futures`` created by this module now attributes
  them to their proper caller instead of the coroutine machinery.
- Several circular references that could delay garbage collection have
  been broken up.
- On Python 3, `asyncio.Task` is used instead of the Tornado coroutine
  runner. This improves compatibility with some `asyncio` libraries
  and adds support for cancellation.
- The ``io_loop`` arguments to ``YieldFuture`` and `.with_timeout` have
  been removed.

`tornado.httpclient`
~~~~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to all `.AsyncHTTPClient` constructors has
  been removed.

`tornado.httpserver`
~~~~~~~~~~~~~~~~~~~~

- It is now possible for a client to reuse a connection after sending
  a chunked request.
- If a client sends a malformed request, the server now responds with
  a 400 error instead of simply closing the connection.
- ``Content-Length`` and ``Transfer-Encoding`` headers are no longer
  sent with 1xx or 204 responses (this was already true of 304
  responses).
- When closing a connection to a HTTP/1.1 client, the ``Connection:
  close`` header is sent with the response.
- The ``io_loop`` argument to the `.HTTPServer` constructor has been
  removed.
- If more than one ``X-Scheme`` or ``X-Forwarded-Proto`` header is
  present, only the last is used.

`tornado.httputil`
~~~~~~~~~~~~~~~~~~

- The string representation of `.HTTPServerRequest` objects (which are
  sometimes used in log messages) no longer includes the request
  headers.
- New function `.qs_to_qsl` converts the result of
  `urllib.parse.parse_qs` to name-value pairs.

`tornado.ioloop`
~~~~~~~~~~~~~~~~

- ``tornado.ioloop.TimeoutError`` is now an alias for
  `tornado.util.TimeoutError`.
- `.IOLoop.instance` is now a deprecated alias for `.IOLoop.current`.
- `.IOLoop.install` and `.IOLoop.clear_instance` are deprecated.
- The ``IOLoop.initialized`` method has been removed.
- On Python 3, the `asyncio`-backed `.IOLoop` is always used and
  alternative `.IOLoop` implementations cannot be configured.
  `.IOLoop.current` and related methods pass through to
  `asyncio.get_event_loop`.
- `~.IOLoop.run_sync` cancels its argument on a timeout. This
  results in better stack traces (and avoids log messages about leaks)
  in native coroutines.
- New methods `.IOLoop.run_in_executor` and
  `.IOLoop.set_default_executor` make it easier to run functions in
  other threads from native coroutines (since
  `concurrent.futures.Future` does not support ``await``).
- ``PollIOLoop`` (the default on Python 2) attempts to detect misuse
  of `.IOLoop` instances across `os.fork`.
- The ``io_loop`` argument to `.PeriodicCallback` has been removed.
- It is now possible to create a `.PeriodicCallback` in one thread
  and start it in another without passing an explicit event loop.
- The ``IOLoop.set_blocking_signal_threshold`` and
  ``IOLoop.set_blocking_log_threshold`` methods are deprecated because
  they are not implemented for the `asyncio` event loop`. Use the
  ``PYTHONASYNCIODEBUG=1`` environment variable instead.
- `.IOLoop.clear_current` now works if it is called before any
  current loop is established.

`tornado.iostream`
~~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to the `.IOStream` constructor has been removed.
- New method `.BaseIOStream.read_into` provides a minimal-copy alternative to
  `.BaseIOStream.read_bytes`.
- `.BaseIOStream.write` is now much more efficient for very large amounts of data.
- Fixed some cases in which ``IOStream.error`` could be inaccurate.
- Writing a `memoryview` can no longer result in "BufferError:
  Existing exports of data: object cannot be re-sized".

`tornado.locks`
~~~~~~~~~~~~~~~

- As a side effect of the ``Future`` changes, waiters are always
  notified asynchronously with respect to `.Condition.notify`.

`tornado.netutil`
~~~~~~~~~~~~~~~~~

- The default `.Resolver` now uses `.IOLoop.run_in_executor`.
  `.ExecutorResolver`, `.BlockingResolver`, and `.ThreadedResolver` are
  deprecated.
- The ``io_loop`` arguments to `.add_accept_handler`,
  `.ExecutorResolver`, and `.ThreadedResolver` have been removed.
- `.add_accept_handler` returns a callable which can be used to remove
  all handlers that were added.
- `.OverrideResolver` now accepts per-family overrides.

`tornado.options`
~~~~~~~~~~~~~~~~~

- Duplicate option names are now detected properly whether they use
  hyphens or underscores.

`tornado.platform.asyncio`
~~~~~~~~~~~~~~~~~~~~~~~~~~

- `.AsyncIOLoop` and `.AsyncIOMainLoop` are now used automatically
  when appropriate; referencing them explicitly is no longer
  recommended.
- Starting an `.IOLoop` or making it current now also sets the
  `asyncio` event loop for the current thread. Closing an `.IOLoop`
  closes the corresponding `asyncio` event loop.
- `.to_tornado_future` and `.to_asyncio_future` are deprecated since
  they are now no-ops.
- `~.AnyThreadEventLoopPolicy` can now be used to easily allow the creation
  of event loops on any thread (similar to Tornado's prior policy).

`tornado.platform.caresresolver`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to `.CaresResolver` has been removed.

`tornado.platform.twisted`
~~~~~~~~~~~~~~~~~~~~~~~~~~

- The ``io_loop`` arguments to ``TornadoReactor``, ``TwistedResolver``,
  and ``tornado.platform.twisted.install`` have been removed.

`tornado.process`
~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to the `.Subprocess` constructor and
  `.Subprocess.initialize` has been removed.

`tornado.routing`
~~~~~~~~~~~~~~~~~

- A default 404 response is now generated if no delegate is found for
  a request.

`tornado.simple_httpclient`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to `.SimpleAsyncHTTPClient` has been removed.
- TLS is now configured according to `ssl.create_default_context` by
  default.

`tornado.tcpclient`
~~~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to the `.TCPClient` constructor has been
  removed.
- `.TCPClient.connect` has a new ``timeout`` argument.

`tornado.tcpserver`
~~~~~~~~~~~~~~~~~~~

- The ``io_loop`` argument to the `.TCPServer` constructor has been
  removed.
- `.TCPServer` no longer logs ``EBADF`` errors during shutdown.

`tornado.testing`
~~~~~~~~~~~~~~~~~

- The deprecated ``tornado.testing.get_unused_port`` and
  ``tornado.testing.LogTrapTestCase`` have been removed.
- `.AsyncHTTPTestCase.fetch` now supports absolute URLs.
- `.AsyncHTTPTestCase.fetch` now connects to ``127.0.0.1``
  instead of ``localhost`` to be more robust against faulty
  ipv6 configurations.

`tornado.util`
~~~~~~~~~~~~~~

- `tornado.util.TimeoutError` replaces ``tornado.gen.TimeoutError``
  and ``tornado.ioloop.TimeoutError``.
- `.Configurable` now supports configuration at multiple levels of an
  inheritance hierarchy.

`tornado.web`
~~~~~~~~~~~~~

- `.RequestHandler.set_status` no longer requires that the given
  status code appear in `http.client.responses`.
- It is no longer allowed to send a body with 1xx or 204 responses.
- Exception handling now breaks up reference cycles that could delay
  garbage collection.
- `.RedirectHandler` now copies any query arguments from the request
  to the redirect location.
- If both ``If-None-Match`` and ``If-Modified-Since`` headers are present
  in a request to `.StaticFileHandler`, the latter is now ignored.

`tornado.websocket`
~~~~~~~~~~~~~~~~~~~

- The C accelerator now operates on multiple bytes at a time to
  improve performance.
- Requests with invalid websocket headers now get a response with
  status code 400 instead of a closed connection.
- `.WebSocketHandler.write_message` now raises `.WebSocketClosedError` if
  the connection closes while the write is in progress.
- The ``io_loop`` argument to `.websocket_connect` has been removed.

# ===== SOURCE: https://raw.githubusercontent.com/tornadoweb/tornado/master/docs/releases/v6.0.0.rst =====

What's new in Tornado 6.0
=========================

Mar 1, 2019
-----------

Backwards-incompatible changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Python 2.7 and 3.4 are no longer supported; the minimum supported
  Python version is 3.5.2.
- APIs deprecated in Tornado 5.1 have been removed. This includes the
  ``tornado.stack_context`` module and most ``callback`` arguments
  throughout the package. All removed APIs emitted
  `DeprecationWarning` when used in Tornado 5.1, so running your
  application with the ``-Wd`` Python command-line flag or the
  environment variable ``PYTHONWARNINGS=d`` should tell you whether
  your application is ready to move to Tornado 6.0.
- ``.WebSocketHandler.get`` is now a coroutine and must be called
  accordingly in any subclasses that override this method (but note
  that overriding ``get`` is not recommended; either ``prepare`` or
  ``open`` should be used instead).

General changes
~~~~~~~~~~~~~~~

- Tornado now includes type annotations compatible with ``mypy``.
  These annotations will be used when type-checking your application
  with ``mypy``, and may be usable in editors and other tools.
- Tornado now uses native coroutines internally, improving performance.

`tornado.auth`
~~~~~~~~~~~~~~

- All ``callback`` arguments in this package have been removed. Use
  the coroutine interfaces instead.
- The ``OAuthMixin._oauth_get_user`` method has been removed.
  Override `~.OAuthMixin._oauth_get_user_future` instead.

`tornado.concurrent`
~~~~~~~~~~~~~~~~~~~~

- The ``callback`` argument to `.run_on_executor` has been removed.
- ``return_future`` has been removed.

`tornado.gen`
~~~~~~~~~~~~~

- Some older portions of this module have been removed. This includes
  ``engine``, ``YieldPoint``, ``Callback``, ``Wait``, ``WaitAll``,
  ``MultiYieldPoint``, and ``Task``.
- Functions decorated with ``@gen.coroutine`` no longer accept
  ``callback`` arguments.

`tornado.httpclient`
~~~~~~~~~~~~~~~~~~~~

- The behavior of ``raise_error=False`` has changed. Now only
  suppresses the errors raised due to completed responses with non-200
  status codes (previously it suppressed all errors).
- The ``callback`` argument to `.AsyncHTTPClient.fetch` has been removed.

`tornado.httputil`
~~~~~~~~~~~~~~~~~~

- ``HTTPServerRequest.write`` has been removed. Use the methods of
  ``request.connection`` instead.
- Unrecognized ``Content-Encoding`` values now log warnings only for
  content types that we would otherwise attempt to parse.

`tornado.ioloop`
~~~~~~~~~~~~~~~~

- ``IOLoop.set_blocking_signal_threshold``,
  ``IOLoop.set_blocking_log_threshold``, ``IOLoop.log_stack``,
  and ``IOLoop.handle_callback_exception`` have been removed.
- Improved performance of `.IOLoop.add_callback`.

`tornado.iostream`
~~~~~~~~~~~~~~~~~~

- All ``callback`` arguments in this module have been removed except
  for `.BaseIOStream.set_close_callback`.
- ``streaming_callback`` arguments to `.BaseIOStream.read_bytes` and
  `.BaseIOStream.read_until_close` have been removed.
- Eliminated unnecessary logging of "Errno 0".

`tornado.log`
~~~~~~~~~~~~~

- Log files opened by this module are now explicitly set to UTF-8 encoding.

`tornado.netutil`
~~~~~~~~~~~~~~~~~

- The results of ``getaddrinfo`` are now sorted by address family to
  avoid partial failures and deadlocks.

`tornado.platform.twisted`
~~~~~~~~~~~~~~~~~~~~~~~~~~

- ``TornadoReactor`` and ``TwistedIOLoop`` have been removed.

``tornado.simple_httpclient``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- The default HTTP client now supports the ``network_interface``
  request argument to specify the source IP for the connection.
- If a server returns a 3xx response code without a ``Location``
  header, the response is raised or returned directly instead of
  trying and failing to follow the redirect.
- When following redirects, methods other than ``POST`` will no longer
  be transformed into ``GET`` requests. 301 (permanent) redirects are
  now treated the same way as 302 (temporary) and 303 (see other)
  redirects in this respect.
- Following redirects now works with ``body_producer``.

``tornado.stack_context``
~~~~~~~~~~~~~~~~~~~~~~~~~

- The ``tornado.stack_context`` module has been removed.

`tornado.tcpserver`
~~~~~~~~~~~~~~~~~~~

- `.TCPServer.start` now supports a ``max_restarts`` argument (same as
  `.fork_processes`).

`tornado.testing`
~~~~~~~~~~~~~~~~~

- `.AsyncHTTPTestCase` now drops all references to the `.Application`
  during ``tearDown``, allowing its memory to be reclaimed sooner.
- `.AsyncTestCase` now cancels all pending coroutines in ``tearDown``,
  in an effort to reduce warnings from the python runtime about
  coroutines that were not awaited. Note that this may cause
  ``asyncio.CancelledError`` to be logged in other places. Coroutines
  that expect to be running at test shutdown may need to catch this
  exception.

`tornado.web`
~~~~~~~~~~~~~

- The ``asynchronous`` decorator has been removed.
- The ``callback`` argument to `.RequestHandler.flush` has been removed.
- `.StaticFileHandler` now supports large negative values for the
  ``Range`` header and returns an appropriate error for ``end >
  start``.
- It is now possible to set ``expires_days`` in ``xsrf_cookie_kwargs``.

`tornado.websocket`
~~~~~~~~~~~~~~~~~~~

- Pings and other messages sent while the connection is closing are
  now silently dropped instead of logging exceptions.
- Errors raised by ``open()`` are now caught correctly when this method
  is a coroutine.

`tornado.wsgi`
~~~~~~~~~~~~~~

- ``WSGIApplication`` and ``WSGIAdapter`` have been removed.

# ===== SOURCE: https://raw.githubusercontent.com/tornadoweb/tornado/master/docs/releases/v6.3.0.rst =====

What's new in Tornado 6.3.0
===========================

Apr 17, 2023
------------

Highlights
~~~~~~~~~~

- The new `.Application` setting ``xsrf_cookie_name`` can now be used to
  take advantage of the ``__Host`` cookie prefix for improved security.
  To use it, add ``{"xsrf_cookie_name": "__Host-xsrf", "xsrf_cookie_kwargs": 
  {"secure": True}}`` to your `.Application` settings. Note that this feature
  currently only works when HTTPS is used.
- `.WSGIContainer` now supports running the application in a ``ThreadPoolExecutor`` so
  the event loop is no longer blocked.
- `.AsyncTestCase` and `.AsyncHTTPTestCase`, which were deprecated in Tornado 6.2,
  are no longer deprecated.
- WebSockets are now much faster at receiving large messages split into many
  fragments.

General changes
~~~~~~~~~~~~~~~

- Python 3.7 is no longer supported; the minimum supported Python version is 3.8.
  Python 3.12 is now supported.
- To avoid spurious deprecation warnings, users of Python 3.10 should upgrade
  to at least version 3.10.9, and users of Python 3.11 should upgrade to at least
  version 3.11.1. 
- Tornado submodules are now imported automatically on demand. This means it is
  now possible to use a single ``import tornado`` statement and refer to objects
  in submodules such as `tornado.web.RequestHandler`.

Deprecation notices
~~~~~~~~~~~~~~~~~~~

- In Tornado 7.0, `tornado.testing.ExpectLog` will match ``WARNING``
  and above regardless of the current logging configuration, unless the
  ``level`` argument is used.
- `.RequestHandler.get_secure_cookie` is now a deprecated alias for
  `.RequestHandler.get_signed_cookie`. `.RequestHandler.set_secure_cookie`
  is now a deprecated alias for `.RequestHandler.set_signed_cookie`.
- `.RequestHandler.clear_all_cookies` is deprecated. No direct replacement
  is provided; `.RequestHandler.clear_cookie` should be used on individual
  cookies.
- Calling the `.IOLoop` constructor without a ``make_current`` argument, which was
  deprecated in Tornado 6.2, is no longer deprecated.
- `.AsyncTestCase` and `.AsyncHTTPTestCase`, which were deprecated in Tornado 6.2,
  are no longer deprecated.
- `.AsyncTestCase.get_new_ioloop` is deprecated. 

``tornado.auth``
~~~~~~~~~~~~~~~~

- New method `.GoogleOAuth2Mixin.get_google_oauth_settings` can now be overridden
  to get credentials from a source other than the `.Application` settings.

``tornado.gen``
~~~~~~~~~~~~~~~

- `contextvars` now work properly when a ``@gen.coroutine`` calls a native coroutine.

``tornado.options``
~~~~~~~~~~~~~~~~~~~

- `~.OptionParser.parse_config_file` now recognizes single comma-separated strings (in addition to
  lists of strings) for options with ``multiple=True``.

``tornado.web``
~~~~~~~~~~~~~~~

- New `.Application` setting ``xsrf_cookie_name`` can be used to change the
  name of the XSRF cookie. This is most useful to take advantage of the
  ``__Host-`` cookie prefix. 
- `.RequestHandler.get_secure_cookie` and `.RequestHandler.set_secure_cookie`
  (and related methods and attributes) have been renamed to
  `~.RequestHandler.get_signed_cookie` and `~.RequestHandler.set_signed_cookie`.
  This makes it more explicit what kind of security is provided, and avoids
  confusion with the ``Secure`` cookie attribute and ``__Secure-`` cookie prefix.
  The old names remain supported as deprecated aliases.
- `.RequestHandler.clear_cookie` now accepts all keyword arguments accepted by
  `~.RequestHandler.set_cookie`. In some cases clearing a cookie requires certain
  arguments to be passed the same way in which it was set. 
- `.RequestHandler.clear_all_cookies` now accepts additional keyword arguments
  for the same reason as ``clear_cookie``. However, since the requirements
  for additional arguments mean that it cannot reliably clear all cookies,
  this method is now deprecated.


``tornado.websocket``
~~~~~~~~~~~~~~~~~~~~~

- It is now much faster (no longer quadratic) to receive large messages that
  have been split into many fragments.
- `.websocket_connect` now accepts a ``resolver`` parameter.

``tornado.wsgi``
~~~~~~~~~~~~~~~~

- `.WSGIContainer` now accepts an ``executor`` parameter which can be used
  to run the WSGI application on a thread pool. 