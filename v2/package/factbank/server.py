"""VENDORED SNAPSHOT of NEW BANK/factbank/factbank/serve.py (2026-07-13, post live-smoke).
The research tree is the lab; this package ships the evaluated system. Do not
edit here without syncing intent with the lab copy.

serve.py - The sealed loop as one hardened OpenAI-compatible endpoint.

From the OUTSIDE: a single, normal chat endpoint. Any OpenAI client talks to
it like a plain model. On the INSIDE every request runs the validated loop
(factloop.FactLoop): capped draft -> per-source version map -> double-key
hybrid retrieval -> refine through the native tool channel (or prose).

v2, practical-implementation chapter (2026-07-12). The v1 research skeleton
was explicitly not shippable (TECHNICAL 8.4). What each complaint became:

    bind 0.0.0.0, no auth        -> default 127.0.0.1; --api-key (Bearer,
                                    constant-time compare)
    no body/rate limits          -> --max-body (413 over it); --concurrency
                                    semaphore, 503 when saturated
    history/system discarded     -> full history rides every pass; client
                                    system text APPENDS to the channel prompt
    client params ignored        -> temperature honored; max_tokens honored
                                    up to the server ceiling (draft cap stays
                                    fixed: it is architecture, not preference)
    stream=true returned JSON    -> real SSE chunks + [DONE]
    exceptions leaked to client  -> generic JSON errors; detail goes to the
                                    server log only. Truncated is its own 502
                                    ("budget, not reasoning" -- F-009)
    <user_prompt> injectable     -> no invented tags anywhere: the native
                                    channel carries facts in a tool_response;
                                    user text is never wrapped in tags
    (new) JIT-load eviction      -> UpstreamGuard: chat requests are only
                                    ever sent for ids the upstream reports
                                    LOADED (read-only check). Unlisted ->
                                    503, never forwarded. The repo's hard
                                    rule, productized.

Dropped from v1: --gguf self-spawn and embedded-bank reading. Packaging is
its own phase (TECHNICAL 8.2) and must ship the EVALUATED system, not grow
here ad hoc.

Modes:
  --upstream http://127.0.0.1:1234/v1 --model <loaded-id>   real backend
  --mock                                                    tests, no GPU

Run:
  python serve.py --upstream http://127.0.0.1:1234/v1 \
                  --model google/gemma-4-12b-qat --bank facts_v2.jsonl
Then point any OpenAI client at http://127.0.0.1:8000/v1 (model "factbank").
"""

import argparse
import hmac
import json
import os
import sys
import threading
import time
import traceback
import urllib.error
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .bank import Bank
from .factloop import FactLoop, MockNativeModel, Truncated
from .native_tags import NativeToolModel

STATE: dict = {}


# ----------------------------------------------------------------- guard
class GuardError(RuntimeError):
    """Refusing to forward: the model is not confirmed loaded upstream."""


class UpstreamGuard:
    """Never send a chat request for a model id the upstream has not loaded.

    Requesting an unloaded id makes LM Studio JIT-load it, which EVICTS the
    model the user loaded (repo hard rule #1). So before any forward we
    consult a read-only listing and fail CLOSED: unreachable upstream or an
    unlisted id means 503, never a forward.

    LM Studio's /api/v0/models reports a true per-model "state" field; when
    that endpoint exists we trust only state=="loaded". Plain /v1/models is
    the fallback, where "listed" is the best signal available (on backends
    that list downloaded-but-unloaded models this is weaker -- documented,
    and still strictly safer than not checking).
    """

    def __init__(self, base_url: str, ttl: float = 15.0):
        self.base_url = base_url.rstrip("/")
        self.ttl = ttl
        self._cache: tuple[float, set] | None = None
        self._lock = threading.Lock()

    def _get(self, url: str) -> dict:
        with urllib.request.urlopen(
                urllib.request.Request(url), timeout=10) as r:
            return json.loads(r.read())

    def loaded_ids(self) -> set:
        with self._lock:
            now = time.time()
            if self._cache and now - self._cache[0] < self.ttl:
                return self._cache[1]
            root = self.base_url[:-3] if self.base_url.endswith("/v1") \
                else self.base_url
            try:  # LM Studio native API: has real load state
                data = self._get(f"{root}/api/v0/models")
                ids = {m["id"] for m in data.get("data", [])
                       if m.get("state") == "loaded"}
            except Exception:
                data = self._get(f"{self.base_url}/models")   # fallback
                ids = {m.get("id") for m in data.get("data", [])}
            self._cache = (now, ids)
            return ids

    def require(self, model_id: str):
        try:
            ids = self.loaded_ids()
        except Exception as e:
            raise GuardError(f"upstream model listing unreachable "
                             f"({e.__class__.__name__}); refusing to forward "
                             f"unchecked") from None
        if model_id not in ids:
            raise GuardError(
                f"model {model_id!r} is not loaded in the upstream backend. "
                f"Load it there first -- this server never requests unloaded "
                f"ids (a JIT load would evict the loaded model).")


