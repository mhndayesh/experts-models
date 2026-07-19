
# ===== SOURCE: https://raw.githubusercontent.com/django/django/main/docs/releases/4.0.txt =====

========================
Django 4.0 release notes
========================

*December 7, 2021*

Welcome to Django 4.0!

These release notes cover the :ref:`new features <whats-new-4.0>`, as well as
some :ref:`backwards incompatible changes <backwards-incompatible-4.0>` you'll
want to be aware of when upgrading from Django 3.2 or earlier. We've
:ref:`begun the deprecation process for some features
<deprecated-features-4.0>`.

See the :doc:`/howto/upgrade-version` guide if you're updating an existing
project.

Python compatibility
====================

Django 4.0 supports Python 3.8, 3.9, and 3.10. We **highly recommend** and only
officially support the latest release of each series.

The Django 3.2.x series is the last to support Python 3.6 and 3.7.

.. _whats-new-4.0:

What's new in Django 4.0
========================

``zoneinfo`` default timezone implementation
--------------------------------------------

The Python standard library's :mod:`zoneinfo` is now the default timezone
implementation in Django.

This is the next step in the migration from using ``pytz`` to using
:mod:`zoneinfo`. Django 3.2 allowed the use of non-``pytz`` time zones. Django
4.0 makes ``zoneinfo`` the default implementation. Support for ``pytz`` is now
deprecated and will be removed in Django 5.0.

:mod:`zoneinfo` is part of the Python standard library from Python 3.9. The
``backports.zoneinfo`` package is automatically installed alongside Django if
you are using Python 3.8.

The move to ``zoneinfo`` should be largely transparent. Selection of the
current timezone, conversion of datetime instances to the current timezone in
forms and templates, as well as operations on aware datetimes in UTC are
unaffected.

However, if you are working with non-UTC time zones, and using the ``pytz``
``normalize()`` and ``localize()`` APIs, possibly with the :setting:`TIME_ZONE
<DATABASE-TIME_ZONE>` setting, you will need to audit your code, since ``pytz``
and ``zoneinfo`` are not entirely equivalent.

To give time for such an audit, the transitional ``USE_DEPRECATED_PYTZ``
setting allows continued use of ``pytz`` during the 4.x release cycle. This
setting will be removed in Django 5.0.

In addition, a `pytz_deprecation_shim`_ package, created by the ``zoneinfo``
author, can be used to assist with the migration from ``pytz``. This package
provides shims to help you safely remove ``pytz``, and has a detailed
`migration guide`_ showing how to move to the new ``zoneinfo`` APIs.

Using `pytz_deprecation_shim`_ and the ``USE_DEPRECATED_PYTZ``
transitional setting is recommended if you need a gradual update path.

.. _pytz_deprecation_shim: https://pytz-deprecation-shim.readthedocs.io/en/latest/index.html
.. _migration guide: https://pytz-deprecation-shim.readthedocs.io/en/latest/migration.html

Functional unique constraints
-----------------------------

The new :attr:`*expressions <django.db.models.UniqueConstraint.expressions>`
positional argument of
:class:`UniqueConstraint() <django.db.models.UniqueConstraint>` enables
creating functional unique constraints on expressions and database functions.
For example::

    from django.db import models
    from django.db.models import UniqueConstraint
    from django.db.models.functions import Lower


    class MyModel(models.Model):
        first_name = models.CharField(max_length=255)
        last_name = models.CharField(max_length=255)

        class Meta:
            constraints = [
                UniqueConstraint(
                    Lower("first_name"),
                    Lower("last_name").desc(),
                    name="first_last_name_unique",
                ),
            ]

Functional unique constraints are added to models using the
:attr:`Meta.constraints <django.db.models.Options.constraints>` option.

``scrypt`` password hasher
--------------------------

The new :ref:`scrypt password hasher <scrypt-usage>` is more secure and
recommended over PBKDF2. However, it's not the default as it requires OpenSSL
1.1+ and more memory.

Redis cache backend
-------------------

The new ``django.core.cache.backends.redis.RedisCache`` cache backend provides
built-in support for caching with Redis. :pypi:`redis-py <redis>` 3.0.0 or
higher is required. For more details, see the :ref:`documentation on caching
with Redis in Django <redis>`.

Template based form rendering
-----------------------------

:class:`Forms <django.forms.Form>`, :doc:`Formsets </topics/forms/formsets>`,
and :class:`~django.forms.ErrorList` are now rendered using the template engine
to enhance customization. See the new :meth:`~django.forms.Form.render`,
:meth:`~django.forms.Form.get_context`, and
:attr:`~django.forms.Form.template_name` for ``Form`` and
:ref:`formset rendering <formset-rendering>` for ``Formset``.

Minor features
--------------

:mod:`django.contrib.admin`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The ``admin/base.html`` template now has a new block ``header`` which
  contains the admin site header.

* The new :meth:`.ModelAdmin.get_formset_kwargs` method allows customizing the
  keyword arguments passed to the constructor of a formset.

* The navigation sidebar now has a quick filter toolbar.

* The new context variable ``model`` which contains the model class for each
  model is added to the :meth:`.AdminSite.each_context` method.

* The new :attr:`.ModelAdmin.search_help_text` attribute allows specifying a
  descriptive text for the search box.

* The :attr:`.InlineModelAdmin.verbose_name_plural` attribute now fallbacks to
  the :attr:`.InlineModelAdmin.verbose_name` + ``'s'``.

* jQuery is upgraded from version 3.5.1 to 3.6.0.

:mod:`django.contrib.admindocs`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The admindocs now allows esoteric setups where :setting:`ROOT_URLCONF` is not
  a string.

* The model section of the ``admindocs`` now shows cached properties.

:mod:`django.contrib.auth`
~~~~~~~~~~~~~~~~~~~~~~~~~~

* The default iteration count for the PBKDF2 password hasher is increased from
  260,000 to 320,000.

* The new
  :attr:`LoginView.next_page <django.contrib.auth.views.LoginView.next_page>`
  attribute and
  :meth:`~django.contrib.auth.views.LoginView.get_default_redirect_url` method
  allow customizing the redirect after login.

:mod:`django.contrib.gis`
~~~~~~~~~~~~~~~~~~~~~~~~~

* Added support for SpatiaLite 5.

* :class:`~django.contrib.gis.gdal.GDALRaster` now allows creating rasters in
  any GDAL virtual filesystem.

* The new :class:`~django.contrib.gis.admin.GISModelAdmin` class allows
  customizing the widget used for ``GeometryField``. This is encouraged instead
  of deprecated ``GeoModelAdmin`` and ``OSMGeoAdmin``.

:mod:`django.contrib.postgres`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The PostgreSQL backend now supports connecting by a service name. See
  :ref:`postgresql-connection-settings` for more details.

* The new :class:`~django.contrib.postgres.operations.AddConstraintNotValid`
  operation allows creating check constraints on PostgreSQL without verifying
  that all existing rows satisfy the new constraint.

* The new :class:`~django.contrib.postgres.operations.ValidateConstraint`
  operation allows validating check constraints which were created using
  :class:`~django.contrib.postgres.operations.AddConstraintNotValid` on
  PostgreSQL.

