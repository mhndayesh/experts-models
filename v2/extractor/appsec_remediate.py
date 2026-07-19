#!/usr/bin/env python3
"""appsec_remediate.py - apply the confirmed audit fixes (_audit_confirmed.json) to the per-source fact
files, then the caller re-merges FINAL.jsonl. SAFE rules (never inject unverifiable code):

  WEAK                          -> REMOVE (not a real landmine)
  code-problem (issue is code)  -> STRIP code_bad/code_good (fact becomes text-only)
  fix is truth-shaped           -> replace truth with the confirmed corrected truth
  WRONG + truth not salvageable -> REMOVE (fix is not a truth AND it is not a code-only problem)
  else                          -> keep, tag _audit_fix

Writes each source file in place; logs every change to _audit_changes.json. Run with --dry to preview.
"""
import json, os, re, sys, html

HERE = os.path.dirname(os.path.abspath(__file__))
FACTS = os.path.join(HERE, "experts", "appsec", "facts")
SOURCES = ["cwe", "codeql", "sast", "mastg", "rustsec", "crypto_net", "owasp_cs"]

CODE_ISSUE = re.compile(r"byte-for-byte|identical|code_good is not|does not (?:fix|actually)|not valid|"
                        r"nonexist|does not exist|no such|is broken|invalid (?:java|ruby|rust|go|c\+\+|syntax)|"
                        r"code_bad|code_good|placeholder|dereferences|scoped to that block", re.I)
TRUTH_SHAPED = re.compile(r"^\s*(Stop|Use|Do not|Don'?t|Do |Always|Never|Prefer|Avoid|Replace|Set |Validate|"
                          r"Call |Pass |Enable|Disable|Require|Treat|Ensure|Configure|Specify|Omit|Bind|Move|"
                          r"Escape|Encode|Verify|Upgrade|Only|When |For |Leave|Provide|Reject|Block|Restrict|"
                          r"Sanitiz|Parameteriz|Store|Generate|Apply|Add |Remove |Check|Wrap|Return|Declare)", re.I)

# fixes phrased ABOUT the fact (not a replacement truth) must never be written into `truth`
META = re.compile(r"^\s*(Replace the truth|Change the truth|Rewrite the truth|Correct the truth|The truth should|"
                  r"Keep truth|Keep the truth|Fix (?:only )?(?:the )?code|Update (?:the )?code|Change (?:the )?code|"
                  r"Set code|Rewrite (?:the )?code|Replace (?:code_|the code)|Drop the code|Strip|Remove the code)", re.I)

def decide(prob, has_code):
    sev = prob["severity"]
    fix = html.unescape((prob.get("fix") or "").strip())
    issue_code = bool(CODE_ISSUE.search(prob.get("issue", "")))
    # the confirm schema defined `fix` as the corrected REPLACEMENT truth; use it unless it is a pure
    # meta-instruction about the fact (those keep the original truth and rely on code-strip / removal).
    truth_ok = len(fix) > 25 and not META.match(fix)
    if sev == "WEAK":
        return ("REMOVE", None, False)
    strip = issue_code and has_code
    if sev == "WRONG" and not truth_ok and not strip:
        return ("REMOVE", None, False)          # wrong truth, no usable fix, not a code issue
    new_truth = fix if truth_ok else None        # None -> keep original truth
    return ("PATCH", new_truth, strip)

def main():
    dry = "--dry" in sys.argv
    conf = json.load(open(os.path.join(FACTS, "_audit_confirmed.json"), encoding="utf-8"))
    # need has_code per fact: read FINAL for that
    final = {json.loads(l)["id"]: json.loads(l) for l in open(os.path.join(FACTS, "FINAL.jsonl"), encoding="utf-8")}
    plan = {}
    for p in conf:
        has_code = bool(final.get(p["id"], {}).get("code_bad"))
        plan[p["id"]] = (decide(p, has_code), p)
    from collections import Counter
    acts = Counter(v[0][0] for v in plan.values())
    strips = sum(1 for v in plan.values() if v[0][0] == "PATCH" and v[0][2])
    patches_truth = sum(1 for v in plan.values() if v[0][0] == "PATCH" and v[0][1])
    print(f"PLAN: remove {acts['REMOVE']} | patch {acts['PATCH']} (of which strip-code {strips}, reword-truth {patches_truth})")
    if dry:
        print("\n--- sample REMOVE ---")
        for pid, ((a, t, s), p) in list(plan.items()):
            if a == "REMOVE": print(f"  [{p['severity']}] {pid} :: {p['issue'][:100]}")
        print("\n--- sample PATCH (reword) ---")
        n = 0
        for pid, ((a, t, s), p) in plan.items():
            if a == "PATCH" and t and n < 8:
                print(f"  {pid} strip={s}\n     OLD: {(final.get(pid,{}).get('truth') or '')[:95]}\n     NEW: {t[:95]}"); n += 1
        return
    # apply to source files
    changes = []
    for src in SOURCES:
        path = os.path.join(FACTS, src + ".jsonl")
        facts = [json.loads(l) for l in open(path, encoding="utf-8")]
        out = []
        for f in facts:
            if f["id"] in plan:
                (action, new_truth, strip), p = plan[f["id"]]
                rec = {"id": f["id"], "severity": p["severity"], "action": action, "old_truth": f.get("truth")}
                if action == "REMOVE":
                    rec["issue"] = p["issue"]; changes.append(rec); continue
                if new_truth:
                    f["truth"] = new_truth; rec["new_truth"] = new_truth
                if strip:
                    f["code_bad"] = None; f["code_good"] = None; rec["stripped_code"] = True
                f["_audit_fix"] = p["severity"] + ": " + p["issue"][:160]
                changes.append(rec)
            out.append(f)
        with open(path, "w", encoding="utf-8") as fh:
            for f in out: fh.write(json.dumps(f, ensure_ascii=False) + "\n")
    json.dump(changes, open(os.path.join(FACTS, "_audit_changes.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print(f"applied: {len(changes)} changes -> per-source files patched; log in _audit_changes.json")

if __name__ == "__main__":
    main()
