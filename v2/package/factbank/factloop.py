"""VENDORED SNAPSHOT of NEW BANK/factbank/factbank/factloop.py (2026-07-13, post live-smoke).
The research tree is the lab; this package ships the evaluated system. Do not
edit here without syncing intent with the lab copy.

factloop.py - the PRODUCTION sealed loop. One class, the winning config.

This is the practical-implementation consolidation of what the experiments
validated (WORKS.md). The research harnesses stay untouched; this module
re-states their winning path as a single reusable object:

    draft (hard-capped search key)
      -> per-source version map (F-031)
      -> double-key retrieval, prompt-priority (hole 2)
      -> refine through a DELIVERY CHANNEL:
           native   facts arrive as a real tool_response  (tool-RL'd models)
           natural  facts arrive as prose                 (everything else)

The exact request shapes are the ones run_gemma.py measured -- same system
prompts, same k's, same query field, same show_draft=False. Departures from
the harness are PRODUCT decisions, each marked:

  * PASSTHROUGH: if retrieval returns nothing, the refine pass is skipped and
    the question is answered with ONE plain full-quality call. The dead-loop
    arm showed "asking twice" alone buys nothing, so an empty-handed second
    pass is pure cost. Controls mostly land here (and a passthrough cannot
    leak facts it never saw).
  * HISTORY: prior turns ride along on every pass. The research loop was
    single-turn; a server that drops history is broken as a product
    (TECHNICAL 8.4).
  * CLIENT PARAMS: temperature/max_tokens can be overridden per call --
    on the FINAL pass only. The draft cap is part of the architecture
    (a search key, not an answer) and is not client-tunable.

Works with HybridBank (the evaluated retrieval) or bank.Bank (BM25-only,
used by --mock and tests; also the no-embedding-model fallback).
"""

from dataclasses import dataclass, field

from .bank import detect_version, detect_version_map
from .loop import Truncated, build_refine_prompt_natural  # noqa: F401  (Truncated re-exported for serve.py)
from .native_tags import NATIVE_SYSTEM

PLAIN_SYSTEM = "You are a coding assistant. Answer the user's question."

CHANNELS = ("native", "natural")


@dataclass
class LoopAnswer:
    final: str
    draft: str
    facts: list                 # list[Fact]
    version: object             # dict | str | None -- what the filter used
    channel: str                # "native" | "natural" | "passthrough"
    passthrough: bool
    tokens: dict = field(default_factory=dict)   # per-pass completion_tokens