* The new
  :class:`ArraySubquery() <django.contrib.postgres.expressions.ArraySubquery>`
  expression allows using subqueries to construct lists of values on
  PostgreSQL.

* The new :lookup:`trigram_word_similar` lookup, and the
  :class:`TrigramWordDistance()
  <django.contrib.postgres.search.TrigramWordDistance>` and
  :class:`TrigramWordSimilarity()
  <django.contrib.postgres.search.TrigramWordSimilarity>` expressions allow
  using trigram word similarity.

:mod:`django.contrib.staticfiles`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :class:`~django.contrib.staticfiles.storage.ManifestStaticFilesStorage` now
  replaces paths to JavaScript source map references with their hashed
  counterparts.

* The new ``manifest_storage`` argument of
  :class:`~django.contrib.staticfiles.storage.ManifestFilesMixin` and
  :class:`~django.contrib.staticfiles.storage.ManifestStaticFilesStorage`
  allows customizing the manifest file storage.

Cache
~~~~~

* The new async API for ``django.core.cache.backends.base.BaseCache`` begins
  the process of making cache backends async-compatible. The new async methods
  all have ``a`` prefixed names, e.g. ``aadd()``, ``aget()``, ``aset()``,
  ``aget_or_set()``, or ``adelete_many()``.

  Going forward, the ``a`` prefix will be used for async variants of methods
  generally.

CSRF
~~~~

* CSRF protection now consults the ``Origin`` header, if present. To facilitate
  this, :ref:`some changes <csrf-trusted-origins-changes-4.0>` to the
  :setting:`CSRF_TRUSTED_ORIGINS` setting are required.

Forms
~~~~~

* :class:`~django.forms.ModelChoiceField` now includes the provided value in
  the ``params`` argument of a raised
  :exc:`~django.core.exceptions.ValidationError` for the ``invalid_choice``
  error message. This allows custom error messages to use the ``%(value)s``
  placeholder.

* :class:`~django.forms.formsets.BaseFormSet` now renders non-form errors with
  an additional class of ``nonform`` to help distinguish them from
  form-specific errors.

* :class:`~django.forms.formsets.BaseFormSet` now allows customizing the widget
  used when deleting forms via
  :attr:`~django.forms.formsets.BaseFormSet.can_delete` by setting the
  :attr:`~django.forms.formsets.BaseFormSet.deletion_widget` attribute or
  overriding :meth:`~django.forms.formsets.BaseFormSet.get_deletion_widget`
  method.

Internationalization
~~~~~~~~~~~~~~~~~~~~

* Added support and translations for the Malay language.

Generic Views
~~~~~~~~~~~~~

* :class:`~django.views.generic.edit.DeleteView` now uses
  :class:`~django.views.generic.edit.FormMixin`, allowing you to provide a
  :class:`~django.forms.Form` subclass, with a checkbox for example, to confirm
  deletion. In addition, this allows ``DeleteView`` to function with
  :class:`django.contrib.messages.views.SuccessMessageMixin`.

  In accordance with ``FormMixin``, object deletion for POST requests is
  handled in ``form_valid()``. Custom delete logic in ``delete()`` handlers
  should be moved to ``form_valid()``, or a shared helper method, as needed.

Logging
~~~~~~~

* The alias of the database used in an SQL call is now passed as extra context
  along with each message to the :ref:`django-db-logger` logger.

Management Commands
~~~~~~~~~~~~~~~~~~~

* The :djadmin:`runserver` management command now supports the
  :option:`--skip-checks` option.

* On PostgreSQL, :djadmin:`dbshell` now supports specifying a password file.

* The :djadmin:`shell` command now respects :data:`sys.__interactivehook__`
  at startup. This allows loading shell history between interactive sessions.
  As a consequence, ``readline`` is no longer loaded if running in *isolated*
  mode.

* The new :attr:`BaseCommand.suppressed_base_arguments
  <django.core.management.BaseCommand.suppressed_base_arguments>` attribute
  allows suppressing unsupported default command options in the help output.

* The new :option:`startapp --exclude` and :option:`startproject --exclude`
  options allow excluding directories from the template.

Models
~~~~~~

* New :meth:`QuerySet.contains(obj) <.QuerySet.contains>` method returns
  whether the queryset contains the given object. This tries to perform the
  query in the simplest and fastest way possible.

* The new ``precision`` argument of the
  :class:`Round() <django.db.models.functions.Round>` database function allows
  specifying the number of decimal places after rounding.

* :meth:`.QuerySet.bulk_create` now sets the primary key on objects when using
  SQLite 3.35+.

* :class:`~django.db.models.DurationField` now supports multiplying and
  dividing by scalar values on SQLite.

* :meth:`.QuerySet.bulk_update` now returns the number of objects updated.

* The new :attr:`.Expression.empty_result_set_value` attribute allows
  specifying a value to return when the function is used over an empty result
  set.

* The ``skip_locked`` argument of :meth:`.QuerySet.select_for_update` is now
  allowed on MariaDB 10.6+.

* :class:`~django.db.models.Lookup` expressions may now be used in ``QuerySet``
  annotations, aggregations, and directly in filters.

* The new :ref:`default <aggregate-default>` argument for built-in aggregates
  allows specifying a value to be returned when the queryset (or grouping)
  contains no entries, rather than ``None``.

Requests and Responses
~~~~~~~~~~~~~~~~~~~~~~

* The :class:`~django.middleware.security.SecurityMiddleware` now adds the
  :ref:`Cross-Origin Opener Policy <cross-origin-opener-policy>` header with a
  value of ``'same-origin'`` to prevent cross-origin popups from sharing the
  same browsing context. You can prevent this header from being added by
  setting the :setting:`SECURE_CROSS_ORIGIN_OPENER_POLICY` setting to ``None``.

Signals
~~~~~~~

* The new ``stdout`` argument for :func:`~django.db.models.signals.pre_migrate`
  and :func:`~django.db.models.signals.post_migrate` signals allows redirecting
  output to a stream-like object. It should be preferred over
  :data:`sys.stdout` and :func:`print` when emitting verbose output in
  order to allow proper capture when testing.

Templates
~~~~~~~~~

* :tfilter:`floatformat` template filter now allows using the ``u`` suffix to
  force disabling localization.

Tests
~~~~~

* The new ``serialized_aliases`` argument of
  :func:`django.test.utils.setup_databases` determines which
  :setting:`DATABASES` aliases test databases should have their state
  serialized to allow usage of the
  :ref:`serialized_rollback <test-case-serialized-rollback>` feature.

* The :option:`test --buffer` option now supports parallel tests.

* The new ``logger`` argument to :class:`~django.test.runner.DiscoverRunner`
  allows a Python :ref:`logger <logger>` to be used for logging.

* The new :meth:`.DiscoverRunner.log` method provides a way to log messages
  that uses the ``DiscoverRunner.logger``, or prints to the console if not set.

* :class:`~django.test.runner.DiscoverRunner` can now execute tests in a random
  order using the :option:`test --shuffle` option.

* The :option:`test --parallel` option now supports the value ``auto`` to run
  one test process for each processor core.

