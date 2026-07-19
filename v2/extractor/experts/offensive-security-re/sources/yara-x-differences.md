# YARA-X Differences from YARA: Complete Technical Reference

Source: https://virustotal.github.io/yara-x/docs/writing_rules/differences-with-yara/

## 1. Regular Expression `{` Character Escaping
**Change:** The `{` character must be explicitly escaped when used outside repetition operators.

- YARA 4.x: `/abc{/` treats `{` as literal
- YARA-X: `/abc{/` is invalid; must write `/abc\{/`

**Rationale:** Catches errors like `[0-9]{1:5}` (should be `{1,5}`) and `.{,N}` (should be `.*`)

**CLI Option:** `--relaxed-re-syntax` auto-escapes `{` characters

---

## 2. Stricter Escaped Characters in Regex
**Change:** Invalid escape sequences now trigger errors instead of silent fallback.

YARA 4.x behavior example: In `/foo\gbar/`, the invalid `\g` sequence becomes `g`, producing `/foogbar/`

Real problems this catches:
- `\\x64\Release\\create.pdb` (missing `\\` before `R`)
- `/%TEMP%\NewGame/`
- `/(debug|release)\eda2.pdb/`

**CLI Option:** `--relaxed-re-syntax` enables YARA 4.x behavior

---

## 3. Base64 Pattern Requirements
**Minimum Length:** YARA-X requires patterns ≥ 3 characters (YARA 4.x has no minimum)

**Benefit:** Eliminates false positives; YARA 4.x documentation notes identical encodings for `"Dhis program cannow"` and `" This program cannot"`

---

## 4. Base64 Modifier Alphabets
**Change:** Different alphabets allowed for `base64` and `base64wide` in same string

Invalid in YARA 4.x:
```
$a = "foo" base64 base64wide("./ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789")
```

Valid in YARA-X: `base64` uses default alphabet; `base64wide` uses custom alphabet

---

## 5. "of" Statement Accepts Boolean Expression Tuples
**Expansion:** Now accepts arbitrary boolean expressions, not just identifiers

Valid in YARA-X:
```
1 of (true, false)
1 of ($a and not $b, $c, false)
```

**Limitation:** Wildcards with rule names removed
- Valid: `1 of (some_rule)`
- Invalid: `1 of (some_rule*)`

---

## 6. New "with" Statement
**Syntax:**
```
with a = 1 + 1, b = 2 : (a == b)
```

Enables local identifier binding within boolean expressions; eliminates repetitive expressions

---

## 7. XOR and Fullword Combination
**Change:** Bytes before/after XORed pattern are also XORed before alphanumeric check

Example: `"mississippi" xor(1) fullword` matching `{lhrrhrrhqqh}` is invalid in YARA-X because XORing yields `zmississippiz` (searches for full words in XORed context)

---

## 8. Negative Array Indexes
**Change:** `@a[-1]` is now an error (was `undefined` in YARA 4.x)

---

## 9. Hex Pattern Jump Bounds
**Change:** Bounds accept hex and octal values (base-10 only in YARA 4.x)

Now valid: `{ 01 02 03 [0x00-0x100] 04 05 06 }`

---

## 10. Duplicate Rule Modifiers
**Change:** Each `global` or `private` modifier can appear only once

Invalid in YARA-X:
```
global global global rule duplicated_global { ... }
```

---

## 11. Built-in `.len()` Method
**New Feature:** Returns length for strings (bytes), arrays (elements), dictionaries (entries)

```
some_module.some_string.len() == 3
some_module.some_array.len() >= 2
some_module.some_dict.len() == 1
```

===================================================================

# YARA-X Python API (the new binding that replaces libyara / yara-python)

Source: https://virustotal.github.io/yara-x/docs/api/python/

The YARA-X Python module provides pattern matching functionality through a two-phase workflow: compilation and scanning.

## Installation & Verification

Installation is handled via `pip install yara-x`. Note the import name is `yara_x` (underscore), replacing the old `import yara` from yara-python. Users can verify proper setup by running:

```python
import yara_x

rules = yara_x.compile('''
  rule test {
    strings:
      $a = "foobar"
    condition:
      $a
  }''')

results = rules.scan(b"foobar")
```

## Core Workflow

**Compilation Phase:** Rules are transformed from text into compiled `Rules` objects using either `yara_x.compile()` for simple cases or `Compiler` for complex scenarios with multiple namespaces.

**Scanning Phase:** The compiled `Rules` object scans data via `Rules.scan()` or through a `Scanner` instance for advanced control.

## Key Classes & Methods

**`compile(source_string)`** – Converts YARA rule text into executable `Rules` object.

**`Compiler`** – Advanced compilation supporting:
- `add_source(string, origin=None)` – Adds rule source code
- `new_namespace(string)` – Isolates rule sets
- `define_global(identifier, value)` – Sets global variables
- `build()` – Produces final `Rules` object

**`Rules`** – Represents compiled rules with methods:
- `scan(bytes)` – Executes pattern matching
- `serialize_into(file)` / `deserialize_from(file)` – Persistence operations

**`Scanner`** – Provides fine-grained scanning control:
- `scan(bytes)` – Scans in-memory data
- `scan_file(path)` – Scans files
- `set_timeout(seconds)` – Enforces time limits
- `set_global(identifier, value)` – Modifies variables mid-scan

## Result Types

**`ScanResults`** contains `matching_rules` (array of `Rule` objects) and `module_outputs` (metadata dictionary).

**`Rule`** exposes `identifier`, `namespace`, `patterns` (tuple of `Pattern` objects), and `metadata`.

**`Pattern`** contains `identifier` and `matches` (tuple of `Match` objects showing `offset`, `length`, and optional `xor_key`).

## Exception Handling

Three exception types: `CompileError` (compilation failures), `ScanError` (runtime scan issues), and `TimeoutError` (exceeded duration limits).

===================================================================

# Seed facts (existing curated YARA -> YARA-X breaking changes for rule authors)

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
