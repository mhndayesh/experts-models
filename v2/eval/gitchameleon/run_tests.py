#!/usr/bin/env python3
"""run_tests.py - EXECUTION scoring for GitChameleon (real pass@1, not a data comparison).

For each problem: build a venv with the problem's EXACT pinned python + library version +
dependencies (uv, one venv per unique (library,version,python,deps) - reused), drop the model's
solution as sample_<id>.py, run the HIDDEN pytest test against it. Pass = tests green. Base and
baked are scored on the SAME buildable set.

  python run_tests.py <solutions.jsonl> --tag base-12b [--only 12,40] [--out-dir DIR]

Outputs: <out-dir>/<tag>_results.jsonl  {example_id, status: pass|fail|env_error, detail}
         <out-dir>/<tag>_buildlog.jsonl  {example_id, key, stderr}   (build failures, retained)

FAITHFULNESS (see PROVENANCE.md; the official benchmark uses pinned DOCKER envs, py 3.7/3.9/3.10):
  * EXACT python version per problem - NO 3.7->3.9 remap. If uv cannot provide the pinned interpreter
    (3.7 is EOL and may not be available from uv's python-build-standalone), the build fails LOUDLY and
    the real error is RECORDED (not silently remapped, not discarded). A faithful 3.7 run needs a real
    interpreter available to uv (e.g. `uv python install 3.7` if offered, or a pyenv/Docker fallback).
  * cache key includes DEPENDENCIES, so two problems that share lib@version@py but differ in deps do
    NOT share a venv (the previous key omitted deps and cross-contaminated venvs).
  * build stderr is retained to a buildlog, so "unbuildable" is EVIDENCED, not asserted.
  * pytest timeout matches upstream (constants.TIMEOUT_SEC = 240s).
  * results are written to --out-dir (default v2/eval/results/), NOT into the vendored upstream tree.
"""
import sys, os, json, re, subprocess, tempfile, shutil, argparse, collections, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
DS = os.path.join(HERE, "dataset", "dataset.jsonl")
HID = os.path.join(HERE, "dataset", "hidden_tests")
ENVROOT = os.path.join(os.environ.get("TEMP", "/tmp"), "gc_envs")
os.makedirs(ENVROOT, exist_ok=True)

TIMEOUT_SEC = 240          # match upstream gitchameleon/constants.py:TIMEOUT_SEC
HARNESS_REV = "2"          # bump to invalidate cached .ok markers on harness changes

def rows():
    return {json.loads(l)["example_id"]: json.loads(l) for l in open(DS, encoding="utf-8")}

def pyver(v):
    # EXACT pinned version - no remap. The dataset gives 3.7 / 3.9 / 3.10.
    return str(v).strip()

def deps_of(r):
    d = (r.get("additional_dependencies") or "").strip()
    e = (r.get("extra_dependencies") or "").strip()
    return (d + " " + e).split()

def envkey(r):
    deps = " ".join(sorted(deps_of(r)))
    base = f"{r['library']}@{r['version']}@{pyver(r['python_version'])}"
    return base + ("@" + hashlib.sha1(deps.encode()).hexdigest()[:8] if deps else "")

def build_env(r, cache, buildlog):
    """create (or reuse) a venv for this (lib,version,py,deps). -> venv-python path or None."""
    key = envkey(r)
    if key in cache: return cache[key]
    vdir = os.path.join(ENVROOT, re.sub(r"[^A-Za-z0-9._@-]", "_", key))
    vpy = os.path.join(vdir, "Scripts", "python.exe")
    if not os.path.exists(vpy):
        vpy = os.path.join(vdir, "bin", "python")          # posix layout
    marker = os.path.join(vdir, ".ok")
    if os.path.exists(marker) and os.path.exists(vpy) and \
            open(marker).read().strip() == HARNESS_REV:     # revalidate on harness rev
        cache[key] = vpy; return vpy
    shutil.rmtree(vdir, ignore_errors=True)
    py = pyver(r["python_version"])
    try:
        subprocess.run(["uv", "venv", "--python", py, vdir], check=True,
                       capture_output=True, text=True, timeout=300)
        vpy = os.path.join(vdir, "Scripts", "python.exe")
        if not os.path.exists(vpy): vpy = os.path.join(vdir, "bin", "python")
        pkgs = [f"{r['library']}=={r['version']}", "pytest"] + deps_of(r)
        subprocess.run(["uv", "pip", "install", "--python", vpy, *pkgs],
                       check=True, capture_output=True, text=True, timeout=900)
        open(marker, "w").write(HARNESS_REV)
        cache[key] = vpy; return vpy
    except subprocess.CalledProcessError as e:
        buildlog.write(json.dumps({"example_id": r["example_id"], "key": key,
                                   "stderr": (e.stderr or "")[-1500:]}) + "\n"); buildlog.flush()
        cache[key] = None; return None
    except Exception as e:
        buildlog.write(json.dumps({"example_id": r["example_id"], "key": key,
                                   "stderr": f"{type(e).__name__}: {e}"}) + "\n"); buildlog.flush()
        cache[key] = None; return None

