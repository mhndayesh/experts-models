"""VENDORED SNAPSHOT of NEW BANK/factbank/factbank/loop.py (2026-07-13, post live-smoke).
The research tree is the lab; this package ships the evaluated system. Do not
edit here without syncing intent with the lab copy.


loop.py - The code-driven 3-pass loop.

The model never decides to retrieve. This code runs:
  pass 1 (draft) -> double-key bank lookup -> pass 3 (refine with tags).

Model interface is OpenAI-compatible chat completions, so it works with
vLLM, llama.cpp server, LM Studio, Ollama (openai endpoint), or any API.
A MockModel is included so the pipeline is testable without a GPU.
"""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass
from .bank import Bank, Fact, detect_version, detect_version_map


SYSTEM_PROMPT = """You are a coding assistant.
When the user message contains <user_prompt>, <draft>, and <facts> tags:
- <user_prompt> is the actual question. Answer it.
- <draft> is your earlier rough attempt. It may contain mistakes.
- <facts> are verified ground truth from official documentation.
Rules:
- If a fact contradicts the draft on anything checkable (function name,
  signature, parameter, version behavior), the fact wins. Rewrite that part.
- If a fact is irrelevant to this question, ignore it and do not force it in.
- Do not copy facts verbatim as the answer. Adapt them to the user's problem.
- Never invent APIs. If you are unsure and no fact covers it, say so."""


# ---------------- model backends ----------------

def strip_think(text: str) -> str:
    """Remove <think>...</think> blocks so reasoning traces never pollute
    the draft search key or the shipped final answer.

    An UNCLOSED <think> (budget cut the model off mid-thought) used to leak
    the whole trace through untouched (audit find, 2026-07-12). Now anything
    from a dangling <think> to end-of-text is stripped too."""
    import re as _re
    text = _re.sub(r"<think>.*?</think>", "", text, flags=_re.S)
    text = _re.sub(r"<think>.*\Z", "", text, flags=_re.S)   # unclosed tail
    return text.strip()


class Truncated(RuntimeError):
    """The backend cut the model off before it wrote an answer.

    Reasoning models spend max_tokens on reasoning FIRST, then the answer.
    Blow the budget mid-thought and backends that separate reasoning (e.g.
    LM Studio's reasoning_content) return content="" with
    finish_reason="length" -- a silent empty answer, no error.

    Never swallow this. An empty string flows through the loop and scores as
    a reasoning failure when it is really a budget failure. (FINDINGS F-009)
    """


class OpenAICompatModel:
    """Talks to any OpenAI-compatible /v1/chat/completions endpoint.

    thinking=True/False uses BOTH control paths for Qwen3-class models:
      1. chat_template_kwargs {"enable_thinking": ...} (vLLM, llama.cpp)
      2. the /think and /no_think soft-switch tags appended to the user turn
    Backends that support neither simply ignore them, so this is safe
    for any model."""

    def __init__(self, base_url: str, model: str, api_key: str = "none",
                 temperature: float = 0.2, max_tokens: int = 4096,
                 soft_switch: bool = True):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.api_key = api_key
        self.temperature = temperature
        self.max_tokens = max_tokens
        # soft_switch: append the Qwen3 /think and /no_think control tokens.
        #
        # TURN THIS OFF on Qwen3.5+ / Qwen3.6. Those models DROPPED the soft
        # switch, so "/no_think" is no longer a control token -- it is literal
        # garbage text glued onto the user's question, silently taxing every
        # prompt. Measured on qwen3.6-35b-a3b: no control path disables thinking
        # (enable_thinking=False produced MORE reasoning than the default), so
        # the tag buys nothing and costs prompt quality. (FINDINGS F-018)
        self.soft_switch = soft_switch
        self.last_call: dict = {}

    def complete(self, system: str, user: str,
                 thinking: bool = False) -> str:
        if self.soft_switch:
            user = f"{user} " + ("/think" if thinking else "/no_think")
        body = json.dumps({
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens,
            "chat_template_kwargs": {"enable_thinking": thinking},
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        }).encode()
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=body,
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {self.api_key}"},
        )
        try:
            with urllib.request.urlopen(req, timeout=600) as resp:
                data = json.loads(resp.read())
        except urllib.error.HTTPError as e:
            # urllib throws the server's explanation away and leaves you staring
            # at "HTTP Error 400: Bad Request". The reason is in the BODY. Read it.
            detail = e.read().decode("utf-8", "replace")[:500]
            raise RuntimeError(
                f"backend rejected the request (HTTP {e.code}) "
                f"model={self.model!r}: {detail}") from None
        choice = data["choices"][0]
        msg = choice["message"]
        # some backends put reasoning in a separate field already
        content = msg.get("content") or ""
        self.last_call = {
            "thinking": thinking,
            "finish_reason": choice.get("finish_reason"),
            "completion_tokens": data.get("usage", {}).get("completion_tokens"),
        }
        if choice.get("finish_reason") == "length" or not content.strip():
            raise Truncated(
                f"no answer written (finish_reason="
                f"{choice.get('finish_reason')!r}, thinking={thinking}, "
                f"completion_tokens={self.last_call['completion_tokens']}). "
                f"Raise max_tokens (currently {self.max_tokens}).")
        return content


