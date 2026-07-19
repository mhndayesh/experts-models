# LangChain v1 Migration Guide (old -> new)

Source: https://docs.langchain.com/oss/python/migrate/langchain-v1 (fetched 2026-07-15)

## Import path changes
- `from langgraph.prebuilt import create_react_agent` is replaced by `from langchain.agents import create_agent`.

## Moved to the `langchain-classic` package
- Legacy chains `LLMChain` and `ConversationChain` are moved to `langchain-classic`.
- The retrievers module (e.g. `MultiQueryRetriever`) is moved to `langchain-classic`.
- The indexing API is moved to `langchain-classic`.
- The hub module is moved to `langchain-classic`.
- Embeddings modules (`CacheBackedEmbeddings`, community embeddings) are moved to `langchain-classic`.
- `langchain-community` re-exports are moved to `langchain-classic`.

## Parameter renames
- The `prompt` parameter is renamed to `system_prompt` in agent creation.

## Removed features
- Pre-bound models with tools via `.bind_tools()` are no longer supported when creating agents.
- Pydantic models and dataclasses for state schemas are removed; use `TypedDict` only.
- The `example` parameter is removed from `AIMessage`.
- Prompted output via `response_format` is removed.
- Passing `ToolNode` instances in the tools argument is removed.
- Pre-model and post-model hook functions are removed.

## Replaced with
- Hook functions are replaced by middleware with `before_model` / `after_model` methods.
- Tool error handling is replaced by middleware with a `wrap_tool_call` method.
- Dynamic prompts are replaced by the `@dynamic_prompt` decorator.
- Dynamic models are replaced by `DynamicModelMiddleware`.

## Structural changes
- The streaming node name changed from `"agent"` to `"model"`.
- Runtime context moved from `config["configurable"]` to the `context` parameter.
- The message `.text()` method is replaced by the `.text` property.

## Namespace consolidation
- The core `langchain` package now contains only: `agents`, `messages`, `tools`, `chat_models`, `embeddings`.