# ------------------------------------------------------------------ http
class ClientError(Exception):
    def __init__(self, status: int, code: str, message: str):
        super().__init__(message)
        self.status, self.code = status, code


def _extract(req: dict) -> tuple[str, list, str, dict]:
    """OpenAI messages -> (question, history, client_system, options).

    Last user message is the question; earlier user/assistant turns are
    history; system text is collected to APPEND to the channel prompt.
    Multimodal text parts are joined; non-text parts are refused.
    """
    msgs = req.get("messages")
    if not isinstance(msgs, list) or not msgs:
        raise ClientError(400, "invalid_request", "messages must be a "
                          "non-empty list")

    def text_of(m) -> str:
        c = m.get("content")
        if isinstance(c, str):
            return c
        if isinstance(c, list):
            parts = []
            for p in c:
                if isinstance(p, dict) and p.get("type") == "text":
                    parts.append(p.get("text", ""))
                else:
                    raise ClientError(400, "unsupported",
                                      "only text content is supported")
            return "\n".join(parts)
        raise ClientError(400, "invalid_request",
                          "message content must be a string or text parts")

    system_texts, convo = [], []
    for m in msgs:
        role = m.get("role")
        if role == "system":
            system_texts.append(text_of(m))
        elif role in ("user", "assistant"):
            convo.append({"role": role, "content": text_of(m)})
        # tool/function/etc. from the client are ignored: the loop owns the
        # tool channel (that is the whole point of the sealed design)

    if not convo or convo[-1]["role"] != "user":
        raise ClientError(400, "invalid_request",
                          "the last non-system message must be a user turn")
    question, history = convo[-1]["content"], convo[:-1]
    if not question.strip():
        raise ClientError(400, "invalid_request", "empty user message")

    opts = {}
    if req.get("temperature") is not None:
        try:
            opts["temperature"] = min(2.0, max(0.0,
                                               float(req["temperature"])))
        except (TypeError, ValueError):
            raise ClientError(400, "invalid_request",
                              "temperature must be a number") from None
    if req.get("max_tokens") is not None:
        try:
            mt = int(req["max_tokens"])
        except (TypeError, ValueError):
            raise ClientError(400, "invalid_request",
                              "max_tokens must be an integer") from None
        if mt <= 0:
            raise ClientError(400, "invalid_request",
                              "max_tokens must be positive")
        # the server ceiling exists so one client cannot buy an unbounded
        # reasoning spiral on a shared GPU (F-025)
        opts["max_tokens"] = min(mt, STATE["max_tokens"])
    opts["stream"] = bool(req.get("stream"))
    return question, history, "\n\n".join(t for t in system_texts if t), opts


def _log_run(entry: dict):
    if not STATE.get("log_path"):
        return
    entry["ts"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    with STATE["log_lock"]:
        with open(STATE["log_path"], "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry, ensure_ascii=False,
                                default=str) + "\n")


