"""extract.py - docs/changelog section -> candidate facts, via a READY
model (extractor of record: google/gemma-4-e2b, owner decision). The
model proposes; gates.py disposes. Safety is the quote gate, not trust.
"""

import json
import re
import urllib.request

from .loop import Truncated

# v3 prompt (2026-07-13). v2 targeted measured e2b failures (fabricated
# quotes, invented labels). v3 adds the F-036 audit lesson: 5 true 12B
# facts died because the identifier lived only in the quote — rule 2 now
# demands it in "text" itself. Output is an OBJECT to match the
# structured-output schema below.
EXTRACT_SYSTEM = """You extract facts from library release notes and docs.

RULES — follow every one:
1. One fact = one checkable claim about a named API.
2. Every fact MUST name at least one exact identifier: a function,
   method, class, constant, flag, or command. Examples: pl.concat,
   retry(), --no-cache, -q, OPT_INDENT_2, uv tree. Write that
   identifier INSIDE the "text" field itself — a fact whose text does
   not contain the identifier is rejected, even if the quote has it.
3. "quote" MUST be copied character-for-character from the source text.
   Never reword it, never combine sentences. If you cannot copy an exact
   supporting line, SKIP that fact — writing nothing is correct.
4. "kind" is exactly one of:
   signature  = how to call something
   behavior   = what something does
   removed    = renamed, removed or deprecated — name BOTH old and new
   example    = a usage pattern
   concept    = a rule or limitation
5. "text" is 20-60 words, self-contained, and states the library name
   and version.
6. Skip entirely: contributor credits, internal refactors, performance
   percentages, CI/build/packaging changes, and version bumps of bundled
   or vendored components. Only facts a developer USING the library
   needs when writing code.
7. "probes" = 2-3 short questions a developer would type when they need
   this fact.

OUTPUT: only JSON, no commentary. Shape:
{"facts": [{"text": "...", "kind": "...", "quote": "...",
"probes": ["...", "..."]}]}
No facts worth keeping -> {"facts": []}

EXAMPLE
Source: "Renamed `DataFrame.groupby` to `DataFrame.group_by` (#12345)"
Output: {"facts": [{"text": "polars 1.0 renamed DataFrame.groupby to
DataFrame.group_by; code calling the old groupby name fails on polars
1.0.", "kind": "removed", "quote": "Renamed `DataFrame.groupby` to
`DataFrame.group_by`", "probes": ["polars groupby not working",
"group rows polars 1.0"]}]}"""

# grammar-enforced structured output (LM Studio + llama-server, verified
# live 2026-07-13): shape and the kind ENUM become sampler-impossible to
# violate — kills the invented-label and parse-failure classes. Content
# quality (quotes, vagueness) stays the gates' job: shape != truth.
CANDIDATES_SCHEMA = {
    "type": "json_schema",
    "json_schema": {
        "name": "fact_candidates", "strict": True,
        "schema": {
            "type": "object",
            "properties": {"facts": {"type": "array", "items": {
                "type": "object",
                "properties": {
                    "text": {"type": "string"},
                    "kind": {"type": "string",
                             "enum": ["signature", "behavior", "removed",
                                      "example", "concept", "doc"]},
                    "quote": {"type": "string"},
                    "probes": {"type": "array",
                               "items": {"type": "string"},
                               "minItems": 1, "maxItems": 3},
                },
                "required": ["text", "kind", "quote", "probes"]}}},
            "required": ["facts"],
        },
    },
}

_JSON_ARR = re.compile(r"\[.*\]", re.S)


# 8192, not 2048: thinking models spend the SAME budget on reasoning
# first (F-018 — thinking is a global LM Studio toggle we cannot turn
# off per-request). gemma-4-12b burned 2045/2048 tokens thinking and
# returned content="" on every source — which scored as "0 candidates".
def chat(base_url: str, model: str, system: str, user: str,
         max_tokens: int = 8192, temperature: float = 0.1,
         schema: dict | None = None) -> str:
    payload = {
        "model": model, "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [{"role": "system", "content": system},
                     {"role": "user", "content": user}]}
    if schema is not None:
        payload["response_format"] = schema
    body = json.dumps(payload).encode()
    req = urllib.request.Request(
        f"{base_url.rstrip('/')}/chat/completions", data=body,
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=600) as r:
        data = json.loads(r.read())
    ch = data["choices"][0]
    content = ch["message"].get("content") or ""
    if ch.get("finish_reason") == "length" and not content.strip():
        raise Truncated(       # F-009: a budget failure must never be
            f"{model}: {max_tokens}-token budget spent before any "
            f"answer (thinking model?) — raise max_tokens")
    return content


def parse_candidates(raw: str) -> list[dict]:
    raw = re.sub(r"<think>.*?</think>", "", raw, flags=re.S)
    # structured path: pure JSON object {"facts": [...]} (or bare array)
    try:
        obj = json.loads(raw.strip())
        if isinstance(obj, dict) and isinstance(obj.get("facts"), list):
            return [c for c in obj["facts"] if isinstance(c, dict)]
        if isinstance(obj, list):
            return [c for c in obj if isinstance(c, dict)]
    except json.JSONDecodeError:
        pass
    # prose fallback: first JSON array embedded in commentary
    m = _JSON_ARR.search(raw)
    if not m:
        return []
    try:
        arr = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    return [c for c in arr if isinstance(c, dict)]


class ModelExtractor:
    """Extraction via any OpenAI-compatible endpoint (LM Studio, the
    spawned llama-server, anything)."""

    def __init__(self, base_url: str, model: str):
        self.base_url = base_url
        self.model = model

    def __call__(self, section_text: str, source: str,
                 version: str) -> list[dict]:
        user = (f"Library: {source} (version {version}).\n"
                f"Source text:\n---\n{section_text}\n---\n"
                f"Extract the atomic facts as the JSON object.")
        try:
            raw = chat(self.base_url, self.model, EXTRACT_SYSTEM, user,
                       schema=CANDIDATES_SCHEMA)
        except urllib.error.HTTPError as e:
            if e.code != 400:
                raise
            # backend without structured output: plain prompt still works
            raw = chat(self.base_url, self.model, EXTRACT_SYSTEM, user)
        return parse_candidates(raw)


def sections(text: str, max_chars: int = 4000) -> list[str]:
    """Split source text at natural boundaries (headings, blank-line
    runs) — never inside a paragraph. Sections, not windows."""
    parts = re.split(r"\n(?=#{1,4} )|\n{3,}", text)
    out, buf = [], ""
    for p in parts:
        if len(buf) + len(p) < max_chars:
            buf += ("\n" + p if buf else p)
        else:
            if buf.strip():
                out.append(buf)
            buf = p
    if buf.strip():
        out.append(buf)
    return out
