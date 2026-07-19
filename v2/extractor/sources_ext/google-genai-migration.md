# Google GenAI SDK Migration Guide (google-generativeai -> google-genai)

Source: https://ai.google.dev/gemini-api/docs/migrate (fetched 2026-07-15)

## Package Installation Changes
- Python: `google-generativeai` is replaced by `google-genai`.
- JavaScript: `@google/generative-ai` is replaced by `@google/genai`.
- Go: `github.com/google/generative-ai-go` is replaced by `google.golang.org/genai`.

## Core API Architecture Shift
A centralized `Client` object replaces ad hoc API access patterns.

```python
# Before
import google.generativeai as genai
model = genai.GenerativeModel('gemini-3.5-flash')
response = model.generate_content(...)

# After
from google import genai
client = genai.Client()
response = client.models.generate_content(model='gemini-3.5-flash', contents=...)
```

## Method Renames and Service Access Patterns
- Content generation: `model.generate_content()` is replaced by `client.models.generate_content()`.
- Streaming: `model.generate_content_stream()` is replaced by `client.models.generate_content_stream()`.
- Chat creation: `model.start_chat()` is replaced by `client.chats.create()`.
- File upload: `genai.upload_file()` is replaced by `client.files.upload()`.
- File list: `genai.list_files()` is replaced by `client.files.list()`.
- Token counting: `model.count_tokens()` is replaced by `client.models.count_tokens()`.
- Embeddings: `genai.embed_content()` is replaced by `client.models.embed_content()`.
- Image generation: `ImageGenerationModel.generate_images()` is replaced by `client.models.generate_images()`.

## Configuration Parameter Changes
Safety settings and generation config now use a unified `config` parameter with pydantic classes.

```python
config=types.GenerateContentConfig(
    temperature=0.5,
    safety_settings=[types.SafetySetting(...)]
)
```

## Async Operations
Python async is now accessed through the `client.aio.*` namespace instead of `*_async()` methods.

```python
# Before
response = await model.generate_content_async(...)

# After
response = await client.aio.models.generate_content(...)
```