def _update_worker(cfg: dict, st: list):
    """Background auto-update: scan -> gates -> apply (snapshot/rollback)
    -> hot-reload the serving bank. Appends progress lines to st."""
    try:
        from .extract import ModelExtractor
        from .watch import apply, scan, write_pending
        ex = ModelExtractor(cfg["base_url"], cfg["model"])
        if STATE.get("guard"):
            STATE["guard"].require(cfg["model"])   # no-JIT-load rule on the update lane too
        props = scan(cfg["bank"], ex, log=lambda m: st.append(str(m)))
        if not props:
            st.append("DONE — everything is up to date")
            return
        write_pending(cfg["bank"], props)
        if not apply(cfg["bank"], props, log=lambda m: st.append(str(m))):
            st.append("DONE — rolled back, bank unchanged")
            return
        try:                                   # hot-reload the live bank
            loop = STATE["loop"]
            if type(loop.bank).__name__ == "HybridBank":
                from .lmstudio_embed import HybridBank
                loop.bank = HybridBank.from_jsonl_cached(
                    cfg["bank"], base_url=cfg["embed_base"],
                    model=cfg["embed_model"])
            else:
                loop.bank = Bank.from_jsonl(cfg["bank"])
            st.append(f"DONE — {len(props)} fact(s) applied and live "
                      f"(bank now {len(loop.bank.facts)} facts)")
        except Exception as e:
            st.append(f"applied, but hot-reload failed "
                      f"({type(e).__name__}) — restart serve to load "
                      f"the new facts")
    except Exception as e:
        st.append(f"update failed: {type(e).__name__}: {e}")


