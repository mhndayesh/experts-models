
# ===== SOURCE: https://raw.githubusercontent.com/falconry/falcon/master/docs/changes/2.0.0.rst =====

Changelog for Falcon 2.0.0
==========================

.. falcon-release: 2019-04-26

Summary
-------

Many thanks to all of our awesome contributors (listed down below) who made
this release possible!

In 2.0 we added a number of new convenience methods and properties. We also
made it a lot cleaner and less error-prone to assign multiple routes to the
same resource class via suffixed responders.

Also noteworthy is the significant effort we invested in improving the
accuracy, clarity, and breadth of the docs. We hope these changes will help
make the framework easier to learn for newcomers.

Middleware methods can now short-circuit request processing, and we improved
cookie and ETag handling. Plus, the testing framework received several
improvements to make it easier to simulate certain types of requests.

As this is the first major release that we have had in quite a while, we have
taken the opportunity to clean up many parts of the framework. Deprecated
variables, methods, and classes have been removed, along with all
backwards-compatibility shims for old method signatures. We also changed the
defaults for a number of request options based on community feedback.

Please carefully review the list of breaking changes below to see what
you may need to tweak in your app to make it compatible with this release.

Changes to Supported Platforms
------------------------------

- CPython 3.7 is now fully supported.
- Falcon 2.x series is the last to support Python language version 2. As a
  result, support for CPython 2.7 and PyPy2.7 will be removed in Falcon 3.0.
- Support for CPython 3.4 is now deprecated and will be removed in Falcon 3.0.
- Support for CPython 2.6, CPython 3.3 and Jython 2.7 has been dropped.

Breaking Changes
----------------

- Previously, several methods in the :class:`~falcon.Response` class
  could be used to attempt to set raw cookie headers. However,
  due to the Set-Cookie header values not being combinable
  as a comma-delimited list, this resulted in an
  incorrect response being constructed for the user agent in
  the case that more than one cookie was being set. Therefore,
  the following methods of ``falcon.Response`` now raise an
  instance of ``ValueError`` if an attempt is made to use them
  for Set-Cookie: :meth:`~falcon.Response.set_header`,
  :meth:`~falcon.Response.delete_header`, :meth:`~falcon.Response.get_header`,
  :meth:`~falcon.Response.set_headers`.
- :attr:`falcon.testing.Result.json` now returns ``None`` when the response body is
  empty, rather than raising an error.
- :meth:`~falcon.Request.get_param_as_bool` now defaults to treating valueless
  parameters as truthy, rather than falsy. ``None`` is still returned
  by default when the parameter is altogether missing.
- :meth:`~falcon.Request.get_param_as_bool` no longer raises an error for a
  valueless parameter when the ``blank_as_true`` keyword argument is ``False``.
  Instead, ``False`` is simply returned in that case.
- :attr:`~falcon.RequestOptions.keep_blank_qs_values` now defaults to ``True``
  instead of ``False``.
- :attr:`~falcon.RequestOptions.auto_parse_qs_csv` now defaults to ``False``
  instead of ``True``.
- ``independent_middleware`` kwarg on :class:`falcon.API` now defaults to
  ``True`` instead of ``False``.
- The ``stream_len`` property of the :class:`~falcon.Response` class was changed to
  be an alias of the new :attr:`~falcon.Response.content_length` property. Please
  use :meth:`~falcon.Response.set_stream` or :attr:`~falcon.Response.content_length`
  instead, going forward, as ``stream_len`` is now deprecated.
- Request :attr:`~falcon.Request.context_type` was changed from dict to a bare class
  implementing the mapping interface.
  (See also: :ref:`bare_class_context_type`)
- Response :attr:`~falcon.Response.context_type` was changed from dict to a bare class
  implementing the mapping interface.
  (See also: :ref:`bare_class_context_type`)
- :class:`~.media.JSONHandler` and :class:`~.HTTPError` no longer use
  `ujson` in lieu of the standard `json` library (when `ujson` is available in
  the environment). Instead, :class:`~.media.JSONHandler` can now be configured
  to use arbitrary ``dumps()`` and ``loads()`` functions. If you
  also need to customize :class:`~.HTTPError` serialization, you can do so via
  :meth:`~.API.set_error_serializer`.
- The ``find()`` method for a custom router is now required to accept the
  ``req`` keyword argument that was added in a previous release. The
  backwards-compatible shim was removed.
- All :ref:`middleware <middleware>` methods and :ref:`hooks <hooks>` must
  now accept the arguments as specified in the relevant interface definitions
  as of Falcon 2.0. All backwards-compatible shims have been removed.
- Custom error serializers are now required to accept the arguments as
  specified by :meth:`~.API.set_error_serializer` for the past few releases.
  The backwards-compatible shim has been removed.
- An internal function, ``make_router_search()``, was removed from the
  ``api_helpers`` module.
- An internal function, ``wrap_old_error_serializer()``, was removed from the
  ``api_helpers`` module.
- In order to improve performance, the :attr:`falcon.Request.headers` and
  :attr:`falcon.Request.cookies` properties now return a direct reference to
  an internal cached object, rather than making a copy each time. This
  should normally not cause any problems with existing apps since these objects
  are generally treated as read-only by the caller.
- The :attr:`falcon.Request.stream` attribute is no longer wrapped in a bounded
  stream when Falcon detects that it is running on the wsgiref server. If you
  need to normalize stream semantics between wsgiref and a production WSGI
  server, :attr:`~falcon.Request.bounded_stream` may be used instead.
- :attr:`falcon.Request.cookies` now gives precedence to the first value
  encountered in the Cookie header for a given cookie name, rather than the
  last.
