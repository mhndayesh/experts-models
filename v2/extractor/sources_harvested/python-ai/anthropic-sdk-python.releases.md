# anthropics/anthropic-sdk-python - last 20 releases (latest: v0.116.0)


## v0.116.0  (2026-07-02T19:07:55Z)

## 0.116.0 (2026-07-02)

Full Changelog: [v0.115.1...v0.116.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.115.1...v0.116.0)

### Features

* **api:** add agent-memory-2026-07-22 beta header ([e181d5c](https://github.com/anthropics/anthropic-sdk-python/commit/e181d5c1b233d5b0b313c78b27cf1dd27f620e74))

---

## v0.115.1  (2026-07-01T21:54:06Z)

## 0.115.1 (2026-07-01)

Full Changelog: [v0.115.0...v0.115.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.115.0...v0.115.1)

### Chores

* **api:** remove some nonfunctional types from the SDKs ([5e7c431](https://github.com/anthropics/anthropic-sdk-python/commit/5e7c431ef31b72b3f1f59902e678316fea14d983))

---

## v0.115.0  (2026-06-30T19:47:18Z)

## 0.115.0 (2026-06-30)

Full Changelog: [v0.114.0...v0.115.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.114.0...v0.115.0)

### Features

* **api:** add support for Managed Agents event delta streaming, agent overrides, reverse pagination, vault credential injection scoping, and agent and deployment webhook events ([8c23f7e](https://github.com/anthropics/anthropic-sdk-python/commit/8c23f7ef103c287362364c12503de85eb31f07fb))

---

## v0.114.0  (2026-06-30T17:48:39Z)

## 0.114.0 (2026-06-30)

Full Changelog: [v0.113.0...v0.114.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.113.0...v0.114.0)

### Features

* **api:** add support for claude-sonnet-5 ([b893033](https://github.com/anthropics/anthropic-sdk-python/commit/b893033b32951e0e2e04afa36a3a7eb016ae4b99))


### Bug Fixes

* **agent_toolset:** allow absolute paths that resolve inside workdir ([#121](https://github.com/anthropics/anthropic-sdk-python/issues/121)) ([0105529](https://github.com/anthropics/anthropic-sdk-python/commit/0105529fe15b1f80bbf9c56f4ae684fdfa10e2b3))

---

## v0.113.0  (2026-06-29T14:57:11Z)

## 0.113.0 (2026-06-29)

Full Changelog: [v0.112.0...v0.113.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.112.0...v0.113.0)

### Features

* **api:** add support for 20260318 web fetch and support tools ([88dbfb1](https://github.com/anthropics/anthropic-sdk-python/commit/88dbfb14a2a838eda889469ad7fe07a47618e85f))


### Bug Fixes

* async count_tokens missing output_format/output_config merge block ([#162](https://github.com/anthropics/anthropic-sdk-python/issues/162)) ([122c958](https://github.com/anthropics/anthropic-sdk-python/commit/122c95811566bf6f5cbc682ae0a74972ae75a223))


### Chores

* **api:** accept user profile ID's when counting tokens ([0b4d17a](https://github.com/anthropics/anthropic-sdk-python/commit/0b4d17a49d39e8224adbee6a97be0e8b1b7ebff5))
* **docs:** updates to descriptions and example values ([f3ab694](https://github.com/anthropics/anthropic-sdk-python/commit/f3ab694453326a2765623b9aafeb7588ea296325))

---

## v0.112.0  (2026-06-24T18:45:45Z)

## 0.112.0 (2026-06-24)

Full Changelog: [v0.111.0...v0.112.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.111.0...v0.112.0)

### Features

* **client:** add support for system.message streaming events ([2450d59](https://github.com/anthropics/anthropic-sdk-python/commit/2450d595731f9532080bb94eb8a43c0bd5189659))


### Bug Fixes

* **memory tool:** create parent directories with the correct permissions ([#135](https://github.com/anthropics/anthropic-sdk-python/issues/135)) ([f2fc2a9](https://github.com/anthropics/anthropic-sdk-python/commit/f2fc2a9e0ad8507e4108e9a6b85d023416c2f14c))


### Chores

* **api:** add support for new refusal category ([5ab533e](https://github.com/anthropics/anthropic-sdk-python/commit/5ab533e58ee99bcd2e5071bab91d99caee66aa6a))
* **api:** add support for sending User Profile ID in request headers ([83319be](https://github.com/anthropics/anthropic-sdk-python/commit/83319bed74f4414d54e0f4237d70b945ed671008))

---

## v0.111.0  (2026-06-18T17:31:32Z)

## 0.111.0 (2026-06-18)

Full Changelog: [v0.110.0...v0.111.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.110.0...v0.111.0)

### Features

* **helpers:** tag refusal-fallback middleware requests with fallback-refusal-middleware ([#96](https://github.com/anthropics/anthropic-sdk-python/issues/96)) ([2f8ac78](https://github.com/anthropics/anthropic-sdk-python/commit/2f8ac789506efc0719b06f1f646c9a98bb25ce7b))

---

## v0.110.0  (2026-06-18T17:18:34Z)

## 0.110.0 (2026-06-18)

Full Changelog: [v0.109.2...v0.110.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.109.2...v0.110.0)

### Features

* **api:** add support for new code_execution_20260120 tool ([5e23212](https://github.com/anthropics/anthropic-sdk-python/commit/5e23212dc0883174c879b97ef8e7e33ead4e8da5))


### Bug Fixes

* append x-stainless-helper across header merges instead of clobbering ([#105](https://github.com/anthropics/anthropic-sdk-python/issues/105)) ([922558e](https://github.com/anthropics/anthropic-sdk-python/commit/922558e2ce52e18863dab27bcc04067068827364))
* **bedrock:** preserve stream event type ([#1682](https://github.com/anthropics/anthropic-sdk-python/issues/1682)) ([b27e343](https://github.com/anthropics/anthropic-sdk-python/commit/b27e3439699174dbc41e34e2d6ef5cb1e2930c18))
* **helpers:** single source of truth for x-stainless-helper key + closed value vocabulary ([#95](https://github.com/anthropics/anthropic-sdk-python/issues/95)) ([e6f7a56](https://github.com/anthropics/anthropic-sdk-python/commit/e6f7a56bb624f4c946cb15ba7973fd6fe052e10f))

---

## v0.109.2  (2026-06-15T17:30:11Z)

## 0.109.2 (2026-06-15)

Full Changelog: [v0.109.1...v0.109.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.109.1...v0.109.2)

### Chores

* **api:** remove retired models from API and SDKs ([d4bcfcc](https://github.com/anthropics/anthropic-sdk-python/commit/d4bcfcc257bd0c97d5e75060bd19c97abddd9f49))

---

## v0.109.1  (2026-06-09T23:55:10Z)

## 0.109.1 (2026-06-09)

Full Changelog: [v0.109.0...v0.109.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.109.0...v0.109.1)

### Bug Fixes

* **api:** add `frontier_llm` refusal category ([d3a806b](https://github.com/anthropics/anthropic-sdk-python/commit/d3a806b454d8aaf5806db11c651deebe61836131))

---

## v0.109.0  (2026-06-09T20:04:14Z)

## 0.109.0 (2026-06-09)

Full Changelog: [v0.108.0...v0.109.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.108.0...v0.109.0)

### Features

* **api:** add support for Managed Agents deployments and environment variable credentials ([47633bf](https://github.com/anthropics/anthropic-sdk-python/commit/47633bff658d4aaced3cd920ef6782c48cf31a9a))

---

## v0.108.0  (2026-06-09T16:37:30Z)

## 0.108.0 (2026-06-09)

Full Changelog: [v0.107.1...v0.108.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.107.1...v0.108.0)

### Features

* **api:** add support for claude-mythos-5 and claude-fable-5, with support for server-side fallbacks on refusal ([6b76649](https://github.com/anthropics/anthropic-sdk-python/commit/6b76649f99bd782d2300f2a6aa3f4a3f040af324))
* **client:** adds client-side fallbacks middleware for API providers that do not support server-side fallbacks ([6b76649](https://github.com/anthropics/anthropic-sdk-python/commit/6b76649f99bd782d2300f2a6aa3f4a3f040af324))

---

## v0.107.1  (2026-06-07T17:18:45Z)

## 0.107.1 (2026-06-07)

Full Changelog: [v0.107.0...v0.107.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.107.0...v0.107.1)

### Bug Fixes

* **foundry:** send x-api-key header for API-key auth ([#62](https://github.com/anthropics/anthropic-sdk-python/issues/62)) ([1338141](https://github.com/anthropics/anthropic-sdk-python/commit/13381413d22ad14d85e66836c67cc8a13bd2b7bd)), closes [#1661](https://github.com/anthropics/anthropic-sdk-python/issues/1661)

---

## v0.107.0  (2026-06-06T17:13:25Z)

## 0.107.0 (2026-06-06)

Full Changelog: [v0.106.0...v0.107.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.106.0...v0.107.0)

### Features

* **api:** small updates to Managed Agents types ([72923f9](https://github.com/anthropics/anthropic-sdk-python/commit/72923f986f808597f86482a7eae4fba9a791e6ae))

---

## v0.106.0  (2026-06-05T21:13:11Z)

## 0.106.0 (2026-06-05)

Full Changelog: [v0.105.2...v0.106.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.105.2...v0.106.0)

### Features

* **api:** mark Claude Opus 4.1 as deprecated ([85068cc](https://github.com/anthropics/anthropic-sdk-python/commit/85068cc4cb42feecb80a378942cec71e1baa8dcf))


### Bug Fixes

* **client:** make Foundry client copy() and with_options() work ([94146ac](https://github.com/anthropics/anthropic-sdk-python/commit/94146acdc1c6f66f187d5a42e4afbb911e692fe8))
* **transform schema:** preserve $defs when schema root is a $ref ([#1642](https://github.com/anthropics/anthropic-sdk-python/issues/1642)) ([fc58e06](https://github.com/anthropics/anthropic-sdk-python/commit/fc58e06b78407b447c50dfea109c6fb300f4b97d))


### Chores

* **internal:** fix artifact url ([a6ed0c4](https://github.com/anthropics/anthropic-sdk-python/commit/a6ed0c4124d29989a568a27293dadf66e7ebcd6f))
* **internal:** fix branch names ([3b03370](https://github.com/anthropics/anthropic-sdk-python/commit/3b0337074f0bbab47bf7f5a2b76b4d240cff719a))
* **internal:** update private repo name ([7dbcb05](https://github.com/anthropics/anthropic-sdk-python/commit/7dbcb05706f1865afeee62fb06e400f5c4bf619e))


### Documentation

* point security reports to Anthropic's HackerOne program ([#10](https://github.com/anthropics/anthropic-sdk-python/issues/10)) ([80f2c97](https://github.com/anthropics/anthropic-sdk-python/commit/80f2c97b8e9534f9879945de11c11aba00cf8704))

---

## v0.105.2  (2026-05-29T00:20:59Z)

## 0.105.2 (2026-05-29)

Full Changelog: [v0.105.1...v0.105.2](https://github.com/anthropics/anthropic-sdk-python/compare/v0.105.1...v0.105.2)

---

## v0.105.1  (2026-05-29T00:07:37Z)

## 0.105.1 (2026-05-29)

Full Changelog: [v0.105.0...v0.105.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.105.0...v0.105.1)

### Chores

* **internal:** use Trusted Publishing for PyPI releases ([1d04fc5](https://github.com/anthropics/anthropic-sdk-python/commit/1d04fc52d2dd1f88e22808de2c53b0d66913631f))

---

## v0.105.0  (2026-05-28T16:52:38Z)

## 0.105.0 (2026-05-28)

Full Changelog: [v0.104.1...v0.105.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.104.1...v0.105.0)

### Features

* **api:** Add support for claude-opus-4-8, mid-conversation system blocks, and usage.output_tokens_details ([f18b014](https://github.com/anthropics/anthropic-sdk-python/commit/f18b01414b21b49943a6ba2cdaa30ff7dd6a3025))
* support custom file size caps ([#1825](https://github.com/anthropics/anthropic-sdk-python/issues/1825)) ([7e5f944](https://github.com/anthropics/anthropic-sdk-python/commit/7e5f944ad85bd99526d9df30dc034f657472adaa))


### Chores

* **examples:** rename managed-agents private-sandbox-worker to self-hosted-sandbox-worker ([#1822](https://github.com/anthropics/anthropic-sdk-python/issues/1822)) ([750f956](https://github.com/anthropics/anthropic-sdk-python/commit/750f956a535b9e4772951d6bf1abd81203f27d4e))


### Documentation

* replace literal newlines ([8f7f6c0](https://github.com/anthropics/anthropic-sdk-python/commit/8f7f6c0d1b5ffb9563affdcf3dd2410dc72ed1b4))

---

## v0.104.1  (2026-05-22T15:36:38Z)

## 0.104.1 (2026-05-21)

Full Changelog: [v0.104.0...v0.104.1](https://github.com/anthropics/anthropic-sdk-python/compare/v0.104.0...v0.104.1)

### Bug Fixes

* **streaming:** carry encrypted_content through beta compaction accumulator ([#1821](https://github.com/anthropics/anthropic-sdk-python/issues/1821)) ([f7a720c](https://github.com/anthropics/anthropic-sdk-python/commit/f7a720c514cc5e428b310f46249ca1c807894c2e))

---

## v0.104.0  (2026-05-21T20:01:49Z)

## 0.104.0 (2026-05-21)

Full Changelog: [v0.103.1...v0.104.0](https://github.com/anthropics/anthropic-sdk-python/compare/v0.103.1...v0.104.0)

### Features

* **api:** Add support for thinking-token-count beta for estimated tokens in thinking block deltas when streaming ([80d0fdf](https://github.com/anthropics/anthropic-sdk-python/commit/80d0fdf460d6cd4f190681fd2241baf8ed76cc5f))

---