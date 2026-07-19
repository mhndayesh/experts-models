# pefile CHANGELOG (GitHub releases: erocarrera/pefile)

Source: https://github.com/erocarrera/pefile/releases

## v2024.8.26 — pefile 2024.8.26  (2024-08-26)

## What's Changed
* Close the __data__ attribute before reassigning it by @adang1345 in https://github.com/erocarrera/pefile/pull/367
* Floor division (//) does mathematical division with the floor functio… by @j-t-1 in https://github.com/erocarrera/pefile/pull/373
* Update new dvrt type and Load Config filed adapt to Windows11 by @zjgcjy in https://github.com/erocarrera/pefile/pull/374
* fix PE.get_data by @mak in https://github.com/erocarrera/pefile/pull/379
* Fix ambiguous string syntax for PEid parsing regexp by @hillu in https://github.com/erocarrera/pefile/pull/388
* fixed a memory leak that caused the pe file to be access locked. by @daniel-mekuria in https://github.com/erocarrera/pefile/pull/386
* Exphash from sha256 to md5 to match imphash by @N0fix in https://github.com/erocarrera/pefile/pull/377
* More readable calls to superclass by @j-t-1 in https://github.com/erocarrera/pefile/pull/393
* Fix cache_adjust_FileAlignment to work with files not aligned to 0x200 by @asivery in https://github.com/erocarrera/pefile/pull/397
* [StepSecurity] Apply security best practices by @step-security-bot in https://github.com/erocarrera/pefile/pull/399
* Create sets using curly brackets by @j-t-1 in https://github.com/erocarrera/pefile/pull/400
* Change IOError to OSError by @j-t-1 in https://github.com/erocarrera/pefile/pull/401
* Apply isort to sort all imports by @j-t-1 in https://github.com/erocarrera/pefile/pull/403
* Remove "OC Patch" comments by @j-t-1 in https://github.com/erocarrera/pefile/pull/408
* Update tox.ini Python versions by @j-t-1 in https://github.com/erocarrera/pefile/pull/409
* Use with statement to write to file by @j-t-1 in https://github.com/erocarrera/pefile/pull/418
* Remove distutils use by @j-t-1 in https://github.com/erocarrera/pefile/pull/417
* Use chaining comparison operators by @j-t-1 in https://github.com/erocarrera/pefile/pull/416
* Replace list comprehension with set comprehension by @j-t-1 in https://github.com/erocarrera/pefile/pull/415
* Use not in operator by @j-t-1 in https://github.com/erocarrera/pefile/pull/414
* Replace base class name with super() by @j-t-1 in https://github.com/erocarrera/pefile/pull/413
* Increase readability and consistency by @j-t-1 in https://github.com/erocarrera/pefile/pull/412
* Tiny comment improvements by @j-t-1 in https://github.com/erocarrera/pefile/pull/410
* Update oleaut32.py from oleaut32.dll by @j-t-1 in https://github.com/erocarrera/pefile/pull/406
* Improve parse_rich_header by @j-t-1 in https://github.com/erocarrera/pefile/pull/402
* Include ordinals for wsock32.dll by @j-t-1 in https://github.com/erocarrera/pefile/pull/405
* Update ws2_32.py from ws2_32.dll by @j-t-1 in https://github.com/erocarrera/pefile/pull/404
* Update pefile.py for typo by @Derekt2 in https://github.com/erocarrera/pefile/pull/398
* Add parsing for IMAGE_DEBUG_TYPE_EX_DLLCHARACTERISTICS by @aursulis in https://github.com/erocarrera/pefile/pull/365

## New Contributors
* @adang1345 made their first contribution in https://github.com/erocarrera/pefile/pull/367
* @zjgcjy made their first contribution in https://github.com/erocarrera/pefile/pull/374
* @mak made their first contribution in https://github.com/erocarrera/pefile/pull/379
* @daniel-mekuria made their first contribution in https://github.com/erocarrera/pefile/pull/386
* @N0fix made their first contribution in https://github.com/erocarrera/pefile/pull/377
* @asivery made their first contribution in https://github.com/erocarrera/pefile/pull/397
* @step-security-bot made their first contribution in https://github.com/erocarrera/pefile/pull/399
* @Derekt2 made their first contribution in https://github.com/erocarrera/pefile/pull/398
* @aursulis made their first contribution in https://github.com/erocarrera/pefile/pull/365

**Full Changelog**: https://github.com/erocarrera/pefile/compare/v2023.2.7...v2024.8.26

## v2023.2.7  (2023-02-07)

## What's Changed
* This release includes Python Wheels (https://github.com/erocarrera/pefile/issues/341)
* accept dot in valid charset for name by @nbourdau in https://github.com/erocarrera/pefile/pull/346
* Remove future from dependencies by @FantasqueX in https://github.com/erocarrera/pefile/pull/349
* Add machine types by @j-t-1 in https://github.com/erocarrera/pefile/pull/361
* Incorporate PEP 238 and PEP 3120 by @j-t-1 in https://github.com/erocarrera/pefile/pull/362
* Generate GUID fields of CV_INFO_PDB70 readable by Python by @UserUnknownFactor in https://github.com/erocarrera/pefile/pull/363
* Dynamic relocations support by @pspcreateprocess in https://github.com/erocarrera/pefile/pull/353
* Add Export Hash Method by @LloydLabs in https://github.com/erocarrera/pefile/pull/354
* Loosen export symbol validation: by @learn-more in https://github.com/erocarrera/pefile/pull/360

Finally @pombredanne's great suite of tests (forked from https://github.com/pombredanne/pefile-tests) now runs for regression tests and coverage as a GitHub Action. ["Making a coverage badge"](https://nedbatchelder.com/blog/202209/making_a_coverage_badge.html) was helpful in setting up tests and coverage reporting.

## New Contributors
* @nbourdau made their first contribution in https://github.com/erocarrera/pefile/pull/346
* @FantasqueX made their first contribution in https://github.com/erocarrera/pefile/pull/349
* @j-t-1 made their first contribution in https://github.com/erocarrera/pefile/pull/361
* @UserUnknownFactor made their first contribution in https://github.com/erocarrera/pefile/pull/363
* @pspcreateprocess made their first contribution in https://github.com/erocarrera/pefile/pull/353
* @LloydLabs made their first contribution in https://github.com/erocarrera/pefile/pull/354

**Full Changelog**: https://github.com/erocarrera/pefile/compare/v2022.5.30...v2023.2.7

## v2022.5.30 — pefile 2022.5.30  (2022-05-30)

* Merged pull request [#344](https://github.com/erocarrera/pefile/issues/344) from elicn/faster-reloc: Speed up relocation process
* Merged pull request [#175](https://github.com/erocarrera/pefile/issues/175) from tdube/patch-1: Fix catch-all exception clause in parse_resources_directory
* Turn __data__ into a bytearray to avoid copying data around (from elicn)
* Merged pull request [#343](https://github.com/erocarrera/pefile/issues/343) from mat-gas/master: various performances improvements (30-50% in certain workflows, 15-25% in average)
* Merged pull request [#340](https://github.com/erocarrera/pefile/issues/340) from dinateper/feature/PEfile_context_manager: Update PE to allow with statements
* Removed legacy Python 2 code
* Miscellaneous other fixes.

## v2021.9.3 — pefile 2021.9.3  (2021-09-03)

Fixed issue #334 coming from the new functionality in #327 and also merged PR #333 adding the method `get_rich_header_hash`

## v2021.9.2 — pefile 2021.9.2  (2021-09-02)

* Merged the great PR #327 and #292 
* Fixed #332 #291 
* Run `black` to format the code and addressed a handful of the many issues flagged by `pylint`
* Dropped old Python 2 code and compatibility tweaks.

## v2021.5.24 — pefile 2021.5.24  (2021-05-24)

This release incorporates the issues fixed since the last release.

## v2021.5.13 — pefile 2021.5.13  (2021-05-13)

This release incorporates the merged PRs and issues fixed since the last release.
I am also stopping to support Python 2.7.

## v2019.4.18 — pefile 2019.4.18  (2019-04-18)

This release incorporates the merged PRs and issues fixed since the last release. These should speed up parsing of files with many ordinals or exports.

## v2019.4.14 — pefile 2019.4.14  (2019-04-14)

This release incorporates the merged PRs and issues fixed since the last release.

## v2018.8.8 — pefile 2018.8.8  (2018-08-08)

This release incorporates the merged PRs and issues fixed since the last release.

## v2017.11.5 — pefile 2017.11.5  (2017-11-05)

Merged PR #212 and fixed a few miscellaneous crashed parsing malformed files.

## v2017.9.3 — pefile 2017.9.3  (2017-09-03)

Merged PRs: #188, #169, #166, #165, #154, #174, and #210. 
I've also improved handling of some corner cases of files with invalid exports and improved the is_driver check.

## v2017.8.1 — pefile 2017.8.1  (2017-08-01)

Merged PRs: #180, #183, #190, #200, #202 and fixed a bug handling bytearrays under certain conditions.

## v2017.5.26 — pefile 2017.5.26  (2017-05-26)

Maintenance release.

## v2016.3.28 — pefile 2016.3.28  (2016-03-28)

Minor fixes, merged some pending pull requests.
[pefile-2016.3.28.tar.gz](https://github.com/erocarrera/pefile/files/192316/pefile-2016.3.28.tar.gz)
[pefile-2016.3.28.zip](https://github.com/erocarrera/pefile/files/192317/pefile-2016.3.28.zip)

## v2016.3.4 — pefile 2016.3.4  (2016-03-04)

Version 2016.3.4 of pefile now runs under Python 2.7 and Python 3 in addition to addressing a few of the long standing issues.
