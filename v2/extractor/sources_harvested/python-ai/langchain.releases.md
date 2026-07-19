# langchain-ai/langchain - last 20 releases (latest: langchain==1.3.13)


## langchain==1.3.13  (2026-07-10T23:06:20Z)

Changes since langchain==1.3.12

release(langchain): 1.3.13 (#38787)
feat(langchain): add `meta` extra and support langchain-meta in init_chat_model (#38786)
feat(openai): support explicit prompt caching (#38762)
chore(deps): refresh lockfiles (#38746)

---

## langchain-openai==1.3.5  (2026-07-10T18:58:46Z)

Changes since langchain-openai==1.3.4

release(openai): 1.3.5 (#38785)
feat(openai): support explicit prompt caching (#38762)
chore(model-profiles): refresh model profile data (#38774)

---

## langchain-fireworks==1.4.4  (2026-07-09T17:56:49Z)

Changes since langchain-fireworks==1.4.3

release(fireworks): 1.4.4 (#38753)
fix(fireworks): report cached prompt token usage (#38751)
chore(deps): refresh lockfiles (#38746)
chore(model-profiles): refresh model profile data (#38663)
chore: bump pytest from 9.1.0 to 9.1.1 in /libs/partners/fireworks (#38594)
chore: bump langsmith from 0.8.18 to 0.9.5 in /libs/partners/fireworks (#38595)
docs(fireworks): clarify prompt-cache session affinity guidance (#38522)
test(fireworks): cover request-level extra headers (#38518)

---

## langchain==1.3.12  (2026-07-08T22:38:27Z)

Changes since langchain==1.3.11

release(langchain): 1.3.12 (#38730)
fix(langchain): propagate interrupts through ToolRetryMiddleware (#38722)
fix(langchain): avoid shared process-group kill in shell middleware (#36359)
fix(langchain): sanitize anthropic cache markers on fallback retries (#37867)
style: fix some ruff preview rules in `langchain_v1` and `standard-tests` (#38657)
chore(langchain): add types in agent middleware tests (#38188)

---

## langchain-openai==1.3.4  (2026-07-08T23:00:08Z)

Changes since langchain-openai==1.3.3

release(openai): 1.3.4 (#38731)
fix(openai): suppress Pydantic serializer warning on structured output parsed field (#37727)
test(openai): skip Codex VCR tests before cassette setup (#38690)
chore: bump the minor-and-patch group across 3 directories with 11 updates (#38587)
chore: bump langgraph-checkpoint from 4.1.0 to 4.1.1 in /libs/partners/openai (#38476)
fix(core): use `asyncio.get_running_loop()` in async contexts (#38157)
test(openai): clarify async API key sync failure trace (#38379)

---

## langchain-core==1.4.9  (2026-07-08T20:07:10Z)

Changes since langchain-core==1.4.8

release(core): 1.4.9 (#38728)
fix(core): improve langsmith loader error messages (#35648)
fix(core): output parser bugs in xml.py and pydantic.py (#35641)
style(core): fix some ruff preview rules (#38656)
fix(core): avoid `dict` shadowing in language models (#38480)
fix(core): `_parse_google_docstring` mishandling continuation lines with colons (#35680)
fix(core): add messages to bare `raise ValueError` calls (#38158)
fix(core): use `asyncio.get_running_loop()` in async contexts (#38157)
chore: bump langsmith from 0.8.0 to 0.8.18 in /libs/core (#38319)
chore: bump jupyterlab from 4.5.7 to 4.5.9 in /libs/core (#38326)
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/core (#38327)

---

## langchain-openrouter==0.2.6  (2026-07-05T20:53:14Z)

Changes since langchain-openrouter==0.2.5

release(openrouter): 0.2.6 (#38681)
fix(openrouter): support `default_headers` for custom HTTP header injection (#36582)
chore(model-profiles): refresh model profile data (#38663)

---

## langchain-mistralai==1.1.6  (2026-07-05T21:30:35Z)

Changes since langchain-mistralai==1.1.5

release(mistralai): 1.1.6 (#38684)
feat(mistralai): surface citation metadata from chat responses (#37008)
chore(model-profiles): refresh model profile data (#38663)
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/partners/mistralai (#38302)
chore: bump langsmith from 0.8.5 to 0.8.18 in /libs/partners/mistralai (#38304)
chore(model-profiles): refresh model profile data (#38210)
docs: refresh `README` installation and resources (#38119)
release(core): 1.4.7 (#38111)
fix(core,partners): rename package version trace metadata (#38110)
style(core,langchain,langchain-classic,partners): replace double backticks in docstrings (#38095)
release(core): 1.4.6 (#38061)
feat(core,partners): add package version tracking to tracing metadata (#35295)
chore(infra): bump mypy to 2.1 and unify type-check config across the monorepo (#36470)
feat(mistralai): support `stop` sequences (#38047)

---

## langchain-openrouter==0.2.5  (2026-06-29T19:47:27Z)

Changes since langchain-openrouter==0.2.4

release(openrouter): 0.2.5 (#38553)
fix(openrouter): deduplicate repeated finish metadata (#38552)
fix(openrouter): strip Responses reasoning IDs (#38383)

---

## langchain-fireworks==1.4.3  (2026-06-26T06:52:05Z)

Changes since langchain-fireworks==1.4.2

release(fireworks): 1.4.3
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/partners/fireworks (#38314)
chore: bump langsmith from 0.8.16 to 0.8.18 in /libs/partners/fireworks (#38313)
chore: bump langsmith from 0.8.14 to 0.8.16 in /libs/partners/fireworks (#38235)
chore: bump pytest from 9.0.3 to 9.1.0 in /libs/partners/fireworks (#38233)
chore(model-profiles): refresh model profile data (#38210)
chore(model-profiles): refresh model profile data (#38191)
chore(model-profiles): refresh model profile data (#38133)
docs: refresh `README` installation and resources (#38119)
release(core): 1.4.7 (#38111)
fix(core,partners): rename package version trace metadata (#38110)
style(core,langchain,langchain-classic,partners): replace double backticks in docstrings (#38095)
chore: bump langsmith from 0.8.9 to 0.8.14 in /libs/partners/fireworks (#38093)
release(core): 1.4.6 (#38061)
feat(core,partners): add package version tracking to tracing metadata (#35295)
chore(infra): bump mypy to 2.1 and unify type-check config across the monorepo (#36470)
feat(standard-tests): validate tool call chunks during streaming (#34707)
chore(partners): bump locks (#38052)
hotfix(openai): min core dep (#37990)
chore(model-profiles): refresh model profile data (#37973)
chore(model-profiles): refresh model profile data (#37936)
test(langchain,partners): disable pytest-benchmark under xdist to silence `PytestBenchmarkWarning` (#37901)
fix(partners): cap aiohttp below 3.14 for vcrpy compat (#37898)
chore(model-profiles): refresh model profile data (#37895)
chore: bump aiohttp from 3.13.5 to 3.14.0 in /libs/partners/fireworks (#37882)
chore: bump langsmith from 0.8.7 to 0.8.9 in /libs/partners/fireworks (#37883)
chore: bump langsmith from 0.8.0 to 0.8.7 in /libs/partners/fireworks (#37781)
chore: bump requests from 2.34.0 to 2.34.2 in /libs/partners/fireworks (#37782)

---

## langchain-anthropic==1.4.8  (2026-06-26T21:28:59Z)

Changes since langchain-anthropic==1.4.7

release(anthropic): 1.4.8 (#38490)
fix(anthropic): keep initial text on `content_block_start` (#38442)
chore: bump langgraph-checkpoint from 4.1.0 to 4.1.1 in /libs/partners/anthropic (#38479)
fix(core): add messages to bare `raise ValueError` calls (#38158)

---

## langchain-openrouter==0.2.4  (2026-06-23T03:45:32Z)

Changes since langchain-openrouter==0.2.3

release(openrouter): 0.2.4 (#38381)
chore(openrouter): bump `openrouter` floor to 0.9.2, drop file workaround (#38216)
test(openrouter): cover `cache_control` passthrough on tool defs (#38215)
feat(openrouter): surface `parallel_tool_calls` on `bind_tools` (#38214)
chore(model-profiles): refresh model profile data (#38341)
chore(model-profiles): refresh model profile data (#38331)
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/partners/openrouter (#38291)
chore: bump langsmith from 0.8.5 to 0.8.18 in /libs/partners/openrouter (#38292)
chore(model-profiles): refresh model profile data (#38274)
chore(model-profiles): refresh model profile data (#38244)
chore(model-profiles): refresh model profile data (#38210)
chore(model-profiles): refresh model profile data (#38160)
chore(model-profiles): refresh model profile data (#38133)
docs: refresh `README` installation and resources (#38119)
release(core): 1.4.7 (#38111)
fix(core,partners): rename package version trace metadata (#38110)
chore(model-profiles): refresh model profile data (#38100)
style(core,langchain,langchain-classic,partners): replace double backticks in docstrings (#38095)
release(core): 1.4.6 (#38061)
feat(core,partners): add package version tracking to tracing metadata (#35295)
chore(infra): bump mypy to 2.1 and unify type-check config across the monorepo (#36470)
feat(standard-tests): validate tool call chunks during streaming (#34707)
fix(langchain): tighten structured output model fallbacks (#38042)
test(partners): account for warning behavior in partner tests (#38046)
chore(model-profiles): refresh model profile data (#38012)
hotfix(openai): min core dep (#37990)
chore(model-profiles): refresh model profile data (#37973)
chore(model-profiles): refresh model profile data (#37958)
chore(model-profiles): refresh model profile data (#37936)
chore(model-profiles): refresh model profile data (#37916)
test(langchain,partners): disable pytest-benchmark under xdist to silence `PytestBenchmarkWarning` (#37901)
chore(model-profiles): refresh model profile data (#37895)
chore(model-profiles): refresh model profile data (#37870)
chore(model-profiles): refresh model profile data (#37852)
chore(model-profiles): refresh model profile data (#37802)
chore(model-profiles): refresh model profile data (#37791)
chore(model-profiles): refresh model profile data (#37771)
chore(model-profiles): refresh model profile data (#37726)
chore(model-profiles): refresh model profile data (#37712)
chore(model-profiles): refresh model profile data (#37694)
chore(model-profiles): refresh model profile data (#37650)
chore(model-profiles): refresh model profile data (#37626)
chore(infra): bump `langchain-tests` floor to 1.1.9 (#37610)
chore: bump idna from 3.11 to 3.15 in /libs/partners/openrouter (#37546)
chore: bump langsmith from 0.8.4 to 0.8.5 in /libs/partners/openrouter (#37547)
chore(model-profiles): refresh model profile data (#37524)
ci(infra): harden Dependabot version-bound preservation (#37510)
chore(core,langchain,openai): refresh stale OpenAI model references (#37487)
chore(model-profiles): refresh model profile data (#37477)
chore(model-profiles): refresh model profile data (#37466)
chore: bump langsmith from 0.8.0 to 0.8.4 in /libs/partners/openrouter (#37414)
chore: bump langsmith from 0.7.31 to 0.8.0 in /libs/partners/openrouter (#37397)
chore: bump urllib3 from 2.6.3 to 2.7.0 in /libs/partners/openrouter (#37352)
chore: bump langchain-core from 1.3.2 to 1.3.3 in /libs/partners/openrouter (#37263)
chore(model-profiles): refresh model profile data (#37247)
chore(model-profiles): refresh model profile data (#37231)
chore(model-profiles): refresh model profile data (#37182)
chore(model-profiles): refresh model profile data (#37162)
chore(model-profiles): refresh model profile data (#37148)

---

## langchain==1.3.11  (2026-06-22T23:00:47Z)

Changes since langchain==1.3.10

release(langchain): 1.3.11 (#38377)
fix(langchain,openai): only set `strict=True` on tools for OpenAI-compatible models in `ProviderStrategy` (#38370)
chore: bump pydantic-settings from 2.12.0 to 2.14.2 in /libs/langchain_v1 (#38279)
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/langchain_v1 (#38280)
chore: bump langsmith from 0.8.9 to 0.8.18 in /libs/langchain_v1 (#38281)
docs(langchain): document summarization prompt contract (#38256)

---

## langchain-openai==1.3.3  (2026-06-22T22:54:23Z)

Changes since langchain-openai==1.3.2

release(openai): 1.3.3 (#38375)
fix(openai): drop response item ids when `store` is false (#38372)
fix(langchain,openai): only set `strict=True` on tools for OpenAI-compatible models in `ProviderStrategy` (#38370)
test(openai): clarify expected strict schema error (#38338)
fix(openai): drop `stop` from Responses API payload (#38336)
chore: bump langsmith from 0.8.5 to 0.8.18 in /libs/partners/openai (#38293)
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/partners/openai (#38294)
chore(model-profiles): refresh model profile data (#38274)
test(openai): vcr embedding raw equivalence tests (#38199)

---

## langchain-anthropic==1.4.7  (2026-06-22T22:56:18Z)

Changes since langchain-anthropic==1.4.6

hotfix(anthropic): regenerate cassette (#38376)
release(anthropic): 1.4.7 (#38373)
chore: bump vcrpy from 8.1.1 to 8.2.1 in /libs/partners/anthropic (#38324)
chore: bump langsmith from 0.8.5 to 0.8.18 in /libs/partners/anthropic (#38325)
docs(anthropic): clarify prompt caching middleware docstring (#38206)
docs: refresh `README` installation and resources (#38119)
test(core,langchain): update tests for explicit deserialization allowlists (#38118)
release(core): 1.4.7 (#38111)
fix(core,partners): rename package version trace metadata (#38110)

---

## langchain==1.3.10  (2026-06-18T19:43:17Z)

Changes since langchain==1.3.9

release(langchain): 1.3.10 (#38255)
chore: bump cryptography from 46.0.7 to 48.0.1 in /libs/langchain_v1 (#38176)
chore: bump aiohttp from 3.14.0 to 3.14.1 in /libs/langchain_v1 (#38179)
fix(langchain): switch summary format (#38171)
fix(langchain): detect provider strategy for dated `gpt-5.2`/`gpt-5.4` snapshots (#38222)
chore(langchain): improve typing in tests (#38163)
chore: bump pyjwt from 2.12.0 to 2.13.0 in /libs/langchain_v1 (#38168)
release(openai): 1.3.2 (#38130)
hotfix(openai): switch version (#38123)
release(openai): 1.4.0 (#38120)
docs: refresh `README` installation and resources (#38119)
test(core,langchain): update tests for explicit deserialization allowlists (#38118)
release(core): 1.4.7 (#38111)
release(anthropic): 1.4.6 (#38105)

---

## langchain-core==1.4.8  (2026-06-18T19:39:42Z)

Changes since langchain-core==1.4.7

chore: bump jupyter-server from 2.18.0 to 2.20.0 in /libs/core (#38252)
chore: bump tornado from 6.5.6 to 6.5.7 in /libs/core (#38184)
chore: bump bleach from 6.3.0 to 6.4.0 in /libs/core (#38198)
release(core): 1.4.8 (#38254)
refactor(langchain-classic): remove code for Python < 3.10 (#38194)
perf(core): memoize `BaseTool.tool_call_schema` subset model and cache `model_json_schema` (#38073)
style(core): fix style in `langchain_core`/`_security` (#38189)
fix(core): preserve usage token details in v3 streaming events (#38021)
fix(core): `disallow_any_generics` (#38156)
chore(core): add mypy `warn_unreachable` (#38109)
docs: refresh `README` installation and resources (#38119)
test(core,langchain): update tests for explicit deserialization allowlists (#38118)

---

## langchain-openai==1.3.2  (2026-06-13T05:42:30Z)

Changes since langchain-openai==1.3.1

release(openai): 1.3.2 (#38130)

---

## langchain-openai==1.3.1  (2026-06-13T02:42:27Z)

Changes since langchain-openai==1.3.0

docs: refresh `README` installation and resources (#38119)
test(core,langchain): update tests for explicit deserialization allowlists (#38118)
release(core): 1.4.7 (#38111)
fix(core,partners): rename package version trace metadata (#38110)
style(core,langchain,langchain-classic,partners): replace double backticks in docstrings (#38095)
test(openai): use `gpt-4o` for image token counting (#38089)
release(core): 1.4.6 (#38061)
feat(core,partners): add package version tracking to tracing metadata (#35295)
fix(core,openai): normalize v1 streamed tool calls (#35983)
chore(infra): bump mypy to 2.1 and unify type-check config across the monorepo (#36470)
feat(standard-tests): validate tool call chunks during streaming (#34707)
fix(langchain): tighten structured output model fallbacks (#38042)

---

## langchain==1.3.9  (2026-06-12T16:53:43Z)

Changes since langchain==1.3.8

release(anthropic): 1.4.6 (#38105)
release(langchain): 1.3.9 (#38104)
fix(langchain,anthropic): confine file-search results and tighten anthropic `allowed_prefixes` (#38106)

---