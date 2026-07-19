"""VENDORED SNAPSHOT of NEW BANK/factbank/factbank/native_tags.py (2026-07-13, post live-smoke).
The research tree is the lab; this package ships the evaluated system. Do not
edit here without syncing intent with the lab copy.


native_tags.py - Deliver the bank through the model's OWN trained protocol.

THE IDEA
--------
We have been inventing a format (<user_prompt>/<draft>/<facts>) and hoping an
untrained model interprets it. It does not -- it reads the tags as a request to
REVIEW something and writes commentary instead of code (FINDINGS F-014), and on
big models it thinks itself in circles trying to work out what we want (4 of 5
truncations were in the tagged arm).

Then we read Gemma-4's chat template out of its GGUF and found:

    <|tool_response>  response:name{...}  <tool_response|>     <- REAL TOKENS

These are single tokens in its 262k vocab. Our <facts> is not a token at all --
it is plain text the tokenizer shreds into pieces. So our tags never collided
with Gemma's; they were simply FOREIGN. We wrote a protocol in a language the
model does not speak.

And the model already HAS the concept we need. It is RL-trained to treat a
tool_response as authoritative data fetched from an external source -- exactly
the status we want bank facts to have. That is the same prior we have been
FAKING with prose ("these are the source of truth, trust them over your memory",
F-014's RL-proxy).

    We do not have to fake it. The model was already trained on it.
    We just have to speak its language.

So: present the fact bank AS A TOOL. The model "calls" search_docs, and the bank's
facts come back as a real tool_response. In-distribution, zero invented syntax,
and the "trust this, it is external ground truth" semantics come free from
Google's RL rather than from our prompt engineering.

HOW (and why not just paste the tokens as text)
-----------------------------------------------
We do NOT hand-write "<|tool_response>..." into the user message -- whether the
backend parses those as special tokens or as literal text is not something we
should be guessing at. Instead we use the OpenAI tools API properly:

    system  -> user  -> assistant(tool_calls=[search_docs])  -> tool(facts)

and let the chat template render the native blocks. Guaranteed in-distribution,
whatever the backend does under the hood.

Gemma-4 also honors enable_thinking for real (its template PRE-FILLS an empty
<|channel>thought<channel|> to suppress reasoning), so the two-speed trick --
cheap draft, expensive refine -- works again. Qwen3.6 had taken that away.
"""

import json
import urllib.error
import urllib.request
from dataclasses import dataclass

from .bank import Fact, detect_version
from .loop import Truncated, strip_think

# The tool the model "called". The description is what teaches it what came back:
# verified documentation, not a guess.
SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_docs",
        "description": ("Search the official documentation for verified API "
                        "facts: exact signatures, version notes, and explicit "
                        "warnings about APIs that do not exist or were removed. "
                        "Returns ground truth from the official docs."),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string",
                          "description": "What to look up in the docs."},
            },
            "required": ["query"],
        },
    },
}


def facts_payload(facts: list[Fact]) -> str:
    """What comes back from the 'tool'. Plain, dense, no invented syntax."""
    if not facts:
        return "No matching documentation found."
    return "\n".join(f"- {f.render()}" for f in facts)


