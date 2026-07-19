# niche_facts/ — the SCALE-TEST bank (2026-07-13)

933 facts across 12 niche language ecosystems, authored by Claude (Fable 5,
knowledge cutoff 2026-01) from knowledge of the official documentation, on
the owner's order ("pick very niche language and codes ... make like 1000
facts as start"). Merged with the repo's 94 research facts into
`../facts_scale_v1.jsonl` (1027 facts, 42 library tabs).

PROVENANCE / HONESTY: these facts did NOT go through the package's v3
quote-verification gates (verbatim quote + anchor). They exist to stress
the TEMPLATE-BRAIN MATCHING at realistic scale and vocabulary - treat
individual fact texts as high-confidence but unverified. The research
bank (`NEW BANK/.../facts_v2.jsonl`) remains the only gate-verified bank
and was not modified.

| file | facts | version basis |
|---|---|---|
| zig.jsonl | 115 | 0.13 (0.11/0.12/0.14 changes marked) |
| nim.jsonl | 108 | 2.x |
| ocaml.jsonl | 95 | 5.x |
| raku.jsonl | 95 | 6.d |
| gleam.jsonl | 80 | 1.x |
| crystal.jsonl | 80 | 1.x |
| dlang.jsonl | 75 | 2.x |
| odin.jsonl | 70 | dev |
| racket.jsonl | 70 | 8.x |
| haxe.jsonl | 55 | 4.3 |
| janet.jsonl | 50 | 1.x |
| bqn.jsonl | 40 | CBQN |

Calibration record (density wall, real vocabulary): 4 sweep rounds
against 42 no-match questions + 15 language probes drove false
injections 4 -> 0 and probes to 15/15 own-language-only. Root causes
fixed in enrich.py: (1) STOP-list bypass for `App()`-style cores (bug),
(2) generic programming vocabulary (script/app/json/struct/convert/
float/date/...) acquiring keyword status through dotted-token segments.
The extended STOP list in enrich.py IS the calibration artifact.