* :meth:`.TestCase.captureOnCommitCallbacks` now captures new callbacks added
  while executing :func:`.transaction.on_commit` callbacks.

.. _backwards-incompatible-4.0:

Backwards incompatible changes in 4.0
=====================================

Database backend API
--------------------

This section describes changes that may be needed in third-party database
backends.

* ``DatabaseOperations.year_lookup_bounds_for_date_field()`` and
  ``year_lookup_bounds_for_datetime_field()`` methods now take the optional
  ``iso_year`` argument in order to support bounds for ISO-8601 week-numbering
  years.

* The second argument of ``DatabaseSchemaEditor._unique_sql()`` and
  ``_create_unique_sql()`` methods is now ``fields`` instead of ``columns``.

:mod:`django.contrib.gis`
-------------------------

* Support for PostGIS 2.3 is removed.

* Support for GDAL 2.0 and GEOS 3.5 is removed.

Dropped support for PostgreSQL 9.6
----------------------------------

Upstream support for PostgreSQL 9.6 ends in November 2021. Django 4.0 supports
PostgreSQL 10 and higher.

Also, the minimum supported version of ``psycopg2`` is increased from 2.5.4 to
2.8.4, as ``psycopg2`` 2.8.4 is the first release to support Python 3.8.

Dropped support for Oracle 12.2 and 18c
---------------------------------------

Upstream support for Oracle 12.2 ends in March 2022 and for Oracle 18c it ends
in June 2021. Django 3.2 will be supported until April 2024. Django 4.0
officially supports Oracle 19c.

.. _csrf-trusted-origins-changes-4.0:

``CSRF_TRUSTED_ORIGINS`` changes
--------------------------------

Format change
~~~~~~~~~~~~~

Values in the :setting:`CSRF_TRUSTED_ORIGINS` setting must include the scheme
(e.g. ``'http://'`` or ``'https://'``) instead of only the hostname.

Also, values that started with a dot, must now also include an asterisk before
the dot. For example, change ``'.example.com'`` to ``'https://*.example.com'``.

A system check detects any required changes.

Configuring it may now be required
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

As CSRF protection now consults the ``Origin`` header, you may need to set
:setting:`CSRF_TRUSTED_ORIGINS`, particularly if you allow requests from
subdomains by setting :setting:`CSRF_COOKIE_DOMAIN` (or
:setting:`SESSION_COOKIE_DOMAIN` if :setting:`CSRF_USE_SESSIONS` is enabled) to
a value starting with a dot.

``SecurityMiddleware`` no longer sets the ``X-XSS-Protection`` header
---------------------------------------------------------------------

The :class:`~django.middleware.security.SecurityMiddleware` no longer sets the
``X-XSS-Protection`` header if the ``SECURE_BROWSER_XSS_FILTER`` setting is
``True``. The setting is removed.

Most modern browsers don't honor the ``X-XSS-Protection`` HTTP header. You can
use Content-Security-Policy_ without allowing ``'unsafe-inline'`` scripts
instead.

If you want to support legacy browsers and set the header, use this line in a
custom middleware::

    response.headers.setdefault("X-XSS-Protection", "1; mode=block")

.. _Content-Security-Policy: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy

Migrations autodetector changes
-------------------------------

The migrations autodetector now uses model states instead of model classes.
Also, migration operations for ``ForeignKey`` and ``ManyToManyField`` fields no
longer specify attributes which were not passed to the fields during
initialization.

As a side-effect, running ``makemigrations`` might generate no-op
``AlterField`` operations for ``ManyToManyField`` and ``ForeignKey`` fields in
some cases.

``DeleteView`` changes
----------------------

:class:`~django.views.generic.edit.DeleteView` now uses
:class:`~django.views.generic.edit.FormMixin` to handle POST requests. As a
consequence, any custom deletion logic in ``delete()`` handlers should be
moved to ``form_valid()``, or a shared helper method, if required.

Table and column naming scheme changes on Oracle
------------------------------------------------

Django 4.0 inadvertently changed the table and column naming scheme on Oracle.
This causes errors for models and fields with names longer than 30 characters.
Unfortunately, renaming some Oracle tables and columns is required. Use the
upgrade script in :ticket:`33789 <33789#comment:15>` to generate ``RENAME``
statements to change naming scheme.

Miscellaneous
-------------

* Support for ``cx_Oracle`` < 7.0 is removed.

* To allow serving a Django site on a subpath without changing the value of
  :setting:`STATIC_URL`, the leading slash is removed from that setting (now
  ``'static/'``) in the default :djadmin:`startproject` template.

* The :class:`~django.contrib.admin.AdminSite` method for the admin ``index``
  view is no longer decorated with ``never_cache`` when accessed directly,
  rather than via the recommended ``AdminSite.urls`` property, or
  ``AdminSite.get_urls()`` method.

* Unsupported operations on a sliced queryset now raise ``TypeError`` instead
  of ``AssertionError``.

* The undocumented ``django.test.runner.reorder_suite()`` function is renamed
  to ``reorder_tests()``. It now accepts an iterable of tests rather than a
  test suite, and returns an iterator of tests.

* Calling ``FileSystemStorage.delete()`` with an empty ``name`` now raises
  ``ValueError`` instead of ``AssertionError``.

* Calling ``EmailMultiAlternatives.attach_alternative()`` or
  ``EmailMessage.attach()`` with an invalid ``content`` or ``mimetype``
  arguments now raise ``ValueError`` instead of ``AssertionError``.

* :meth:`~django.test.SimpleTestCase.assertHTMLEqual` no longer considers a
  non-boolean attribute without a value equal to an attribute with the same
  name and value.

* Tests that fail to load, for example due to syntax errors, now always match
  when using :option:`test --tag`.

* The undocumented ``django.contrib.admin.utils.lookup_needs_distinct()``
  function is renamed to ``lookup_spawns_duplicates()``.

* The undocumented ``HttpRequest.get_raw_uri()`` method is removed. The
  :meth:`.HttpRequest.build_absolute_uri` method may be a suitable alternative.

* The ``object`` argument of undocumented ``ModelAdmin.log_addition()``,
  ``log_change()``, and ``log_deletion()`` methods is renamed to ``obj``.

* :class:`~django.utils.feedgenerator.RssFeed`,
  :class:`~django.utils.feedgenerator.Atom1Feed`, and their subclasses now emit
  elements with no content as self-closing tags.

* ``NodeList.render()`` no longer casts the output of ``render()`` method for
  individual nodes to a string. ``Node.render()`` should always return a string
  as documented.

* The ``where_class`` property of ``django.db.models.sql.query.Query`` and the
  ``where_class`` argument to the private ``get_extra_restriction()`` method of
  ``ForeignObject`` and ``ForeignObjectRel`` are removed. If needed, initialize
  ``django.db.models.sql.where.WhereNode`` instead.

* The ``filter_clause`` argument of the undocumented ``Query.add_filter()``
  method is replaced by two positional arguments ``filter_lhs`` and
  ``filter_rhs``.