ADMIN_HTML = """<!doctype html><meta charset="utf-8">
<title>factbank</title>
<style>body{font-family:system-ui;margin:2rem auto;max-width:44rem}
button{font-size:1.1rem;padding:.5rem 1.4rem}pre{background:#f4f4f4;
padding:1rem;white-space:pre-wrap}</style>
<h1>factbank</h1><p>%(facts)d facts · channel %(channel)s</p>
<button onclick="fetch('/admin/update',{method:'POST',headers:{'X-FactBank-Admin':'1'}}).then(r=>r.text()).then(t=>document.getElementById('s').textContent=t).catch(e=>document.getElementById('s').textContent=e)">Update facts now</button>
<h2>last update</h2><pre id="s">%(status)s</pre>
<p><small>CSRF-guarded: the update needs the X-FactBank-Admin header (this page sends it);
a cross-site form cannot.</small></p>"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *a):  # stdlib access log off; we write our own
        pass

    # ------------------------------------------------------------ replies
    def _json(self, status: int, obj: dict):
        body = json.dumps(obj, ensure_ascii=False).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status: int, code: str, message: str):
        self._json(status, {"error": {"message": message, "type": code,
                                      "code": code}})

    # -------------------------------------------------------------- auth
    def _authed(self) -> bool:
        key = STATE.get("api_key")
        if not key:
            return True
        got = self.headers.get("Authorization", "")
        return got.startswith("Bearer ") and \
            hmac.compare_digest(got[7:], key)

    # --------------------------------------------------------------- GET
    def _loopback(self) -> bool:
        return self.client_address[0] in ("127.0.0.1", "::1")

    def _admin_ok(self) -> bool:
        """Guard state-changing admin endpoints. Requires: loopback + bearer
        (honors --api-key; open only when no key is set, like the chat path) +
        a custom header (CSRF: a browser cannot set X-FactBank-Admin cross-origin
        without a CORS preflight) + no foreign Origin."""
        if not self._loopback() or not self._authed():
            return False
        origin = self.headers.get("Origin", "")
        if origin and not origin.startswith((
                "http://127.0.0.1", "http://localhost",
                "https://127.0.0.1", "https://localhost")):
            return False
        return self.headers.get("X-FactBank-Admin") == "1"

    def do_GET(self):
        if self.path == "/admin" and self._loopback():
            body = (ADMIN_HTML % {
                "facts": len(STATE["loop"].bank.facts),
                "channel": STATE["loop"].channel,
                "status": "\n".join(str(x) for x in STATE.get(
                    "update_status", ["no update has run yet"])[-20:]),
            }).encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
            return
        if self.path in ("/health", "/v1/health"):
            return self._json(200, {"status": "ok"})   # liveness only; no bank details
        if self.path == "/v1/models":
            if not self._authed():
                return self._error(401, "unauthorized", "bad or missing "
                                   "Bearer token")
            return self._json(200, {"object": "list", "data": [{
                "id": STATE["served_name"], "object": "model",
                "owned_by": "factbank",
            }]})
        self._error(404, "not_found", "unknown path")

    # -------------------------------------------------------------- POST
    def do_POST(self):
        if self.path == "/admin/update":
            if not self._admin_ok():
                return self._error(403, "forbidden", "admin update requires loopback, "
                                   "bearer auth (if --api-key set), and the "
                                   "X-FactBank-Admin header")
            self._update_command(True)
            return
        if self.path not in ("/v1/chat/completions", "/chat/completions"):
            return self._error(404, "not_found", "unknown path")
        if not self._authed():
            return self._error(401, "unauthorized", "bad or missing Bearer "
                               "token")
        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            length = 0
        if length <= 0:
            return self._error(411, "length_required",
                               "Content-Length required")
        if length > STATE["max_body"]:
            return self._error(413, "payload_too_large",
                               f"body over {STATE['max_body']} bytes")
        try:
            req = json.loads(self.rfile.read(length))
        except (json.JSONDecodeError, UnicodeDecodeError):
            return self._error(400, "invalid_request", "body is not JSON")

        t0 = time.time()
        try:
            question, history, client_system, opts = _extract(req)
        except ClientError as e:
            return self._error(e.status, e.code, str(e))

        # clerk mode: "update your facts" is a COMMAND code intercepts —
        # the model never decides this (PLAN P4b)
        # Update authority is SEPARATE from chat: a chat message mutates the bank
        # only when the operator opts in with --allow-chat-update. Off by default,
        # so a normal chat user cannot trigger an update (use /admin/update).
        cmd = question.strip().lower().rstrip("!. ")
        if STATE.get("allow_chat_update") and cmd in (
                "/update", "update", "update facts", "update your facts",
                "update the facts", "update status"):
            return self._update_command(cmd != "update status")

        # requested model: we serve exactly one; mismatches are accepted but
        # logged (chat UIs send all sorts of ids), never forwarded upstream
        asked = req.get("model")
        if asked and asked not in (STATE["served_name"],
                                   STATE["upstream_model"]):
            if STATE.get("strict_model"):
                return self._error(400, "model_not_served",
                                   f"this endpoint serves {STATE['served_name']!r}, "
                                   f"not {asked!r}")
            _log_run({"kind": "model_mismatch", "asked": asked})

        # the no-JIT-load rule: confirm the upstream id is loaded, or refuse
        if STATE.get("guard"):
            try:
                STATE["guard"].require(STATE["upstream_model"])
            except GuardError as e:
                return self._error(503, "model_not_loaded", str(e))

        if not STATE["sem"].acquire(timeout=STATE["sem_timeout"]):
            return self._error(503, "overloaded",
                               "server is at max concurrency; retry")
        try:
            res = STATE["loop"].answer(
                question, history=history,
                system_suffix=client_system or None,
                max_tokens=opts.get("max_tokens"),
                temperature=opts.get("temperature"))
        except Truncated as e:
            _log_run({"kind": "truncated", "question": question,
                      "error": str(e), "secs": round(time.time() - t0, 2)})
            return self._error(502, "budget_exhausted",
                               "the model spent its whole token budget "
                               "reasoning and wrote no answer; retry, or "
                               "raise max_tokens")
        except GuardError as e:
            return self._error(503, "model_not_loaded", str(e))
        except Exception:
            print(f"[serve] internal error:\n{traceback.format_exc()}",
                  file=sys.stderr)
            _log_run({"kind": "internal_error", "question": question,
                      "trace": traceback.format_exc()[-1500:]})
            return self._error(500, "internal_error", "internal error")
        finally:
            STATE["sem"].release()

        with STATE["id_lock"]:
            STATE["req_n"] += 1
            rid = f"chatcmpl-factbank-{STATE['req_n']}"
        extra = {"channel": res.channel, "passthrough": res.passthrough,
                 "facts_used": [f.id for f in res.facts],
                 "version": res.version, "tokens": res.tokens}
        _log_run({"kind": "ok", "id": rid, "question": question,
                  "draft": res.draft, "answer": res.final, **extra,
                  "secs": round(time.time() - t0, 2)})

        if opts["stream"]:
            return self._stream(rid, res.final, extra)
        total = sum(v for v in res.tokens.values() if isinstance(v, int))
        self._json(200, {
            "id": rid, "object": "chat.completion",
            "created": int(time.time()), "model": STATE["served_name"],
            "choices": [{"index": 0,
                         "message": {"role": "assistant",
                                     "content": res.final},
                         "finish_reason": "stop"}],
            "usage": {"completion_tokens": total},
            "factbank": extra,      # observability; harmless extra field
        })

    # -------------------------------------------------- clerk update flow
    def _update_command(self, start: bool):
        st = STATE.setdefault("update_status", ["no update has run yet"])
        cfg = STATE.get("update_cfg")
        if start and cfg is None:
            st = ["updates are not available in mock mode"]
        elif start:
            th = STATE.get("update_thread")
            if th and th.is_alive():
                st.append("(an update is already running)")
            else:
                st = STATE["update_status"] = ["update started..."]
                STATE["update_thread"] = t = threading.Thread(
                    target=_update_worker, args=(cfg, st), daemon=True)
                t.start()
        text = "\n".join(str(x) for x in STATE["update_status"][-14:])
        with STATE["id_lock"]:
            STATE["req_n"] += 1
            rid = f"chatcmpl-factbank-{STATE['req_n']}"
        self._json(200, {
            "id": rid, "object": "chat.completion",
            "created": int(time.time()), "model": STATE["served_name"],
            "choices": [{"index": 0,
                         "message": {"role": "assistant", "content": text},
                         "finish_reason": "stop"}],
            "usage": {"completion_tokens": 0},
            "factbank": {"channel": "control", "passthrough": True,
                         "facts_used": [], "version": None, "tokens": {}}})

    # ---------------------------------------------------------- streaming
    def _stream(self, rid: str, text: str, extra: dict):
        """SSE. The loop is two upstream passes, so tokens cannot stream
        live end-to-end; the completed answer is chunked instead -- every
        OpenAI streaming client renders it correctly."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "close")
        self.end_headers()

        def send(obj):
            self.wfile.write(f"data: {json.dumps(obj, ensure_ascii=False)}"
                             f"\n\n".encode())

        base = {"id": rid, "object": "chat.completion.chunk",
                "created": int(time.time()), "model": STATE["served_name"]}
        send({**base, "choices": [{"index": 0, "finish_reason": None,
                                   "delta": {"role": "assistant",
                                             "content": ""}}]})
        for i in range(0, len(text), 512):
            send({**base, "choices": [{"index": 0, "finish_reason": None,
                                       "delta": {"content":
                                                 text[i:i + 512]}}]})
        send({**base, "factbank": extra,
              "choices": [{"index": 0, "delta": {},
                           "finish_reason": "stop"}]})
        self.wfile.write(b"data: [DONE]\n\n")