- The ordering of the parameters passed to custom error handlers was adjusted
  to be more intuitive and consistent with the rest of the framework::

    # Before
    def handle_error(ex, req, resp, params):
      pass

    # Falcon 2.0
    def handle_error(req, resp, ex, params):
      pass

  See also: :meth:`~.API.add_error_handler`

- :attr:`~.falcon.RequestOptions.strip_url_path_trailing_slash` now defaults
  to ``False`` instead of ``True``.
- The deprecated ``falcon.testing.TestCase.api`` property was removed.
- The deprecated ``falcon.testing.TestCase.api_class`` class variable was removed.
- The deprecated ``falcon.testing.TestBase`` class was removed.
- The deprecated ``falcon.testing.TestResource`` class was removed.
- The deprecated ``protocol`` property was removed from the
  :class:`~falcon.Request` class.
- The deprecated ``get_param_as_dict()`` method alias was removed from the
  :class:`~falcon.Request` class. Please use :meth:`~falcon.Request.get_param_as_json`
  instead.
- Routers were previously allowed to accept additional args and
  keyword arguments, and were not required to use the variadic form. Now,
  they are only allowed to accept additional options as variadic keyword
  arguments, and to ignore any arguments they don't support. This helps
  overridden router logic be less fragile in terms of their interface
  contracts, which also makes it easier to keep Falcon backwards-compatible
  in the face of any future changes in this area.
- :meth:`~.API.add_route` previously accepted `*args`, but now no longer does.
- The ``add_route()`` method for custom routers no longer takes a `method_map`
  argument. Custom routers should, instead, call the
  :meth:`~falcon.routing.map_http_methods` function directly
  from their ``add_route()`` method if they require this mapping.
- The ``serialize()`` media handler method now receives an extra
  `content_type` argument, while the ``deserialize()`` method now takes
  `stream`, `content_type`, and `content_length` arguments, rather than a
  single `raw` argument. The raw data can still be obtained by executing
  ``raw = stream.read()``.

  See also: :class:`~.media.BaseHandler`

- The deprecated ``falcon.routing.create_http_method_map()`` method was
  removed.
- The keyword arguments for :meth:`~falcon.uri.parse_query_string` were renamed
  to be more concise::

    # Before
    parsed_values = parse_query_string(
        query_string, keep_blank_qs_values=True, parse_qs_csv=False
    )

    # Falcon 2.0
    parsed_values = parse_query_string(
        query_string, keep_blank=True, csv=False
    )

- :attr:`~.falcon.RequestOptions.auto_parse_qs_csv` now defaults
  to ``False`` instead of ``True``.
- The ``HTTPRequestEntityTooLarge`` class was renamed to
  :class:`~falcon.HTTPPayloadTooLarge`.
- Two of the keyword arguments for :meth:`~falcon.Request.get_param_as_int` were
  renamed to avoid shadowing built-in Python names::

    # Before
    dpr = req.get_param_as_int('dpr', min=0, max=3)

    # Falcon 2.0
    dpr = req.get_param_as_int('dpr', min_value=0, max_value=3)

- The :meth:`falcon.media.validators.jsonschema.validate` decorator now uses
  :meth:`functools.wraps` to make the decorated method look like the original.
- Previously, :class:`~.HTTPError` instances for which the `has_representation`
  property evaluated to ``False`` were not passed to custom error serializers
  (such as in the case of types that subclass
  :class:`~.NoRepresentation`). This has now been fixed so
  that custom error serializers will be called for all instances of
  :class:`~.HTTPError`.
- Request cookie parsing no longer uses the standard library
  for most of the parsing logic. This may lead to subtly different results
  for archaic cookie header formats, since the new implementation is based on
  RFC 6265.
- The :attr:`~falcon.Request.if_match` and :attr:`~falcon.Request.if_none_match` properties
  now return a list of :class:`falcon.ETag` objects rather than the raw
  value of the If-Match or If-None-Match headers, respectively.
- When setting the :attr:`~falcon.Response.etag` header property, the value will
  now be wrapped with double-quotes (if not already present) to ensure
  compliance with RFC 7232.
- The default error serializer no longer sets the `charset` parameter for the
  media type returned in the Content-Type header, since UTF-8 is the default
  encoding for both JSON and XML media types. This should not break
  well-behaved clients, but could impact test cases in apps that
  assert on the exact value of the Content-Type header.
- Similar to the change made to the default error serializer, the default JSON
  media type generally used for successful responses was also modified
  to no longer specify the `charset` parameter.
  This change affects both the :data:`falcon.DEFAULT_MEDIA_TYPE` and
  :data:`falcon.MEDIA_JSON` :ref:`constants <media_type_constants>`, as well
  as the default value of the `media_type` keyword argument specified for
  the :class:`falcon.API` initializer. This change also affects the default
  value of the :attr:`.RequestOptions.default_media_type` and
  :attr:`.ResponseOptions.default_media_type` options.

New & Improved
--------------

- Several performance optimizations were made to hot code paths in the
  framework to make Falcon 2.0 even faster than 1.4 in some cases.
- Numerous changes were made to the docs to improve clarity and to provide
  better recommendations on how to best use various parts of the framework.
- Added a new :attr:`~falcon.Response.headers` property to the :class:`~falcon.Response` class.
- Removed the :mod:`six` and :mod:`python-mimeparse` dependencies.
- Added a new :attr:`~falcon.Response.complete` property to the :class:`~falcon.Response`
  class. This can be used to short-circuit request processing when the response
  has been pre-constructed.
