# plaso (log2timeline) — release changes, 2024 (and the late-2023 removals that land into 2024)

plaso uses date-based versioning (YYYYMMDD). The GitHub release bodies contain no
changelog text (each release body is literally "Release of version YYYYMMDD"), so the
real removals/renames below are reconstructed verbatim from the git commit log between
release tags and from the tracking issue #4543 "Remove various legacy/backwards
compatibility components".

2024 release tags: **20240308**, **20240826**.
Immediately-preceding release: **20231224** (where the issue #4543 legacy removals landed).

---

## Release 20240826 — commit log (tag 20240308...20240826), removals/renames

- Removed bdist_rpm configuration (#4836)
- Removed support for 20221023 storage format (#4849)
- Renamed SQLite-base storage reader and writer (#4856)
- Removed unnecessary override from SQLite storage file (#4863)
- Removed obsolete future dependency (#4868)
- Changed winlnk to not generate duplicate DLT events #4831 (#4833)
- Added Windows 10 push notification database plugin #4458 (#4780)
- Added GetFieldValues to output modules (#4848)
- Changes to make year-less log helper support full dates #4697
- Changes to make timeliner support date-less log formats #4697
- Changed end-to-end tests to use Ubuntu 24.04 (#4857)
- Added multiple TeamViewer text log file parser plugins (#4847)
- Refactored Redis store (#4865)
- Added Android turbo.db SQLite parser plugin (#4880)
- Added Android application usage SQLite parser plugin (#4881)
- Added Container Runtime Interface (CRI) text parser plugin (#4742)
- Improved normalization of EventLog paths (#4890 / #4894)

Note on "Removed support for 20221023 storage format" (#4849): plaso 20240826 can no
longer read .plaso storage files written in the 20221023 storage format. Storage files
produced by older plaso versions using that format must be regenerated.

Note on "Renamed SQLite-base storage reader and writer" (#4856): the SQLite-based
storage reader/writer classes were renamed. Code that imported the old class names for
reading/writing .plaso SQLite storage must be updated.

---

## Release 20240308 — commit log (tag 20231224...20240308), removals + infra changes

- Removed end-of-life Python 3.7 support (#4801)
- Moved data files into Python module #4769 (#4810)
- Changed tools to entry points #4769 (#4811)
- Added Mac OS startup item plist parser plugin (#4800)  -> plugin: macos_startup_item_plist
- Added Mac OS login window plist parser plugin (#4799)  -> plugin: macos_login_window_plist
- Added Mac OS launchd.log text parser plugin #4685 (#4686)
- Added Mac OS login and background items plist plugins (#4790) -> macos_login_items_plist, macos_background_items_plist
- Added decoder for NSKeyedArchiver encoded plists (#4804)
- Added support for SystemResources .mun files #4259 (message file resource handling)
- Support for additional Windows shell item types (#4820)

Note on "Removed end-of-life Python 3.7 support" (#4801): plaso 20240308 no longer
supports Python 3.7. Python 3.8+ is required.

Note on "Moved data files into Python module / Changed tools to entry points" (#4769):
data files were moved into the Python module, and the command-line tools (log2timeline.py,
psort.py, pinfo.py, psteal.py, image_export.py) were migrated to Python entry points /
console_scripts. This changes how the tools are installed and located.

Blog (osdfir.blogspot.com) 20240308 release notes, verbatim highlights:
"Mac OS login window", "startup item", "login and background items plist plugins",
"Mac OS launchd.log text parser plugin", "Improvements to Windows EventLog resource
extraction and message formatting", "Moved data into Python module and migrated tools
to Python entry points". Planned future work: Docker image upgrade to Ubuntu 24.04;
image export functionality transfer to the dfImageTools project; preprocessing and
knowledge base development (#4543).

---

## Issue #4543 "Remove various legacy/backwards compatibility components"
Milestone: 2023 December release (landed in 20231224). Verbatim checklist:

1. remove SessionStart, SessionConfiguration and SessionCompletion (PR #4712)
2. remove backwards compatibility for parser attribute — related to renaming `parser`
   to `parser_chain` (issue #3700) (PR #4713)
3. clean up `_RESERVED_VARIABLE_NAMES` in default formatter and l2t_csv output modules (PR #4714)
4. clean up `_RESERVED_ATTRIBUTES` in raw output module (PR #4716)
5. remove `process_archives` CLI option (PR #4720)
6. remove text-based filter file support and its documentation (PR #4721)
7. rename `plist/macosx_install_history` to `plist/macos_install_history` (PR #4722)

Note on #4720: the `--process_archives` / `process_archives` command line option was
removed from log2timeline.py. Invocations passing it now error.

Note on #4721: text-based (line-based) filter files are no longer supported; filtering
now requires YAML-based artifact filter files.

Note on #4722: the plist plugin previously named `macosx_install_history` is now
`macos_install_history`. Any `--parsers` selection or de-selection referencing the old
name no longer matches. Confirmed in current Parsers-and-plugins docs: the plugin is
listed as `macos_install_history` ("Parser for MacOS installation history plist files.");
no plugin named `macosx_install_history` exists.

Note on #4712: SessionStart, SessionConfiguration and SessionCompletion attribute
container classes were removed from the storage/session API.

Note on #4713 / #3700: the event `parser` attribute was renamed to `parser_chain`, and
the backwards-compatibility shim exposing the old `parser` attribute was removed.