# ------------------------------------------------------------------ main
def build_state(args) -> dict:
    """Everything the handler needs. Separated from main() so tests can
    build a fully wired server around a mock with no CLI and no network."""
    spawned = []
    if args.mock:
        model, guard = MockNativeModel(), None
        bank = Bank.from_jsonl(args.bank)
    elif getattr(args, "gguf", None):
        # self-contained mode: our own llama-server, no LM Studio/Ollama
        import os as _os

        from .spawn import LlamaServer
        chat = LlamaServer(args.gguf, bin_path=args.llama_bin,
                           ctx=args.llama_ctx, ngl=args.llama_ngl,
                           alias="factbank-local",
                           log=None if args.no_log else args.log + ".llama")
        spawned.append(chat)
        guard = UpstreamGuard(chat.base_url)
        if args.embed_gguf:
            emb = LlamaServer(args.embed_gguf, bin_path=args.llama_bin,
                              ctx=2048, ngl=args.llama_ngl, embedding=True,
                              alias="factbank-embed")
            spawned.append(emb)
            from .lmstudio_embed import HybridBank
            bank = HybridBank.from_jsonl_cached(
                args.bank, base_url=emb.base_url,
                model=_os.path.basename(args.embed_gguf))
        elif args.bm25_only:
            bank = Bank.from_jsonl(args.bank)
        else:
            sys.exit("--gguf mode needs --embed-gguf (hybrid retrieval, "
                     "the evaluated setup) or --bm25-only (weaker, "
                     "F-005/F-012)")
        args.model = chat.alias
        model = NativeToolModel(chat.base_url, model=chat.alias,
                                temperature=args.temperature,
                                max_tokens=args.max_tokens,
                                draft_max_tokens=args.draft_max_tokens)
    else:
        guard = UpstreamGuard(args.upstream)
        if args.bm25_only:
            bank = Bank.from_jsonl(args.bank)
        else:
            # embedding the bank sends /v1/embeddings requests, so the
            # embedding model gets the same no-JIT-load check as chat
            guard.require(args.embed_model)   # queries encode per request
            from .lmstudio_embed import HybridBank
            bank = HybridBank.from_jsonl_cached(
                args.bank, base_url=args.upstream, model=args.embed_model)
        model = NativeToolModel(args.upstream, model=args.model,
                                temperature=args.temperature,
                                max_tokens=args.max_tokens,
                                draft_max_tokens=args.draft_max_tokens)
        try:
            guard.require(args.model)
        except GuardError as e:
            print(f"[serve] WARNING: {e}\n[serve] serving anyway; requests "
                  f"return 503 until it is loaded", file=sys.stderr)

    if args.mock:
        update_cfg = None
    elif getattr(args, "gguf", None):
        # self-contained: the served model doubles as extractor; embed
        # endpoint is the spawned embedding server if any
        emb_srv = next((s for s in spawned if s.alias == "factbank-embed"),
                       None)
        update_cfg = {"bank": args.bank, "base_url": model.base_url,
                      "model": args.model,
                      "embed_base": emb_srv.base_url if emb_srv else None,
                      "embed_model": os.path.basename(args.embed_gguf)
                      if args.embed_gguf else None}
    else:
        # each model extracts with itself (owner rule; F-036) unless a
        # different extractor is explicitly configured
        update_cfg = {"bank": args.bank, "base_url": args.upstream,
                      "model": args.extract_model or args.model,
                      "embed_base": args.upstream,
                      "embed_model": args.embed_model}

    return {
        "loop": FactLoop(model, bank, channel=args.channel,
                         k_prompt=args.k_prompt, k_draft=args.k_draft),
        "spawned": spawned,
        "update_cfg": update_cfg,
        "guard": guard,
        "allow_chat_update": getattr(args, "allow_chat_update", False),
        "strict_model": getattr(args, "strict_model", False),
        "upstream_model": getattr(args, "model", "mock"),
        "served_name": args.served_name,
        "api_key": args.api_key,
        "max_body": args.max_body,
        "max_tokens": args.max_tokens,
        "sem": threading.Semaphore(args.concurrency),
        "sem_timeout": args.sem_timeout,
        "log_path": None if args.no_log else args.log,
        "log_lock": threading.Lock(),
        "id_lock": threading.Lock(),
        "req_n": 0,
    }


