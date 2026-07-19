# ===== RELEASE tqdm/tqdm v4.28.0 =====

- remove installation of man pages by default (#460, #628)
- CLI:add `--manpath` option (#629)
- documentation additions and fixes
# ===== RELEASE tqdm/tqdm v4.29.0 =====

- Avoid global multiprocessing locks (#611 -> #617)
- Add support for infinite iterables (#651)
- Fix missing attr pos when used in multi-threaded environment (#573)
- Do not join `TMonitor` if it is the current thread (#613 -> #641)
- Add OpenBSD NIX support (#638)
- Unit tests, general documentation fixes and tidying (e.g. #642)
- CI travis improvements
  + `py37-dev` -> `py37` (#622)
  + fix `py26`
