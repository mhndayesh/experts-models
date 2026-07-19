# LlamaIndex Deprecated Terms (old -> new)

Source: https://developers.llamaindex.ai/python/framework/changes/deprecated_terms/ (fetched 2026-07-15)

- `GPTSimpleVectorIndex` is deprecated and replaced by `VectorStoreIndex`.
- `GPTVectorStoreIndex` is deprecated and replaced by `VectorStoreIndex`.
- `LLMPredictor` is deprecated; instantiate an LLM directly and pass it into `Settings` instead.
- `PromptHelper` and `max_input_size` are deprecated and replaced by the `context_window` parameter in `Settings` and `node_parser`.
- `ServiceContext` is deprecated and replaced by the `Settings` object.
- The `llama-index-legacy` package is deprecated and removed; migrate to current framework versions.
- Agent classes `AgentRunner`, `AgentWorker`, `FunctionCallingAgent`, `FunctionCallingAgentWorker`, `ReActAgent`, `ReActAgentWorker`, `LATSAgentWorker`, `CoAAgentWorker`, `FnAgentWorker`, `QueryPipelineAgentWorker`, `MultiModalReActAgentWorker`, `IntrospectiveAgentWorker`, `SelfReflectiveAgentWorker`, `ToolInteractiveReflectionAgentWorker`, `LLMCompilerAgentWorker`, and `QueryUnderstandAgentWorker` are deprecated and replaced by `AgentWorkflow` and `Workflows`.
- `QueryPipeline` is deprecated and replaced by `Workflows`.
- Query pipeline component classes `AgentFnComponent`, `InputComponent`, `RouterComponent`, `SelectorComponent`, `ToolRunnerComponent`, and `LoopComponent` are deprecated and replaced by `Workflows`.