- Request :attr:`~falcon.Request.context_type` now defaults to a bare class allowing
  to set attributes on the request context object::

    # Before
    req.context['role'] = 'trial'
    req.context['user'] = 'guest'

    # Falcon 2.0
    req.context.role = 'trial'
    req.context.user = 'guest'

  To ease the migration path, the previous behavior is supported by
  implementing the mapping interface in a way that object attributes and
  mapping items are linked, and setting one sets the other as well. However, as
  of Falcon 2.0, the dict context interface is considered deprecated, and may
  be removed in a future release.

  Applications can work around this change by explicitly overriding
  :attr:`~falcon.Request.context_type` to dict.
  (See also: :ref:`bare_class_context_type`)
- Response :attr:`~falcon.Response.context_type` now defaults to a bare class allowing
  to set attributes on the response context object::

    # Before
    resp.context['cache_strategy'] = 'lru'

    # Falcon 2.0
    resp.context.cache_strategy = 'lru'

  To ease the migration path, the previous behavior is supported by
  implementing the mapping interface in a way that object attributes and
  mapping items are linked, and setting one sets the other as well. However, as
  of Falcon 2.0, the dict context interface is considered deprecated, and may
  be removed in a future release.

  Applications can work around this change by explicitly overriding
  :attr:`~falcon.Response.context_type` to dict.
  (See also: :ref:`bare_class_context_type`)
- :class:`~.media.JSONHandler` can now be configured to use arbitrary
  ``dumps()`` and ``loads()`` functions. This enables support not only for
  using any of a number of third-party JSON libraries, but also for
  customizing the keyword arguments used when (de)serializing objects.
- Added a new method, :meth:`~falcon.Request.get_cookie_values`, to the
  :class:`~falcon.Request` class. The new method supports getting all values
  provided for a given cookie, and is now the preferred mechanism for
  reading request cookies.
- Optimized request cookie parsing. It is now roughly an order of magnitude
  faster.
- :meth:`~falcon.Response.append_header` now supports appending raw Set-Cookie header values.
- Multiple routes can now be added for the same resource instance using a
  suffix to distinguish the set of responders that should be used. In this way,
  multiple closely-related routes can be mapped to the same resource while
  preserving readability and consistency.

  See also: :meth:`~.API.add_route`

- The :meth:`falcon.media.validators.jsonschema.validate` decorator now
  supports both request and response validation.
- A static route can now be configured to return the data from a default file
  when the requested file path is not found.

  See also: :meth:`~.API.add_static_route`

- The ordering of the parameters passed to custom error handlers was adjusted
  to be more intuitive and consistent with the rest of the framework::

    # Before
    def handle_error(ex, req, resp, params):
      pass

    # Falcon 2.0
    def handle_error(req, resp, ex, params):
      pass

  See also: :meth:`~.API.add_error_handler`.

- All error classes now accept a `headers` keyword argument for customizing
  response headers.
- A new method, :meth:`~falcon.Request.get_param_as_float`, was added to the
  :class:`~falcon.Request` class.
- A new method, :meth:`~falcon.Request.has_param`, was added to the
  :class:`~falcon.Request` class.
- A new property, :attr:`~falcon.Response.content_length`, was added to the
  :class:`~falcon.Response` class. Either :meth:`~falcon.Response.set_stream` or
  :attr:`~falcon.Response.content_length` should be used going forward, as
  ``stream_len`` is now deprecated.
- All ``get_param_*()`` methods of the :class:`~falcon.Request` class now accept a
  `default` argument.
- A new header property, :attr:`~falcon.Response.expires`, was added to the
  :class:`~falcon.Response` class.
- The :class:`~.routing.CompiledRouter` class now exposes a
  :class:`~falcon.routing.CompiledRouter.map_http_methods` method that child
  classes can override in order to customize the mapping of HTTP methods to
  resource class methods.
- The ``serialize()`` media handler method now receives an extra
  `content_type` argument, while the ``deserialize()`` method now takes
  `stream`, `content_type`, and `content_length` arguments, rather than a
  single `raw` argument. The raw data can still be obtained by executing
  ``raw = stream.read()``.

  See also: :class:`~.media.BaseHandler`

- The :meth:`~falcon.Response.get_header` method now accepts a `default` keyword
  argument.
- The :meth:`~falcon.testing.TestClient.simulate_request` method now supports
  overriding the host and remote IP address in the WSGI environment, as well
  as setting arbitrary additional CGI variables in the WSGI environment.
- The :meth:`~falcon.testing.TestClient.simulate_request` method now supports
  passing a query string as part of the path, as an alternative to using the
  `params` or `query_string` keyword arguments.
- Added a deployment guide to the docs for uWSGI and NGINX on Linux.
- The :meth:`~.uri.decode` method now accepts an `unquote_plus` keyword
  argument. The new argument defaults to ``False`` to avoid a breaking change.
- The :meth:`~falcon.Request.if_match` and :meth:`~falcon.Request.if_none_match` properties
  now return a list of :class:`falcon.ETag` objects rather than the raw
  value of the If-Match or If-None-Match headers, respectively.
- :meth:`~.API.add_error_handler` now supports specifying an iterable of
  exception types to match.
- The default error serializer no longer sets the `charset` parameter for the
  media type returned in the Content-Type header, since UTF-8 is the default
  encoding for both JSON and XML media types.
- Similar to the change made to the default error serializer, the default JSON
  media type generally used for successful responses was also modified
  to no longer specify the `charset` parameter.
  This change affects both the :data:`falcon.DEFAULT_MEDIA_TYPE` and
  :data:`falcon.MEDIA_JSON` :ref:`constants <media_type_constants>`, as well
  as the default value of the `media_type` keyword argument specified for
  the :class:`falcon.API` initializer. This change also affects the default
  value of the :attr:`.RequestOptions.default_media_type` and
  :attr:`.ResponseOptions.default_media_type` options.

