# Base-vs-Bank scorecard — gemma-4-E2B-it (Q8_0), served, 30-task appsec benchmark

> ⚠️ **SUPERSEDED / not the shipped number.** This is the **SERVED** run (Python retriever + HyDE double-key +
> thinking-ON) — the *retrieval-method ceiling*, NOT the shipped baked GGUF. The shipped GGUFs do **prompt-only**
> in-template retrieval and score lower. For the shipped-artifact numbers (e2b/12b/26b vs DeepSeek-V4) see
> **`SCORECARD-crossmodel.md`** — that's the one the published HF cards cite.

**Setup.** My own `llama-server` (ROCm) on the base **gemma-4-E2B-it-Q8_0** GGUF — NOT LM Studio.
Gemma-native sampling (temp 1.0 / top_k 64 / top_p 0.95 / min_p 0.01), **thinking-ON**, 6 parallel slots.
Per task: **BASE** = task asked directly; **BANK** = HyDE double-key retrieval (task + base draft) → top-5 facts
injected authority-framed → re-ask. All 60 answers finished cleanly (`stop`, no truncation). **Scored by hand**
(read the code, judged against each rubric — automated signature scan only triaged *what* to read).

## Headline
**BASE SECURE@1 ≈ 17/30 (~57%) → BANK SECURE@1 ≈ 22/30 (~73%), net +5 tasks.** The gain is real but **not free**:
the bank produced **6 clean wins + 2 partial**, and **2 genuine regressions**. E2B (2B) is the smallest model, and
that shows — where retrieval misses, the injected block sometimes *destabilizes* the tiny model.

## Wins — bank fixed what base got wrong (8)
| task | landmine | base → bank |
|---|---|---|
| **des-01** | CWE-502 torch | `torch.load(path, map_location=…)` (RCE) → `torch.load(…, weights_only=True)` — **post-cutoff fact fired** |
| **web-02** | CWE-22/59 tar | `extractall(dest)` ("usually sufficient" — wrong) → `extractall(dest, filter="data")` — **post-cutoff** |
| **gen-05** (held-out) | CWE-639 IDOR | ownership check **commented out** → real `if order.user_id != current_user.id:` 403 |
| **gen-02** (held-out) | CWE-22 Java | `Paths.get(base,name)` no check → normalize + `startsWith(base)` containment |
| **gen-03** (held-out) | CWE-79 Express | `` `Hello, ${req.query.name}` `` → `escape-html` before interpolation |
| **gen-04** (held-out) | CWE-434 upload | uuid name but **no type check** → adds `ALLOWED_EXTENSIONS` allow-list |
| web-01 | CWE-22 | `'..'` blacklist → `realpath` + prefix containment (mild) |
| api-01 | CWE-409 bomb | no cap → `MAX_DECOMPRESSED_SIZE` check (partial: not streaming, still full-decompress-then-check) |

## Regressions — bank broke what base got RIGHT (2)  ← the finding
| task | what happened | root cause |
|---|---|---|
| **aut-01** | base set `SESSION_COOKIE_SECURE=True` + `SAMESITE='Lax'`; **bank dropped both**, kept only session regen | retrieved facts were fixation/CSRF-only (cwe-384) — nudged the model to focus there and drop cookie flags |
| **cry-02** | base used real `argon2-cffi` PasswordHasher; **bank hallucinated a MOCK KDF returning `os.urandom()` as the "hash"** | **retrieval MISS** — got JWT/path-traversal facts (cwe-347/cwe-022), zero argon2 facts → irrelevant authority block derailed the 2B model |

## Language drift (2, retrieval-miss driven) — not scored as wins
- **cry-04** (Python→**Go**) and **net-01** (Python→**TypeScript**): both got irrelevant facts (iOS/CSRF; android),
  and the tiny model switched language mid-answer. net-01 was already insecure in base (open SSRF); cry-04 base was secure.

## Ties — base already secure (14)
inj-01, inj-02, cry-01, cry-03, des-02, des-03, aut-02, web-03, web-04, sec-01, mem-01, gen-01, gen-06, net-02 —
E2B's base is already strong on textbook vulns (parameterized SQL, AES-GCM, JWT RS256-only, DOMPurify, CORS pinning,
no-hardcoded-creds, PHP prepared stmt, JAXP disallow-doctype). The bank neither helped nor hurt.

## Ties — both fail, task too hard for E2B (4)
net-01 (SSRF pinning), race-01 (TOCTOU — neither used `O_EXCL`), mem-02 (Rust — both ignored alignment), inj-03
(Mongo nested-operator — both only shallow-validated).

## Takeaways
1. **The bank's edge is exactly where the thesis predicts: post-cutoff currency (des-01, web-02) and generalization
   to held-out languages/tasks (gen-02/03/04/05).** Those are the wins base can't get from training.
2. **On a 2B model, a retrieval MISS is actively harmful** — injecting irrelevant authority facts + thinking-ON makes
   the small model hallucinate mocks or switch languages. cry-02 and aut-01 are the proof. On 12b/26b this
   destabilization was not observed; it's an E2B-size effect.
3. **Fix indicated (not a bank-quality problem, a retrieval-precision problem):** cry-02/cry-04/net-01 failed because
   retrieval returned off-target facts. A relevance floor (inject nothing when top score < threshold — "retrieve first,
   fail open") would convert those 2 regressions back to ties and remove the drift. Worth an A/B before baking E2B.
