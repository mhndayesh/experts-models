# OpenAI Python SDK v1.0.0 Migration Guide (old -> new)

Source: https://github.com/openai/openai-python/discussions/742 (fetched 2026-07-15)

- Module-level `openai.api_key = ...` is replaced by instantiating a client: `client = OpenAI(api_key=...)`.
- `openai.ChatCompletion.create()` is replaced by `client.chat.completions.create()`.
- `openai.Completion.create()` is replaced by `client.completions.create()`.
- `openai.Embedding.create()` is replaced by `client.embeddings.create()`.
- Response access `completion['choices'][0]['text']` (dict) is replaced by `completion.choices[0].text` (pydantic model attribute access).
- Serializing the response as a dict is replaced by `completion.model_dump_json(indent=2)`.
- The error class `openai.InvalidRequestError` is replaced by `openai.BadRequestError`.
- Error classes moved from `openai.error` to the top-level `openai` namespace.
- `openai.embeddings_utils` is removed (moved to the cookbook).
- `openai.api_key_path`, `openai.debug`, and `openai.log` are removed.
- `openai.requestssession` and `openai.aiosession` are removed; the client now uses `httpx`.