def run_one(eid, ans, vpy):
    testf = os.path.join(HID, f"test_sample_{eid}.py")
    if not os.path.exists(testf): return "no_test", ""
    wd = tempfile.mkdtemp(prefix=f"gc_{eid}_")
    try:
        open(os.path.join(wd, f"sample_{eid}.py"), "w", encoding="utf-8").write(ans)
        shutil.copy(testf, os.path.join(wd, f"test_sample_{eid}.py"))
        env = dict(os.environ, PYTHONPATH=wd)
        r = subprocess.run([vpy, "-m", "pytest", f"test_sample_{eid}.py", "-q", "-x", "--no-header"],
                           cwd=wd, capture_output=True, text=True, timeout=TIMEOUT_SEC, env=env)
        return ("pass" if r.returncode == 0 else "fail"), (r.stdout + r.stderr)[-400:]
    except subprocess.TimeoutExpired:
        return "fail", "timeout"
    finally:
        shutil.rmtree(wd, ignore_errors=True)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("solutions"); ap.add_argument("--tag", required=True)
    ap.add_argument("--only", default="", help="comma-separated ids for a quick smoke")
    ap.add_argument("--out-dir", default=os.path.join(HERE, "..", "results"),
                    help="where to write results (default v2/eval/results/, NOT the vendored tree)")
    a = ap.parse_args()
    out_dir = os.path.abspath(a.out_dir); os.makedirs(out_dir, exist_ok=True)
    R = rows()
    sols = {json.loads(l)["example_id"]: json.loads(l)["answer"] for l in open(a.solutions, encoding="utf-8")}
    if a.only: sols = {k: v for k, v in sols.items() if k in set(a.only.split(","))}
    cache = {}
    out = open(os.path.join(out_dir, f"{a.tag}_results.jsonl"), "w", encoding="utf-8")
    buildlog = open(os.path.join(out_dir, f"{a.tag}_buildlog.jsonl"), "w", encoding="utf-8")
    cnt = collections.Counter()
    for i, (eid, ans) in enumerate(sorted(sols.items(), key=lambda x: int(x[0])), 1):
        r = R.get(eid)
        if not r: continue
        vpy = build_env(r, cache, buildlog)
        if not vpy:
            st, detail = "env_error", envkey(r)
        else:
            st, detail = run_one(eid, ans, vpy)
        cnt[st] += 1
        out.write(json.dumps({"example_id": eid, "library": r["library"],
                              "python_version": r.get("python_version"),
                              "status": st, "detail": detail}) + "\n"); out.flush()
        if i % 20 == 0: print(f"  {i}/{len(sols)}  {dict(cnt)}")
    out.close(); buildlog.close()
    built = cnt["pass"] + cnt["fail"]
    print(f"\n[{a.tag}] pass={cnt['pass']} fail={cnt['fail']} env_error={cnt['env_error']} no_test={cnt['no_test']}")
    print(f"[{a.tag}] pass@1 over buildable ({built}): {100*cnt['pass']/built:.1f}%" if built else "no buildable")
    print(f"[{a.tag}] pass@1 over all 328: {100*cnt['pass']/328:.1f}%")
    print(f"[{a.tag}] build failures retained in {a.tag}_buildlog.jsonl (env-error causes are now EVIDENCED)")

if __name__ == "__main__":
    main()
