# YARA to YARA-X differences (breaking changes for rule authors)

In YARA-X an unescaped `{` outside a repetition operator in a regex is now invalid; it must be escaped as `\{`.
In YARA-X invalid regex escape sequences like `\g` are no longer treated as literal characters; they now produce an error.
In YARA-X a base64 pattern must be at least 3 characters; strings shorter than 3 characters are no longer supported.
In YARA-X the `base64` and `base64wide` modifiers may use different alphabets; in YARA they had to share the same alphabet.
In YARA-X wildcard rule names in `of` statements like `1 of (rule_name*)` are no longer valid.
In YARA-X the `xor` modifier applies XOR before checking `fullword` delimiters; in YARA it applied XOR after checking delimiters.
In YARA-X a negative array index like `@a[-1]` now produces an error instead of evaluating to undefined.
In YARA-X hex-pattern jump bounds accept hex and octal values; YARA accepted base-10 only.
In YARA-X each rule modifier (`global`, `private`) may appear only once; YARA allowed duplicates.
In YARA-X strings, arrays, and dictionaries have a new `.len()` method that did not exist in YARA 4.x.