* :class:`~django.middleware.csrf.CsrfViewMiddleware` now uses
  ``request.META['CSRF_COOKIE_NEEDS_UPDATE']`` in place of
  ``request.META['CSRF_COOKIE_USED']``, ``request.csrf_cookie_needs_reset``,
  and ``response.csrf_cookie_set`` to track whether the CSRF cookie should be
  sent. This is an undocumented, private API.

* The undocumented ``TRANSLATOR_COMMENT_MARK`` constant is moved from
  ``django.template.base`` to ``django.utils.translation.template``.

* The ``real_apps`` argument of the undocumented
  ``django.db.migrations.state.ProjectState.__init__()`` method must now be a
  set if provided.

* :class:`~django.forms.RadioSelect` and
  :class:`~django.forms.CheckboxSelectMultiple` widgets are now rendered in
  ``<div>`` tags so they are announced more concisely by screen readers. If you
  need the previous behavior, :ref:`override the widget template
  <overriding-built-in-widget-templates>` with the appropriate template from
  Django 3.2.

* The :tfilter:`floatformat` template filter no longer depends on the
  ``USE_L10N`` setting and always returns localized output. Use the ``u``
  suffix to disable localization.

* The default value of the ``USE_L10N`` setting is changed to ``True``. See the
  :ref:`Localization section <use_l10n_deprecation>` above for more details.

* As part of the :ref:`move to zoneinfo <whats-new-4.0>`,
  ``django.utils.timezone.utc`` is changed to alias
  :attr:`datetime.timezone.utc`.

* The minimum supported version of ``asgiref`` is increased from 3.3.2 to
  3.4.1.

.. _deprecated-features-4.0:

Features deprecated in 4.0
==========================

Use of ``pytz`` time zones
--------------------------

As part of the :ref:`move to zoneinfo <whats-new-4.0>`, use of ``pytz`` time
zones is deprecated.

Accordingly, the ``is_dst`` arguments to the following are also deprecated:

* :meth:`django.db.models.query.QuerySet.datetimes`
* :func:`django.db.models.functions.Trunc`
* :func:`django.db.models.functions.TruncSecond`
* :func:`django.db.models.functions.TruncMinute`
* :func:`django.db.models.functions.TruncHour`
* :func:`django.db.models.functions.TruncDay`
* :func:`django.db.models.functions.TruncWeek`
* :func:`django.db.models.functions.TruncMonth`
* :func:`django.db.models.functions.TruncQuarter`
* :func:`django.db.models.functions.TruncYear`
* :func:`django.utils.timezone.make_aware`

Support for use of ``pytz`` will be removed in Django 5.0.

Time zone support
-----------------

In order to follow good practice, the default value of the :setting:`USE_TZ`
setting will change from ``False`` to ``True``, and time zone support will be
enabled by default, in Django 5.0.

Note that the default :file:`settings.py` file created by
:djadmin:`django-admin startproject <startproject>` includes
:setting:`USE_TZ = True <USE_TZ>` since Django 1.4.

You can set ``USE_TZ`` to ``False`` in your project settings before then to
opt-out.

.. _use_l10n_deprecation:

Localization
------------

In order to follow good practice, the default value of the ``USE_L10N`` setting
is changed from ``False`` to ``True``.

Moreover ``USE_L10N`` is deprecated as of this release. Starting with Django
5.0, by default, any date or number displayed by Django will be localized.

The :ttag:`{% localize %} <localize>` tag and the :tfilter:`localize`/
:tfilter:`unlocalize` filters will still be honored by Django.

Miscellaneous
-------------

* ``SERIALIZE`` test setting is deprecated as it can be inferred from the
  :attr:`~django.test.TestCase.databases` with the
  :ref:`serialized_rollback <test-case-serialized-rollback>` option enabled.

* The undocumented ``django.utils.baseconv`` module is deprecated.

* The undocumented ``django.utils.datetime_safe`` module is deprecated.

* The default sitemap protocol for sitemaps built outside the context of a
  request will change from ``'http'`` to ``'https'`` in Django 5.0.

* The ``extra_tests`` argument for :meth:`.DiscoverRunner.build_suite` and
  :meth:`.DiscoverRunner.run_tests` is deprecated.

* The :class:`~django.contrib.postgres.aggregates.ArrayAgg`,
  :class:`~django.contrib.postgres.aggregates.JSONBAgg`, and
  :class:`~django.contrib.postgres.aggregates.StringAgg` aggregates will return
  ``None`` when there are no rows instead of ``[]``, ``[]``, and ``''``
  respectively in Django 5.0. If you need the previous behavior, explicitly set
  ``default`` to ``Value([])``, ``Value('[]')``, or ``Value('')``.

* The ``django.contrib.gis.admin.GeoModelAdmin`` and ``OSMGeoAdmin`` classes
  are deprecated. Use :class:`~django.contrib.admin.ModelAdmin` and
  :class:`~django.contrib.gis.admin.GISModelAdmin` instead.

* Since form rendering now uses the template engine, the undocumented
  ``BaseForm._html_output()`` helper method is deprecated.

* The ability to return a ``str`` from ``ErrorList`` and ``ErrorDict`` is
  deprecated. It is expected these methods return a ``SafeString``.

Features removed in 4.0
=======================

These features have reached the end of their deprecation cycle and are removed
in Django 4.0.

See :ref:`deprecated-features-3.0` for details on these changes, including how
to remove usage of these features.

* ``django.utils.http.urlquote()``, ``urlquote_plus()``, ``urlunquote()``, and
  ``urlunquote_plus()`` are removed.

* ``django.utils.encoding.force_text()`` and ``smart_text()`` are removed.

* ``django.utils.translation.ugettext()``, ``ugettext_lazy()``,
  ``ugettext_noop()``, ``ungettext()``, and ``ungettext_lazy()`` are removed.

* ``django.views.i18n.set_language()`` doesn't set the user language in
  ``request.session`` (key ``_language``).

* ``alias=None`` is required in the signature of
  ``django.db.models.Expression.get_group_by_cols()`` subclasses.

* ``django.utils.text.unescape_entities()`` is removed.

* ``django.utils.http.is_safe_url()`` is removed.

See :ref:`deprecated-features-3.1` for details on these changes, including how
to remove usage of these features.

* The ``PASSWORD_RESET_TIMEOUT_DAYS`` setting is removed.

* The :lookup:`isnull` lookup no longer allows using non-boolean values as the
  right-hand side.

* The ``django.db.models.query_utils.InvalidQuery`` exception class is removed.

* The ``django-admin.py`` entry point is removed.

* The ``HttpRequest.is_ajax()`` method is removed.

* Support for the pre-Django 3.1 encoding format of cookies values used by
  ``django.contrib.messages.storage.cookie.CookieStorage`` is removed.

* Support for the pre-Django 3.1 password reset tokens in the admin site (that
  use the SHA-1 hashing algorithm) is removed.

* Support for the pre-Django 3.1 encoding format of sessions is removed.

* Support for the pre-Django 3.1 ``django.core.signing.Signer`` signatures
  (encoded with the SHA-1 algorithm) is removed.

* Support for the pre-Django 3.1 ``django.core.signing.dumps()`` signatures
  (encoded with the SHA-1 algorithm) in ``django.core.signing.loads()`` is
  removed.