Fixed
-----

- Fixed a docs issue where with smaller browser viewports, the API
  documentation will start horizontal scrolling.
- The color scheme for the docs was modified to fix issues with contrast and
  readability when printing the docs or generating PDFs.
- The :meth:`~falcon.testing.TestClient.simulate_request` method now forces
  header values to `str` on Python 2 as required by PEP-3333.
- The ``HTTPRequestEntityTooLarge`` class was renamed to
  :class:`~falcon.HTTPPayloadTooLarge` and the reason phrase was updated
  per RFC 7231.
- The  :class:`falcon.CaseInsensitiveDict` class now inherits from
  :class:`collections.abc.MutableMapping` under Python 3, instead of
  :class:`collections.MutableMapping`.
- The ``\ufffd`` character is now disallowed in requested static file paths.
- The :meth:`falcon.media.validators.jsonschema.validate` decorator now uses
  :meth:`functools.wraps` to make the decorated method look like the original.
- The ``falcon-print-routes`` CLI tool no longer raises an unhandled error
  when Falcon is cythonized.
- The plus character (``'+'``) is no longer unquoted in the request path, but
  only in the query string.
- Previously, :class:`~.HTTPError` instances for which the `has_representation`
  property evaluated to ``False`` were not passed to custom error serializers
  (such as in the case of types that subclass
  :class:`~.NoRepresentation`). This has now been fixed so
  that custom error serializers will be called for all instances of
  :class:`~.HTTPError`.
- When setting the :attr:`~falcon.Response.etag` header property, the value will
  now be wrapped with double-quotes (if not already present) to ensure
  compliance with RFC 7232.
- Fixed ``TypeError`` being raised when using Falcon's testing framework
  to simulate a request to a generator-based WSGI app.

Contributors to this Release
----------------------------

Many thanks to all of our talented and stylish contributors for this release!

- Bertrand Lemasle
- `CaselIT <https://github.com/CaselIT>`_
- `DmitriiTrofimov <https://github.com/DmitriiTrofimov>`_
- `KingAkeem <https://github.com/KingAkeem>`_
- `Nateyo <https://github.com/Nateyo>`_
- Patrick Schneeweis
- `TheMushrr00m <https://github.com/TheMushrr00m>`_
- `ZDBioHazard <https://github.com/ZDBioHazard>`_
- `alysivji <https://github.com/alysivji>`_
- `aparkerlue <https://github.com/aparkerlue>`_
- `astonm <https://github.com/astonm>`_
- `awbush <https://github.com/awbush>`_
- `bendemaree <https://github.com/bendemaree>`_
- `bkcsfi <https://github.com/bkcsfi>`_
- `brooksryba <https://github.com/brooksryba>`_
- `carlodri <https://github.com/carlodri>`_
- `grktsh <https://github.com/grktsh>`_
- `hugovk <https://github.com/hugovk>`_
- `jmvrbanac <https://github.com/jmvrbanac>`_
- `kandziu <https://github.com/kandziu>`_
- `kgriffs <https://github.com/kgriffs>`_
- `klardotsh <https://github.com/klardotsh>`_
- `mikeylight <https://github.com/mikeylight>`_
- `mumrau <https://github.com/mumrau>`_
- `nZac <https://github.com/nZac>`_
- `navyad <https://github.com/navyad>`_
- `ozzzik <https://github.com/ozzzik>`_
- `paneru-rajan <https://github.com/paneru-rajan>`_
- `safaozturk93 <https://github.com/safaozturk93>`_
- `santeyio <https://github.com/santeyio>`_
- `sbensoussan <https://github.com/sbensoussan>`_
- `selfvin <https://github.com/selfvin>`_
- `snobu <https://github.com/snobu>`_
- `steven-upside <https://github.com/steven-upside>`_
- `tribals <https://github.com/tribals>`_
- `vytas7 <https://github.com/vytas7>`_

# ===== SOURCE: https://raw.githubusercontent.com/falconry/falcon/master/docs/changes/3.0.0.rst =====

Changelog for Falcon 3.0.0
==========================

.. falcon-release: 2021-04-05

Summary
-------

We are pleased to present Falcon 3.0, a major new release that includes
:class:`ASGI-based <falcon.asgi.App>` :mod:`asyncio` and :class:`WebSocket
<falcon.asgi.WebSocket>` support, fantastic :ref:`multipart/form-data parsing
<multipart>`, better error handling, enhancements to existing features, and the
usual assortment of bug fixes.

This is easily the biggest release—in terms of both hours volunteered and code
contributed—that we have ever done. We sincerely thank our stupendous group of
38 contributors who submitted pull requests for this release, as well as all
those who have generously provided financial support to the project.

When we began working on this release, we knew we wanted to not only evolve the
framework's existing features, but also to deliver first-class, user-friendly
:mod:`asyncio` support alongside our existing :class:`WSGI <falcon.App>` feature
set.

On the other hand, we have always fought the temptation to expand Falcon's
scope, in order to leave room for community projects and standards to innovate
around common, self-contained capabilities. And so when `ASGI
<https://asgi.readthedocs.io/en/latest/>`_ arrived on the scene, we saw it as
the perfect opportunity to deliver long-requested :mod:`asyncio` and
:class:`WebSocket <falcon.asgi.WebSocket>` features while still encouraging
sharing and reuse within the Python web community.

