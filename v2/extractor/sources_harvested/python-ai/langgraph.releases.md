# langchain-ai/langgraph - last 20 releases (latest: 1.2.9)


## 1.2.9  (2026-07-10T01:30:24Z)

Changes since 1.2.8

* release(langgraph): 1.2.9 (#8316)
* fix: updateState metadata/counters for delta channel (#8315)

---

## cli==0.4.31  (2026-07-10T22:58:04Z)

Changes since cli==0.4.30

* chore(cli): allow langgraph-api versions up to 1.0.0 (#8319)
* chore(deps): bump the minor-and-patch group in /libs/cli with 5 updates (#8251)
* chore(deps): bump the minor-and-patch group in /libs/cli/js-examples with 6 updates (#8246)
* chore(deps): bump the minor-and-patch group in /libs/cli/js-monorepo-example with 7 updates (#8245)
* chore(deps): bump starlette from 1.0.1 to 1.3.1 in /libs/cli (#8105)
* chore(deps): bump langsmith from 0.8.0 to 0.8.18 in /libs/cli (#8172)
* feat(cli): allow prebuild images for langgraph deploy (#8100)
* chore(deps): bump langchain-anthropic from 1.0.0a5 to 1.4.6 in /libs/cli/examples/graph_prerelease_reqs in the pip group across 1 directory (#8145)
* chore(deps): bump @babel/core from 7.25.2 to 7.29.7 in /libs/cli/js-examples (#8144)
* chore(deps): bump js-yaml from 4.1.1 to 4.2.0 in /libs/cli/js-monorepo-example (#8143)
* chore(deps): bump cryptography from 46.0.7 to 48.0.1 in /libs/cli (#8103)
* chore(deps): bump pyjwt from 2.12.1 to 2.13.0 in /libs/cli (#8093)

---

## 1.2.8  (2026-07-06T20:40:30Z)

Changes since 1.2.7

* release(langgraph): 1.2.8 (#8292)
* fix: delta channel bug with updateState on fresh thread will force snapshot instead of stub checkpoint (#8290)
* chore(deps): bump the minor-and-patch group in /libs/langgraph with 8 updates (#8255)
* chore(deps): bump websockets from 15.0.1 to 16.0 in /libs/langgraph in the major group (#8256)
* chore(deps): bump the minor-and-patch group in /libs/sdk-py with 9 updates (#8252)

---

## 1.2.7  (2026-06-30T01:24:26Z)

Changes since 1.2.6

* release(langgraph): 1.2.7 (#8223)
* fix(langgraph): snapshot `DeltaChannel` overwrite supersteps (#8125)
* fix(langgraph): Make `Overwrite` survive JSON roundtrips (#8127)
* chore(deps): bump redis in /libs/langgraph (#7976)
* chore(deps): bump langsmith from 0.8.0 to 0.8.18 in /libs/langgraph (#8176)
* chore(deps): bump jupyterlab from 4.5.7 to 4.5.9 in /libs/langgraph (#8164)
* fix(langgraph): emit valid UUIDs for exit-mode delta task_ids for langgraph-api (#8165)
* chore(deps): bump bleach from 6.3.0 to 6.4.0 in /libs/langgraph (#8107)
* chore(deps): bump cryptography from 46.0.7 to 48.0.1 in /libs/langgraph (#8106)
* chore(deps): bump jupyter-server from 2.18.0 to 2.20.0 in /libs/langgraph (#8134)
* chore(deps): bump tornado from 6.5.6 to 6.5.7 in /libs/langgraph (#8108)
* chore(deps): bump pyjwt from 2.12.0 to 2.13.0 in /libs/langgraph (#8092)

---

## 1.2.6  (2026-06-18T20:58:32Z)

Changes since 1.2.5

* release(langgraph): 1.2.6 (#8139)
* fix: nested subgraph inherits parent checkpoint_ns (regression in 1.2.3) (#8053)
* fix: cancel running subgraphs on v3 stream abort [closes #8029] (#8057)
* release(cli): 0.4.30 (#8101)
* docs: standardize package `README.md` structure (#8064)
* chore(deps): bump tornado from 6.5.5 to 6.5.6 in /libs/langgraph (#8063)

---

## cli==0.4.30  (2026-06-16T19:46:45Z)

Changes since cli==0.4.29

* release(cli): 0.4.30 (#8101)
* feat(cli): support compatible api version ranges (#8023)
* docs: standardize package `README.md` structure (#8064)

---

## 1.2.5  (2026-06-12T20:31:14Z)

Changes since 1.2.4

* release(langgraph): 1.2.5 (#8062)
* fix(langgraph): merge `lc_versions` config metadata (#8052)
* release(cli): 0.4.28 (#8041)
* fix: updateState bug for deltaChannel on empty thread (#8011)
* chore: migrate Python type checking to ty (#8002)
* chore(deps-dev): bump types-requests from 2.33.0.20260408 to 2.33.0.20260518 in /libs/langgraph (#7977)
* chore(deps): bump the minor-and-patch group in /libs/langgraph with 14 updates (#7975)

---

## cli==0.4.29  (2026-06-11T19:53:04Z)

Changes since cli==0.4.28

* release(cli): 0.4.29 (#8046)
* feat(cli): add support for passing certfile and cert key to run dev server under HTTPS (#8031)

---

## cli==0.4.28  (2026-06-10T18:20:32Z)

Changes since cli==0.4.27

* release(cli): 0.4.28 (#8041)
* chore(deps): bump starlette from 1.0.0 to 1.0.1 in /libs/cli (#8005)
* chore: migrate Python type checking to ty (#8002)
* chore(deps): bump the minor-and-patch group in /libs/cli with 4 updates (#7962)
* chore(deps): bump typescript from 5.9.3 to 6.0.3 in /libs/cli/js-monorepo-example (#7672)
* chore(deps-dev): bump typescript from 5.9.3 to 6.0.3 in /libs/cli/js-examples in the major group across 1 directory (#7966)
* chore(deps-dev): bump mypy from 1.20.2 to 2.1.0 in /libs/cli in the major group (#7968)
* chore(deps): bump the minor-and-patch group in /libs/cli/js-monorepo-example with 7 updates (#7959)
* chore(deps): bump the minor-and-patch group in /libs/cli/js-examples with 8 updates (#7963)
* chore(deps): bump uv from 0.11.7 to 0.11.15 in /libs/cli (#7943)
* chore(langgraph): Track ADK/other library usage when deploying using cli (#7939)

---

## 1.2.4  (2026-06-02T17:07:49Z)

Changes since 1.2.3

* release(langgraph): 1.2.4 (#7991)
* test(sdk-py): add factory-graph integration test exercising the server factory path (#7978)
* fix(langgraph): keep _on_started backward-compatible with overrides predating cause (#7987)

---

## 1.2.3  (2026-06-01T18:56:09Z)

Changes since 1.2.2

* release(langgraph): 1.2.3 (#7945)
* feat(langgraph): wire RemoteGraph.interleave to sdk-py interleave_projections (#7938)
* feat(langgraph): add v3 streaming support to RemoteGraph (#7927)
* feat(langgraph): name tool-dispatched subagents via lc_agent_name (#7928)
* fix(langgraph): rename ProtocolEvent.eventId to event_id to match the wire field (#7942)
* fix(langgraph): merge instead of overwrite in ensure_config for callbacks, tags, metadata, configurable (#7926)
* fix(langgraph): [LSD-1507] Distinguish between user cancelled and other cancellations (#7920)
* fix(cli): bump api bound to 0.10.0 (#7922)
* feat(sdk-py): add websocket stream transports (#7830)
* feat(sdk-py): add messages and tool call projections (#7823)
* feat(sdk-py): add v3 streaming primitives and SSE transport (#7818)

---

## sdk==0.4.2  (2026-06-01T17:51:31Z)

Changes since sdk==0.4.1

* release(sdk-py): 0.4.2 (#7955)
* fix(sdk-py): percent-encode thread_id in v3 stream transport default paths (#7954)

---

## sdk==0.4.1  (2026-06-01T15:23:38Z)

Changes since sdk==0.4.0

* release(sdk-py): 0.4.1 (#7944)
* feat(sdk-py): extract stream decoders and add interleave_projections (#7935)
* feat(langgraph): add v3 streaming support to RemoteGraph (#7927)
* fix(sdk-py): make `tools_agent` fake model stateless (#7930)

---

## sdk==0.4.0  (2026-05-28T14:11:35Z)

Changes since sdk==0.3.15

* release(sdk-py): 0.4.0 (#7923)
* feat(sdk-py): add thread stream helpers (#7833)
* feat(sdk-py): wire websocket stream selection (#7832)
* feat(sdk-py): add websocket stream transports (#7830)
* feat(sdk-py): harden streaming reconnects (#7829)
* feat(sdk-py): add sync scoped subgraphs (#7828)
* feat(sdk-py): add sync messages and tool calls (#7827)
* feat(sdk-py): add sync thread stream core (#7826)
* feat(sdk-py): add async stream reconnect support (#7825)
* feat(sdk-py): add scoped subgraph handles (#7824)
* feat(sdk-py): add messages and tool call projections (#7823)
* feat(sdk-py): add output, values, and controller extraction (#7822)
* feat(sdk-py): wire lifecycle state and output prerequisites (#7821)
* feat(sdk-py): add shared stream subscriptions (#7820)
* feat(sdk-py): add async thread stream skeleton (#7819)
* feat(sdk-py): add v3 streaming primitives and SSE transport (#7818)
* chore(langgraph): bump version to 1.2.2 (#7914)

---

## cli==0.4.27  (2026-05-28T14:25:48Z)

Changes since cli==0.4.26

* release(cli): 0.4.27 (#7925)
* fix(cli): pin internal_docker deploy images by digest (#7924)
* fix(cli): bump api bound to 0.10.0 (#7922)
* chore(deps): bump the uv group across 2 directories with 1 update (#7853)
* chore(deps): bump idna from 3.11 to 3.15 in /libs/cli (#7865)
* chore(deps): bump turbo from 2.9.7 to 2.9.14 in /libs/cli/js-monorepo-example (#7868)
* chore(deps): bump langsmith from 0.6.3 to 0.7.1 in /libs/cli/js-monorepo-example (#7854)
* chore(deps): bump langsmith from 0.7.32 to 0.8.0 in /libs/cli (#7791)
* chore(deps): bump langsmith from 0.5.20 to 0.6.3 in /libs/cli/js-monorepo-example (#7783)
* chore(deps): bump langsmith from 0.5.20 to 0.6.3 in /libs/cli/js-examples (#7782)
* chore(deps): bump the uv group across 2 directories with 1 update (#7769)

---

## 1.2.2  (2026-05-26T18:07:40Z)

Changes since 1.2.1

* chore(langgraph): bump version to 1.2.2 (#7914)
* fix(langgraph): assign stable IDs to id=None BaseMessages before DeltaChannel checkpoint writes (#7913)
* release(checkpoint): 4.1.1 (#7890)

---

## sdk==0.3.15  (2026-05-22T16:54:42Z)

Changes since sdk==0.3.14

* release(checkpoint): 4.1.1 (#7890)
* release(sdk-py): 0.3.15 (#7891)
* fix(sdk-py): percent-encode caller-supplied identifiers in URL paths (#7893)
* release(langgraph): 1.2.1 (#7883)
* chore(deps): bump idna from 3.11 to 3.15 in /libs/sdk-py (#7863)
* chore(deps): bump urllib3 from 2.6.3 to 2.7.0 in /libs/sdk-py (#7764)
* chore(deps): bump langsmith from 0.7.31 to 0.8.0 in /libs/sdk-py (#7789)
* release: bump alpha packages to official versions (#7775)
* chore(langgraph): bump langchain-core to 1.4.0 (#7767)
* feat(sdk-py): support metadata filter for crons search/count (#7737)
* chore(deps): bump ty from 0.0.23 to 0.0.33 in /libs/sdk-py (#7666)

---

## checkpoint==4.1.1  (2026-05-22T16:57:50Z)

Changes since checkpoint==4.1.0

* release(checkpoint): 4.1.1 (#7890)
* fix(checkpoint): restrict lc:2 envelope revival to default constructor (#7892)
* chore(deps): bump idna from 3.11 to 3.15 in /libs/checkpoint (#7860)
* chore(deps): bump langsmith from 0.7.31 to 0.8.0 in /libs/checkpoint (#7784)

---

## 1.2.1  (2026-05-21T18:33:24Z)

Changes since 1.2.0

* release(langgraph): 1.2.1 (#7883)
* feat(langgraph): add `before_builtins` opt-in for stream transformers (#7882)
* chore(deps): bump idna from 3.11 to 3.15 in /libs/langgraph (#7866)
* fix(langgraph): keep tool results out of v3 messages (#7838)
* chore(deps): bump langsmith from 0.7.31 to 0.8.0 in /libs/langgraph (#7788)

---

## 1.2.0  (2026-05-12T03:46:55Z)

Changes since 1.2.0a7

* release: bump alpha packages to official versions (#7775)
* feat(langgraph): durable error-handler resume across host crashes (#7773)
* feat(langgraph): add set_node_defaults() to StateGraph (#7747)
* chore(deps): bump urllib3 from 2.6.3 to 2.7.0 in /libs/langgraph (#7766)
* chore(deps): bump mistune from 3.2.0 to 3.2.1 in /libs/langgraph (#7733)
* chore(langgraph): bump langchain-core to 1.4.0 (#7767)
* feat(checkpoint): force delta channel snapshot after max supersteps since last snapshot (#7746)
* test(langgraph): de-flake heartbeat progress test (#7735)
* chore(langgraph): re-implement exit mode for delta channel (#7730)
* chore(deps): bump ty from 0.0.23 to 0.0.33 in /libs/sdk-py (#7666)
* docs(checkpoint): mark DeltaChannel and delta-history APIs as beta (#7732)
* chore(deps): bump jupyter-server from 2.17.0 to 2.18.0 in /libs/langgraph (#7713)
* feat(checkpoint-sqlite): override get_delta_channel_history with streaming walk (#7702)
* chore: "chore: minor clean up around checkpoint and delta channel" (#7706)
* chore: minor clean up around checkpoint and delta channel (#7705)

---