* Support for the pre-Django 3.1 user sessions (that use the SHA-1 algorithm)
  is removed.

* The ``get_response`` argument for
  ``django.utils.deprecation.MiddlewareMixin.__init__()`` is required and
  doesn't accept ``None``.

* The ``providing_args`` argument for ``django.dispatch.Signal`` is removed.

* The ``length`` argument for ``django.utils.crypto.get_random_string()`` is
  required.

* The ``list`` message for ``ModelMultipleChoiceField`` is removed.

* Support for passing raw column aliases to ``QuerySet.order_by()`` is removed.

* The ``NullBooleanField`` model field is removed, except for support in
  historical migrations.

* ``django.conf.urls.url()`` is removed.

* The ``django.contrib.postgres.fields.JSONField`` model field is removed,
  except for support in historical migrations.

* ``django.contrib.postgres.fields.jsonb.KeyTransform`` and
  ``django.contrib.postgres.fields.jsonb.KeyTextTransform`` are removed.

* ``django.contrib.postgres.forms.JSONField`` is removed.

* The ``{% ifequal %}`` and ``{% ifnotequal %}`` template tags are removed.

* The ``DEFAULT_HASHING_ALGORITHM`` transitional setting is removed.

# ===== SOURCE: https://raw.githubusercontent.com/django/django/main/docs/releases/5.0.txt =====

========================
Django 5.0 release notes
========================

*December 4, 2023*

Welcome to Django 5.0!

These release notes cover the :ref:`new features <whats-new-5.0>`, as well as
some :ref:`backwards incompatible changes <backwards-incompatible-5.0>` you'll
want to be aware of when upgrading from Django 4.2 or earlier. We've
:ref:`begun the deprecation process for some features
<deprecated-features-5.0>`.

See the :doc:`/howto/upgrade-version` guide if you're updating an existing
project.

Python compatibility
====================

Django 5.0 supports Python 3.10, 3.11, and 3.12. We **highly recommend** and
only officially support the latest release of each series.

The Django 4.2.x series is the last to support Python 3.8 and 3.9.

Third-party library support for older version of Django
=======================================================

Following the release of Django 5.0, we suggest that third-party app authors
drop support for all versions of Django prior to 4.2. At that time, you should
be able to run your package's tests using ``python -Wd`` so that deprecation
warnings appear. After making the deprecation warning fixes, your app should be
compatible with Django 5.0.

.. _whats-new-5.0:

What's new in Django 5.0
========================

Facet filters in the admin
--------------------------

Facet counts are now shown for applied filters in the admin changelist when
toggled on via the UI. This behavior can be changed via the new
:attr:`.ModelAdmin.show_facets` attribute. For more information see
:ref:`facet-filters`.

Simplified templates for form field rendering
---------------------------------------------

Django 5.0 introduces the concept of a field group, and field group templates.
This simplifies rendering of the related elements of a Django form field such
as its label, widget, help text, and errors.

For example, the template below:

.. code-block:: html+django

    <form>
    ...
    <div>
      {{ form.name.label_tag }}
      {% if form.name.help_text %}
        <div class="helptext" id="{{ form.name.auto_id }}_helptext">
          {{ form.name.help_text|safe }}
        </div>
      {% endif %}
      {{ form.name.errors }}
      {{ form.name }}
      <div class="row">
        <div class="col">
          {{ form.email.label_tag }}
          {% if form.email.help_text %}
            <div class="helptext" id="{{ form.email.auto_id }}_helptext">
              {{ form.email.help_text|safe }}
            </div>
          {% endif %}
          {{ form.email.errors }}
          {{ form.email }}
        </div>
        <div class="col">
          {{ form.password.label_tag }}
          {% if form.password.help_text %}
            <div class="helptext" id="{{ form.password.auto_id }}_helptext">
              {{ form.password.help_text|safe }}
            </div>
          {% endif %}
          {{ form.password.errors }}
          {{ form.password }}
        </div>
      </div>
    </div>
    ...
    </form>

Can now be simplified to:

.. code-block:: html+django

    <form>
    ...
    <div>
      {{ form.name.as_field_group }}
      <div class="row">
        <div class="col">{{ form.email.as_field_group }}</div>
        <div class="col">{{ form.password.as_field_group }}</div>
      </div>
    </div>
    ...
    </form>

:meth:`~django.forms.BoundField.as_field_group` renders fields with the
``"django/forms/field.html"`` template by default and can be customized on a
per-project, per-field, or per-request basis. See
:ref:`reusable-field-group-templates`.

Database-computed default values
--------------------------------

The new :attr:`Field.db_default <django.db.models.Field.db_default>` parameter
sets a database-computed default value. For example::

    from django.db import models
    from django.db.models.functions import Now, Pi


    class MyModel(models.Model):
        age = models.IntegerField(db_default=18)
        created = models.DateTimeField(db_default=Now())
        circumference = models.FloatField(db_default=2 * Pi())

Database generated model field
------------------------------

The new :class:`~django.db.models.GeneratedField` allows creation of database
generated columns. This field can be used on all supported database backends
to create a field that is always computed from other fields. For example::

    from django.db import models
    from django.db.models import F


    class Square(models.Model):
        side = models.IntegerField()
        area = models.GeneratedField(
            expression=F("side") * F("side"),
            output_field=models.BigIntegerField(),
            db_persist=True,
        )

More options for declaring field choices
----------------------------------------

:attr:`.Field.choices` *(for model fields)* and :attr:`.ChoiceField.choices`
*(for form fields)* allow for more flexibility when declaring their values. In
previous versions of Django, ``choices`` should either be a list of 2-tuples,
or an :ref:`field-choices-enum-types` subclass, but the latter required
accessing the ``.choices`` attribute to provide the values in the expected
form::

    from django.db import models

    Medal = models.TextChoices("Medal", "GOLD SILVER BRONZE")

    SPORT_CHOICES = [
        ("Martial Arts", [("judo", "Judo"), ("karate", "Karate")]),
        ("Racket", [("badminton", "Badminton"), ("tennis", "Tennis")]),
        ("unknown", "Unknown"),
    ]


    class Winner(models.Model):
        name = models.CharField(...)
        medal = models.CharField(..., choices=Medal.choices)
        sport = models.CharField(..., choices=SPORT_CHOICES)

Django 5.0 adds support for accepting a mapping or a callable instead of an
iterable, and also no longer requires ``.choices`` to be used directly to
expand :ref:`enumeration types <field-choices-enum-types>`::

    from django.db import models

    Medal = models.TextChoices("Medal", "GOLD SILVER BRONZE")

    SPORT_CHOICES = {  # Using a mapping instead of a list of 2-tuples.
        "Martial Arts": {"judo": "Judo", "karate": "Karate"},
        "Racket": {"badminton": "Badminton", "tennis": "Tennis"},
        "unknown": "Unknown",
    }


    def get_scores():
        return [(i, str(i)) for i in range(10)]


    class Winner(models.Model):
        name = models.CharField(...)
        medal = models.CharField(..., choices=Medal)  # Using `.choices` not required.
        sport = models.CharField(..., choices=SPORT_CHOICES)
        score = models.IntegerField(choices=get_scores)  # A callable is allowed.