It can be painful to migrate a large code base to a major new version of a
framework. Therefore, in 3.0 we went to great lengths to minimize breaking
changes, although a number of methods and attributes were deprecated. That being
said, everyone will likely run up against at least one or two items in the
breaking changes list below. Please carefully review the list of changes and
thoroughly test your apps with Falcon 3.0 before deploying to production.

Leading up to this release, members of the core maintainers team spent many
hours (and not a few late nights and weekends) prototyping, tuning, and testing
in order to uphold the high standards of correctness and reliability for which
Falcon is known. That being said, no code is perfect, so please don't hesitate
to reach out on `falconry/user <https://gitter.im/falconry/user>`_ or `GitHub
<https://github.com/falconry/falcon/issues>`_ if you run into any issues.

Again, thanks so much to everyone who supported this release! Over the years we
like to think that our little framework has had a positive impact on the Python
community, and has even helped nudge the state of the art forward. And it is all
thanks to our amazing supporters and contributors.


Changes to Supported Platforms
------------------------------

- Python 3.8 and 3.9 are now fully supported.
- Python 3.6+ is only required when using the new ASGI interface. WSGI is still
  supported on Python 3.5+.
- Python 3.5 support is deprecated and may be removed in the next major release.
- Python 3.4 is no longer supported.
- The Falcon 2.x series was the last to support Python language version 2. As a
  result, support for CPython 2.7 and PyPy2.7 was removed in Falcon 3.0.


Breaking Changes
----------------

- The class :class:`~.falcon.http_error.OptionalRepresentation` and the attribute
  :attr:`~.falcon.HTTPError.has_representation` were deprecated. The default error
  serializer now generates a representation for every error type that derives from
  :class:`falcon.HTTPError`.
  In addition, Falcon now ensures that any previously set response body is cleared
  before handling any raised exception. (`#452 <https://github.com/falconry/falcon/issues/452>`__)
- The class :class:`~.falcon.http_error.NoRepresentation` was deprecated. All
  subclasses of :class:`falcon.HTTPError` now have a media type representation. (`#777 <https://github.com/falconry/falcon/issues/777>`__)
- In order to reconcile differences between the framework's support for WSGI vs. ASGI, the following
  breaking changes were made:

      - :func:`falcon.testing.create_environ` previously set a default User-Agent header, when one
        was not provided, to the value ``'curl/7.24.0 (x86_64-apple-darwin12.0)'``. As of Falcon
        3.0, the default User-Agent string is now ``f'falcon-client/{falcon.__version__}'``. This
        value can be overridden for the sake of backwards-compatibility by setting
        ``falcon.testing.helpers.DEFAULT_UA``.
      - The :func:`falcon.testing.create_environ` function's `protocol` keyword argument was renamed
        to `http_version` and now only includes the version number (the value is no longer prefixed
        with ``'HTTP/'``).
      - The :func:`falcon.testing.create_environ` function's `app` keyword argument was renamed to
        `root_path`.
      - The `writeable` property of :class:`falcon.stream.BoundedStream` was renamed to `writable` per the
        standard file-like I/O interface (the old name was a misspelling)
      - If an error handler raises an exception type other than :class:`falcon.HTTPStatus` or
        :class:`falcon.HTTPError`, remaining middleware `process_response` methods will no longer be
        executed before bubbling up the unhandled exception to the web server.
      - :func:`falcon.get_http_status` no longer accepts floats, and the method itself is deprecated.
      - :func:`falcon.app_helpers.prepare_middleware` no longer accepts a single object; the value
        that is passed must be an iterable.
      - :attr:`falcon.Request.access_route` now includes the value of the
        :attr:`~falcon.Request.remote_addr` property as the last element in the route, if not already
        present in one of the headers that are checked.
      - When the ``'REMOTE_ADDR'`` field is not present in the WSGI environ, Falcon will assume
        ``'127.0.0.1'`` for the value, rather than simply returning ``None`` for
        :attr:`falcon.Request.remote_addr`.

  The changes above were implemented as part of the ASGI+HTTP work stream. (`#1358 <https://github.com/falconry/falcon/issues/1358>`__)
- Header-related methods of the :class:`~falcon.Response` class no longer coerce the
  passed header name to a string via ``str()``. (`#1497 <https://github.com/falconry/falcon/issues/1497>`__)
- An unhandled exception will no longer be raised to the web server. Rather, the framework now installs a default error handler for the :class:`Exception` type. This also means that middleware `process_response` methods will still be called in this case, rather than being skipped as previously. The new default error handler simply generates an HTTP 500 response. This behavior can be overridden by specifying your own error handler for :class:`Exception` via :meth:`~falcon.API.add_error_handler`. (`#1507 <https://github.com/falconry/falcon/issues/1507>`__)
- Exceptions are now handled by the registered handler for the most specific matching exception class, rather than in reverse order of registration. "Specificity" is determined by the method resolution order of the raised exception type. (See :meth:`~falcon.App.add_error_handler` for more details.) (`#1514 <https://github.com/falconry/falcon/issues/1514>`__)
- The deprecated ``stream_len`` property was removed from the :class:`~falcon.Response` class.
  Please use :meth:`~falcon.Response.set_stream()` or :attr:`~falcon.Response.content_length` instead. (`#1517 <https://github.com/falconry/falcon/issues/1517>`__)
- If :attr:`RequestOptions.strip_url_path_trailing_slash
  <falcon.RequestOptions.strip_url_path_trailing_slash>` is enabled, routes
  should now be added without a trailing slash. Previously, the trailing slash
  was always removed as a side effect of a bug regardless of the
  :attr:`~falcon.RequestOptions.strip_url_path_trailing_slash` option value.
  See also: :ref:`trailing_slash_in_path` (`#1544 <https://github.com/falconry/falcon/issues/1544>`__)