class NativeToolModel:
    """OpenAI-compatible, but able to speak the tool protocol.

    complete()        - a normal single call (used for the draft pass).
    complete_with_facts() - the refine pass: the facts arrive as a real
                            tool_response, through the model's own channel.
    """

    def __init__(self, base_url: str, model: str, temperature: float = 0.2,
                 max_tokens: int = 8192, draft_max_tokens: int = 512):
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        # The draft is a SEARCH KEY, not an answer. It gets thrown away. Do not
        # let it reason for 10,000 tokens -- cap it hard and let it be cut off.
        self.draft_max_tokens = draft_max_tokens
        self.last_call: dict = {}

    def _post(self, body: dict) -> dict:
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=1800) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise RuntimeError(f"HTTP {e.code}: "
                               f"{e.read().decode('utf-8','replace')[:400]}") from None

    def _finish(self, data: dict, allow_empty: bool = False) -> str:
        ch = data["choices"][0]
        msg = ch["message"]
        content = msg.get("content") or ""
        reasoning = msg.get("reasoning_content") or ""
        self.last_call = {
            "finish_reason": ch.get("finish_reason"),
            "completion_tokens": data.get("usage", {}).get("completion_tokens"),
            "reasoning_chars": len(reasoning),
        }
        if not allow_empty and (ch.get("finish_reason") == "length"
                                or not content.strip()):
            raise Truncated(
                f"no answer written (finish={ch.get('finish_reason')!r}, "
                f"tokens={self.last_call['completion_tokens']})")
        # For the DRAFT only: if the cap cut it off mid-thought, the reasoning
        # trace is itself a fine search key -- see draft().
        return strip_think(content) or (reasoning if allow_empty else "")

    # ---------------------------------------------------------------- passes
    def draft(self, system: str, question: str,
              history: list[dict] | None = None) -> str:
        """Pass 1: the SEARCH KEY. Not an answer -- it is thrown away.

        We cap it hard (512 tokens) because its only job is to reveal which
        libraries the model is reaching for. That is the HyDE trick: the draft
        names `httpx.get(retries=3)` and so retrieves the httpx docs the bare
        question never mentioned.

        Two things we learned the hard way:

        - LM Studio DROPS chat_template_kwargs. enable_thinking is ignored on
          every model (measured: identical token counts for True/False/absent).
          So we cannot switch thinking off; we can only CAP it. (F-018)
        - Capped, the model spends its whole budget reasoning and returns
          content="". But the REASONING TRACE is an excellent search key in its
          own right -- it is full of the exact library and API names the model
          is considering. So we fall back to it rather than searching with "".
          A cut-off draft is not a failure here; it is the intended shape.

        history: prior conversation turns, used only by the serving path
        (serve.py). Research harnesses pass none, so their request bodies
        are byte-identical to what the experiments measured.
        """
        data = self._post({
            "model": self.model, "temperature": self.temperature,
            "max_tokens": self.draft_max_tokens,
            "messages": [{"role": "system", "content": system},
                         *(history or []),
                         {"role": "user", "content": question}],
        })
        return self._finish(data, allow_empty=True)   # cut-off draft is FINE

    def complete_plain(self, system: str, question: str,
                       thinking: bool = True,
                       history: list[dict] | None = None,
                       max_tokens: int | None = None,
                       temperature: float | None = None) -> str:
        # history / max_tokens / temperature: serving-path extras (serve.py
        # honors client params). Defaults leave research requests unchanged.
        data = self._post({
            "model": self.model,
            "temperature": self.temperature if temperature is None
            else temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "chat_template_kwargs": {"enable_thinking": thinking},
            "messages": [{"role": "system", "content": system},
                         *(history or []),
                         {"role": "user", "content": question}],
        })
        return self._finish(data)

    def complete_with_facts(self, system: str, question: str,
                            facts: list[Fact], query: str,
                            thinking: bool = True,
                            history: list[dict] | None = None,
                            max_tokens: int | None = None,
                            temperature: float | None = None) -> str:
        """Pass 3, NATIVE. The bank's facts arrive as a real tool_response.

        The message chain the template renders:
            <|turn>system ... <|tool>declaration:search_docs{...}<tool|><turn|>
            <|turn>user    the question <turn|>
            <|turn>model   <|tool_call>call:search_docs{query:...}<tool_call|>
                           <|tool_response>response:search_docs{...}<tool_response|>
            <|turn>model   <- the model answers from here

        Every one of those is a token Gemma was trained on. We invent nothing.
        """
        data = self._post({
            "model": self.model,
            "temperature": self.temperature if temperature is None
            else temperature,
            "max_tokens": max_tokens or self.max_tokens,
            "chat_template_kwargs": {"enable_thinking": thinking},
            "tools": [SEARCH_TOOL],
            "messages": [
                {"role": "system", "content": system},
                *(history or []),
                {"role": "user", "content": question},
                {"role": "assistant", "content": None,
                 "tool_calls": [{
                     "id": "call_1", "type": "function",
                     "function": {"name": "search_docs",
                                  "arguments": json.dumps({"query": query})},
                 }]},
                {"role": "tool", "tool_call_id": "call_1",
                 "name": "search_docs",
                 "content": facts_payload(facts)},
            ],
        })
        return self._finish(data)


# ------------------------------------------------------------------ the loop
@dataclass
class NativeResult:
    draft: str
    facts: list[Fact]
    final: str
    version_used: str | None


NATIVE_SYSTEM = ("You are a coding assistant. You have a search_docs tool that "
                 "returns verified facts from the official documentation. "
                 "Answer the user's question with correct, working code.")


def run_loop_native(model: NativeToolModel, bank, question: str,
                    k_prompt: int = 5, k_draft: int = 3,
                    system: str = NATIVE_SYSTEM) -> NativeResult:
    # Pass 1: draft. Thinking OFF, hard-capped. It is only a search key -- it
    # reveals which libraries the model is reaching for (the HyDE trick).
    draft = model.draft(system, question)

    version = detect_version(question) or detect_version(draft)
    facts = bank.double_key_search(question, draft, k_prompt=k_prompt,
                                   k_draft=k_draft, version_filter=version)

    # Pass 3: refine. Facts arrive through the model's OWN tool channel.
    final = model.complete_with_facts(system, question, facts, query=question,
                                      thinking=True)
    return NativeResult(draft=draft, facts=facts, final=final,
                        version_used=version)
