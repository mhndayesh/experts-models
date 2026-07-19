# Django 5.0 — removed features, deprecations, backwards-incompatible changes

## Removed
The `USE_L10N` setting is removed (localization is always enabled).
The `USE_DEPRECATED_PYTZ` transitional setting and support for pytz timezones are removed; use `zoneinfo`.
The `django.utils.timezone.utc` alias is removed; use `datetime.timezone.utc`.
The `is_dst` argument is removed from `QuerySet.datetimes()`, `django.utils.timezone.make_aware()`, and the `Trunc` functions.
The `django.contrib.sessions.serializers.PickleSerializer` is removed.
The `django.contrib.auth.hashers.CryptPasswordHasher` is removed.
The `django.utils.baseconv` and `django.utils.datetime_safe` modules are removed.
Support for logging out via GET requests in `LogoutView` and `logout_then_login()` is removed.
The default form and formset rendering changed to div-based templates; the `default.html` form templates are removed.
The `SERIALIZE` test setting is removed.
The `name` argument is removed from `django.utils.functional.cached_property()`.

## Deprecated
Passing positional arguments `name` and `violation_error_message` to `BaseConstraint` is deprecated; use keyword-only arguments.
The `request` argument in `ModelAdmin.lookup_allowed()` is deprecated.
`ForeignObject.get_joining_columns()` is deprecated; use `get_joining_fields()`.
The `django.db.models.enums.ChoicesMeta` metaclass is deprecated; it is renamed to `ChoicesType`.
`Prefetch.get_current_queryset()` is deprecated.
The related-manager `get_prefetch_queryset()` method is deprecated; use `get_prefetch_querysets()`.
Support for `cx_Oracle` is deprecated in favor of `oracledb` 1.3.2+.
Calling `format_html()` without passing args or kwargs is deprecated.

## Backwards-incompatible
The default `USE_TZ` changed from `False` to `True`.
The default sitemap protocol changed from `http` to `https`.
`QuerySet.update_or_create()` now supports a `create_defaults` parameter.
The XOR operator `^` now returns rows matched by an odd number of operands instead of exactly one.
`AlreadyRegistered` and `NotRegistered` exceptions moved from `django.contrib.admin.sites` to `django.contrib.admin.exceptions`.
The minimum SQLite version increased to 3.27.0 and minimum MySQL to 8.0.11.