class FactLoop:
    """The sealed loop. Code decides to retrieve; the model never does."""

    def __init__(self, model, bank, channel: str = "native",
                 k_prompt: int = 5, k_draft: int = 3):
        if channel not in CHANNELS:
            raise ValueError(f"channel must be one of {CHANNELS}")
        self.model = model
        self.bank = bank
        self.channel = channel
        self.k_prompt = k_prompt
        self.k_draft = k_draft

    # ------------------------------------------------------------- helpers
    def _sources(self) -> list[str]:
        # HybridBank exposes .sources; bank.Bank does not (same getattr
        # fallback loop.py uses, but derived so the per-source version map
        # still works on a BM25-only bank).
        s = getattr(self.bank, "sources", None)
        if s:
            return list(s)
        return sorted({f.source for f in getattr(self.bank, "facts", [])})

    @staticmethod
    def _with_suffix(system: str, system_suffix: str | None) -> str:
        # Client system messages are honored (8.4) but never REPLACE the
        # measured channel prompt -- they append to it.
        if system_suffix and system_suffix.strip():
            return f"{system}\n\n# Additional instructions from the client\n{system_suffix.strip()}"
        return system

    # ---------------------------------------------------------------- main
    def answer(self, question: str,
               history: list[dict] | None = None,
               system_suffix: str | None = None,
               max_tokens: int | None = None,
               temperature: float | None = None) -> LoopAnswer:
        """Run the full sealed loop for one user question.

        Raises Truncated if the FINAL pass blows its token budget (F-009:
        surface it, never return an empty answer as if it were one).
        """
        tokens: dict = {}
        history = history or []

        # Pass 1: draft = search key. Hard-capped inside the model object;
        # a cut-off draft is the intended shape (reasoning trace fallback).
        draft = self.model.draft(NATIVE_SYSTEM, question, history=history)
        tokens["draft"] = self.model.last_call.get("completion_tokens")

        # Version constraints: per-source map first (F-031), legacy single
        # detection as fallback. Never lets one library's version delete
        # another library's facts.
        version = detect_version_map(question + "\n" + draft,
                                     self._sources()) \
            or detect_version(question) or detect_version(draft)

        # Retrieval: double key, prompt-priority, retrieve-first-
        # filter-second with structural fail-open (all inside the bank).
        facts = self.bank.double_key_search(
            question, draft,
            k_prompt=self.k_prompt, k_draft=self.k_draft,
            version_filter=version)

        # PASSTHROUGH (product decision): bank has nothing -> behave like
        # the plain model, one full-quality call, no scaffolding to leak.
        if not facts:
            final = self.model.complete_plain(
                self._with_suffix(PLAIN_SYSTEM, system_suffix),
                question, thinking=True, history=history,
                max_tokens=max_tokens, temperature=temperature)
            tokens["final"] = self.model.last_call.get("completion_tokens")
            return LoopAnswer(final=final, draft=draft, facts=[],
                              version=version, channel="passthrough",
                              passthrough=True, tokens=tokens)

        # Pass 3: refine, facts delivered through the configured channel.
        if self.channel == "native":
            final = self.model.complete_with_facts(
                self._with_suffix(NATIVE_SYSTEM, system_suffix),
                question, facts, query=question,
                thinking=True, history=history,
                max_tokens=max_tokens, temperature=temperature)
        else:  # natural
            user = build_refine_prompt_natural(question, draft, facts,
                                               show_draft=False)
            final = self.model.complete_plain(
                self._with_suffix(PLAIN_SYSTEM, system_suffix),
                user, thinking=True, history=history,
                max_tokens=max_tokens, temperature=temperature)
        tokens["final"] = self.model.last_call.get("completion_tokens")

        return LoopAnswer(final=final, draft=draft, facts=facts,
                          version=version, channel=self.channel,
                          passthrough=False, tokens=tokens)


# ------------------------------------------------------------------- mocks
class MockNativeModel:
    """Deterministic stand-in speaking NativeToolModel's full interface.

    No GPU, no network. Answers are labeled by the path taken so tests can
    assert WHICH pass produced them; call kwargs are recorded so tests can
    assert what a client override actually reached the backend as.
    """

    def __init__(self, draft_text: str | None = None):
        # Default: the draft ECHOES the question, so retrieval hit/miss
        # follows the question alone and tests stay deterministic. A fixed
        # draft_text would feed the draft key the same libraries on every
        # question -- which is real HyDE behavior, but it makes an
        # off-topic question retrieve facts and no test can ever miss.
        self.draft_text = draft_text
        self.last_call: dict = {}
        self.calls: list[dict] = []

    def _record(self, kind: str, **kw):
        self.calls.append({"kind": kind, **kw})
        self.last_call = {"finish_reason": "stop", "completion_tokens": 42,
                          "reasoning_chars": 0}

    def draft(self, system, question, history=None):
        self._record("draft", question=question,
                     history_len=len(history or []))
        return self.draft_text or f"Rough attempt: {question}"

    def complete_plain(self, system, question, thinking=True, history=None,
                       max_tokens=None, temperature=None):
        self._record("plain", system=system, question=question,
                     history_len=len(history or []),
                     max_tokens=max_tokens, temperature=temperature)
        return f"[PLAIN] {question[:120]}"

    def complete_with_facts(self, system, question, facts, query,
                            thinking=True, history=None,
                            max_tokens=None, temperature=None):
        self._record("native", system=system, question=question,
                     fact_ids=[f.id for f in facts],
                     history_len=len(history or []),
                     max_tokens=max_tokens, temperature=temperature)
        return f"[NATIVE facts={','.join(f.id for f in facts)}] answer"


class TruncatingMockModel(MockNativeModel):
    """Every FINAL pass blows the budget (F-009). Draft still succeeds."""

    def complete_plain(self, *a, **kw):
        super().complete_plain(*a, **kw)
        self.last_call = {"finish_reason": "length",
                          "completion_tokens": 24576}
        raise Truncated("no answer written (finish='length', tokens=24576)")

    def complete_with_facts(self, *a, **kw):
        super().complete_with_facts(*a, **kw)
        self.last_call = {"finish_reason": "length",
                          "completion_tokens": 24576}
        raise Truncated("no answer written (finish='length', tokens=24576)")