class MockModel:
    """Deterministic stand-in for pipeline tests. No GPU, no network."""

    def complete(self, system: str, user: str,
                 thinking: bool = False) -> str:
        if "<facts>" in user:
            prefix = "<think>checking draft against facts</think>" if thinking else ""
            return (prefix + "[REFINED] I checked the draft against the "
                    "facts and corrected it where they conflicted.\n"
                    + user[:200])
        return ("[DRAFT] Rough attempt using requests.get with the timeout "
                "parameter and session.mount for retries.")


# ---------------- the loop ----------------

@dataclass
class LoopResult:
    draft: str
    facts: list[Fact]
    final: str
    version_used: str | None


def build_refine_prompt(user_prompt: str, draft: str, facts: list[Fact]) -> str:
    fact_block = "\n".join(f"- {f.render()}" for f in facts) if facts \
        else "(no relevant facts found in the bank)"
    return (f"<user_prompt>\n{user_prompt}\n</user_prompt>\n\n"
            f"<draft>\n{draft}\n</draft>\n\n"
            f"<facts>\n{fact_block}\n</facts>")


def build_refine_prompt_natural(user_prompt: str, draft: str,
                                facts: list[Fact],
                                show_draft: bool = True) -> str:
    """Hand the facts over the way a colleague would, instead of as tagged
    scaffolding.

    Why: the tagged form makes an untrained model behave like a REVIEWER --
    it writes "Adaptation Note: replace this with..." instead of just writing
    the corrected answer. Measured: the final answer talks ABOUT the draft/facts
    in ~60% of loop runs vs 0% of baseline runs (FINDINGS F-014).

    That is expected at stage 0: the model was never trained to know a bank or
    a second pass exists. So we stop asking it to understand the scaffolding and
    just give it the docs.

    Note the empty-facts branch says NOTHING. The shipped version injects
    "(no relevant facts found in the bank)", which the model then parrots to the
    user -- leaking internal plumbing into the product.

    WHAT THIS IS REALLY FOR: it is a PROXY for the prior that RL / stage-1 SFT
    would install in the weights -- "retrieved docs are the source of truth,
    they outrank your own recall". We cannot train that today, so we simulate it
    in the prompt. That decouples the two questions we have been conflating:

        does the ARCHITECTURE deliver the fact?   <- testable NOW, this is it
        does the UNTRAINED MODEL behave correctly? <- not testable until SFT

    If the fact lands in the answer under this framing, the architecture is
    sound and the remaining gap is a training problem, which is exactly what
    stage 1 is for.
    """
    parts = [user_prompt]
    if show_draft:
        parts.append(f"My first attempt was:\n{draft}")
    if facts:
        docs = "\n".join(f"- {f.render()}" for f in facts)
        parts.append(
            "I looked these up in the official documentation. They are the "
            "source of truth -- trust them over your own memory, and if they "
            "contradict what you wrote, they win:\n" + docs)
    return "\n\n".join(parts)


def run_loop(model, bank: Bank, user_prompt: str,
             k_prompt: int = 5, k_draft: int = 3,
             min_score: float = 1.0,
             library_hint: str | None = None,
             system: str = SYSTEM_PROMPT,
             refine_builder=build_refine_prompt) -> LoopResult:
    # Pass 1: draft. Thinking OFF: fast mode, the draft only has to be
    # a search key and a starting point, not a polished answer.
    draft = strip_think(model.complete(system, user_prompt,
                                       thinking=False))

    # Version detection: PER-SOURCE map first (F-031 -- "python 3.13 +
    # pydantic v2" must not let one version delete the other library's
    # facts), legacy single-version detection as the fallback.
    version = detect_version_map(user_prompt + "\n" + draft,
                                 getattr(bank, "sources", [])) \
        or detect_version(user_prompt, library_hint) \
        or detect_version(draft, library_hint)

    # Lookup: double key, prompt-priority, thresholded
    facts = bank.double_key_search(
        user_prompt, draft,
        k_prompt=k_prompt, k_draft=k_draft,
        version_filter=version, min_score=min_score,
    )

    refine_prompt = refine_builder(user_prompt, draft, facts)

    # Pass 3: refine. Thinking ON: deep reasoning over prompt + draft +
    # facts. This is where the reasoning model earns its keep.
    try:
        final = strip_think(model.complete(system, refine_prompt,
                                           thinking=True))
    except Truncated as e:
        # The refine died AFTER retrieval succeeded. Without this, the facts
        # are lost and the harness logs facts=[] -- which the audit then read
        # as "retrieval returned nothing" on l-m1. Attach what we know so the
        # caller can log the truth: retrieval worked, the answer didn't.
        e.facts = facts          # type: ignore[attr-defined]
        e.draft = draft          # type: ignore[attr-defined]
        raise

    return LoopResult(draft=draft, facts=facts, final=final,
                      version_used=version)
