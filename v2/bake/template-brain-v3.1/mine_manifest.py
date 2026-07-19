#!/usr/bin/env python3
"""mine_manifest.py - run mine_api.py across the whole library manifest.

Each row: (domain, lib/tab, import module, extra submodules, objects.inv URL,
doc base URL, which venv has it installed). Domains map 1:1 onto the planned
per-domain FactBank models (BANK-EXPANSION-RESEARCH.md §4).

usage: python mine_manifest.py [--domain data] [--only pandas,numpy]
"""
import argparse, json, os, subprocess, sys

SCRATCH = (r"C:\Users\mhnda\AppData\Local\Temp\claude\c--projects-LLM-BANK"
           r"\1ed4b2f9-1147-4ea5-8edb-ab072322505f\scratchpad")
VENV = {
    "data": os.path.join(SCRATCH, "mine313", "Scripts", "python.exe"),
    "web":  os.path.join(SCRATCH, "mineweb", "Scripts", "python.exe"),
    "ai":   os.path.join(SCRATCH, "mineai",  "Scripts", "python.exe"),
    "std":  os.path.join(SCRATCH, "mine313", "Scripts", "python.exe"),
}

# (domain, lib, module, submodules, inv_url, inv_base)
MANIFEST = [
    # ---- data ----
    ("data", "pandas", "pandas", "", "https://pandas.pydata.org/docs/objects.inv", "https://pandas.pydata.org/docs/"),
    ("data", "numpy", "numpy", "numpy.strings,numpy.linalg,numpy.random,numpy.fft,numpy.dtypes", "https://numpy.org/doc/stable/objects.inv", "https://numpy.org/doc/stable/"),
    ("data", "polars", "polars", "polars.selectors", "https://docs.pola.rs/api/python/stable/objects.inv", "https://docs.pola.rs/api/python/stable/"),
    ("data", "pyarrow", "pyarrow", "pyarrow.compute,pyarrow.parquet,pyarrow.dataset", "https://arrow.apache.org/docs/objects.inv", "https://arrow.apache.org/docs/"),
    ("data", "scipy", "scipy", "scipy.stats,scipy.optimize,scipy.signal,scipy.linalg,scipy.interpolate,scipy.integrate,scipy.spatial,scipy.sparse,scipy.fft,scipy.ndimage", "https://docs.scipy.org/doc/scipy/objects.inv", "https://docs.scipy.org/doc/scipy/"),
    ("data", "sklearn", "sklearn", "sklearn.linear_model,sklearn.ensemble,sklearn.model_selection,sklearn.preprocessing,sklearn.metrics,sklearn.cluster,sklearn.decomposition,sklearn.pipeline,sklearn.svm,sklearn.tree,sklearn.neighbors,sklearn.impute,sklearn.feature_selection,sklearn.compose", "https://scikit-learn.org/stable/objects.inv", "https://scikit-learn.org/stable/"),
    ("data", "matplotlib", "matplotlib", "matplotlib.pyplot,matplotlib.axes,matplotlib.figure,matplotlib.colors,matplotlib.patches,matplotlib.ticker", "https://matplotlib.org/stable/objects.inv", "https://matplotlib.org/stable/"),
    ("data", "xarray", "xarray", "", "https://docs.xarray.dev/en/stable/objects.inv", "https://docs.xarray.dev/en/stable/"),
    ("data", "statsmodels", "statsmodels.api", "statsmodels.formula.api,statsmodels.tsa.api", "https://www.statsmodels.org/stable/objects.inv", "https://www.statsmodels.org/stable/"),
    ("data", "duckdb", "duckdb", "", "", "https://duckdb.org/docs/stable/clients/python/overview"),

    # ---- web ----
    ("web", "django", "django", "django.db.models,django.forms,django.http,django.urls,django.views.generic,django.contrib.auth,django.core.validators,django.template,django.test", "https://docs.djangoproject.com/en/6.0/_objects/", "https://docs.djangoproject.com/en/6.0/"),
    ("web", "sqlalchemy", "sqlalchemy", "sqlalchemy.orm,sqlalchemy.sql,sqlalchemy.ext.asyncio,sqlalchemy.pool,sqlalchemy.types", "https://docs.sqlalchemy.org/en/20/objects.inv", "https://docs.sqlalchemy.org/en/20/"),
    ("web", "fastapi", "fastapi", "fastapi.responses,fastapi.security,fastapi.testclient", "https://fastapi.tiangolo.com/objects.inv", "https://fastapi.tiangolo.com/reference/"),
    ("web", "starlette", "starlette", "starlette.responses,starlette.requests,starlette.routing,starlette.middleware,starlette.testclient,starlette.websockets", "", "https://www.starlette.io/"),
    ("web", "pydantic", "pydantic", "pydantic.fields,pydantic.functional_validators,pydantic.types,pydantic.networks", "https://docs.pydantic.dev/latest/objects.inv", "https://docs.pydantic.dev/latest/api/base_model/"),
    ("web", "httpx", "httpx", "", "", "https://www.python-httpx.org/api/"),
    ("web", "litestar", "litestar", "litestar.response,litestar.di,litestar.params,litestar.testing", "https://docs.litestar.dev/2/objects.inv", "https://docs.litestar.dev/2/"),
    ("web", "flask", "flask", "", "https://flask.palletsprojects.com/en/stable/objects.inv", "https://flask.palletsprojects.com/en/stable/"),
    ("web", "requests", "requests", "", "https://requests.readthedocs.io/en/latest/objects.inv", "https://requests.readthedocs.io/en/latest/"),
    ("web", "celery", "celery", "", "https://docs.celeryq.dev/en/stable/objects.inv", "https://docs.celeryq.dev/en/stable/"),
    ("web", "redis", "redis", "", "https://redis.readthedocs.io/en/stable/objects.inv", "https://redis.readthedocs.io/en/stable/"),

    # ---- ai sdks ----
    ("ai", "openai", "openai", "openai.types", "", "https://github.com/openai/openai-python"),
    ("ai", "anthropic", "anthropic", "anthropic.types", "", "https://docs.anthropic.com/en/api/client-sdks"),
    ("ai", "langchain", "langchain", "langchain_core.messages,langchain_core.tools,langchain_core.runnables,langchain_core.prompts,langchain_core.output_parsers,langchain_core.documents", "https://python.langchain.com/api_reference/objects.inv", "https://python.langchain.com/api_reference/"),
    ("ai", "pydantic_ai", "pydantic_ai", "pydantic_ai.models,pydantic_ai.tools,pydantic_ai.messages", "https://ai.pydantic.dev/objects.inv", "https://ai.pydantic.dev/api/agent/"),

    # ---- python stdlib (3.13) : per-module tabs ----
    ("std", "pathlib", "pathlib", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "asyncio", "asyncio", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "itertools", "itertools", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "functools", "functools", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "collections", "collections", "collections.abc", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "dataclasses", "dataclasses", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "typing", "typing", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "subprocess", "subprocess", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "json", "json", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "re", "re", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "os", "os", "os.path", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "shutil", "shutil", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "datetime", "datetime", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "argparse", "argparse", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "logging", "logging", "logging.handlers,logging.config", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "unittest", "unittest", "unittest.mock", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "sqlite3", "sqlite3", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "csv", "csv", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "enum", "enum", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "concurrent", "concurrent.futures", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "contextlib", "contextlib", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "socket", "socket", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "hashlib", "hashlib", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "textwrap", "textwrap", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "statistics", "statistics", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "random", "random", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "math", "math", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "inspect", "inspect", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "tempfile", "tempfile", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
    ("std", "zipfile", "zipfile", "", "https://docs.python.org/3/objects.inv", "https://docs.python.org/3/"),
]

OUT = "api_facts"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--domain", default="")
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    only = {s.strip() for s in a.only.split(",") if s.strip()}
    os.makedirs(OUT, exist_ok=True)
    total, rows = 0, []
    for domain, lib, module, subs, inv, base in MANIFEST:
        if a.domain and domain != a.domain:
            continue
        if only and lib not in only:
            continue
        out = os.path.join(OUT, f"{domain}__{lib}.jsonl")
        cmd = [sys.executable, "-X", "utf8", "mine_api.py", "--lib", lib, "--module", module,
               "--submodules", subs, "--inv", inv, "--inv-base", base,
               "--python", VENV[domain], "--out", out, "--prefix", f"{lib}api"]
        p = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
        if p.returncode != 0:
            print(f"FAIL {domain}/{lib}: {(p.stderr or '')[-300:]}")
            continue
        n = sum(1 for _ in open(out, encoding="utf-8")) if os.path.exists(out) else 0
        total += n
        rows.append((domain, lib, n))
        print(f"{domain:5} {lib:14} {n:5} facts")
    print(f"\nTOTAL: {total} signature facts across {len(rows)} libraries")
    json.dump([{"domain": d, "lib": l, "facts": n} for d, l, n in rows],
              open(os.path.join(OUT, "_counts.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
