# openai/openai-python - last 20 releases (latest: v2.45.0)


## v2.45.0  (2026-07-09T18:02:01Z)

## 2.45.0 (2026-07-09)

Full Changelog: [v2.44.0...v2.45.0](https://github.com/openai/openai-python/compare/v2.44.0...v2.45.0)

### Features

* **api:** gpt-5.6-sol updates ([039d1fe](https://github.com/openai/openai-python/commit/039d1feb264a2dca7195ba5028e9fb47a5e04987))


### Bug Fixes

* **api:** restore beta resource accessors ([2dfc130](https://github.com/openai/openai-python/commit/2dfc130b8f0fdb0049e075aac21aaef29482b4e3))


### Chores

* retrigger release automation ([7b61351](https://github.com/openai/openai-python/commit/7b61351b014bb6ca4623ff6cce7f32f45038a92e))

---

## v2.44.0  (2026-06-24T20:55:08Z)

## 2.44.0 (2026-06-24)

Full Changelog: [v2.43.0...v2.44.0](https://github.com/openai/openai-python/compare/v2.43.0...v2.44.0)

### Bug Fixes

* **auth:** prioritize first auth header ([797e336](https://github.com/openai/openai-python/commit/797e3362e222ae14e587a4543b76a54d8992d66c))

---

## v2.43.0  (2026-06-17T17:05:59Z)

## 2.43.0 (2026-06-17)

Full Changelog: [v2.42.0...v2.43.0](https://github.com/openai/openai-python/compare/v2.42.0...v2.43.0)

### Features

* **api:** update OpenAPI spec or Stainless config ([2254235](https://github.com/openai/openai-python/commit/22542358490ef8f31f0d373e17f7b791b3d983ca))

---

## v2.42.0  (2026-06-16T21:51:39Z)

## 2.42.0 (2026-06-16)

Full Changelog: [v2.41.1...v2.42.0](https://github.com/openai/openai-python/compare/v2.41.1...v2.42.0)

### Features

* **api:** admin spend_alerts ([6134198](https://github.com/openai/openai-python/commit/6134198a488996c4ff6fca4551afd55fb3294fdc))
* **api:** manual updates ([f337bf4](https://github.com/openai/openai-python/commit/f337bf43276c880d2daf09a5d7f9fc9a886c4bf2))
* **api:** update OpenAPI spec or Stainless config ([7015158](https://github.com/openai/openai-python/commit/7015158c3119acf57af6c20903587cef928530a9))


### Build System

* fix release workflow permissions ([#3389](https://github.com/openai/openai-python/issues/3389)) ([a526ee8](https://github.com/openai/openai-python/commit/a526ee813f085318fe3c6923ac3fa10c1cf56420))
* Use CI environment for examples API key ([#3394](https://github.com/openai/openai-python/issues/3394)) ([d64d811](https://github.com/openai/openai-python/commit/d64d811e82aff724397e32d593e50657fee3f905))

---

## v2.41.1  (2026-06-10T16:09:44Z)

## 2.41.1 (2026-06-05)

Full Changelog: [v2.41.0...v2.41.1](https://github.com/openai/openai-python/compare/v2.41.0...v2.41.1)

### Build System

* Remove scheduled release workflow trigger ([#3366](https://github.com/openai/openai-python/issues/3366)) ([2a91011](https://github.com/openai/openai-python/commit/2a91011abc21032db9566b98068afefb5fbb9b24))

---

## v2.41.0  (2026-06-03T22:39:25Z)

## 2.41.0 (2026-06-03)

Full Changelog: [v2.40.0...v2.41.0](https://github.com/openai/openai-python/compare/v2.40.0...v2.41.0)

### Features

* **api:** responses.moderation and chat_completions.moderation ([87e46c2](https://github.com/openai/openai-python/commit/87e46c25ac9ca8cff407b52ad9fb33e326c059d6))

---

## v2.40.0  (2026-06-01T21:48:03Z)

## 2.40.0 (2026-06-01)

Full Changelog: [v2.39.0...v2.40.0](https://github.com/openai/openai-python/compare/v2.39.0...v2.40.0)

### Features
* **api:** Add Amazon Bedrock Responses support 

### Bug Fixes

* **api:** allow setting bedrock api keys on the client directly ([4d5bfde](https://github.com/openai/openai-python/commit/4d5bfdec37fa8a2b2a0413724755e586e627e28d))

---

## v2.39.0  (2026-06-01T18:58:01Z)

## 2.39.0 (2026-06-01)

Full Changelog: [v2.38.0...v2.39.0](https://github.com/openai/openai-python/compare/v2.38.0...v2.39.0)

### Features

* **api:** workload identity in audit logs, additional_tools item in responses, fix ActionSearch.query to be optional. ([ab60d7a](https://github.com/openai/openai-python/commit/ab60d7a52c310bb0490ff36b8bdc33b8d4ea725f))

---

## v2.38.0  (2026-05-21T21:23:25Z)

## 2.38.0 (2026-05-21)

Full Changelog: [v2.37.0...v2.38.0](https://github.com/openai/openai-python/compare/v2.37.0...v2.38.0)

### Features

* **api:** api update ([33d1d01](https://github.com/openai/openai-python/commit/33d1d013250053886a73d178136e6bd1b09df059))
* **api:** manual updates ([a21700a](https://github.com/openai/openai-python/commit/a21700a2cd510cb9e6c88065ac8e942d4c041aa8))
* **api:** update OpenAPI spec or Stainless config ([00265c5](https://github.com/openai/openai-python/commit/00265c5daba4d2481452ad35220f1556dab6bcf6))


### Chores

* **api:** docs updates ([ee10152](https://github.com/openai/openai-python/commit/ee101520d49e22c09cf8096f8cbb3848ea58a1f9))
* check release PR custom code sync ([2638779](https://github.com/openai/openai-python/commit/2638779a5b8fffaa8fdb6eebc1d734f15d2491f8))
* remove release automation trigger ([bd6eea5](https://github.com/openai/openai-python/commit/bd6eea559f2996d914258a65e645981bdce3cad4))
* trigger release automation ([f62d082](https://github.com/openai/openai-python/commit/f62d08201eea8e08d4bb3385662f934d4adccb29))

---

## v2.37.0  (2026-05-15T22:30:20Z)

## 2.37.0 (2026-05-13)

Full Changelog: [v2.36.0...v2.37.0](https://github.com/openai/openai-python/compare/v2.36.0...v2.37.0)

### Features

* **api:** add service_tier parameter to responses compact method ([625827c](https://github.com/openai/openai-python/commit/625827c5509ece3c40e5002be37a9bd9d91b5374))
* **internal/types:** support eagerly validating pydantic iterators ([7e527bc](https://github.com/openai/openai-python/commit/7e527bc927cc58b74d7619abf7f1fbcfff8bddfa))
* Remove unnecessary client_id when using workload identity provider for auth ([c39ea8d](https://github.com/openai/openai-python/commit/c39ea8d12a010052d7f02cebe8daabd2d1f89597))


### Bug Fixes

* **client:** add missing f-string prefix in file type error message ([c85ebd9](https://github.com/openai/openai-python/commit/c85ebd935cb4b80e7e97ce255437684f6411fb00))

---

## v2.36.0  (2026-05-07T17:33:02Z)

## 2.36.0 (2026-05-07)

Full Changelog: [v2.35.1...v2.36.0](https://github.com/openai/openai-python/compare/v2.35.1...v2.36.0)

### Features

* **api:** manual updates ([13c639c](https://github.com/openai/openai-python/commit/13c639cc7d57e4fbd4406563511e15eeb88a54b2))
* **api:** realtime 2 ([8fe0ab8](https://github.com/openai/openai-python/commit/8fe0ab87e67eeb3cc27426b50093845229520f0e))

---

## v2.35.1  (2026-05-06T21:37:58Z)

## 2.35.1 (2026-05-06)

Full Changelog: [v2.35.0...v2.35.1](https://github.com/openai/openai-python/compare/v2.35.0...v2.35.1)

### Bug Fixes

* **api:** fix imagegen `size` enum regression ([4484653](https://github.com/openai/openai-python/commit/44846536bc3b02c393daa5bae70a85de04c7f621))

---

## v2.35.0  (2026-05-06T16:36:40Z)

## 2.35.0 (2026-05-06)

Full Changelog: [v2.34.0...v2.35.0](https://github.com/openai/openai-python/compare/v2.34.0...v2.35.0)

### Features

* **api:** update image 2 ([0ba55d7](https://github.com/openai/openai-python/commit/0ba55d7569565045426e1587906a70d5682a4bba))
* **api:** manual updates ([72bf67a](https://github.com/openai/openai-python/commit/72bf67acbc9f030c20db3d5a1a74ea6d67d55f51))


### Chores

* remove legacy python cli ([32f36e4](https://github.com/openai/openai-python/commit/32f36e447d02c3124af8ab48fcc3537df2fed66e))
* rename legacy python cli entrypoint ([a3b182d](https://github.com/openai/openai-python/commit/a3b182d6d2c2e6fe1d53ca7550b2d43e0f8b2cd3))


### Documentation

* **api:** update top_logprobs parameter description across chat and responses ([f9d339f](https://github.com/openai/openai-python/commit/f9d339fcea63feaa1bdf918a4599f2b032c83517))

---

## v2.34.0  (2026-05-04T17:33:53Z)

## 2.34.0 (2026-05-04)

Full Changelog: [v2.33.0...v2.34.0](https://github.com/openai/openai-python/compare/v2.33.0...v2.34.0)

### Features

* **api:** add external_key_id to projects, email/metadata params to users, update types ([2d232ee](https://github.com/openai/openai-python/commit/2d232eebb2fe021bb21f2576b17d1d588f81a608))
* **api:** add support for Admin API Keys per endpoint ([b8b176a](https://github.com/openai/openai-python/commit/b8b176af84172f27d2fde8dca062ca4c41f94bf7))
* **api:** admin API updates ([4ae1138](https://github.com/openai/openai-python/commit/4ae1138ae1f76e81a2267e4deb45b435c10774d5))
* **api:** manual updates ([c1870f1](https://github.com/openai/openai-python/commit/c1870f1b881bb914e4e62a6c8b08d4c2b9a6fd54))
* **api:** manual updates ([f6bb9c7](https://github.com/openai/openai-python/commit/f6bb9c7d7bdcc45425d37722358bed097e83d493))
* support setting headers via env ([1e89d8b](https://github.com/openai/openai-python/commit/1e89d8b56aba12f99a8ef2b1b78fdee84751275a))


### Bug Fixes

* allow explicit Azure auth headers ([a0626ba](https://github.com/openai/openai-python/commit/a0626babf0548fb03cf3c2d054da116dd6466701))
* **api:** correct prompt_cache_retention enum value from in-memory to in_memory ([d47d9f0](https://github.com/openai/openai-python/commit/d47d9f0f79c612c4d14005a0a3cf44e1968c9bff))
* **api:** preserve python api key attribute type ([62607f6](https://github.com/openai/openai-python/commit/62607f61c542ed559ef114849e31307c0c290286))
* **api:** resolve python auth type checks ([42a31a7](https://github.com/openai/openai-python/commit/42a31a7efb6784633108c1a73e1779ed79ab8bed))
* **api:** support admin api key auth ([f029eb9](https://github.com/openai/openai-python/commit/f029eb937f976110c1a67b9342525a38a214072e))
* avoid bearer fallback for admin auth ([22e01a8](https://github.com/openai/openai-python/commit/22e01a8cf791a143ecc576f46de50eee9b3c2147))
* preserve selected auth credentials ([0d27f9d](https://github.com/openai/openai-python/commit/0d27f9dbd3b2ae82b2e8c2eeb9e7e78f3edecdf1))
* require bearer auth for stream helpers ([d055539](https://github.com/openai/openai-python/commit/d0555390bcf4a704c10d318c7de2fe006750c3d0))
* **types:** correct created_at and completed_at to float in Response ([7da4b88](https://github.com/openai/openai-python/commit/7da4b88c1985028f7ee9a98b919e71f863f979f0))
* **types:** correct timestamp types to int in Response model ([e55631c](https://github.com/openai/openai-python/commit/e55631c868b1d0b720fda0abdbc342787cd95e2c))
* use correct field name format for multipart file arrays ([9ee4825](https://github.com/openai/openai-python/commit/9ee482576c2bd6b33b6cf7458c37ab2e7d5bc725))


### Performance Improvements

* **client:** optimize file structure copying in multipart requests ([dca474e](https://github.com/openai/openai-python/commit/dca474e5beac7cc8e05855f042c3227843030c1b))


### Chores

* **internal:** more robust bootstrap script ([9ec1600](https://github.com/openai/openai-python/commit/9ec1600d48fda10abb144b2a62d07c5abd7e9ab1))
* **internal:** reformat pyproject.toml ([12ad57b](https://github.com/openai/openai-python/commit/12ad57b8da5b5c0615641af273d4bbf2981d6bf7))
* **tests:** bump steady to v0.22.1 ([486dfed](https://github.com/openai/openai-python/commit/486dfedfec8484bb00318b0ea798c2260f7a720c))


### Documentation

* **api:** add rate limit and vector store info to files create ([4f776df](https://github.com/openai/openai-python/commit/4f776df78d757fdbf25662c4be98b5c98183aaaf))
* **api:** update files rate limit documentation ([b141a20](https://github.com/openai/openai-python/commit/b141a20e948b5af3b8fbe4261798c191d2857b4a))

---

## v2.33.0  (2026-04-28T14:03:52Z)

## 2.33.0 (2026-04-28)

Full Changelog: [v2.32.0...v2.33.0](https://github.com/openai/openai-python/compare/v2.32.0...v2.33.0)

### Features

* **api:** api update ([18f834a](https://github.com/openai/openai-python/commit/18f834a54f92ea827452471a46a4f442f251e2c8))


### Bug Fixes

* **api:** correct prompt_cache_retention enum value from in-memory to in_memory ([#1822](https://github.com/openai/openai-python/issues/1822)) ([f9d2d13](https://github.com/openai/openai-python/commit/f9d2d1359688a6247ecba858fc687173c480c9c8))


### Chores

* **ci:** remove release-doctor workflow ([00b2091](https://github.com/openai/openai-python/commit/00b20910e3539842f21d86ab5928fb5216d3a765))

---

## v2.32.0  (2026-04-15T22:27:40Z)

## 2.32.0 (2026-04-15)

Full Changelog: [v2.31.0...v2.32.0](https://github.com/openai/openai-python/compare/v2.31.0...v2.32.0)

### Features

* **api:** Add detail to InputFileContent ([60de21d](https://github.com/openai/openai-python/commit/60de21d1fcfbcadea0d9b8d884c73c9dc49d14ff))
* **api:** add OAuthErrorCode type ([0c8d2c3](https://github.com/openai/openai-python/commit/0c8d2c3b44242c9139dc554896ea489b56e236b8))
* **client:** add event handler implementation for websockets ([0280d05](https://github.com/openai/openai-python/commit/0280d0568f706684ecbf0aabf3575cdcb7fd22d5))
* **client:** allow enqueuing to websockets even when not connected ([67aa20e](https://github.com/openai/openai-python/commit/67aa20e69bc0e4a3b7694327c808606bfa24a966))
* **client:** support reconnection in websockets ([eb72a95](https://github.com/openai/openai-python/commit/eb72a953ea9dc5beec3eef537be6eb32292c3f65))


### Bug Fixes

* ensure file data are only sent as 1 parameter ([c0c2ecd](https://github.com/openai/openai-python/commit/c0c2ecd0f6b64fa5fafda6134bb06995b143a2cf))


### Documentation

* improve examples ([84712fa](https://github.com/openai/openai-python/commit/84712fa0f094b53151a0fe6ac85aa98018b2a7e2))

---

## v2.31.0  (2026-04-08T21:01:00Z)

## 2.31.0 (2026-04-08)

Full Changelog: [v2.30.0...v2.31.0](https://github.com/openai/openai-python/compare/v2.30.0...v2.31.0)

### Features

* **api:** add phase field to conversations message ([3e5834e](https://github.com/openai/openai-python/commit/3e5834efb39b24e019a29dc54d890c67d18cbb54))
* **api:** add web_search_call.results to ResponseIncludable type ([ffd8741](https://github.com/openai/openai-python/commit/ffd8741dd38609a5af0159ceb800d8ddba7925f8))
* **client:** add support for short-lived tokens ([#1608](https://github.com/openai/openai-python/issues/1608)) ([22fe722](https://github.com/openai/openai-python/commit/22fe7228d4990c197cd721b3ad7931ad05cca5dd))
* **client:** support sending raw data over websockets ([f1bc52e](https://github.com/openai/openai-python/commit/f1bc52ef641dfca6fdf2a5b00ce3b09bff2552f5))
* **internal:** implement indices array format for query and form serialization ([49194cf](https://github.com/openai/openai-python/commit/49194cfa711328216ff131d6f65c9298822a7c51))


### Bug Fixes

* **client:** preserve hardcoded query params when merging with user params ([92e109c](https://github.com/openai/openai-python/commit/92e109c3d9569a942e1919e75977dc13fa015f9a))
* **types:** remove web_search_call.results from ResponseIncludable ([d3cc401](https://github.com/openai/openai-python/commit/d3cc40165cd86015833d15167cc7712b4102f932))


### Chores

* **tests:** bump steady to v0.20.1 ([d60e2ee](https://github.com/openai/openai-python/commit/d60e2eea7f6916540cd4ba901dceb07051119da4))
* **tests:** bump steady to v0.20.2 ([6508d47](https://github.com/openai/openai-python/commit/6508d474332d4e82d9615c0a9a77379f9b5e4412))


### Documentation

* **api:** update file parameter descriptions in vector_stores files and file_batches ([a9e7ebd](https://github.com/openai/openai-python/commit/a9e7ebd505b9ae90514339aa63c6f1984a08cf6b))

---

## v2.30.0  (2026-03-25T22:08:18Z)

## 2.30.0 (2026-03-25)

Full Changelog: [v2.29.0...v2.30.0](https://github.com/openai/openai-python/compare/v2.29.0...v2.30.0)

### Features

* **api:** add keys field to Click/DoubleClick/Drag/Move/Scroll computer actions ([ee1bbed](https://github.com/openai/openai-python/commit/ee1bbeddbb38dab817557412dc106354409bb950))


### Bug Fixes

* **api:** align SDK response types with expanded item schemas ([f3f258a](https://github.com/openai/openai-python/commit/f3f258a9d4d19db3fb0c6c35e25ad3cedbe71254))
* sanitize endpoint path params ([89f6698](https://github.com/openai/openai-python/commit/89f66988fde790c0c83ff8b876d1e1b10d616367))
* **types:** make type required in ResponseInputMessageItem ([cfdb167](https://github.com/openai/openai-python/commit/cfdb1676ea0550840330a58f1a31a40a41a0a53f))


### Chores

* **ci:** skip lint on metadata-only changes ([faa93e1](https://github.com/openai/openai-python/commit/faa93e19a1d5c30c7dd672a08dbbdbb3c0374714))
* **internal:** update gitignore ([c468477](https://github.com/openai/openai-python/commit/c468477f1546579618865a726e35a685cffeacd9))
* **tests:** bump steady to v0.19.4 ([f350af8](https://github.com/openai/openai-python/commit/f350af86c13ade0237778010d264c55fda443354))
* **tests:** bump steady to v0.19.5 ([5c03401](https://github.com/openai/openai-python/commit/5c0340128fc1a416e2dfdc6ab4b05f1e954e8482))
* **tests:** bump steady to v0.19.6 ([b6353b8](https://github.com/openai/openai-python/commit/b6353b8411d31dcc95875d801ce9e90a21e0fd52))
* **tests:** bump steady to v0.19.7 ([1d654be](https://github.com/openai/openai-python/commit/1d654bea74ac9c3d43302587f98f33cfff502e48))


### Refactors

* **tests:** switch from prism to steady ([4a82035](https://github.com/openai/openai-python/commit/4a82035669b739d16a0e85d4ded778d51e061948))

---

## v2.29.0  (2026-03-17T17:53:05Z)

## 2.29.0 (2026-03-17)

Full Changelog: [v2.28.0...v2.29.0](https://github.com/openai/openai-python/compare/v2.28.0...v2.29.0)

### Features

* **api:** 5.4 nano and mini model slugs ([3b45666](https://github.com/openai/openai-python/commit/3b456661f77ca3196aceb5ab3350664a63481114))
* **api:** add /v1/videos endpoint to batches create method ([c0e7a16](https://github.com/openai/openai-python/commit/c0e7a161a996854021e9eb69ea2a60ca0d08047f))
* **api:** add defer_loading field to ToolFunction ([3167595](https://github.com/openai/openai-python/commit/3167595432bdda2f90721901d30ad316db49323e))
* **api:** add in and nin operators to ComparisonFilter type ([664f02b](https://github.com/openai/openai-python/commit/664f02b051af84e1ca3fa313981ec72fdea269b3))


### Bug Fixes

* **deps:** bump minimum typing-extensions version ([a2fb2ca](https://github.com/openai/openai-python/commit/a2fb2ca55142c6658a18be7bd1392a01f5a83f35))
* **pydantic:** do not pass `by_alias` unless set ([8ebe8fb](https://github.com/openai/openai-python/commit/8ebe8fbcb011c6a005a715cae50c6400a8596ee0))


### Chores

* **internal:** tweak CI branches ([96ccc3c](https://github.com/openai/openai-python/commit/96ccc3cca35645fd3140f99b0fc8e55545065212))

---

## v2.28.0  (2026-03-13T19:55:50Z)

## 2.28.0 (2026-03-13)

Full Changelog: [v2.27.0...v2.28.0](https://github.com/openai/openai-python/compare/v2.27.0...v2.28.0)

### Features

* **api:** custom voices ([50dc060](https://github.com/openai/openai-python/commit/50dc060b55767615419219ef567d31210517e613))

---