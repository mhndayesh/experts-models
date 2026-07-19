# Pydantic V1 to V2 Migration Guide (API changes)

## Method renames on BaseModel
`__fields__` is renamed to `model_fields`.
`__private_attributes__` is renamed to `__pydantic_private__`.
`__validators__` is renamed to `__pydantic_validator__`.
`construct()` is renamed to `model_construct()`.
`copy()` is renamed to `model_copy()`.
`dict()` is renamed to `model_dump()`.
`json_schema()` is renamed to `model_json_schema()`.
`json()` is renamed to `model_dump_json()`.
`parse_obj()` is renamed to `model_validate()`.
`update_forward_refs()` is renamed to `model_rebuild()`.

## Deprecated methods
`parse_raw` is deprecated; use `model_validate_json()`.
`parse_file` is deprecated; load the data then use `model_validate()`.
`from_orm()` is deprecated; use `model_validate()` with `from_attributes=True`.

## Config changes
The inner `Config` class is replaced by a `model_config` class attribute (a dict, typically `ConfigDict`).
Config setting `allow_population_by_field_name` is renamed to `populate_by_name`.
Config setting `anystr_lower` is renamed to `str_to_lower`.
Config setting `anystr_strip_whitespace` is renamed to `str_strip_whitespace`.
Config setting `anystr_upper` is renamed to `str_to_upper`.
Config setting `keep_untouched` is renamed to `ignored_types`.
Config setting `max_anystr_length` is renamed to `str_max_length`.
Config setting `min_anystr_length` is renamed to `str_min_length`.
Config setting `orm_mode` is renamed to `from_attributes`.
Config setting `schema_extra` is renamed to `json_schema_extra`.
Config setting `validate_all` is renamed to `validate_default`.
Config settings removed in V2: `allow_mutation`, `error_msg_templates`, `fields`, `getter_dict`, `smart_union`, `underscore_attrs_are_private`, `json_loads`, `json_dumps`, `copy_on_model_validation`, `post_init_call`.

## Validator decorators
`@validator` is deprecated; use `@field_validator`.
`@root_validator` is deprecated; use `@model_validator`.
`@validate_arguments` is renamed to `@validate_call`.

## Field changes
The `Field` property `const` is removed.
The `Field` property `min_items` is removed; use `min_length`.
The `Field` property `max_items` is removed; use `max_length`.
The `Field` property `unique_items` is removed.
The `Field` property `allow_mutation` is removed; use `frozen`.
The `Field` property `regex` is removed; use `pattern`.
The `Field` property `final` is removed; use `typing.Final`.
Alias behavior changed: in V1 `alias` returned the field name when unset; in V2 `alias` returns `None` when unset.

## GenericModel and Root models
`pydantic.generics.GenericModel` is removed; inherit from `BaseModel, Generic[T]` directly.
The `__root__` field is replaced by the `RootModel` class.

## Custom type hooks
`__get_validators__()` is replaced by `__get_pydantic_core_schema__()`.
`__modify_schema__()` is replaced by `__get_pydantic_json_schema__()`.

## Moved / relocated imports
`pydantic.BaseSettings` is moved to `pydantic_settings.BaseSettings`.
`pydantic.color` is moved to `pydantic_extra_types.color`.
`pydantic.types.PaymentCardNumber` is moved to `pydantic_extra_types.PaymentCardNumber`.
`pydantic.utils.version_info` is moved to `pydantic.version.version_info`.
`pydantic.error_wrappers.ValidationError` is moved to `pydantic.ValidationError`.
`pydantic.utils.to_camel` is moved to `pydantic.alias_generators.to_camel`.
`pydantic.PyObject` is renamed to `pydantic.types.ImportString`.

## Removals
All `Constrained*` types (`ConstrainedInt`, `ConstrainedStr`, etc.) are removed; use `Annotated[type, Field(...)]`.
Type aliases removed: `NoneStr`, `NoneBytes`, `NoneStrBytes`, `StrBytes`, `JsonWrapper`.
The utility `validate_model` is removed.