Under the hood the provided ``choices`` are normalized into a list of 2-tuples
as the canonical form whenever the ``choices`` value is updated. For more
information, please check the :ref:`model field reference on choices
<field-choices>`.

Minor features
--------------

:mod:`django.contrib.admin`
~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The new :meth:`.AdminSite.get_log_entries` method allows customizing the
  queryset for the site's listed log entries.

* The ``django.contrib.admin.AllValuesFieldListFilter``,
  ``ChoicesFieldListFilter``, ``RelatedFieldListFilter``, and
  ``RelatedOnlyFieldListFilter`` admin filters now handle multi-valued query
  parameters.

* ``XRegExp`` is upgraded from version 3.2.0 to 5.1.1.

* The new :meth:`.AdminSite.get_model_admin` method returns an admin class for
  the given model class.

* Properties in :attr:`.ModelAdmin.list_display` now support ``boolean``
  attribute.

* jQuery is upgraded from version 3.6.4 to 3.7.1.


:mod:`django.contrib.auth`
~~~~~~~~~~~~~~~~~~~~~~~~~~

* The default iteration count for the PBKDF2 password hasher is increased from
  600,000 to 720,000.

* The new asynchronous functions are now provided, using an
  ``a`` prefix: :func:`django.contrib.auth.aauthenticate`,
  :func:`~.django.contrib.auth.aget_user`,
  :func:`~.django.contrib.auth.alogin`, :func:`~.django.contrib.auth.alogout`,
  and :func:`~.django.contrib.auth.aupdate_session_auth_hash`.

* ``AuthenticationMiddleware`` now adds an :meth:`.HttpRequest.auser`
  asynchronous method that returns the currently logged-in user.

* The new :func:`django.contrib.auth.hashers.acheck_password` asynchronous
  function and :meth:`.AbstractBaseUser.acheck_password` method allow
  asynchronous checking of user passwords.

:mod:`django.contrib.contenttypes`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* :meth:`.QuerySet.prefetch_related` now supports prefetching
  :class:`~django.contrib.contenttypes.fields.GenericForeignKey` with
  non-homogeneous set of results.

:mod:`django.contrib.gis`
~~~~~~~~~~~~~~~~~~~~~~~~~

* The new
  :class:`ClosestPoint() <django.contrib.gis.db.models.functions.ClosestPoint>`
  function returns a 2-dimensional point on the geometry that is closest to
  another geometry.

* :ref:`GIS aggregates <gis-aggregation-functions>` now support the ``filter``
  argument.

* Support for GDAL 3.7 and GEOS 3.12 is added.

* The new :meth:`.GEOSGeometry.equals_identical` method allows point-wise
  equivalence checking of geometries.

:mod:`django.contrib.messages`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The new :meth:`.MessagesTestMixin.assertMessages` assertion method allows
  testing :mod:`~django.contrib.messages` added to a
  :class:`response <django.http.HttpResponse>`.

:mod:`django.contrib.postgres`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* The new :attr:`~.ExclusionConstraint.violation_error_code` attribute of
  :class:`~django.contrib.postgres.constraints.ExclusionConstraint` allows
  customizing the ``code`` of ``ValidationError`` raised during
  :ref:`model validation <validating-objects>`.

Asynchronous views
~~~~~~~~~~~~~~~~~~

* Under ASGI, ``http.disconnect`` events are now handled. This allows views to
  perform any necessary cleanup if a client disconnects before the response is
  generated. See :ref:`async-handling-disconnect` for more details.

Decorators
~~~~~~~~~~

* The following decorators now support wrapping asynchronous view functions:

  * :func:`~django.views.decorators.cache.cache_control`
  * :func:`~django.views.decorators.cache.never_cache`
  * :func:`~django.views.decorators.common.no_append_slash`
  * :func:`~django.views.decorators.csrf.csrf_exempt`
  * :func:`~django.views.decorators.csrf.csrf_protect`
  * :func:`~django.views.decorators.csrf.ensure_csrf_cookie`
  * :func:`~django.views.decorators.csrf.requires_csrf_token`
  * :func:`~django.views.decorators.debug.sensitive_variables`
  * :func:`~django.views.decorators.debug.sensitive_post_parameters`
  * :func:`~django.views.decorators.gzip.gzip_page`
  * :func:`~django.views.decorators.http.condition`
  * ``conditional_page()``
  * :func:`~django.views.decorators.http.etag`
  * :func:`~django.views.decorators.http.last_modified`
  * :func:`~django.views.decorators.http.require_http_methods`
  * :func:`~django.views.decorators.http.require_GET`
  * :func:`~django.views.decorators.http.require_POST`
  * :func:`~django.views.decorators.http.require_safe`
  * :func:`~django.views.decorators.vary.vary_on_cookie`
  * :func:`~django.views.decorators.vary.vary_on_headers`
  * ``xframe_options_deny()``
  * ``xframe_options_sameorigin()``
  * ``xframe_options_exempt()``

Error Reporting
~~~~~~~~~~~~~~~

* :func:`~django.views.decorators.debug.sensitive_variables` and
  :func:`~django.views.decorators.debug.sensitive_post_parameters` can now be
  used with asynchronous functions.

File Storage
~~~~~~~~~~~~

* :meth:`.File.open` now passes all positional (``*args``) and keyword
  arguments (``**kwargs``) to Python's built-in :func:`python:open`.

Forms
~~~~~

* The new :attr:`~django.forms.URLField.assume_scheme` argument for
  :class:`~django.forms.URLField` allows specifying a default URL scheme.

* In order to improve accessibility, the following changes are made:

  * Form fields now include the ``aria-describedby`` HTML attribute to enable
    screen readers to associate form fields with their help text.
  * Invalid form fields now include the ``aria-invalid="true"`` HTML attribute.

Internationalization
~~~~~~~~~~~~~~~~~~~~

* Support and translations for the Uyghur language are now available.

Migrations
~~~~~~~~~~

* Serialization of functions decorated with :func:`functools.cache` or
  :func:`functools.lru_cache` is now supported without the need to write a
  custom serializer.

Models
~~~~~~

* The new ``create_defaults`` argument of :meth:`.QuerySet.update_or_create`
  and :meth:`.QuerySet.aupdate_or_create` methods allows specifying a different
  field values for the create operation.

* The new ``violation_error_code`` attribute of
  :class:`~django.db.models.BaseConstraint`,
  :class:`~django.db.models.CheckConstraint`, and
  :class:`~django.db.models.UniqueConstraint` allows customizing the ``code``
  of ``ValidationError`` raised during
  :ref:`model validation <validating-objects>`.

* The :ref:`force_insert <ref-models-force-insert>` argument of
  :meth:`.Model.save` now allows specifying a tuple of parent classes that must
  be forced to be inserted.

* :meth:`.QuerySet.bulk_create` and :meth:`.QuerySet.abulk_create` methods now
  set the primary key on each model instance when the ``update_conflicts``
  parameter is enabled (if the database supports it).