def add_serve_args(ap):
    """Serve flags, shared by the standalone entry and the factbank CLI."""
    ap.add_argument("--host", default="127.0.0.1",
                    help="bind address (default localhost-only)")
    ap.add_argument("--port", type=int, default=8000)
    ap.add_argument("--upstream", default="http://127.0.0.1:1234/v1")
    ap.add_argument("--model", default="google/gemma-4-12b-qat",
                    help="upstream model id -- must ALREADY be loaded")
    ap.add_argument("--bank", default="facts_v2.jsonl")
    ap.add_argument("--channel", choices=["native", "natural"],
                    default="native",
                    help="native for tool-RL'd models (gemma-class), "
                         "natural prose for everything else (WORKS.md)")
    ap.add_argument("--served-name", default="factbank")
    ap.add_argument("--api-key", default=None,
                    help="require this Bearer token (recommended off "
                         "localhost)")
    ap.add_argument("--k-prompt", type=int, default=5)
    ap.add_argument("--k-draft", type=int, default=3)
    ap.add_argument("--temperature", type=float, default=0.2)
    ap.add_argument("--max-tokens", type=int, default=16384,
                    help="refine ceiling; also caps client max_tokens")
    ap.add_argument("--draft-max-tokens", type=int, default=512)
    ap.add_argument("--concurrency", type=int, default=2)
    ap.add_argument("--sem-timeout", type=float, default=120.0)
    ap.add_argument("--max-body", type=int, default=1_048_576)
    ap.add_argument("--log", default="serve_runs.jsonl",
                    help="JSONL run log (draft, facts, answer) -- the ship "
                         "checklist's failure-mining input")
    ap.add_argument("--no-log", action="store_true")
    ap.add_argument("--embed-model",
                    default="text-embedding-nomic-embed-text-v1.5")
    ap.add_argument("--bm25-only", action="store_true",
                    help="skip embeddings (weaker retrieval: F-005/F-012)")
    ap.add_argument("--gguf", default=None,
                    help="self-contained mode: spawn a bundled "
                         "llama-server on this GGUF (no LM Studio needed)")
    ap.add_argument("--embed-gguf", default=None,
                    help="embedding-model GGUF for --gguf mode (hybrid "
                         "retrieval, the evaluated setup)")
    ap.add_argument("--llama-bin", default=None,
                    help="path to llama-server (default: PATH, then "
                         "~/tools/llama-cpp/)")
    ap.add_argument("--llama-ctx", type=int, default=16384)
    ap.add_argument("--llama-ngl", type=int, default=99)
    ap.add_argument("--extract-model", default=None,
                    help="model for in-chat/admin fact updates. Default: "
                         "the served model itself — owner rule 2026-07-13 "
                         "'each model extracts with itself' (F-036: the "
                         "served 12B beat a dedicated e2b on every "
                         "quality axis). Set this only to delegate "
                         "extraction to a different loaded model.")
    ap.add_argument("--mock", action="store_true")
    ap.add_argument("--allow-chat-update", action="store_true",
                    help="allow a chat message ('update your facts') to trigger a bank "
                         "update. OFF by default: update authority is separate from chat, "
                         "so a normal chat user cannot mutate the bank (use /admin/update).")
    ap.add_argument("--strict-model", action="store_true",
                    help="reject requests whose 'model' is neither the served nor the "
                         "upstream id (default: log and continue, for lenient chat UIs).")
    return ap


def run_serve(args):
    STATE.update(build_state(args))
    try:
        _run_serve_inner(args)
    finally:
        for s in STATE.get("spawned") or []:   # VRAM rule: never squat
            s.stop()


def _run_serve_inner(args):
    srv = ThreadingHTTPServer((args.host, args.port), Handler)
    srv.daemon_threads = True
    loop = STATE["loop"]
    print(f"factbank serving on http://{args.host}:{args.port}/v1  "
          f"model={args.served_name!r}  channel={loop.channel}  "
          f"bank={len(loop.bank.facts)} facts  "
          f"upstream={'MOCK' if args.mock else (getattr(args, 'gguf', None) or args.upstream)}")
    srv.serve_forever()


def main():
    ap = argparse.ArgumentParser(
        description="factbank sealed-loop server (winning stage-0 config)")
    add_serve_args(ap)
    run_serve(ap.parse_args())


if __name__ == "__main__":
    main()
