# OpenAI Responses API Migration Guide (Chat Completions -> Responses)

Source: https://developers.openai.com/api/docs/guides/migrate-to-responses (fetched 2026-07-15)

- `client.chat.completions.create()` (Chat Completions) is superseded by `client.responses.create()` (Responses API).
- The endpoint `/v1/chat/completions` is replaced by `/v1/responses`.
- The `messages` parameter is replaced by the `input` parameter (a string or Items array).
- A system-role message is replaced by the top-level `instructions` parameter.
- Output access `choices[0].message.content` is replaced by the `output_text` helper.
- The `response_format` parameter is replaced by `text.format`.
- The `n` parameter for multiple outputs is no longer available in the Responses API; make separate requests instead.
- Manual message-array state tracking is replaced by chaining with `previous_response_id`.
- Function/tool definitions change from external tagging (nested under `function`) to internal tagging (fields at the top level).
- Function strictness changes from non-strict by default to strict by default.
- Chat Completions streaming `delta` chunks are replaced by typed server-sent events (`response.output_text.delta`, `response.completed`, etc.).
- The Assistants API is deprecated as of August 26, 2025, with a sunset date of August 26, 2026; use the Responses API instead.