* The new :attr:`.UniqueConstraint.nulls_distinct` attribute allows customizing
  the treatment of ``NULL`` values on PostgreSQL 15+.

* The new :func:`~django.shortcuts.aget_object_or_404` and
  :func:`~django.shortcuts.aget_list_or_404` asynchronous shortcuts allow
  asynchronous getting objects.

* The new :func:`~django.db.models.aprefetch_related_objects` function allows
  asynchronous prefetching of model instances.

* :meth:`.QuerySet.aiterator` now supports previous calls to
  ``prefetch_related()``.

* On MariaDB 10.7+, ``UUIDField`` is now created as ``UUID`` column rather than
  ``CHAR(32)`` column. See the migration guide above for more details on
  :ref:`migrating-uuidfield`.

* Django now supports `oracledb`_ version 1.3.2 or higher. Support for
  ``cx_Oracle`` is deprecated as of this release and will be removed in Django
  6.0.

Pagination
~~~~~~~~~~

* The new :attr:`django.core.paginator.Paginator.error_messages` argument
  allows customizing the error messages raised by :meth:`.Paginator.page`.

Signals
~~~~~~~

* The new :meth:`.Signal.asend` and :meth:`.Signal.asend_robust` methods allow
  asynchronous signal dispatch. Signal receivers may be synchronous or
  asynchronous, and will be automatically adapted to the correct calling style.

Templates
~~~~~~~~~

* The new :tfilter:`escapeseq` template filter applies :tfilter:`escape` to
  each element of a sequence.

Tests
~~~~~

* :class:`~django.test.Client` and :class:`~django.test.AsyncClient` now
  provide asynchronous methods, using an ``a`` prefix:
  :meth:`~django.test.Client.asession`, :meth:`~django.test.Client.alogin`,
  :meth:`~django.test.Client.aforce_login`, and
  :meth:`~django.test.Client.alogout`.

* :class:`~django.test.AsyncClient` now supports the ``follow`` parameter.

* :class:`~django.test.runner.DiscoverRunner` now allows showing the duration
  of the slowest tests using the :option:`test --durations` option (available
  on Python 3.12+).

Validators
~~~~~~~~~~

* The new ``offset`` argument of
  :class:`~django.core.validators.StepValueValidator` allows specifying an
  offset for valid values.

.. _backwards-incompatible-5.0:

Backwards incompatible changes in 5.0
=====================================

Database backend API
--------------------

This section describes changes that may be needed in third-party database
backends.

* ``DatabaseFeatures.supports_expression_defaults`` should be set to ``False``
  if the database doesn't support using database functions as defaults.

* ``DatabaseFeatures.supports_default_keyword_in_insert`` should be set to
  ``False`` if the database doesn't support the ``DEFAULT`` keyword in
  ``INSERT`` queries.

* ``DatabaseFeatures.supports_default_keyword_in_bulk_insert`` should be set to
  ``False`` if the database doesn't support the ``DEFAULT`` keyword in bulk
  ``INSERT`` queries.

:mod:`django.contrib.gis`
-------------------------

* Support for GDAL 2.2 and 2.3 is removed.

* Support for GEOS 3.6 and 3.7 is removed.

:mod:`django.contrib.sitemaps`
------------------------------

* The ``django.contrib.sitemaps.ping_google()`` function and the
  ``ping_google`` management command are removed as the Google
  Sitemaps ping endpoint is deprecated and will be removed in January 2024.

* The ``django.contrib.sitemaps.SitemapNotFound`` exception class is removed.

Dropped support for MySQL < 8.0.11
----------------------------------

Support for pre-releases of MySQL 8.0.x series is removed. Django 5.0 supports
MySQL 8.0.11 and higher.

Using ``create_defaults__exact`` may now be required with ``QuerySet.update_or_create()``
-----------------------------------------------------------------------------------------

:meth:`.QuerySet.update_or_create` now supports the parameter
``create_defaults``. As a consequence, any models that have a field named
``create_defaults`` that are used with an ``update_or_create()`` should specify
the field in the lookup with ``create_defaults__exact``.

.. _migrating-uuidfield:

Migrating existing ``UUIDField`` on MariaDB 10.7+
-------------------------------------------------

On MariaDB 10.7+, ``UUIDField`` is now created as ``UUID`` column rather than
``CHAR(32)`` column. As a consequence, any ``UUIDField`` created in
Django < 5.0 should be replaced with a ``UUIDField`` subclass backed by
``CHAR(32)``::

    class Char32UUIDField(models.UUIDField):
        def db_type(self, connection):
            return "char(32)"

        def get_db_prep_value(self, value, connection, prepared=False):
            value = super().get_db_prep_value(value, connection, prepared)
            if value is not None:
                value = value.hex
            return value

For example::

    class MyModel(models.Model):
        uuid = models.UUIDField(primary_key=True, default=uuid.uuid4)

Should become::

    class Char32UUIDField(models.UUIDField): ...


    class MyModel(models.Model):
        uuid = Char32UUIDField(primary_key=True, default=uuid.uuid4)

Running the :djadmin:`makemigrations` command will generate a migration
containing a no-op ``AlterField`` operation.

Miscellaneous
-------------

* The ``instance`` argument of the undocumented
  ``BaseModelFormSet.save_existing()`` method is renamed to ``obj``.

* The undocumented ``django.contrib.admin.helpers.checkbox`` is removed.

* Integer fields are now validated as 64-bit integers on SQLite to match the
  behavior of ``sqlite3``.

* The undocumented ``Query.annotation_select_mask`` attribute is changed from a
  set of strings to an ordered list of strings.

* ``ImageField.update_dimension_fields()`` is no longer called on the
  ``post_init`` signal if ``width_field`` and ``height_field`` are not set.

* :class:`~django.db.models.functions.Now` database function now uses
  ``LOCALTIMESTAMP`` instead of ``CURRENT_TIMESTAMP`` on Oracle.

* :attr:`.AdminSite.site_header` is now rendered in a ``<div>`` tag instead of
  ``<h1>``. Screen reader users rely on heading elements for navigation within
  a page. Having two ``<h1>`` elements was confusing and the site header wasn't
  helpful as it is repeated on all pages.

* In order to improve accessibility, the admin's main content area and header
  content area are now rendered in a ``<main>`` and ``<header>`` tag instead of
  ``<div>``.

* On databases without native support for the SQL ``XOR`` operator, ``^`` as
  the exclusive or (``XOR``) operator now returns rows that are matched by an
  odd number of operands rather than exactly one operand. This is consistent
  with the behavior of MySQL, MariaDB, and Python.

* The minimum supported version of ``asgiref`` is increased from 3.6.0 to
  3.7.0.

* The minimum supported version of ``selenium`` is increased from 3.8.0 to
  4.8.0.

* The ``AlreadyRegistered`` and ``NotRegistered`` exceptions are moved from
  ``django.contrib.admin.sites`` to ``django.contrib.admin.exceptions``.

* The minimum supported version of SQLite is increased from 3.21.0 to 3.27.0.

* Support for ``cx_Oracle`` < 8.3 is removed.

* Executing SQL queries before the app registry has been fully populated now
  raises :exc:`RuntimeWarning`.