- Rename :attr:`falcon.Response.body` and :attr:`falcon.HTTPStatus.body` to ``text``.
  The old name is deprecated, but still available. (`#1578 <https://github.com/falconry/falcon/issues/1578>`__)
- Referencing the class :class:`falcon.stream.BoundedStream` through the
  ``falcon.request_helpers`` module is deprecated. It is now accessible from
  the module ``falcon.stream``. (`#1583 <https://github.com/falconry/falcon/issues/1583>`__)
- General refactoring of internal media handler:

  *  Deserializing an empty body with a handler that does not support it will
     raise :class:`falcon.MediaNotFoundError`, and will be rendered as a
     ``400 Bad Request`` response. This error may be suppressed by passing
     a default value to ``get_media`` to be used in case of empty body.
     See also :meth:`falcon.Request.get_media` for details.
     Previously ``None`` was returned in all cases without calling the handler.
  *  Exceptions raised by the handlers are wrapped as
     :class:`falcon.MediaMalformedError`, and will be rendered as a
     ``400 Bad Request`` response.
  *  Subsequent calls to :meth:`falcon.Request.get_media` or :attr:`falcon.Request.media` will
     re-raise the same exception, if the first call ended in an error, unless the
     exception was a :class:`falcon.MediaNotFoundError` and a default value is
     passed to the ``default_when_empty`` attribute of the current invocation.
     Previously ``None`` was returned.

  External handlers should update their logic to align to the internal Falcon handlers. (`#1589 <https://github.com/falconry/falcon/issues/1589>`__)
- The :attr:`falcon.Response.data` property now just simply returns the same data
  object that it was set to, if any, rather than also checking and serializing
  the value of the :attr:`falcon.Response.media` property. Instead, a new
  :meth:`~falcon.Response.render_body` method has been implemented, which can be
  used to obtain the HTTP response body for the request, taking into account
  the :attr:`~falcon.Response.text`, :attr:`~falcon.Response.data`, and
  :attr:`~falcon.Response.media` attributes. (`#1679 <https://github.com/falconry/falcon/issues/1679>`__)
- The ``params_csv`` parameter now defaults to ``False`` in
  :func:`falcon.testing.simulate_request`.
  The change was made to match the default value of the request option
  :attr:`~falcon.RequestOptions.auto_parse_qs_csv` (``False`` since Falcon 2.0). (`#1730 <https://github.com/falconry/falcon/issues/1730>`__)
- The :meth:`falcon.HTTPError.to_json` now returns ``bytes`` instead of ``str``.
  Importing ``json`` from ``falcon.util`` is deprecated. (`#1767 <https://github.com/falconry/falcon/issues/1767>`__)
- The private attributes for :class:`~.falcon.media.JSONHandler` were renamed, and
  the private attributes used by :class:`~.falcon.media.MessagePackHandler` were
  replaced. Subclasses that refer to these variables will need to be updated. In
  addition, the undocumented :meth:`falcon.media.Handlers.find_by_media_type`
  method was deprecated and may be removed in a future release. (`#1822 <https://github.com/falconry/falcon/issues/1822>`__)


New & Improved
--------------

- ASGI+WebSocket support was added to the framework via :class:`falcon.asgi.App` and :class:`falcon.asgi.WebSocket`. (`#321 <https://github.com/falconry/falcon/issues/321>`__)
- The error classes in ``falcon.errors`` were updated to have the ``title`` and
  ``description`` keyword arguments and to correctly handle headers passed as
  list of tuples (`#777 <https://github.com/falconry/falcon/issues/777>`__)
- :class:`~falcon.media.MultipartFormHandler` was added to enable support for multipart forms (of content
  type ``multipart/form-data``) through :meth:`falcon.Request.get_media()`. (`#953 <https://github.com/falconry/falcon/issues/953>`__)
- The :attr:`falcon.Response.status` attribute can now be also set to an
  ``http.HTTPStatus`` instance, an integer status code, as well as anything
  supported by the :func:`falcon.code_to_http_status` utility method. (`#1135 <https://github.com/falconry/falcon/issues/1135>`__)
- A new kwarg, ``cors_enable``, was added to the :class:`falcon.App` initializer.
  ``cors_enable`` can be used to enable a simple blanket CORS policy for all
  responses. (See also: :ref:`cors`.) (`#1194 <https://github.com/falconry/falcon/issues/1194>`__)
- ASGI+HTTP support was added to the framework via a new class, :class:`falcon.asgi.App`. The
  :ref:`testing <testing>` module was also updated to fully support ASGI apps, including two new
  helper functions: :func:`falcon.testing.create_scope` and :func:`falcon.testing.create_asgi_req`.
  WSGI users also get a new :func:`falcon.testing.create_req` method. As part of the ASGI work,
  several additional utility functions were added, including :func:`falcon.is_python_func`,
  :func:`falcon.http_status_to_code` and :func:`falcon.code_to_http_status`; as well as sync/async
  helpers :func:`falcon.get_running_loop`, :func:`falcon.create_task`, :func:`falcon.sync_to_async`,  :func:`falcon.wrap_sync_to_async`,
  and  :func:`falcon.wrap_sync_to_async_unsafe`. (`#1358 <https://github.com/falconry/falcon/issues/1358>`__)
- The :class:`falcon.App` class initializer now supports a new argument
  ``sink_before_static_route`` (default ``True``, maintaining 2.0 behavior) to
  specify if :meth:`sinks <falcon.App.add_sink>` should be handled before or
  after :meth:`static routes <falcon.App.add_static_route>`. (`#1372 <https://github.com/falconry/falcon/issues/1372>`__)
