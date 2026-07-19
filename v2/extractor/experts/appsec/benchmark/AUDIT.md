# Benchmark Audit Trail — appsec_bench.jsonl

The benchmark grades the model; a **wrong benchmark task mis-grades the model**, so every task was put
through an **adversarial correctness audit** before use — one Sonnet agent per task, each told to *try to
break* the task: web-verify every currency/library/default claim against official docs/source, confirm the
CWE, and prove each `rubric.must`/`must_not` clause can't false-pass an insecure answer or false-fail a
secure one. Two full rounds were run (round 2 re-audits the round-1 fixes). Scoring follows the project rule:
**the agent verdicts TRIAGE; the fixes were read and judged by hand before applying.**

## Round 1 — 24 core tasks
- **Verdicts:** 0 BROKEN, 7 SOUND, 17 FIX.
- **Nature of fixes:** grading-precision, not broken landmines. Representative:
  - `web-03` `lang` was `python` for a React/JSX task → `javascript`.
  - `inj-02` SSTI mis-tagged CWE-94 → **CWE-1336** (server-side template injection).
  - `cry-01` static-IV clause needed **CWE-329** alongside CWE-327.
  - `cry-03` prose implied PyJWT *omits* `algorithms=`; current PyJWT ≥2.0 **requires** it → reworded so the
    live trap is a *too-permissive* list, not omission.
  - several rubrics had a `must`/`must_not` loophole (an insecure answer could satisfy a `must`, or a secure
    one trip a `must_not`) → tightened.
- **All 17 folded into `build_bench.py`**, then the 6 held-out general tasks were added (→ 30 total).

## Round 2 — all 30 tasks (re-audit after applying round 1)
- **Verdicts:** **0 BROKEN, 0 currency-stale, 18 SOUND, 12 FIX.**
- **SOUND (18):** inj-01, inj-03, cry-03, des-02, aut-01, aut-02, net-01, net-02, web-01, web-02, web-03,
  web-04, sec-01, mem-01, api-01, gen-03, gen-04, gen-05.
- **The 12 FIX were dominated by one class: a `must` clause that would false-FAIL a genuinely secure
  ALTERNATIVE form** — which matters because a false-fail would *understate the bank's win*, not inflate it.
  Every fix broadens `must` to accept all secure forms, closes a false-pass loophole, or corrects a CWE.

| id | class | fix applied |
|---|---|---|
| cry-01 | false-fail | `must` now accepts a correctly composed **AES-CBC + HMAC** (encrypt-then-MAC), not only AEAD primitives |
| cry-02 | false-pass | added `must_not`: **Argon2 cost params explicitly weakened below library defaults** (the trap named weak params but no clause caught them) |
| cry-04 | CWE + false-fail | landmine CWE split **CWE-347 + CWE-208** (timing); `must` accepts `secrets.compare_digest` as well as `hmac.compare_digest` |
| des-01 | clarity | task now takes an explicit `device` arg (was "moved to the target device" with no such param) |
| des-03 | false-fail | `must` now also accepts the explicit **`resolve_entities='internal'`** form (restating the lxml≥5.0 default) |
| inj-02 | false-fail ×3 | `must` accepts `subprocess.run/call/Popen` (not only `.run`); allow-list-only filename validation (drops the redundant-AND); a hardcoded `render_template_string` literal as a static source |
| mem-02 | false-fail | `must` accepts `align_to()`'s correctly-sized middle slice (not only literal `/4`) |
| race-01 | CWE + rigor | added **CWE-276** (default perms); `must` now requires the `0o600` mode be passed to the **same atomic `os.open(O_CREAT\|O_EXCL)`** call, not a later `chmod` |
| sec-02 | realism | replaced **`Set-Cookie`** (a *response* header that won't appear in `request.headers`) with `X-Api-Key` in the request-logging rubric |
| gen-01 | false-fail | `must` accepts PHP 8.2+ **`mysqli::execute_query()`** as well as `prepare`+`bind_param` |
| gen-02 | false-fail + false-pass | `must` accepts `normalize`/`getCanonicalPath`/`cleanPath`; added `must_not` for raw **`String.startsWith`** sibling-prefix collision |
| gen-06 | false-fail | JAXP secondary path now requires **`load-external-dtd=false`** too (the two-feature form was incomplete); added the partial-mitigation `must_not` |

- **Currency spot-checks that PASSED (web-verified, no change):** `torch.load` `weights_only=True` default flip
  in PyTorch 2.6 (2025-01, closes CVE-2025-32434); lxml ≥5.0 `resolve_entities='internal'` + `no_network=True`;
  tarfile `filter='data'` / PEP 706; paramiko `RejectPolicy`; PyJWT `algorithms=` requirement; FastAPI/Starlette
  wildcard-origin+credentials reflection; boto3 default credential provider chain; POSIX `O_EXCL` atomicity;
  JAXP **unsafe**-by-default (the deliberate contrast with lxml).

## Net result
30 tasks, **0 broken across two rounds**, all 29 (17+12) precision fixes applied and verified present in
`appsec_bench.jsonl`. The benchmark grades a secure answer as pass in **every** secure form we could find, and
no insecure answer we could construct satisfies a `must`. It is ready to run base-vs-bank.

*Reproduce:* `Workflow scriptPath scratchpad/bench_audit.js args '{"file":"…/appsec_bench.jsonl","n":30}'`
(one Sonnet agent per task). Per-agent verdicts persist in the workflow `journal.jsonl`.