* :exc:`~django.core.exceptions.BadRequest` is raised for non-UTF-8 encoded
  requests with the :mimetype:`application/x-www-form-urlencoded` content type.
  See :rfc:`1866` for more details.

* The minimum supported version of ``colorama`` is increased to 0.4.6.

* The minimum supported version of ``docutils`` is increased to 0.19.

* Filtering querysets against overflowing integer values now always returns an
  empty queryset. As a consequence, you may need to use ``ExpressionWrapper()``
  to :ref:`explicitly wrap <using-f-with-annotations>` arithmetic against
  integer fields in such cases.

.. _deprecated-features-5.0:

Features deprecated in 5.0
==========================

Miscellaneous
-------------

* The ``DjangoDivFormRenderer`` and ``Jinja2DivFormRenderer`` transitional form
  renderers are deprecated.

* Passing positional arguments ``name`` and ``violation_error_message`` to
  :class:`~django.db.models.BaseConstraint` is deprecated in favor of
  keyword-only arguments.

* ``request`` is added to the signature of :meth:`.ModelAdmin.lookup_allowed`.
  Support for ``ModelAdmin`` subclasses that do not accept this argument is
  deprecated.

* The ``get_joining_columns()`` method of ``ForeignObject`` and
  ``ForeignObjectRel`` is deprecated. Starting with Django 6.0,
  ``django.db.models.sql.datastructures.Join`` will no longer fallback to
  ``get_joining_columns()``. Subclasses should implement
  ``get_joining_fields()`` instead.

* The ``ForeignObject.get_reverse_joining_columns()`` method is deprecated.

* The default scheme for ``forms.URLField`` will change from ``"http"`` to
  ``"https"`` in Django 6.0. Set ``FORMS_URLFIELD_ASSUME_HTTPS`` transitional
  setting to ``True`` to opt into assuming ``"https"`` during the Django 5.x
  release cycle.

* ``FORMS_URLFIELD_ASSUME_HTTPS`` transitional setting is deprecated.

* Support for calling ``format_html()`` without passing args or kwargs is
  deprecated.

* Support for ``cx_Oracle`` is deprecated in favor of `oracledb`_ 1.3.2+ Python
  driver.

* ``DatabaseOperations.field_cast_sql()`` is deprecated in favor of
  ``DatabaseOperations.lookup_cast()``. Starting with Django 6.0,
  ``BuiltinLookup.process_lhs()`` will no longer call ``field_cast_sql()``.
  Third-party database backends should implement ``lookup_cast()`` instead.

* The ``django.db.models.enums.ChoicesMeta`` metaclass is renamed to
  ``ChoicesType``.

* The ``Prefetch.get_current_queryset()`` method is deprecated.

* The ``get_prefetch_queryset()`` method of related managers and descriptors
  is deprecated. Starting with Django 6.0, ``get_prefetcher()`` and
  ``prefetch_related_objects()`` will no longer fallback to
  ``get_prefetch_queryset()``. Subclasses should implement
  ``get_prefetch_querysets()`` instead.

.. _`oracledb`: https://oracle.github.io/python-oracledb/

Features removed in 5.0
=======================

These features have reached the end of their deprecation cycle and are removed
in Django 5.0.

See :ref:`deprecated-features-4.0` for details on these changes, including how
to remove usage of these features.

* The ``SERIALIZE`` test setting is removed.

* The undocumented ``django.utils.baseconv`` module is removed.

* The undocumented ``django.utils.datetime_safe`` module is removed.

* The default value of the ``USE_TZ`` setting is changed from ``False`` to
  ``True``.

* The default sitemap protocol for sitemaps built outside the context of a
  request is changed from ``'http'`` to ``'https'``.

* The ``extra_tests`` argument for ``DiscoverRunner.build_suite()`` and
  ``DiscoverRunner.run_tests()`` is removed.

* The ``django.contrib.postgres.aggregates.ArrayAgg``, ``JSONBAgg``, and
  ``StringAgg`` aggregates no longer return ``[]``, ``[]``, and ``''``,
  respectively, when there are no rows.

* The ``USE_L10N`` setting is removed.

* The ``USE_DEPRECATED_PYTZ`` transitional setting is removed.

* Support for ``pytz`` timezones is removed.

* The ``is_dst`` argument is removed from:

  * ``QuerySet.datetimes()``
  * ``django.utils.timezone.make_aware()``
  * ``django.db.models.functions.Trunc()``
  * ``django.db.models.functions.TruncSecond()``
  * ``django.db.models.functions.TruncMinute()``
  * ``django.db.models.functions.TruncHour()``
  * ``django.db.models.functions.TruncDay()``
  * ``django.db.models.functions.TruncWeek()``
  * ``django.db.models.functions.TruncMonth()``
  * ``django.db.models.functions.TruncQuarter()``
  * ``django.db.models.functions.TruncYear()``

* The ``django.contrib.gis.admin.GeoModelAdmin`` and ``OSMGeoAdmin`` classes
  are removed.

* The undocumented ``BaseForm._html_output()`` method is removed.

* The ability to return a ``str``, rather than a ``SafeString``, when rendering
  an ``ErrorDict`` and ``ErrorList`` is removed.

See :ref:`deprecated-features-4.1` for details on these changes, including how
to remove usage of these features.

* The ``SitemapIndexItem.__str__()`` method is removed.

* The ``CSRF_COOKIE_MASKED`` transitional setting is removed.

* The ``name`` argument of ``django.utils.functional.cached_property()`` is
  removed.

* The ``opclasses`` argument of
  ``django.contrib.postgres.constraints.ExclusionConstraint`` is removed.

* The undocumented ability to pass ``errors=None`` to
  ``SimpleTestCase.assertFormError()`` and ``assertFormsetError()`` is removed.

* ``django.contrib.sessions.serializers.PickleSerializer`` is removed.

* The usage of ``QuerySet.iterator()`` on a queryset that prefetches related
  objects without providing the ``chunk_size`` argument is no longer allowed.

* Passing unsaved model instances to related filters is no longer allowed.

* ``created=True`` is required in the signature of
  ``RemoteUserBackend.configure_user()`` subclasses.

* Support for logging out via ``GET`` requests in the
  ``django.contrib.auth.views.LogoutView`` and
  ``django.contrib.auth.views.logout_then_login()`` is removed.

* The ``django.utils.timezone.utc`` alias to ``datetime.timezone.utc`` is
  removed.

* Passing a response object and a form/formset name to
  ``SimpleTestCase.assertFormError()`` and ``assertFormSetError()`` is no
  longer allowed.

* The ``django.contrib.gis.admin.OpenLayersWidget`` is removed.

+ The ``django.contrib.auth.hashers.CryptPasswordHasher`` is removed.

* The ``"django/forms/default.html"`` and
  ``"django/forms/formsets/default.html"`` templates are removed.

* The default form and formset rendering style is changed to the div-based.

* Passing ``nulls_first=False`` or ``nulls_last=False`` to ``Expression.asc()``
  and ``Expression.desc()`` methods, and the ``OrderBy`` expression is no
  longer allowed.