- The :meth:`falcon.Response.append_link` method now supports setting the `crossorigin`
  link CORS settings attribute. (`#1410 <https://github.com/falconry/falcon/issues/1410>`__)
- Falcon now supports all WebDAV methods (RFC 2518 and RFC 4918), such as COPY, LOCK, MKCOL, MOVE, PROPFIND, PROPPATCH and UNLOCK. (`#1426 <https://github.com/falconry/falcon/issues/1426>`__)
- Added inspect module to collect information about an application regarding
  the registered routes, middleware, static routes, sinks and error handlers
  (See also: :ref:`inspect`.) (`#1435 <https://github.com/falconry/falcon/issues/1435>`__)
- WSGI path decoding in :class:`falcon.Request` was optimized, and is now
  significantly faster than in Falcon 2.0. (`#1492 <https://github.com/falconry/falcon/issues/1492>`__)
- The :meth:`~falcon.Response.set_headers` method now accepts an instance of any dict-like
  object that implements an ``items()`` method. (`#1546 <https://github.com/falconry/falcon/issues/1546>`__)
- Change :class:`falcon.routing.CompiledRouter` to compile the routes
  only when the first request is routed. This can be changed by
  passing ``compile=True`` to :meth:`falcon.routing.CompiledRouter.add_route`. (`#1550 <https://github.com/falconry/falcon/issues/1550>`__)
- The :meth:`~falcon.Response.set_cookie` method now supports setting the
  `SameSite` cookie attribute. (`#1556 <https://github.com/falconry/falcon/issues/1556>`__)
- The ``falcon.API`` class was renamed to :class:`falcon.App`. The old ``API`` class
  remains available as an alias for backwards-compatibility, but it is now
  considered deprecated and will be removed in a future release. (`#1579 <https://github.com/falconry/falcon/issues/1579>`__)
- :class:`~falcon.media.URLEncodedFormHandler` was added to enable support for URL-encoded forms (of content
  type ``application/x-www-form-urlencoded``) through :meth:`falcon.Request.get_media()`. The :attr:`~.RequestOptions.auto_parse_form_urlencoded` option is now
  deprecated in favor of :class:`~falcon.media.URLEncodedFormHandler`.
  (See also: :ref:`access_urlencoded_form`). (`#1580 <https://github.com/falconry/falcon/issues/1580>`__)
- :meth:`~falcon.Request.get_param_as_bool` now supports the use of ``'t'`` and ``'y'``
  values for ``True``, as well as ``'f'`` and ``'n'`` for ``False``. (`#1606 <https://github.com/falconry/falcon/issues/1606>`__)
- :meth:`falcon.testing.simulate_request()` now accepts a
  `content_type` keyword argument. This provides a more convenient way to set
  this common header vs. the `headers` argument. (`#1646 <https://github.com/falconry/falcon/issues/1646>`__)
- When no route matches a request, the framework will now raise a
  specialized subclass of :class:`~.falcon.HTTPNotFound`
  (:class:`~.falcon.HTTPRouteNotFound`) so that
  a custom error handler can distinguish that specific case if desired. (`#1647 <https://github.com/falconry/falcon/issues/1647>`__)
- :class:`Default media handlers <falcon.media.Handlers>` were simplified by
  removing a separate handler for the now-obsolete
  ``application/json; charset=UTF-8``.
  As a result, providing a custom JSON media handler will now unambiguously cover
  both ``application/json`` and the former ``Content-type``. (`#1717 <https://github.com/falconry/falcon/issues/1717>`__)


Fixed
-----

- Previously, the default :class:`CompiledRouter <falcon.routing.CompiledRouter>`
  was erroneously stripping trailing slashes from URI templates.
  This has been fixed so that it is now possible to add two different routes for
  a path with and without a trailing forward slash (see also:
  :attr:`RequestOptions.strip_url_path_trailing_slash
  <falcon.RequestOptions.strip_url_path_trailing_slash>`). (`#1544 <https://github.com/falconry/falcon/issues/1544>`__)
- :meth:`falcon.uri.decode` and :meth:`falcon.uri.parse_query_string` no longer
  explode quadratically for a large number of percent-encoded characters. The
  time complexity of these utility functions is now always close to *O*\(*n*). (`#1594 <https://github.com/falconry/falcon/issues/1594>`__)
- When :attr:`~falcon.RequestOptions.auto_parse_qs_csv` is enabled, the framework
  now correctly parses all occurrences of the same parameter in the query string,
  rather than only splitting the values in the first occurrence. For example,
  whereas previously ``t=1,2&t=3,4`` would become ``['1', '2', '3,4']``, now the
  resulting list will be ``['1', '2', '3', '4']`` (`#1597 <https://github.com/falconry/falcon/issues/1597>`__)
- The :func:`~falcon.uri.parse_query_string()` utility function is now correctly parsing an
  empty string as ``{}``. (`#1600 <https://github.com/falconry/falcon/issues/1600>`__)
- Previously, response serialization errors (such as in the case of a faulty
  custom media handler, or because an instance of
  :class:`~falcon.HTTPUnsupportedMediaType` was raised for an unsupported
  response content type) were unexpectedly bubbled up to the application server.
  This has been fixed, and these errors are now handled exactly the same way as
  other exceptions raised in a responder (see also: :ref:`errors`). (`#1607 <https://github.com/falconry/falcon/issues/1607>`__)
- :attr:`falcon.Request.forwarded_host` now contains the port when proxy headers
  are not set, to make it possible to correctly reconstruct the URL when the
  application is not behind a proxy. (`#1678 <https://github.com/falconry/falcon/issues/1678>`__)
- The :attr:`Response.downloadable_as <falcon.Response.downloadable_as>` property
  is now correctly encoding non-ASCII filenames as per
  `RFC 6266 <https://tools.ietf.org/html/rfc6266#appendix-D>`_ recommendations. (`#1749 <https://github.com/falconry/falcon/issues/1749>`__)
- The :class:`falcon.routing.CompiledRouter` no longer mistakenly sets route parameters
  while exploring non matching routes. (`#1779 <https://github.com/falconry/falcon/issues/1779>`__)
- The :func:`~falcon.to_query_str` method now correctly encodes parameter keys
  and values. As a result, the `params` parameter in
  :func:`~falcon.testing.simulate_request` will now correctly pass values
  containing special characters (such as ``'&'``) to the application. (`#1871 <https://github.com/falconry/falcon/issues/1871>`__)
- :attr:`falcon.uri.encode` and :attr:`falcon.uri.encode_value` now escape all
  percent characters by default even if it appears they have already been escaped.
  The :attr:`falcon.uri.encode_check_escaped` and :attr:`falcon.uri.encode_value_check_escaped`
  methods have been added to give the option of retaining the previous behavior where needed.
  These new methods have been applied to the :attr:`falcon.Response.location`,
  :attr:`falcon.Response.content_location`, :meth:`falcon.Response.append_link`
  attrs and methods to retain previous behavior. (`#1872 <https://github.com/falconry/falcon/issues/1872>`__)
- Previously, methods marked with the :func:`~falcon.deprecated` utility wrapper
  could raise an unexpected ``AttributeError`` when running under certain
  applications servers such as Meinheld. This has been fixed so that
  :func:`~falcon.deprecated` no longer relies on the availability of
  interpreter-specific stack frame introspection capabilities. (`#1882 <https://github.com/falconry/falcon/issues/1882>`__)


Misc
----

- Deprecate the use of positional arguments for the optional kw args of
  the :class:`falcon.HTTPError` subclasses (`#777 <https://github.com/falconry/falcon/issues/777>`__)
- Setup towncrier to make CHANGES reporting much easier. (`#1461 <https://github.com/falconry/falcon/issues/1461>`__)
- Fix test errors on Windows (`#1656 <https://github.com/falconry/falcon/issues/1656>`__)
- A new method, :meth:`~falcon.Request.get_media`, was added that can now be used
  instead of the :attr:`falcon.Request.media` property to make it more clear to
  app maintainers that getting the media object for a request involves a
  side-effect of consuming and deserializing the body stream. The original
  property remains available to ensure backwards-compatibility with existing apps. (`#1679 <https://github.com/falconry/falcon/issues/1679>`__)
- Falcon now uses the :class:`falcon.Response` media handlers when serializing
  to JSON :class:`falcon.HTTPError` and :class:`falcon.asgi.SSEvent`.
  :class:`falcon.Request` will use its defined media handler when loading a
  param as JSON with :meth:`falcon.Request.get_param_as_json`. (`#1767 <https://github.com/falconry/falcon/issues/1767>`__)
- The `add_link()` method of the :class:`falcon.Request` class was renamed to
  :meth:`falcon.Response.append_link`. The old name is still available as a
  deprecated alias. (`#1801 <https://github.com/falconry/falcon/issues/1801>`__)


Contributors to this Release
----------------------------

Many thanks to all of our talented and stylish contributors for this release!

- `adsahay <https://github.com/adsahay>`_
- `AR4Z <https://github.com/AR4Z>`_
- `ashutoshvarma <https://github.com/ashutoshvarma>`_
- `bibekjoshi54 <https://github.com/bibekjoshi54>`_
- `BigBlueHat <https://github.com/BigBlueHat>`_
- `brunneis <https://github.com/brunneis>`_
- `CaselIT <https://github.com/CaselIT>`_
- `Ciemaar <https://github.com/Ciemaar>`_
- `Coykto <https://github.com/Coykto>`_
- `cozyDoomer <https://github.com/cozyDoomer>`_
- `cravindra <https://github.com/cravindra>`_
- `csojinb <https://github.com/csojinb>`_
- `danilito19 <https://github.com/danilito19>`_
- `edmondb <https://github.com/edmondb>`_
- `flokX <https://github.com/flokX>`_
- `grktsh <https://github.com/grktsh>`_
- `hackedd <https://github.com/hackedd>`_
- `jmvrbanac <https://github.com/jmvrbanac>`_
- `karlhigley <https://github.com/karlhigley>`_
- `kemingy <https://github.com/kemingy>`_
- `kgriffs <https://github.com/kgriffs>`_
- `mattdonders <https://github.com/mattdonders>`_
- `MinesJA <https://github.com/MinesJA>`_
- `minrock <https://github.com/minrock>`_
- `mivade <https://github.com/mivade>`_
- `mosi-kha <https://github.com/mosi-kha>`_
- `myusko <https://github.com/myusko>`_
- `nagaabhinaya <https://github.com/nagaabhinaya>`_
- `nZac <https://github.com/nZac>`_
- `pbjr23 <https://github.com/pbjr23>`_
- `rmyers <https://github.com/rmyers>`_
- `safaozturk93 <https://github.com/safaozturk93>`_
- `screamingskulls <https://github.com/screamingskulls>`_
- `seanharrison <https://github.com/seanharrison>`_
- `timgates42 <https://github.com/timgates42>`_
- `vytas7 <https://github.com/vytas7>`_
- `waghanza <https://github.com/waghanza>`_
- `withshubh <https://github.com/withshubh>`_
