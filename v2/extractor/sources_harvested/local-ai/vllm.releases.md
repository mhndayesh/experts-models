# vllm-project/vllm - last 20 releases (latest: v0.25.1)


## v0.25.1  (2026-07-14T08:51:20Z)

# vLLM v0.25.1

## Highlights

This release features 2 commits from 2 contributors (1 new)!

v0.25.1 is a patch release containing two targeted bug fixes on top of v0.25.0.

### Bug Fixes
* **Avoid blocking model launching when no system FFmpeg is available for TorchCodec** (#47888). Previously `import torchcodec` raised a `RuntimeError` at import time when system FFmpeg was missing, which blocked startup (e.g. `vllm serve Qwen/Qwen3-VL-2B-Instruct`) even when TorchCodec was not in use. The error is now deferred to runtime so it only surfaces if TorchCodec is actually needed.
* **Guard mixed-dtype allreduce RMSNorm quant fusions** (#48330). The fused FlashInfer allreduce + RMSNorm + static-quantization patterns could match graphs where the activation and RMSNorm weight dtypes differ (e.g. a BF16 residual stream with an FP32 Gemma/Qwen-style RMSNorm weight in NVFP4 models), corrupting the hidden state and producing garbage output such as repeated `!!!!!` tokens. A dtype-match guard now routes incompatible mixed-dtype graphs to the safe path, while same-dtype models retain the full allreduce + RMSNorm + quant fusion.

## Contributors

@Isotr0py, @hugo-cen

## New Contributors

* @hugo-cen made their first contribution in https://github.com/vllm-project/vllm/pull/48330

---

## v0.25.0  (2026-07-11T20:06:44Z)

# vLLM v0.25.0 Release Notes

## Highlights

This release features 558 commits from 232 contributors (64 new)!

* **Model Runner V2 is now the default for all dense models** (#44443). Building on quantized-model support from the previous release, MRv2 is now the standard execution path, with new support for EVS (#46535), realtime embeddings (#46762), prefix caching for Mamba hybrid models (#42406), multimodal-prefix bidirectional attention (#46942), and dynamic speculative decoding compatible with full CUDA graphs (#45953).
* **PagedAttention has been removed** (#47361). The legacy attention implementation is deleted now that V1/MRv2 backends are the standard path.
* **The Transformers modeling backend is now as fast as native vLLM** (#47187), and gained FP8 MoE support (#46820), CUDA graph + embed scaling fixes (#48010), and migration of GPTBigCode/Starcoder2 (#30966) and RoBERTa (#47452).
* **New models**: LLaVA-OneVision-2 (#44785), Unlimited OCR (#46564, #47102), MOSS-Transcribe-Diarize (#47729), openai/privacy-filter (#41026), and Hy3 (#47192). GLM-5 / DeepSeek-V3.2 landed in the model zoo (#46808) with GLM-5.2 tuning, and MiniMax-M3 gained pipeline parallelism (#45810) and NVFP4 support (#46756).
* **New Streaming Parser Engine** (#46610) — a unified tool-call/reasoning parsing framework, with a new Kimi k2.5/k2.6/k2.7 parser and ports of seed_oss (#46314) and DeepSeek V4 (#45877). The Rust frontend continues to mature with HTTPS/mTLS (#45890), a DP supervisor (#47076), and profiler control routes (#46306).
* **Universal speculative decoding for heterogeneous vocabularies (TLI)** (#38174), plus new DSpark (#46995) and DFlash (#46770, #46853) drafters.

### Model Support
* New models: LLaVA-OneVision-2 (#44785), Unlimited OCR (#46564) with a Triton R-SWA backend (#47102), MOSS-Transcribe-Diarize (#47729), openai/privacy-filter (#41026), Hy3 with token-suffix and JSON Schema array support (#47192).
* GLM-5 family: GLM-5 / DeepSeek-V3.2 added to the model zoo (#46808), GLM-5.2 FP32 gate (#47410), GLM MTP post-final-norm fix (#47448), GLM4V startup fix (#47155).
* MiniMax-M3: pipeline parallelism (#45810), streaming reasoning parsing (#45718), and `tok_sparse_select` from MSA replacing Triton kernels (#47502).
* Transformers backend: now as fast as native vLLM (#47187), FP8 MoE fix (#46820), embed scaling + CUDA graph fix (#48010), GPTBigCode/Starcoder2 (#30966) and RoBERTa (#47452) migration, M-RoPE `mm_token_type_ids` fix (#46552), tied-embedding `lm_head.bias` fix (#46835).
* Voxtral: migrated to mistral-common 1.11.5 audio API (#46705) and realtime token-feedback hang fix (#44461).
* Gemma family: Gemma4 sliding-window/FA4 attention fixes (#47217, #47332), Gemma4 MTP quant_config fix (#47091); DiffusionGemma tensor parallelism (#45719) and HF stability-window semantics (#45965).
* Other fixes: MiniCPM-V 4.6 language-backbone LoRA (#46740) and placeholder grid fix (#45918), pooled Whisper sliding-window sizing (#47071, #47437), Mamba/Mamba2 checkpoint-without-`architectures` crash fix (#46037), DeepSeek-V2 hidden-size and aux-hidden-state fixes (#46986, #46973).

### Engine Core
* Model Runner V2: default for all dense models (#44443); EVS (#46535), realtime embeddings (#46762), Mamba hybrid prefix caching (#42406), multimodal-prefix bidirectional attention (#46942), cross-attention warmup/block-table fixes (#46753, #47308), Mamba2 crash fix (#47428), scheduling slot accounting (#46974), model-ref cleanup on shutdown (#47483), bounded memory for large-logprobs requests (#46746).
* Speculative decoding: universal spec decode for heterogeneous vocabularies (TLI) (#38174); DSpark drafter + speculators checkpoint support (#46995, #47093); DFlash backend selection (#46770), per-layer RMSNorm fusion (#46761), CPU support (#44029), SWA+DFlash for MiMo (#46104), Laguna XS.2.1 drafter (#46853); MTP for Bailing hybrid models (#44880); block verification for rejection sampling (#46781); reduced TP communication for draft tokens (#46448).
* Sleep mode: pluggable sleep-mode backend abstraction (RFC #34303, #44074) with communicator-agnostic capability flags (#47243).
* Attention: FlashAttention block-size restriction removed for hybrid models (#36701), `FLASH_ATTN_MLA_SPARSE` Hopper sparse-MLA backend (#46189), DCP + FP8 KV cache in MLA decode (#44044), XQA decode kernels (#43232).
* KV offloading: tiering metric plumbing (#45959), request lifecycle fix (#46284), batched lookup in C (#46713), `LookupResult` enum (#46363).
* Misc: `VLLM_GPU_SYNC_CHECK` env var (#44800), VRAM semaphore infrastructure (#44465), skip detokenization in online beam search (#46422), several int32-overflow fixes in sampler/attention kernels (#46560, #47383, #47671).

### Hardware & Performance
* GLM-5.2 / DeepSeek: `fused_indexer_q_rope_quant` Triton kernel (1.9–3.3% E2E throughput) (#46862), reduce-scatter MoE all-reduce (3.1–3.2% E2E) (#46635), op fusion for GLM5/DSV3.2 (#46876), `token_to_req_indices` cache for DSv4 (5–6x kernel speedup) (#47474), better DSv4 MXFP8 kernel (#47229), redundant-op removal (#47198, #46651).
* NVIDIA/Blackwell: FlashInfer fused all-reduce tuned for world_size=16 on GB300 (#46392), restored NVFP4 swizzled-scale zero-init to recover Blackwell decode throughput (#45739), CuTeDSL/FA4-MLA warmup infrastructure (#46182), skip cooperative top-K on SM120 (#47164), B12x backend for non-gated MoEs (#43328).
* Kernels: Helion `fused_qk_norm_rope` (#44010) and `silu_and_mul_per_block_quant` (#43994), Triton MLA logits workspace (#46819), swap-AB optimization for fused MoE (#36559), vectorized fp32 `moe_sum` supporting any top-k (#46643), blocking CUDA events to avoid busy-polling the driver lock (#47081).
* AMD/ROCm: moved to torch 2.11 stable ABI (#47128); AITER FlashAttention MLA prefill backend `ROCM_AITER_FA` (#45033); fused shared-expert for GLM-4.5/6/7 (#44313) and MiniMax-M3 (#46474, #46545); AITER MoE optimization for DeepSeek-V4 (#46122); AITER custom all-reduce in CudaCommunicator (#46065); INT3 quantization for quickreduce (#45666).
* Intel XPU: W8A8 FP8 linear kernel with multi-granularity quant (#43645), pipeline-parallel accuracy fix (#47253), uniform-batch CUDA graph for FA2 (#46555), route mm_prefix models to Triton attention (#47688), C++ `get_memory_info` (#47134).
* CPU: accelerated unquantized MoE for AArch64 (#46353), macOS/Apple Silicon hang fix via OpenMP (#46769) and broken-install fix (#47457), compressed-tensor w8a8 int8 MoE (#42920), Mamba ShortConv (#35059), chunked prefill + prefix caching for Qwen3.5 (#46202), faster gelu via tanh AOR (#44639).
* RISC-V: RVV path for W4A8 INT4 GEMM (#45269), BF16 on VLEN=256 hardware (#45243), reduced LMUL pressure in INT4 LUT dequant (#47538). POWER: fp16 support on PowerPC (#46135).
* Platform: accelerator-agnostic `get_memory_info` (#44825).

### Large Scale Serving & Distributed
* Sequence parallelism without requiring DP, 1.9–5.0% E2E throughput improvement (#47070).
* Distributed: NCCL symmetric memory extended to AllGather and ReduceScatter (#46703), FlashInfer all-reduce defaults to MNNVL on single node (#47219, #47589), fault-tolerance backend to detect all2all peer faults and prevent corrupted output (#43637).
* Data parallel: throttle prefills based on local prefill work (#46532), rotate load-balancer tie-break to avoid engine bias (#47420), DP supervisor via the Rust frontend (#47076), DP MTP hang fix (#40589).
* PD disaggregation: secondary-tier implementation (#42285), Mooncake connector GDN (Qwen3.5) + MLA (DeepSeek-V4-Flash) support (#46807), NIXL Mamba1 support (#45019), MultiConnector `kv_transfer_params` merging (#46777), usage field exposed for disaggregated serving (#42748).
* DCP: FlashInfer MLA support (#43729), FLASHINFER_MLA_SPARSE support (#46076), LSE log-base fixes (#47079); Mooncake parallelized KV load (#45971) and DCP>1 lookup fix (#46855).
* ROCm: stabilized high-throughput DBO for DP+EP (#46990), EPLB for Quark OCP MXFP4 MoE (#47220).

### Quantization
* 2/3/5/6/7-bit pack-quantized weight-only inference (Humming) (#46389), Triton INT4 per-token-head KV cache quantization (#40835).
* NVFP4: fused weight dequantization with compute in the MoE MLP Triton kernel (#44667), NVFP4 KV cache with skip-layers sliding window (#42890), MiniMax-M3 ModelOpt NVFP4 support (#46756).
* FP8: weights padding for per-block online quantization (#44763); deprecated the old FP8 online MoE quantization class (#44514).
* Marlin: thread-tile padding extended to MoE (WNA16 + FP8/MXFP8) (#45703), int8 grouped WNA16 MoE (#47154); FlashInfer MXINT4 MoE for gated SiLU (#46518).
* Fixes: W8A8 int-quant scheme-selection regression (#46860), tied quantized embeddings for ModelOpt Gemma4 (#45544), NVFP4+MTP crash on Qwen3Next (#46316), ModelOpt mixed-precision for sparse configs (#47318), CPU w4a8_int8 MoE path (#46739), actionable error on group-size/TP mismatch (#46230).

### API & Frontend
* Streaming Parser Engine (#46610): unified tool-call/reasoning parsing with a new Kimi k2.5/k2.6/k2.7 parser; ported seed_oss (#46314) and DeepSeek V4 (#45877).
* OpenAI compatibility: Responses API namespace tools (#47024), per-request timing `metrics` field on Chat/Completions responses (#46768), token offsets on render endpoints (#44226), `return_loss_mask` for training-data generation (#46846), HTTP 422 for unprocessable image URLs (#47165).
* gpt-oss / Harmony: dedicated Harmony renderer (#46800), `process_eos()` flush (#46437), raw-output recovery on non-terminal parse (#47062, #47379).
* Rust frontend: static HTTPS and mTLS for HTTP and gRPC (#45890), DP supervisor (#47076), profiler control routes (#46306), `repetition_detection` sampling param (#46684), unified/combined parser interface (#46583), reduced multimodal tensor copies (#47581), plus many parser and validation fixes.
* Video: TorchCodec added as a video decoding backend (#46609).
* CLI/UX: TTFT and TPS printing in `vllm chat` (#46775), `model_class_overrides` for development/debugging (#47148).
* Tooling/validation: many tool-parser fixes (Kimi K2 IDs #46344, PoolsideV1 #46486/#47311, non-ASCII arguments #46308, `thinking_token_budget` re-entry #43757); rejection of invalid config values (#44070, #44002, #46612) and degenerate `structured_outputs` that crash EngineCore (#45346).

### Security
* Prevent image decompression-bomb OOM denial of service (#47010).
* Prevent an infinite loop in `split_audio` with NaN audio samples (#46463).
* Bound tokenizer work when an explicit `truncation_side` is set (#47007).
* Block request-level GPU video backend selection (#47259).
* Document the gRPC interface as insecure, for private use only (#45903).

### Dependencies
* FlashInfer 0.6.13 (#46683), tpu-inference v0.23.0 (#46568), aiter 0.1.16.post2 (#46692), vllm_xpu_kernels v0.1.10.1 (#46607), huggingface-hub v1.22.0 (#47551).
* DeepGEMM updated to enable SM120 support (#47304), FlashAttention 3 built against the torch stable API (#46644), Rust frontend TLS switched from rustls to native-tls/OpenSSL (#46696).

### Deprecations & Removals
* **PagedAttention deleted** (#47361).
* Models removed: Baichuan (#46362), Aquila (#46605), Grok (#46706), Tarsier / Tarsier2 (#47143), AyaVision / MusicFlamingo (#47263), Mantis (#46806).
* Deprecated the old FP8 online MoE quantization class (#44514); legacy `api_server.py` moved to the examples directory (#46783); `gptq_marlin` removed from supported ROCm quant schemes (#46655).

## New Contributors

* @aaarkai made their first contribution in https://github.com/vllm-project/vllm/pull/44610
* @Acaciasama made their first contribution in https://github.com/vllm-project/vllm/pull/45850
* @ACEEE-1222 made their first contribution in https://github.com/vllm-project/vllm/pull/47716
* @adamkbaranowski made their first contribution in https://github.com/vllm-project/vllm/pull/46853
* @AgenticSpark made their first contribution in https://github.com/vllm-project/vllm/pull/46071
* @AIvashov made their first contribution in https://github.com/vllm-project/vllm/pull/42748
* @akinsella made their first contribution in https://github.com/vllm-project/vllm/pull/47165
* @aldenlobo made their first contribution in https://github.com/vllm-project/vllm/pull/45961
* @alex101-ops made their first contribution in https://github.com/vllm-project/vllm/pull/44880
* @aman0603 made their first contribution in https://github.com/vllm-project/vllm/pull/46945
* @Aneureka made their first contribution in https://github.com/vllm-project/vllm/pull/46838
* @ArsalanShakil made their first contribution in https://github.com/vllm-project/vllm/pull/46236
* @ayush1399 made their first contribution in https://github.com/vllm-project/vllm/pull/47091
* @blasrodri made their first contribution in https://github.com/vllm-project/vllm/pull/46827
* @calvarado2004 made their first contribution in https://github.com/vllm-project/vllm/pull/46177
* @chengzheng345 made their first contribution in https://github.com/vllm-project/vllm/pull/44785
* @cpersson-amd made their first contribution in https://github.com/vllm-project/vllm/pull/47519
* @cyq1017 made their first contribution in https://github.com/vllm-project/vllm/pull/46101
* @davispuh made their first contribution in https://github.com/vllm-project/vllm/pull/35232
* @decarpentierg made their first contribution in https://github.com/vllm-project/vllm/pull/46552
* @eparshut made their first contribution in https://github.com/vllm-project/vllm/pull/47467
* @fenghourun made their first contribution in https://github.com/vllm-project/vllm/pull/47384
* @fjosw made their first contribution in https://github.com/vllm-project/vllm/pull/41026
* @guybd made their first contribution in https://github.com/vllm-project/vllm/pull/44029
* @harsha20032020 made their first contribution in https://github.com/vllm-project/vllm/pull/44720
* @hclsys made their first contribution in https://github.com/vllm-project/vllm/pull/44070
* @hhhhhhhhhhhhhhhhho made their first contribution in https://github.com/vllm-project/vllm/pull/46467
* @hillelda made their first contribution in https://github.com/vllm-project/vllm/pull/46069
* @I3eg1nner made their first contribution in https://github.com/vllm-project/vllm/pull/47532
* @imargulis made their first contribution in https://github.com/vllm-project/vllm/pull/46301
* @ItsMatti4 made their first contribution in https://github.com/vllm-project/vllm/pull/45263
* @jesco-absolut made their first contribution in https://github.com/vllm-project/vllm/pull/47589
* @jessiewei7 made their first contribution in https://github.com/vllm-project/vllm/pull/46560
* @jialoop-git made their first contribution in https://github.com/vllm-project/vllm/pull/45159
* @JohnLangford made their first contribution in https://github.com/vllm-project/vllm/pull/46835
* @Jyothirmaikottu made their first contribution in https://github.com/vllm-project/vllm/pull/47250
* @kalyanamdewri made their first contribution in https://github.com/vllm-project/vllm/pull/47517
* @Laurent-Zhang made their first contribution in https://github.com/vllm-project/vllm/pull/47429
* @lcheng321 made their first contribution in https://github.com/vllm-project/vllm/pull/45715
* @LiJzd made their first contribution in https://github.com/vllm-project/vllm/pull/45813
* @lslusarczyk made their first contribution in https://github.com/vllm-project/vllm/pull/43092
* @Lynn-hh made their first contribution in https://github.com/vllm-project/vllm/pull/46543
* @Meihan-chen made their first contribution in https://github.com/vllm-project/vllm/pull/44483
* @nagisa-kunhah made their first contribution in https://github.com/vllm-project/vllm/pull/44124
* @NathanielMcVicar made their first contribution in https://github.com/vllm-project/vllm/pull/45965
* @NicolasHug made their first contribution in https://github.com/vllm-project/vllm/pull/46609
* @omirosh made their first contribution in https://github.com/vllm-project/vllm/pull/44313
* @orestis-z made their first contribution in https://github.com/vllm-project/vllm/pull/46488
* @pranavthakur0-0 made their first contribution in https://github.com/vllm-project/vllm/pull/46306
* @Priyjain-amd made their first contribution in https://github.com/vllm-project/vllm/pull/45818
* @skajre made their first contribution in https://github.com/vllm-project/vllm/pull/46818
* @soaringk made their first contribution in https://github.com/vllm-project/vllm/pull/45810
* @spandantiwari made their first contribution in https://github.com/vllm-project/vllm/pull/46260
* @sriganesh123 made their first contribution in https://github.com/vllm-project/vllm/pull/35076
* @tarjan1 made their first contribution in https://github.com/vllm-project/vllm/pull/45657
* @thisjiang made their first contribution in https://github.com/vllm-project/vllm/pull/45924
* @umarkovi-amd made their first contribution in https://github.com/vllm-project/vllm/pull/46381
* @VectorPeak made their first contribution in https://github.com/vllm-project/vllm/pull/47099
* @wan-danfeng made their first contribution in https://github.com/vllm-project/vllm/pull/38174
* @yangyang-cs95 made their first contribution in https://github.com/vllm-project/vllm/pull/46684
* @yuyue0225sc made their first contribution in https://github.com/vllm-project/vllm/pull/44297
* @zhongjing123 made their first contribution in https://github.com/vllm-project/vllm/pull/47024
* @zhou9402 made their first contribution in https://github.com/vllm-project/vllm/pull/47448
* @ZichenYuan made their first contribution in https://github.com/vllm-project/vllm/pull/46452

## Contributors

Thank you to all the contributors who made this release possible!

@AndreasKaratzas, @njhill, @BugenZhao, @hmellor, @yewentao256, @WoosukKwon, @Sunt-ing, @micah-wil, @mgoin, @reidliu41, @peizhang56, @mawong-amd, @TheEpicDolphin, @jeejeelee, @taneem-ibrahim, @chaunceyjiang, @chaojun-zhang, @divakar-amd, @fxmarty-amd, @LopezCastroRoberto, @wzhao18, @mayuyuace, @jperezdealgaba, @noooop, @yzong-rh, @jikunshang, @zxd1997066, @bigPYJ1151, @yma11, @hickeyma, @benchislett, @xianbaoqian, @andakai, @NickLucche, @ivanium, @joerowell, @EazyReal, @mganczarenko, @majunze2001, @hongxiayang, @WindChimeRan, @Rohan138, @tjtanaa, @bbrowning, @thisjiang, @Fangzhou-Ai, @blasrodri, @Isotr0py, @zhenwei-intel, @zyongye, @frida-andersson, @muhammadfawaz1, @lcheng321, @spandantiwari, @Palaiologos1453, @soaringk, @Lynn-hh, @fadara01, @djramic, @Liangliang-Ma, @ronensc, @aarushjain29, @HDCharles, @qianlihuang, @AgenticSpark, @charlifu, @cleonard530, @shen-shanshan, @xaguilar-amd, @xiaohongchen1991, @varun-sundar-rabindranath, @gau-nernst, @tahsintunan, @GirasoleY, @hclsys, @Yejing-Lai, @LucasWilkinson, @matteso1, @akii96, @atalman, @lucianommartins, @I3eg1nner, @rahulssv-ibm, @ZichenYuan, @tanpinsiang, @hillelda, @Srinivasoo7, @Etelis, @Rukhaiya2004, @Oxygen56, @Priyjain-amd, @GuyStone, @nholmber, @CienetStingLin, @xinyu-intel, @JartX, @esmeetu, @hhhhhhhhhhhhhhhhho, @harsha20032020, @walterbm, @Acaciasama, @jessiewei7, @ashwin-phadke, @shivampr, @cyq1017, @kjiang249, @orestis-z, @xyang16, @tianmu-li, @mgehre-amd, @aaarkai, @guybd, @wcynb1023, @Josephasafg, @qyYue1389, @russellb, @haoyangli0109, @sfeng33, @mikekg, @EanWang211123, @ovidiusm, @ItsMatti4, @hyeongyun0916, @qli88, @juliendenize, @calvarado2004, @tdoublep, @brandonpelfrey, @davispuh, @weizhoublue, @jasonozuzu-cohere, @wentian-byte, @skajre, @gty111, @omirosh, @decarpentierg, @fjosw, @ilmarkov, @yuwenzho, @JisoLya, @JohnLangford, @aldenlobo, @bnellnm, @jasonlizhengjian, @zufangzhu, @izhuhaoran, @MatthewBonanni, @deng451e, @ashwing, @sriganesh123, @linitra24, @liranschour, @umarkovi-amd, @aman0603, @adobrzyn, @jwzheng96, @eicherseiji, @ArsalanShakil, @tc-mb, @imargulis, @fangyuchu, @puririshi98, @JeanPaulShapo, @VectorPeak, @tarjan1, @qiching, @Achyuthan-S, @ZJY0516, @lucifer1004, @cinnamonica02, @jmamou, @almayne, @hao-aaron, @Jyothirmaikottu, @andylolu2, @AIvashov, @stevenkuang-tencent, @lcskrishna, @Aneureka, @wan-danfeng, @chengzheng345, @pranavthakur0-0, @zRzRzRzRzRzRzR, @DanBlanaru, @adamkbaranowski, @wendyliu235, @eparshut, @yangyang-cs95, @kalyanamdewri, @maxdebayser, @fenghourun, @tpopp, @okorzh-amd, @labAxiaoming, @sychen52, @ekagra-ranjan, @gausah01, @yuyue0225sc, @cpersson-amd, @lslusarczyk, @alex101-ops, @Zhenzhong1, @velonica0, @zhongjing123, @zhou9402, @llsj14, @majian4work, @akinsella, @BadrBasowid, @afierka-intel, @ayush1399, @LiJzd, @jesco-absolut, @Laurent-Zhang, @Kevin-XiongC, @NathanielMcVicar, @askliar, @ACEEE-1222, @jinzhen-lin, @SherryC41, @simondanielsson, @nv-nedelman-1, @yisustc, @kylesayrs, @jialoop-git, @NicolasHug, @guan404ming, @HumphreySun98, @danielafrimi, @gcanlin, @robertgshaw2-redhat

---

## v0.24.0  (2026-06-29T19:41:59Z)

# vLLM v0.24.0 Release Notes

## Highlights

This release features 571 commits from 256 contributors (77 new)!

* **MiniMax-M3**: Added support for the new **MiniMax-M3** model (#45381), with a fast follow-on of BF16/FP8 indexer via MSA (#45892), MXFP4 support (#45896), FP8 sparse GQA (#45744), and extensive AMD/ROCm tuning — mxfp8 MoE/linear on gfx950 (#45725), fp8_per_channel for bf16 weights on MI300X (#45854), FP8 KV-cache fix (#45720), and packed-modules mapping (#45794). A MiniMax-M2 perf regression was also fixed (#45935).
* **DeepSeek-V4 keeps maturing**: Following its debut, DeepSeek-V4 received another large optimization pass — a FlashInfer sparse index cache (2–4% TTFT) (#45863), prefill chunk-planning optimization (4% E2E throughput) (#45061), a cluster-cooperative topK kernel for low-latency (#43008), contiguous per-block KV allocations (#44577), TEP=16 for the block-FP8 shared expert (#46001), and native DSA indexer decode for `next_n > 2` on SM100 (#45322). It is now enabled on **SM120** alongside GLM-5.1 (#43477), with XPU (#44144, #44517, #45240) and ROCm (#44899, #45103, #45681) attention/MoE paths added.
* **Model Runner V2 (MRv2) continues to expand**: MRv2 now **supports quantized models by default** (#44446), enables **GraniteMoE by default** (#45461), and gained migration of Qwen + DeepSeek-V2 MoE models (#42667), DFlash speculative decoding (#44586), and more accurate FP32 Gumbel sampling (#45996).
* **Streaming Parser Engine**: A new streaming parser engine unifies tool-call/reasoning parsing across models, with parsers for Qwen3 (#45413), MiniMax-M2 (#45701), GLM-4.7/5.1/5.2 (#45915), and Nemotron V3 (#45755).
* **Diffusion LLMs**: Added **DiffusionGemma** (#45163), including a CPU path (#45690) and structured-output guardrails for diffusion decoders (#45468).
* **WideEP / DeepEP v2**: Integrated **DeepEP v2** for expert parallelism (#41183), with follow-on robustness fixes (#46404, #46432).
* **Rust frontend matures further**: Added API-key authentication (#44321), CORS (#45753), `/tokenize` + `/detokenize` (#44222), `/pause` `/resume` `/is_paused` (#44499), `/abort_requests` (#44382), `/get_world_size` (#44801), `thinking_token_budget` (#46137), a Python bridge for Rust tool parsers (#44624), and many new parsers and validation paths.
* **Device selection change**: vLLM no longer sets `CUDA_VISIBLE_DEVICES` internally; a new `device_ids` argument is provided instead (#45026). On ROCm, a deprecation window for `CUDA_VISIBLE_DEVICES` has begun (#46636).

### Model Support
* **New models**: MiniMax-M3 (#45381), DiffusionGemma (#45163) + Gemma Diffusion on CPU (#45690), Hierarchical Reasoning Model — Text / HrmTextForCausalLM (#43098), OpenMOSS (#44124).
* **Gemma 4**: Unified FlashAttention (FA4) across all layers + `mm_prefix` support (#42175); many parser/serving fixes — forced-JSON skip for required/named tool choice (#45795), parsing with thinking disabled (#45832), streaming reasoning-state init (#45852), reasoning rendering on assistant turns (#45867), offline-parser truncation/token-leak fix (#45553); legacy Gemma4 parsers replaced with an engine-based implementation (#45588).
* **DeepSeek-V4**: OOM fix (#44914), MTP projection prefixing (#44821), supported KV-cache dtypes (#44892).
* **Qwen / multimodal**: Qwen3-VL video loader (#44412), Qwen2-VL/Qwen2.5-VL processor-mapped video loader (#45555), Qwen3-VL multi-video processing optimization (#46026) and multi-video crash fix (#46305), Qwen3-Omni VIT cu_seqlens device fix (#44264), fused qk-rmsnorm-rope-gate for Qwen3.5 (#44176), Qwen3.5 EP weight-loading fix (#45002).
* **ViT full CUDA graph**: GLM-4.1V (#40576), DeepSeek-OCR dual-path (#43586), Kimi-VL (#41992), mllama4 (#40660), Lfm2VL encoder (#44930).
* **Other model fixes**: Llama4 weight loading (#45047) and streamed loading to avoid host-OOM (#44645), MiMo v2.x QKV TP sharding + FP4 (#45200), ColQwen3.5 retrieval correctness (#46108), EXAONE-4.5 vision encoder (#45073), MiDashengLM TP>1 audio-encoder crash (#44408), MiniCPM-o/V device-placement and image-size fixes (#43844, #42332, #44980, #45244), Cohere2 MoE weight loading + parser (#44747, #44907), Nemotron V3 reasoning-as-content (#39091), ColBERT AutoWeightsLoader + query/document embedding io processor (#44999, #45210).
* **Kernels**: GLM-5 TRT-LLM ragged MLA prefill dimensions (#43525), GLM-5 router GEMM (#46385).

### Engine Core
* **Model Runner V2**: Quantized models by default (#44446), GraniteMoE default (#45461), Qwen/DSv2 MoE migration (#42667), DFlash (#44586), simplified async output handling (#45442), attention-group split on `num_heads_q` (#45564), LoRA warmup fix (#35536), more accurate FP32 Gumbel sampling (#45996), `min_tokens` off-by-one fix in the V2 GPU sampler (#46243), plus assorted model/config compatibility fixes (#45868).
* **Speculative decoding**: Dynamic SD (#32374); DFlash with FlashInfer (#43081), mixed KV page sizes (#45181), and Qwen3Next targets (#45319); EAGLE3 support for Qwen3 (#43132); reduced TP communication for large-vocab drafts (#39419); race fix in async accepted counts (#45100); EAGLE multimodal encoder cache fixes (#46315).
* **KV cache & scheduler**: KV-cache watermark to reduce preemptions (#44594), two-phase allocation for cross-group prefix-cache hits (#44409), Marconi-style admission policy for hybrid cache (#37898), prefix-cache retention for Mamba/linear attention (#45845), DS Mamba tail-copy for MTP align mode (#45473), reduced scheduler copy overhead (#45840).
* **Attention**: Re-enabled cross-layer KV cache layout for MLA via stride-aware kernels (#45111), MLA prefill FA4 fp8 output (#43050), FlexAttention custom mask mods made fully cudagraphable (#45232), triton diff-kv backend for MiMo (#41797), FlashMLA sparse accuracy fix (#36616).
* **Weight loading & core**: fastsafetensors `ParallelLoader` for weight loading (#40183), release of cached device memory under pressure on UMA GPUs (#45179), structured outputs for beam search (#35022), `device_ids` arg / no internal `CUDA_VISIBLE_DEVICES` (#45026), graceful fallback when `numactl --membind` is blocked (#45438), config-class registration before tokenizer init (#40299), async scheduling with prompt embeds for multimodal models (#45673).

### Large Scale Serving & Distributed
* **Expert parallel**: DeepEP v2 integration (#41183) with token-bound and topk-index fixes (#46404, #46432); NIXL EP — DBO with NIXL EP (#45275), top-k index dtype query (#45298), NVFP4 post-receive quantization skip (#45606), elastic-EP communicator (#45013); reject NCCL-based EPLB with async EPLB (#44978).
* **KV connectors / disaggregated serving**: KV push from prefill to decode via NIXL (#35264); per-region KV transfer classification for mixed full-attn + MLA groups (#44583); Mooncake pipeline-parallel PD support (#44528), async lookup (#45659), compact chunk-hash zero-copy lookup (#45969), SWA-block skipping (#45444); P/D fixes with DP supervisor (#46628) and DSV4 disaggregation (#45831); removed `P2pNcclConnector` (#44854).
* **KV offloading**: Multi-tier async batched lookup (#44193), packed HMA KV-cache layout (#46205, gated #46252), parallel-agnostic fs-tier cache (#44733), offloading-manager stats (#35669) and labeled/CPU-usage metrics (#45957, #45737), self-describing KV events (#43468), non-blocking idle flush (#45595), and numerous correctness/race fixes (#44784, #45823, #46231, #46278).
* **Distributed core**: Prefill step cadence for better non-PD DP balancing (#44558), KV-event map encoding (#42892), one-shot fused all-reduce PDL NaN fix (#45448).

### Hardware & Performance
* **NVIDIA / kernels**: SM90 CUTLASS FP8 mm odd-M support via swap_ab (180–290% kernel speedup) (#44572), tuned `fused_moe` FP8 for Qwen3-Next-80B on H100 (+25%) (#44830), native DSA indexer decode on SM100 (#45322), cluster-cooperative topK for DeepSeek low-latency (#43008), PDL support for DeepGEMM (#46006), FlashInfer cutedsl NVFP4 GEMM (#42235) and cute-dsl MXFP8 linear kernel (#46393), new Helion kernels for FP8/RMSNorm quant (#36902, #33790, #36895, #34432).
* **torch stable ABI**: Continued (and completed) migration of kernels to the libtorch stable ABI — MoE [10c/n] (#44565), Marlin [11a/n] (#45176), Machete [11b/n] (#45304), final `_C` library migration [12/n] (#45415).
* **AMD ROCm**: Torch 2.11 (#45362); fused AR + RMSNorm + per-group FP8 quant (#42864), fused softplus-sqrt-topk MoE router under AITER (#44945), DSv4 flash-decode split-K kernel (#44899) and inverse-RoPE fusion (#45103), W4A16 FlyDSL MoE (#44400), A8W4 MoE CDNA4 swizzle gate for gpt-oss (#44804); deprecation window begun for `CUDA_VISIBLE_DEVICES` on ROCm (#46636).
* **Intel XPU**: Sequence-parallel support (#38608), torch-xpu 2.12 (#42262), vllm-xpu-kernels v0.1.10 (#40367), W4A16 int4 group_size=32 MoE (#45136), DeepSeek-V4 attention/MoE paths (#44144, #44517, #45240), top-p sampling correctness fix (#44470).
* **CPU & other architectures**: 2.5× faster ASR CPU preprocessing via multi-threading (#44612), CPU W4A16 INT4 MoE (#43409), cgroup memory-limit-aware KV cache sizing (#45086), RISC-V oneDNN W8A8 INT8 (#44478) and RVV micro-GEMM for WNA16 (#44324), pinned memory for WSL2 (#41496), ZenCPU runtime logging (#42726).
* **TPU**: tpu-inference upgraded to v0.22.1 (#45793).
* **Misc perf**: `VLLM_TRITON_FORCE_FIRST_CONFIG` to skip Triton autotuning (#42425), Triton recompile detection (#45631), fused multi-group block-table staged writes (#44944).

### Quantization
* **Online & mixed-precision**: Online FP8 per-token-per-channel (PTPC) quantization (#44132); `modelopt_mixed` support extended to Ampere/SM80-86 (#45306) and Turing/SM75 (#45375).
* **FP4 / MXFP**: FlashInfer cutedsl NVFP4 GEMM backend (#42235) and cute-dsl MXFP8 linear kernel (#46393), MXFP4 W4A4 MoE CUTLASS E8M0 scale fix (#43557), SwiGLU clamp wired for NVFP4 MoE on non-Blackwell (#45836), `flashinfer_cutlass` allowed as a clamped NVFP4 MoE backend (#46492), NVFP4/OCP MX MoE emulation fix (#46254), FP8 MoE re-enabled on NVIDIA Thor (#46339).
* **GGUF / compressed-tensors / AWQ**: GGUF quantization migrated to a plugin (#39612), compressed-tensors WNA16 MoE actorder fix (#41161) and KV-cache-scheme rejection (#45312), AWQ format on XPU (#43404) and AWQ dequantize fix on Intel XPU (#42727).
* **Kernels & correctness**: QuantizedActivation linear-kernel contract (#44260), consolidated Marlin thread-tile padding (#45295), FP8 weight layout canonicalized to (K, N) (#44735), corrupt-output fix for MoE FP8 with LoRAs loaded (#42120), symmetric-quant regression fix in GPTQ/CT MoE (#45656), `fp8_e5m2` KV cache allowed for non-fp8 checkpoints (#45040).

### API & Frontend
* **Tool calling & parsing**: Strict mode for tool calling in Chat Completions (#45003) and Responses API (#45396); new Streaming Parser Engine (#45413) with Qwen3, MiniMax-M2 (#45701), GLM-4.7/5.1/5.2 (#45915), Nemotron V3 (#45755) parsers; unified Parser consolidation in chat serving (#45548); numerous parser correctness fixes (#46047, #46091, #46159, #45763, #46351, #43984).
* **OpenAI / Responses**: Real `/v1/embeddings` support for messages + `chat_template_kwargs` (#45173), multimodal token counts in `usage.prompt_tokens_details` (#45458), omit empty `tool_calls` from chat responses (#44105), Responses API streaming `function_call` id fix (#44608), Harmony refactor of streaming/non-streaming paths (#45171, #45104).
* **Anthropic Messages API**: Cache-usage reporting in `/v1/messages` (#40912), mid-conversation system-message handling (#46025), inline system-message position preserved for prefix caching (#44602), `tool_use` argument-dropping fix (#45287).
* **Rust frontend**: API-key auth (#44321), CORS (#45753), `/tokenize` + `/detokenize` (#44222), `/pause` `/resume` `/is_paused` (#44499), `/abort_requests` (#44382), `/get_world_size` (#44801), `thinking_token_budget` (#46137), `parallel_tool_calls=false` (#44760), continuous usage stats (#43965), model metadata in `/v1/models` (#45950), Python bridge for Rust tool parsers (#44624), dedicated runtime for HTTP/ZMQ (#46051), and many validation/correctness fixes.
* **Metrics**: `vllm:tool_call_parser_invocations_total` (#44448), group-aware KV cache capacity in `vllm:cache_config_info` (#42206), MLA attention metrics for DeepSeek MFU estimation (#39457).
* **Pooling / embeddings**: Validation for Cohere `/v2/embed` input exclusivity (#45640), non-negative rerank `top_n` (#46119), matryoshka embedding dimension bounds (#46313).
* **Benchmarks**: BFCL tool-calling dataset for `vllm bench serve` (#42457), multi-turn benchmark api_key/custom headers (#44516), tokenizer-mismatch auto-correction (#44708).

### Security

This release ships another coordinated security-hardening batch (much of it from security researcher @jperezdealgaba).

* **Denial of service**: Audio decompression bomb in the speech-to-text endpoint (#44970), remote DoS via invalid recovered-token reinjection in speculative decoding (#44744), DoS via `prompt_embeds` on M-RoPE models (#45252), regex-compilation timeout guard in structured outputs (#45118), audio upload size limit before full materialization (#45510), audio decode duration limit in the chat-completions path (#45908).
* **Information disclosure**: int32 truncation in the GGUF dequantize kernels (#44971).
* **Input validation & hardening**: Image EXIF orientation and tRNS transparency handling (#44974), rejection of non-finite `temperature`/`repetition_penalty` (#45116), `sanitize_message` applied to Anthropic and STT error paths (#45119).
* **Dependencies**: Upgrade Starlette to ≥ 1.0.1 to fix CVE-2026-48710 (#45675).

### Dependencies
* Torch 2.11 on ROCm (#45362), torch-xpu 2.12 (#42262), tpu-inference v0.22.1 (#45793), NIXL v0.10.1 for XPU (#40287), Starlette ≥ 1.0.1 (#45675).
* `mistral_common` is now optional via deferred import (#45305); CUDA Dockerfiles upgraded from GCC 10 to GCC 12 for C++20 (#44923); spinloop extension skipped on Python < 3.11 (#44783).

### Deprecations & Removals
* **Removed models**: ERNIE (obsolete) (#45127), Xverse (#45638), Dots1 (#45637), Bamba (#45990), Mono-InternVL (#45129), InternLM registry alias (#45128).
* **Deprecated**: First-generation Qwen and QwenVL models (#45131), Transformers v4 support (#45161), `CUDA_VISIBLE_DEVICES` on ROCm (#46636); general deprecations for v0.23/v0.24 (#44992).

## New Contributors

* @abcd1927 made their first contribution in https://github.com/vllm-project/vllm/pull/43098
* @Achyuthan-S made their first contribution in https://github.com/vllm-project/vllm/pull/44795
* @Alex-ai-future made their first contribution in https://github.com/vllm-project/vllm/pull/45905
* @alexbi29 made their first contribution in https://github.com/vllm-project/vllm/pull/45763
* @amanchugh89 made their first contribution in https://github.com/vllm-project/vllm/pull/45840
* @ankrovv made their first contribution in https://github.com/vllm-project/vllm/pull/44608
* @anony-mous-e made their first contribution in https://github.com/vllm-project/vllm/pull/45412
* @appleparan made their first contribution in https://github.com/vllm-project/vllm/pull/45073
* @ashishpatel26 made their first contribution in https://github.com/vllm-project/vllm/pull/43984
* @Bot1822 made their first contribution in https://github.com/vllm-project/vllm/pull/44053
* @ByteFlowing1337 made their first contribution in https://github.com/vllm-project/vllm/pull/45988
* @Change72 made their first contribution in https://github.com/vllm-project/vllm/pull/43756
* @coder3101 made their first contribution in https://github.com/vllm-project/vllm/pull/44801
* @cquil11 made their first contribution in https://github.com/vllm-project/vllm/pull/45720
* @dmaniloff made their first contribution in https://github.com/vllm-project/vllm/pull/40470
* @factnn made their first contribution in https://github.com/vllm-project/vllm/pull/44955
* @FAUST-BENCHOU made their first contribution in https://github.com/vllm-project/vllm/pull/44760
* @felix0080 made their first contribution in https://github.com/vllm-project/vllm/pull/44602
* @gitbisector made their first contribution in https://github.com/vllm-project/vllm/pull/40183
* @gq112 made their first contribution in https://github.com/vllm-project/vllm/pull/43081
* @guan404ming made their first contribution in https://github.com/vllm-project/vllm/pull/35022
* @HanHan009527 made their first contribution in https://github.com/vllm-project/vllm/pull/44528
* @hello-args made their first contribution in https://github.com/vllm-project/vllm/pull/44109
* @HumphreySun98 made their first contribution in https://github.com/vllm-project/vllm/pull/45466
* @j-i-l made their first contribution in https://github.com/vllm-project/vllm/pull/45319
* @JasonLi314 made their first contribution in https://github.com/vllm-project/vllm/pull/45255
* @jeffye-dev made their first contribution in https://github.com/vllm-project/vllm/pull/43595
* @jimmy-evo made their first contribution in https://github.com/vllm-project/vllm/pull/44516
* @jjppp made their first contribution in https://github.com/vllm-project/vllm/pull/45217
* @JOSH1024 made their first contribution in https://github.com/vllm-project/vllm/pull/44784
* @junkang1991 made their first contribution in https://github.com/vllm-project/vllm/pull/46039
* @KaletoAI made their first contribution in https://github.com/vllm-project/vllm/pull/43495
* @kliukovkin made their first contribution in https://github.com/vllm-project/vllm/pull/43724
* @littlecircle0730 made their first contribution in https://github.com/vllm-project/vllm/pull/44750
* @llx-08 made their first contribution in https://github.com/vllm-project/vllm/pull/45357
* @m4r1k made their first contribution in https://github.com/vllm-project/vllm/pull/45795
* @martin-kukla made their first contribution in https://github.com/vllm-project/vllm/pull/45417
* @MichaelCao0 made their first contribution in https://github.com/vllm-project/vllm/pull/46398
* @mrn3088 made their first contribution in https://github.com/vllm-project/vllm/pull/45383
* @nataliepjlin made their first contribution in https://github.com/vllm-project/vllm/pull/45218
* @nehmathe2 made their first contribution in https://github.com/vllm-project/vllm/pull/44912
* @nikhilesh-csa made their first contribution in https://github.com/vllm-project/vllm/pull/45852
* @nv-nedelman-1 made their first contribution in https://github.com/vllm-project/vllm/pull/42120
* @Oseltamivir made their first contribution in https://github.com/vllm-project/vllm/pull/45879
* @parthash0804 made their first contribution in https://github.com/vllm-project/vllm/pull/43844
* @pjdurden made their first contribution in https://github.com/vllm-project/vllm/pull/44942
* @pst2154 made their first contribution in https://github.com/vllm-project/vllm/pull/45181
* @Saddss made their first contribution in https://github.com/vllm-project/vllm/pull/44409
* @sahilsGit made their first contribution in https://github.com/vllm-project/vllm/pull/44499
* @sasindharan made their first contribution in https://github.com/vllm-project/vllm/pull/44383
* @shantipriya-amd made their first contribution in https://github.com/vllm-project/vllm/pull/39498
* @Sirius29 made their first contribution in https://github.com/vllm-project/vllm/pull/46026
* @srajabos made their first contribution in https://github.com/vllm-project/vllm/pull/44665
* @sridhar-3009 made their first contribution in https://github.com/vllm-project/vllm/pull/44055
* @stefankoncarevic made their first contribution in https://github.com/vllm-project/vllm/pull/45706
* @sunnweiwei made their first contribution in https://github.com/vllm-project/vllm/pull/45100
* @TanNgocDo made their first contribution in https://github.com/vllm-project/vllm/pull/44222
* @thisisjimmyfb made their first contribution in https://github.com/vllm-project/vllm/pull/41496
* @tykow made their first contribution in https://github.com/vllm-project/vllm/pull/44663
* @V-3604 made their first contribution in https://github.com/vllm-project/vllm/pull/43362
* @vincentzed made their first contribution in https://github.com/vllm-project/vllm/pull/44930
* @vraiti made their first contribution in https://github.com/vllm-project/vllm/pull/42331
* @wangjiaxin99 made their first contribution in https://github.com/vllm-project/vllm/pull/45794
* @waynehacking8 made their first contribution in https://github.com/vllm-project/vllm/pull/45376
* @x41lakazam made their first contribution in https://github.com/vllm-project/vllm/pull/43300
* @xiaguan made their first contribution in https://github.com/vllm-project/vllm/pull/45286
* @xiaohuguo2023 made their first contribution in https://github.com/vllm-project/vllm/pull/44804
* @xin3he made their first contribution in https://github.com/vllm-project/vllm/pull/43557
* @xx-thomas made their first contribution in https://github.com/vllm-project/vllm/pull/45210
* @yangdian96 made their first contribution in https://github.com/vllm-project/vllm/pull/44173
* @YellowFoxH4XOR made their first contribution in https://github.com/vllm-project/vllm/pull/45057
* @yzhan1 made their first contribution in https://github.com/vllm-project/vllm/pull/44552
* @Zedong-Liu made their first contribution in https://github.com/vllm-project/vllm/pull/45361
* @ZewenShen-Cohere made their first contribution in https://github.com/vllm-project/vllm/pull/41161
* @zhangshuoming990105 made their first contribution in https://github.com/vllm-project/vllm/pull/40912
* @ZiguanWang made their first contribution in https://github.com/vllm-project/vllm/pull/43981
* @zlxi02 made their first contribution in https://github.com/vllm-project/vllm/pull/44595

## Contributors

Thank you to everyone who made this release possible!

@yewentao256, @Sunt-ing, @jperezdealgaba, @AndreasKaratzas, @BugenZhao, @sfeng33, @njhill, @micah-wil, @bbrowning, @mgoin, @jeejeelee, @hmellor, @tlrmchlsmth, @xianbaoqian, @mmangkad, @jikunshang, @Dao007forever, @zhenwei-intel, @noooop, @Isotr0py, @ivanium, @reidliu41, @varun-sundar-rabindranath, @chaunceyjiang, @WoosukKwon, @mawong-amd, @zxd1997066, @chaojun-zhang, @NickLucche, @bigPYJ1151, @ZJY0516, @charlifu, @yzong-rh, @divakar-amd, @khluu, @cleonard530, @wseaton, @xiaohongchen1991, @ywang96, @taneem-ibrahim, @mikekg, @itayalroy, @Alex-ai-future, @sahilsGit, @bnellnm, @littlecircle0730, @majian4work, @ricky-chaoju, @ronensc, @Fangzhou-Ai, @lucianommartins, @Srinivasoo7, @zyongye, @Rohan138, @Etelis, @wentian-byte, @ekagra-ranjan, @LucasWilkinson, @tahsintunan, @waynehacking8, @gau-nernst, @tuukkjs, @stefankoncarevic, @Palaiologos1453, @lucifer1004, @jmamou, @liulanze, @Terrencezzj, @Change72, @LopezCastroRoberto, @he-yufeng, @benchislett, @juliendenize, @s3woz, @panpan0000, @ilmarkov, @zixi-qi, @wcynb1023, @fynnsu, @ZhanqiuHu, @yuwenzho, @tdoublep, @MatthewBonanni, @hickeyma, @majunze2001, @mrn3088, @Yejing-Lai, @vllmellm, @Saddss, @DarkLight1337, @hongxiayang, @m4r1k, @qli88, @jonathanc-n, @felix0080, @djramic, @aoshen02, @fxmarty-amd, @simon-mo, @llsj14, @akii96, @walterbm, @dmaniloff, @zlxi02, @grYe99, @jeffye-dev, @parthash0804, @qyYue1389, @sagearc, @maeehart, @TanNgocDo, @cinnamonica02, @zucchini-nlp, @tykow, @mganczarenko, @yangdian96, @jimmy-evo, @YellowFoxH4XOR, @yzhan1, @shenoyvvarun, @yufufi, @laviier, @xiaohuguo2023, @EanWang211123, @JartX, @shantipriya-amd, @askliar, @hallerite, @appleparan, @effi-ofer, @angelayi, @TheCodeWrangler, @DanBlanaru, @ankrovv, @velonica0, @pjdurden, @cyyever, @wjinxu, @kliukovkin, @x41lakazam, @Jasen2201, @r-barnes, @tc-mb, @nataliepjlin, @KaletoAI, @WineChord, @fangyuchu, @vraiti, @nascheme, @jjppp, @sasindharan, @xiaguan, @snadampal, @chfeng-cs, @thillai-c, @guan404ming, @sridhar-3009, @vincentzed, @j-i-l, @rjrock, @abinggo, @anony-mous-e, @Achyuthan-S, @Harry-Chen, @mfylcek, @amd-asalykov, @noa-neria, @maobaolong, @TheEpicDolphin, @FAUST-BENCHOU, @martin-kukla, @xin3he, @ZiguanWang, @youkaichao, @factnn, @llx-08, @xx-thomas, @gitbisector, @Bortlesboat, @thisisjimmyfb, @JOSH1024, @wendyliu235, @wangxiyuan, @shen-shanshan, @HanHan009527, @amd-lalithnc, @netanel-haber, @fuscof-ibm, @AjAnubolu, @carlyou, @abcd1927, @CienetStingLin, @kouroshHakha, @alexbi29, @jesse996, @sungsooha, @andakai, @cquil11, @nehmathe2, @liangel-02, @hello-args, @j9smith, @nikhilesh-csa, @ruocco, @oguzhankir, @yiliu30, @xaguilar-amd, @amirkl94, @danisereb, @wangjiaxin99, @shanjiaz, @Oseltamivir, @alexeldeib, @wzhao18, @coder3101, @lyd1992, @markmc, @ashishpatel26, @HumphreySun98, @ByteFlowing1337, @nv-nedelman-1, @JaredforReal, @sammshen, @okorzh-amd, @muhammadfawaz1, @vadiklyutiy, @JasonLi314, @SumanthRH, @Sirius29, @tjtanaa, @zhangshuoming990105, @amanchugh89, @umut-polat, @srajabos, @junkang1991, @pst2154, @WindChimeRan, @Zedong-Liu, @gq112, @sunnweiwei, @athrael-soju, @EazyReal, @Liangliang-Ma, @jinzhen-lin, @V-3604, @aarushjain29, @ZewenShen-Cohere, @Bot1822, @BowenBao, @MichaelCao0, @tanpinsiang, @QwertyJack, @nagisa-kunhah, @Meihan-chen, @robertgshaw2-redhat

---

## v0.23.0  (2026-06-15T05:27:20Z)

# vLLM v0.23.0 Release Notes

Please note that Minimax M3 is not yet supported in this version. Please follow [vLLM recipe](https://recipes.vllm.ai/MiniMaxAI/MiniMax-M3) for usage guides for M3.

## Highlights

This release features 408 commits from 200 contributors (63 new)!

* **DeepSeek-V4 matures across backends**: Following its introduction in v0.22.0, DeepSeek-V4 received another large hardening and optimization pass. Its sparse MLA metadata is now decoupled from DeepSeek-V3.2 (#44699), it gained a TRTLLM-gen attention kernel (#43827), EPLB support for the Mega-MoE (#43339), selective prefix-cache retention for sliding-window KV cache (#43447), and an index-share feature for DSA MTP (#44420). The model was also detached from `torch.compile` (#43746, #43891), its attention and RoPE paths were refactored (#44569, #44262, #43926), and an XPU attention decode path was added (#42953).
* **Model Runner V2 expands to more dense models**: MRv2 is now selected by default for **Llama and Mistral dense models** (#43458) in addition to Qwen3. It gained a FlashInfer sampler (#42472), breakable CUDA graphs (#44050), pipeline-parallel bubble elimination (#42187), kernel block-size support for hybrid models (#38831), and Gemma 4 MTP (#43241).
* **Rust frontend grows up**: The experimental Rust frontend added a streaming `generate` endpoint (#43779), dynamic LoRA endpoints (#43778), `/version` (#43854) and `/server_info` (#43942) endpoints, a server-router extension hook (#43774), request-ID headers (#43883), and many new tool parsers (InternLM2 #43481, hy_v3 #43872, Phi-4-mini #44213, Gemma4 #43850).
* **Gemma 4**: Added encoder-free **Gemma 4 Unified** support (#44429) and Gemma 4 MTP (#43241), plus numerous accuracy and startup fixes.
* **Transformers v5 compatibility**: vLLM now targets Transformers v5, with vendored MiniCPM-V/O processors (#44282) and compatibility fixes for Sarvam (#38804) and Voxtral (#44559).
* **Multi-tier KV cache offloading**: The offloading framework gained an **object-store secondary tier** (#41968), HMA enabled by default for capable connectors (#41847), tiering support for HMA models (#44287), and a per-request offloading policy via the `on_new_request` lifecycle hook (#43205).
* **Unified parser**: Reasoning and tool-call parsing are now unified behind a single `Parser.parse()` interface (#44267), with the Responses parser migrated to it (#42977).

### Model Support
* **New models**: Step-3.7-Flash (#43859), Cosmos3 Reasoner (#43356), Gemma 4 Unified encoder-free (#44429), JetBrains Mellum v2 (#43992), Granite Speech Plus (#43519), Cohere Mini Code (#44707).
* **Gemma 4**: Encoder-free Unified support (#44429), MTP (#43241), native ViT linear layers (#43798), vision-embedder excluded from quantization (#44571), and fixes for MTP under TP>1 (#43909), block-table mismatch under concurrency (#43982), transformers-processor startup crash (#44232), and CPU init (#44615).
* **Transformers v5**: Vendor MiniCPM-V/O processors (#44282), Sarvam compat (#38804), Voxtral `fetch_audio` for transformers≥5.10 (#44559).
* **Model fixes & enhancements**: Qwen3-VL/Qwen3-omni-thinker deepstack accuracy under `torch.compile` (#43617), EVS for Qwen3-VL (#44205), GLM-5.1 PP loading (#42944), GLM-4.1V processor logits (#43575), GLM-4.6V video loader (#44417), OlmoHybrid init (#43846), HyperCLOVAX remote-code removal (#43860), Bailing-MoE rotary factor (#43770), Step3 PP residual KeyError (#37622), MiniCPM-V-4.6 video (#44509), MiniCPM-O audio unpadding (#38053), MiniCPM-V batched preprocessing (#44609), FunASR-Nano init (#44215), Cohere routing method (#44021), Kimi-K2.5 FlashInfer ViT metadata (#44493).
* **Multimodal**: Auto-select registered video loader for VLMs (#44126), O(log n) multimodal item handling per step (#44212), local image encoding in benchmarks (#43843), interleaved custom image benchmark datasets (#43636).
* **Pooling/Classification**: Proper exceptions for pooling UX (#44593), `extra_repr()` for pooler classes (#44805), LoRA-adapter-name pooling fix (#44410), resettled generative scoring entrypoint (#44153), expanded pooler unit tests (#43818, #44471).
* **Refactor**: AutoWeightsLoader for InternLM2 (#38278).

### Engine Core
* **Model Runner V2**: Default for Llama and Mistral dense models (#43458), FlashInfer sampler (#42472), breakable CUDA graphs (#44050), removed Eagle's dedicated CUDA graph pool (#44078), pipeline-parallel bubble elimination (#42187), kernel block size for hybrid models (#38831), zeroing of freshly allocated KV blocks for hybrid + FP8 KV cache (#43990), actual batch `max_seq_len` for attention metadata (#43991), rejection-sampling acceptance-rate fix (#40651), KVConnector + PP cleanup (#43732), speculator-prefill warmup/capture (#44253).
* **Speculative decoding (DFlash)**: Causal DFlash (#43445), proper lookahead-slot allocation (#43733), prefix-cache corruption fix (#42971); independent drafter attention-backend selection (#39930), attention-group split by `num_heads_q` for drafts (#43543), EAGLE/MTP lookahead caching in the SWA prefix-cache mask (#44082).
* **Attention & hybrid/Mamba**: FlexAttention/FlashAttention num-blocks-first layouts (#42095), OOT MLA prefill backend registration (#43325), FlashAttention upstream sync (#44065), Mamba LINEAR attention-module refactor (#43556), corrupted MLA + linear attention fix (#43961), KDA conv-state unification (#44539) and gate/cumsum fusion (#43667), Mamba SSD `do_not_specialize` (#43803), Qwen3.5 mixed prefill+decode split routing (#44700), MiniMax-M2 gate kernel (#38445).
* **KV cache & scheduler**: Pluggable `KVCacheSpec` (#37505), `scheduler_block_size` threaded into KVCacheManager/Coordinator (#44165), `max_concurrent_batches` moved to `VllmConfig` (#44274), config validation rejecting 0/negative knobs (#43794, #44057, #44207), KV-cache scale boilerplate removed from weight loading (#43167).
* **Core**: Freeze the garbage collector in workers after model init (#44363), sparse NCCL weight transfer for in-place updates (#40096), graceful spinloop ext-load failure handling (#43659), scheduled-function deprecations (#43358).

### Large Scale Serving & Distributed
* **KV cache offloading**: Object-store secondary tier (#41968), HMA on by default for capable connectors (#41847) and tiering (#44287), per-request offloading policy (`on_new_request`) (#43205) and `on_schedule_end()` hook (#44206), token-offset selective offload (#39983), skip decode-phase blocks in CPU offload (#43797), page-size block alignment (#43689), Triton fast-path for small CPU→GPU `swap_blocks_batch` (#42212), stale sliding-window block fix (#42959).
* **KV connectors / disaggregated serving**: PP-aware handshake aggregation and intermediate-PP output plumbing (#43720), multiple-async-KV-load deadlock fix (#44560), Nixl Mamba prefix-caching mode (#42554), NixlConnector `kv_both` role deprecation cycle (#43874), Mooncake fixes (#43742, #44103, #42694), LMCache `LMCacheMPConnector` (#42865), EC connector shutdown API (#42423) and non-blocking lookup (#41627), KV-transfer tokens excluded from `iteration_tokens_total` (#43346).
* **EPLB**: Async EPLB by default (#43219), EPLB for DeepSeek-V4 Mega-MoE (#43339), Nixl zero-copy EPLB transfers (#41633).
* **Data parallel**: DP Ray placement groups on specific nodes (#44669) and grouped-node allocation fix (#43998), SSL for the DP supervisor (#43688), DP-coordinator startup timeout raised to 120s (#42343), per-GPU-worker RDMA NIC selection (#42083).

### Hardware & Performance
* **NVIDIA / kernels**: FP8 FlashInfer attention for ViT (#38065), Triton MoE backend on Hopper by default (#44220), CUTLASS FP8 scaled-mm padding bypass (+20%) (#43706), MoE-permute buffer pre-allocation (+9–14%) (#43014), `Fp8BlockScaledMM` `new_empty()` optimization (#43677), TurboQuant shared dequant buffers (#40941), tuned `selective_state_update` for H200/RTX PRO (#44251), Inductor fast-path fallback for vLLM/AITER custom ops (#42129), Gemma RMS all-reduce fusion (#42646), NUMA auto-binding on DGX B300 (#43270).
* **AMD ROCm**: ROCm 7.2.3 (#43136), AITER v0.1.13.post1 (#44265), native W4A16 (#41394) and fused-MoE W4A16 HIP (#44075) kernels for RDNA3 (gfx1100), AITER top-k/top-p sampler by default (#43331), attention-sink support in AITER FA (#43817), AITER hipBLASLt GEMM online tuning (#40426), `permute_cols` for ROCm (#44674), blocks-first KV layout for AMD (#43660), N=5 wvSplitK for spec decode (#40687), MoRI connector improvements (#43303, #41751, #40344).
* **Intel XPU**: vllm-xpu-kernel v0.1.7 (#41019), `block_fp8_moe` (#42139), block-scaled W8A8 FP8 path (#39968), WNA16 oracle for GPTQ sym-int4 (#41426), rms_norm/act quant fusions (#43963), GDN-attention MTP (#43565), Triton selective-scan op (#43421), transparent sleep mode (#37149), CPU/tiering offloading on XPU (#36423), DeepSeek-V4 attention decode path (#42953).
* **CPU & other architectures**: zentorch-accelerated W8A8/W4A16 on AMD Zen CPUs (#41813), CPU top-k/top-p Triton sampling (#43633), non-divisible GQA decode in mixed batches (#43032), `cpu_awq` folded into `awq_marlin` (#43841), RISC-V RVV WNA16 helpers (#42730), fused GDN gated-delta-rule kernels (#43534), PowerPC SHM communicator (#43754), arm64 CI image (#41303).
* **TPU**: tpu-inference upgraded to v0.20.0 (#43394) then v0.21.0 (#44621).
* **torch stable ABI**: Continued migration of kernels to the libtorch stable ABI — merge_attn_states/mamba/sampler [8/n] (#43361), attention/cache kernels [9/n] (#43717), header files (#44013), cuda_view/silu_and_mul [10/n] (#44334), custom all-reduce/DeepSeek-V4 fused MLA/MXFP8 MoE [10b/n] (#44365); ROCm fallback to regular ABI (#44648), `_has_module` trial-import verification (#44035).

### Quantization
* **ModelOpt**: LM-head quantization (#42124), MXFP8 non-gated MoE (#42958).
* **compressed-tensors**: WNA8O8Int linears and WNInt embeddings (#44340), asymmetric MoE WNA16 Marlin (#44025), single-class NVFP4 linear refactor (#42443).
* **Kernels & backends**: Triton W4A16 as CUDA fallback for non-Marlin-aligned shapes (#43731), Marlin MoE on SM 12.x (#40923), Machete W4A16 tests (#35450), fail-fast for unsupported NVFP4 KV-cache-dtype arch (#43669), CuteDSL compressor 128-split kernel optimization (#44230).
* **MoE refactor (oracle)**: Migrated ModelOpt MXFP8 (#42768), W4A8-int8 (#42789), and WNA16 backend selection (#42553) into the modular-kernel oracle; removed `supports_expert_map` (#43108) and the inplace fused-experts mechanism (#43727).

### API & Frontend
* **Anthropic Messages API**: Structured output and effort support (#42396), system-role messages inside the messages array (#44283).
* **OpenAI / Responses API**: `system_fingerprint` field (#40537), streaming tool/function calling with `required` (#40700), `chat_template_kwargs` in Responses (#43761), developer-to-system conversion in the HF renderer (#43590), unstreamed tool-call-args streaming fix (#44348).
* **Parsers**: Unified reasoning + tool-call parsing behind `Parser.parse()` (#44267), Responses parser migrated to the unified interface (#42977), unstreamed tool-arg flush moved into the parser (#44017); new/fixed tool parsers — MiniCPM5 XML (#43175), Qwen3 XML JSON-args-first (#43243), DeepSeek DSML incremental streaming (#42879), first-args-chunk serializer fix (#42683), `tool_choice="none"` honored in streaming (#42752), null-tool-args crash fix (#43862).
* **Frontend**: `thinking_token_budget` validation (#43402), GPT-OSS instruction rendering (#44330), Harmony `stop_token_ids` cleanup (#44009), consistent `VLLMValidationError` in chat/completion validators (#36254), consolidation of dev entrypoints (#44170) and online-serving utils (#44479).
* **Rust frontend**: Streaming `generate` endpoint (#43779), dynamic LoRA endpoints (#43778), `/version` (#43854) and `/server_info` (#43942), server-router extension hook (#43774), `--enable-request-id-headers` (#43883), recursive tool-parameter conversion (#44299), `include_reasoning=false` (#44391), `--language-model-only` skips the multimodal processor (#44500), per-engine batch auto-abort (#44591), UTF-8 char-boundary detokenizer fix (#44620), HF chat-template fixes (#44311), cross-DP aggregation of `is_sleeping`/`reset_prefix_cache` (#43429); new tool parsers — InternLM2 (#43481), hy_v3 (#43872), Phi-4-mini JSON (#44213), Gemma4 (#43850).
* **Benchmarks**: Timed trace replay for Moonshot/Alibaba workloads in `vllm bench serve` (#39795), reasoning-model (thinking) benchmarking via `--chat-template-kwargs` (#44244).

### Security
* **Transport encryption**: SSL/TLS support for the data-parallel supervisor (#43688).
* **Untrusted-input hardening**: Reject out-of-vocabulary token IDs before they reach the GPU logprob path (#44042) and fix a UTF-8 char-boundary panic in the Rust incremental detokenizer on malformed input (#44620), both of which prevent request-triggered crashes.
* **Parameter validation**: Reject invalid `thinking_token_budget` values (#43402), non-positive `ParallelConfig` integer knobs (#44057), zero-valued config fields (#43794), and out-of-range `max_num_scheduled_tokens` (#44207).

### Dependencies
* FlashInfer v0.6.12 (#44036), ROCm 7.2.3 (#43136), AITER v0.1.13.post1 (#44265), tpu-inference v0.21.0 (#44621), mistral-common bump (#44649), fastsafetensors v0.3.2 (#43625).
* Removed the stale cuDNN frontend upper bound (#42599); Docker fixes for flashinfer-jit-cache (#44366), FlashInfer CuTe DSL JIT `libcublas-dev` (#39855), and CUTLASS DSL cu13 install order (#45204).

### Deprecations
* Deprecate `JAISLMHeadModel` (#43784).
* Begin the deprecation cycle for the NixlConnector `kv_both` role (#43874).
* Remove functions previously scheduled for deprecation in v0.21.0 (#43358).

## New Contributors

* @aadwived made their first contribution in https://github.com/vllm-project/vllm/pull/41813
* @adhithyamulticoreware made their first contribution in https://github.com/vllm-project/vllm/pull/44615
* @adityasingh2400 made their first contribution in https://github.com/vllm-project/vllm/pull/43550
* @adotdad made their first contribution in https://github.com/vllm-project/vllm/pull/43100
* @amd-fuweiy made their first contribution in https://github.com/vllm-project/vllm/pull/43684
* @andakai made their first contribution in https://github.com/vllm-project/vllm/pull/43617
* @animeshtrivedi made their first contribution in https://github.com/vllm-project/vllm/pull/39795
* @BramVanroy made their first contribution in https://github.com/vllm-project/vllm/pull/43087
* @CienetStingLin made their first contribution in https://github.com/vllm-project/vllm/pull/43394
* @devin-lai made their first contribution in https://github.com/vllm-project/vllm/pull/44213
* @Dymasik made their first contribution in https://github.com/vllm-project/vllm/pull/43982
* @ECMGit made their first contribution in https://github.com/vllm-project/vllm/pull/43332
* @fallintoplace made their first contribution in https://github.com/vllm-project/vllm/pull/43540
* @gagandhakrey made their first contribution in https://github.com/vllm-project/vllm/pull/43792
* @galletas1712 made their first contribution in https://github.com/vllm-project/vllm/pull/43926
* @garrygale made their first contribution in https://github.com/vllm-project/vllm/pull/44205
* @Gruner-atero made their first contribution in https://github.com/vllm-project/vllm/pull/42967
* @hanlin12-AMD made their first contribution in https://github.com/vllm-project/vllm/pull/40426
* @harshaljanjani made their first contribution in https://github.com/vllm-project/vllm/pull/41459
* @Holworth made their first contribution in https://github.com/vllm-project/vllm/pull/39562
* @hoobnn made their first contribution in https://github.com/vllm-project/vllm/pull/42752
* @HueCodes made their first contribution in https://github.com/vllm-project/vllm/pull/44591
* @IdoAtadTD made their first contribution in https://github.com/vllm-project/vllm/pull/43978
* @jasonboukheir made their first contribution in https://github.com/vllm-project/vllm/pull/41426
* @Jie-Fang made their first contribution in https://github.com/vllm-project/vllm/pull/43584
* @JINO-ROHIT made their first contribution in https://github.com/vllm-project/vllm/pull/43830
* @JMonde made their first contribution in https://github.com/vllm-project/vllm/pull/37622
* @JohnQinAMD made their first contribution in https://github.com/vllm-project/vllm/pull/43331
* @jwzheng96 made their first contribution in https://github.com/vllm-project/vllm/pull/44057
* @Kartavyasonar made their first contribution in https://github.com/vllm-project/vllm/pull/43669
* @Krishnachaitanyakc made their first contribution in https://github.com/vllm-project/vllm/pull/38053
* @linzm1007 made their first contribution in https://github.com/vllm-project/vllm/pull/43402
* @MaciejBalaNV made their first contribution in https://github.com/vllm-project/vllm/pull/43356
* @Majid-Taheri made their first contribution in https://github.com/vllm-project/vllm/pull/43803
* @mfylcek made their first contribution in https://github.com/vllm-project/vllm/pull/43421
* @MHYangAMD made their first contribution in https://github.com/vllm-project/vllm/pull/42595
* @mikekg made their first contribution in https://github.com/vllm-project/vllm/pull/43330
* @nightcityblade made their first contribution in https://github.com/vllm-project/vllm/pull/44118
* @NolanHo made their first contribution in https://github.com/vllm-project/vllm/pull/43774
* @oguzhankir made their first contribution in https://github.com/vllm-project/vllm/pull/41759
* @okorzh-amd made their first contribution in https://github.com/vllm-project/vllm/pull/42129
* @Oxygen56 made their first contribution in https://github.com/vllm-project/vllm/pull/44236
* @QiliangCui2023 made their first contribution in https://github.com/vllm-project/vllm/pull/44476
* @rajkiranjoshi made their first contribution in https://github.com/vllm-project/vllm/pull/42083
* @Rukhaiya2004 made their first contribution in https://github.com/vllm-project/vllm/pull/43754
* @ruocco made their first contribution in https://github.com/vllm-project/vllm/pull/39983
* @sphinx07 made their first contribution in https://github.com/vllm-project/vllm/pull/43817
* @SunskyXH made their first contribution in https://github.com/vllm-project/vllm/pull/44215
* @ThibaultCastells made their first contribution in https://github.com/vllm-project/vllm/pull/43636
* @tianyu-z made their first contribution in https://github.com/vllm-project/vllm/pull/43150
* @tonyliu312 made their first contribution in https://github.com/vllm-project/vllm/pull/40923
* @tushar00jain made their first contribution in https://github.com/vllm-project/vllm/pull/41980
* @viiccwen made their first contribution in https://github.com/vllm-project/vllm/pull/44617
* @Vikrantpalle made their first contribution in https://github.com/vllm-project/vllm/pull/38804
* @wanghenshui made their first contribution in https://github.com/vllm-project/vllm/pull/44410
* @willamhou made their first contribution in https://github.com/vllm-project/vllm/pull/43429
* @william-rom made their first contribution in https://github.com/vllm-project/vllm/pull/43862
* @xiaozcy made their first contribution in https://github.com/vllm-project/vllm/pull/43843
* @XuZhou26 made their first contribution in https://github.com/vllm-project/vllm/pull/44618
* @Yadan-Wei made their first contribution in https://github.com/vllm-project/vllm/pull/44559
* @zhangtao2-1 made their first contribution in https://github.com/vllm-project/vllm/pull/43175
* @zvik made their first contribution in https://github.com/vllm-project/vllm/pull/43519
* @zzt93 made their first contribution in https://github.com/vllm-project/vllm/pull/43770

## Contributors

Thank you to everyone who made this release possible!

@AndreasKaratzas, @WoosukKwon, @BugenZhao, @yewentao256, @hmellor, @khluu, @njhill, @sfeng33, @bnellnm, @vadiklyutiy, @NickLucche, @JartX, @lucianommartins, @cleonard530, @wzhao18, @yma11, @simondanielsson, @jeejeelee, @zyongye, @chaunceyjiang, @bigPYJ1151, @ronensc, @taneem-ibrahim, @LucasWilkinson, @MatthewBonanni, @mmangkad, @chunyang-wen, @yzong-rh, @JaredforReal, @zixi-qi, @Isotr0py, @noooop, @chaojun-zhang, @Xunzhuo, @ivanium, @zufangzhu, @DaoyuanLi2816, @CienetStingLin, @aoshen02, @akii96, @benchislett, @MengqingCao, @rshavitt, @kliuae, @omerpaz95, @willamhou, @Majid-Taheri, @micah-wil, @ricky-chaoju, @mikekg, @mgoin, @mayuyuace, @Etelis, @ilmarkov, @tlrmchlsmth, @UranusSeven, @bedeks, @izhuhaoran, @ZJY0516, @fadara01, @pschlan-amd, @wangxiyuan, @Oxygen56, @charlifu, @varun-sundar-rabindranath, @shen-shanshan, @TheEpicDolphin, @adobrzyn, @XuZhou26, @tjtanaa, @Terrencezzj, @zhejiangxiaomai, @ILikeIneine, @yubofredwang, @chfeng-cs, @ThibaultCastells, @linzm1007, @javierdejesusda, @meenchen, @zhewenl, @xyang16, @angelayi, @nholmber, @zhangtao2-1, @adityasingh2400, @sts07142, @jatseng-ai, @fallintoplace, @andakai, @he-yufeng, @ignaciosica, @JINO-ROHIT, @tonyliu312, @QwertyJack, @animeshtrivedi, @jzakrzew, @juliendenize, @zexplorerhj, @ruocco, @mgehre-amd, @jasonboukheir, @MaciejBalaNV, @JohnQinAMD, @huanghua1994, @rajkiranjoshi, @rasmith, @harshaljanjani, @ltd0924, @wdhongtw, @yintong-lu, @tianmu-li, @jikunshang, @JMonde, @MHYangAMD, @frida-andersson, @gau-nernst, @Wauplin, @czhu-cohere, @gagandhakrey, @nemanjaudovic, @Liangliang-Ma, @liulanze, @sphinx07, @aadwived, @nightcityblade, @umut-polat, @jeffreywang88, @wcynb1023, @zzt93, @shadeMe, @Dao007forever, @alec-flowers, @Krishnachaitanyakc, @orozery, @BWAAEEEK, @cinnamonica02, @albertoperdomo2, @Rukhaiya2004, @mfylcek, @shreyas269, @Gruner-atero, @TomerBN-Nvidia, @wjinxu, @IdoAtadTD, @xiaozcy, @brian-dellabetta, @zhenwei-intel, @adotdad, @Kartavyasonar, @lesj0610, @ECMGit, @cakeng, @william-rom, @qiching, @NolanHo, @andylolu2, @xwu-intel, @linitra24, @hoobnn, @Dymasik, @wanghenshui, @maobaolong, @oguzhankir, @Jie-Fang, @okorzh-amd, @Kevin-XiongC, @jiahanc, @garrygale, @dsikka, @QiliangCui2023, @wjabbour, @zvik, @tc-mb, @jwzheng96, @divakar-amd, @tushar00jain, @galletas1712, @hanlin12-AMD, @tuukkjs, @viiccwen, @Sunt-ing, @HueCodes, @tianyu-z, @adhithyamulticoreware, @rishitdholakia13, @effi-ofer, @Vikrantpalle, @walterbm, @devin-lai, @Yadan-Wei, @amd-fuweiy, @maeehart, @qyYue1389, @BramVanroy, @SunskyXH, @Holworth, @majian4work, @xaguilar-amd, @Rohan138

---

## v0.22.1  (2026-06-05T10:10:00Z)

## Highlights

This release features 8 commits from 6 contributors (1 new)!

v0.22.1 is a patch release on top of v0.22.0 with targeted bug fixes plus a couple of additions: new model support for JetBrains' Mellum v2, zentorch-accelerated quantized linear inference on AMD Zen CPUs, and fixes for multi-node Ray data-parallel serving, DeepSeek-V4 initialization, and a few model-loading regressions.

### Model Support
* New model: JetBrains' **Mellum v2**, an open-weights Mixture-of-Experts code-generation model (#43992).
* **DeepSeek-V4**: resolve a CUTLASS `fmin` compatibility issue that broke initialization (0decac0d).
* Fix `OlmoHybridForCausalLM` failing to initialise after the checkpoint changed `rope_parameters` from `None` to `{"rope_type": None}` (#43846).
* Fix **HyperCLOVAX** loading after the upstream HuggingFace repo removed its remote code (now native in `transformers >= 5.9.0`): register the `hyperclovax` model_type so vLLM uses its vendored config instead of the stale `auto_map` (#43860).

### Hardware & Performance
* **AMD Zen CPUs**: route W8A8 (int8 dynamic-symmetric) and W4A16 (GPTQ) linear inference through zentorch kernels, registered ahead of the generic oneDNN CPU kernels, with transparent fallback on non-Zen CPUs, GPUs, and XPU (#41813).

### Large Scale Serving
* Fix a deterministic hang in multi-node **Ray data-parallel** serving with `num_api_servers > 1` by excluding the Ray DP backend from the deferred (kernel-assigned) port allocation introduced in #42585 (#43864).

### Build & CI
* Docker: stop installing `flashinfer-jit-cache` via `--extra-index-url` while it is quarantined on PyPI, fixing image builds (#44366).
* Normalize **NIXL** KV-connector wheel installs so only the wheel matching the image's CUDA major is kept, fixing `ImportError: libcudart.so.12` when importing `nixl_ep` on CUDA 13 images (#44266).

## Contributors

@khluu, @vadiklyutiy, @aadwived, @shadeMe, @alec-flowers, @hmellor

## New Contributors

* @aadwived made their first contribution in https://github.com/vllm-project/vllm/pull/41813

---

## v0.22.0  (2026-05-29T10:28:13Z)

## Highlights

This release features 459 commits from 230 contributors (63 new)!

* **DeepSeek V4 maturity**: DeepSeek V4 received a major hardening pass this cycle — the model was reorganized into a dedicated `vllm/models/deepseek_v4/` package (#43004, #43039, #43073, #43077, #43149), gained NVFP4 fused MoE support (#42209), full + piecewise CUDA graph (#42604), and MTP speculative decoding (#43385). A large set of fused kernels (MegaMoE, `mhc`, Q-norm, indexer, sparse MLA) and ROCm parity fixes landed alongside accuracy fixes (#42810, #43710).
* **Model Runner V2 advances toward default**: MRv2 is now default for Qwen3 dense models. vLLM will fall back to MRv1 for features that aren't yet supported in MRv2 (#39337). sleep-mode weight reload (#42673), `update_config` (#42783), and shared KV-cache layers (#35045), plus many correctness fixes.
* **Experimental Rust frontend**: A new Rust front-end integration landed (#40848), with the implementation moved into the tree (#43283) and a DP Supervisor for data-parallel serving (#40841).
* **Batch invariance, faster**: Batch-invariant inference gained Cutlass FP8 support for a **28.9% end-to-end latency improvement** (#40408), compile-mode support on SM80 (#42456), and an NVFP4 Cutlass linear path (#39912).
* **Multi-tier KV cache offloading**: A new multi-tier KV cache offloading framework (#40020) with a Python filesystem secondary tier (#41735), DSv4 support (#43142), and Mooncake disk offloading (#42689) extends offloading beyond CPU memory.

### Model Support
* New architectures: MiniCPM-V 4.6 (#41254), InternS2 Preview (#42705), OpenVLA (#42654), MolmoWeb `hf_overrides` docs (#42163); EXAONE-4.5 aligned with Transformers update (#42246).
* Speculative decoding: custom callable proposer backend (#39487), post-norm EAGLE-3 speculators (#42764), peagle speculators (#41826), hybrid-attention models in `extract_hidden_states` (#39949), non-MTP speculation for NemotronH (#43130), shared MTP weights in MRv2 (#42538).
* DeepSeek V4: NVFP4 MoE (#42209), CUDA graph full/piecewise (#42604), MTP (#43385), model package refactor (#43004, #43039, #43073, #43077), sparse MLA + compressor refactor (#43149, #43710), MegaMoE input-prep kernel move (#43632).
* Qwen3.5/3.6: GDN output-projection flatten (#42311), GatedDeltaNet Marlin TP≥2 fix (#36329), ViT full CUDA graph (#42151), runai-streamer weight loading for Qwen3.5/MTP/Qwen3-VL (#42521, #42716), KDA chunk-prefill exp2 semantics (#43195).
* Gemma3/Gemma4: mixed-resolution image co-batching crash fix (#42217), MoE routing closure fix (#42250), tool-parser float-corruption fix (#42128), batched vision encoder for image/video (#43169), multi-GPU fix (#42630).
* Kimi-K2.5: skip vision-tower dtype conversion under quantization (#42869), `mm_projector` dtype fix (#42081).
* Cohere: enable Cohere MoE (#43143), pipeline parallelism for Cohere vision (#42819).
* Tool calling: Apertus tool parser (#41154), Qwen3Coder `anyOf`/`oneOf`/`$ref` resolution re-land (#37831), shared `coerce_to_schema_type` across MiniMax-M2 / DeepSeek-V3.2 / Seed-OSS parsers (#43006, #43019, #43140).
* ViT CUDA graph: Qwen2-VL (#41736), Step3-VL encoder (#42224), Qwen3.5 (#42151), FlashInfer metadata for Qwen2.5-VL vision attention (#42787).

### Engine Core
* Model Runner V2: Qwen3-dense-by-default oracle (#39337), sleep-mode reload weights (#42673), `update_config` (#42783), shared KV-cache layers (#35045), FP32 gumbel sampling (#41775), auto-fallback to MRv1 with connectors (#42955), `logprob_token_ids` correctness (#43125, #41761), prompt-logprobs size fix (#42778).
* KV offloading: multi-tier framework (#40020), Python filesystem secondary tier (#41735), DSv4 support (#43142), tier-offload follow-up (#42529), prefer HND layout (#41928), `reset_cache()` (#41956), per-request tracking (#42507), store-deferral fix (#41945).
* MoE refactor: `ExpertMapManager` (#41046), experts moved to `experts/` (#42334), `RoutedExperts` alias for FusedMoE (#40735), EPLB refactoring for FusedMoE (#41055).
* Mamba: attention module refactor (#41126), Mamba2 SSD kernel warmup (#39822), bf16 SSM cache (#41680), GPU-side state postprocessing fused kernel (#40172), run single-token extends as decodes (#42430).
* KV events: emit KV cache metadata (#40984).
* Allocator: manual cumem allocator enable (#33648), stream-aware free callback (#43020).
* elastic-EP: stage/commit MoE quant method on reconfigure (#40881).

### Hardware & Performance
* **NVIDIA Blackwell / SM12x**: FlashInfer b12x MoE + FP4 GEMM for SM120/121 (#40082), per-tensor FP8 CUTLASS on SM12.1 (#41215), `head_dim=512` for FlashInfer TRTLLM attention (#38822), FlashInfer Blackwell GDN prefill (#40717), GDN prefill kernel for SM100 (#43273).
* **Performance**: batch-invariant Cutlass FP8 (+28.9% E2E) (#40408), CutlassFP8 padding pre-processing (+13.5% TTFT) (#42651), padded NVFP4 quant kernel (+2.4–5.7% E2E) (#42774), GPU<->CPU sync elimination 1/n (#41429) and 4/n (#42347), fused RoPE+KVCache+q_concat for MLA (#40392), MLA `compute_prefill_context` / `_v_up_proj` optimizations (#42460, #42561), penalties Triton kernel (#40657), `do_not_specialize` in fused FP8 RoPE (#42849), FULL CUDA graph capture for TRITON_MLA decode (#42885).
* **AMD ROCm**: DSV4 functionality + accuracy fixes (#42810, #43679 Tilelang MHC), flash sparse MLA Triton kernels (#41812), gluon paged MQA logits on gfx950/MI355X (#42062), RMSNorm+Quant fusion for gfx950 (#41825), AITER FA backend cleanup (#41942), XGMI backend for MoRI connector (#41753), QuickReduce min-size override (#41675), DSV4 MTP (#43385).
* **CPU / RISC-V**: RVV-optimized attention kernels for RISC-V Vector Extension (#40119) with VLEN=256 (#42943), fused GDN for AMX CPU (#42707), MXFP4 W4A16 MoE (#41922), experimental Triton + MRv2 on CPU (#43225), improved CPU thread utilization (#42666), `--cpu-distributed-timeout-seconds` (#42968).
* **Intel XPU**: GPTQ int4 support (#37844), mxfp8 MoE (#41918), FP8 block-scaled quantization (#42952), custom-op collective behavior (#41354), multiple sparse-attention kernels (#37888), MoE topk routing + MXFP4 fallback (#42951), CT W4A4 MXFP4 path (#38896), reduced XPU MoE host overhead (#42915).
* **Kernel ABI**: continued migration to libtorch stable ABI — 5/n (#42339), 6/n (#42663), 7/n (#43209).
* **Experimental**: breakable CUDA graph (#42304).

### Large Scale Serving
* Disaggregated serving (NIXL): lease-renewal TTL for KV blocks on P (#41383), handshake-failure policy honoring (#40364), GDN support for PD with NIXL (#41869), multi-node TP>8 fix (#39907), side-channel host-selection fix (#41806).
* Mooncake: disk offloading in MooncakeStoreConnector (#42689), HMA support for DSV4 (#42828), operation metrics (#43392), load-failure propagation (#42788), block-aligned full hits (#43494), finish-after-preemption handling (#43281).
* Data parallel: DP Supervisor (#40841), publish request counts at engine-step start (#41626), forward `X-data-parallel-rank` header (#42330).
* EPLB: change default EPLB communicator (#43110), VLM-wrapper init fix (#39805), remove dead `torch.accelerator.synchronize()` (#40733).
* LoRA: one-shot Triton kernel for MoE LoRA (#42290), simultaneous 2D & 3D MoE LoRA adapters (#42242), reduced 2D-weight memory under EP (#42737), MoE LoRA align-kernel grid fix (#40131).

### Quantization
* **MXFP4**: linear layers + compressed-tensors integration (#41664), CPU W4A16 MoE (#41922), XPU mxfp8 MoE (#41918).
* **NVFP4**: DeepSeek V4 fused MoE (#42209), ModelOpt W4A16 NVFP4 fused MoE + mixed-precision dispatch (#42566), batch-invariant NVFP4 Cutlass linear (#39912), FlashInfer TRTLLM NvFP4 monolithic MoE routing fix (#43223), TRTLLM NVFP4 MoE chunking fix (#43599).
* **Quark**: load Quark NVFP4 checkpoints (#35859), W8A8 INT8 garbage-output fix on Step-3.5-Flash (#41892), W4A4 oracle refactor (#41436).
* **AutoRound**: W4A16 support (#39778).
* **ModelOpt**: Qwen3.5/3.6 VLM quantized prefix mapping (#42546).
* **Framework**: rework `quantization_config` to use `QuantKey` with activation override (#41566), MoE W4A8 CT migrated to oracle (#42680), AWQ Marlin MoE onto modular WNA16 oracle (#42483), GPTQ consolidation (`gptq_marlin` → `auto_gptq`) (#38288).

### API & Frontend
* **Rust frontend**: integration (#40848), in-tree code move (#43283), utility call-ID newtype (#43405), simplified `AuthenticationMiddleware` path extraction (#43426).
* **Responses API**: `chat_template_kwargs` support (#42272), message-merging fix (#42189), empty channel/recipient harmony fix (#35540).
* **Completions**: `thinking_token_budget` support (#42116) with inverted-condition fix (#41674); map `reasoning_effort` to `enable_thinking` (#43401).
* **Frontend**: truncation side for OpenAI endpoints (#43260), normalize `reasoning_content` → `reasoning` (#42664), reworked fastokens integration (#43168), consolidated Speech-to-Text entrypoints (#42370, #42274), beam-search consolidation via `BeamSearchMixin` (#42946), score/rerank chat-template instructions (#42412).
* **Auth**: API-key authorization for `/v2` endpoints (#42594).
* **Offline API**: pooling offline API split into `PoolingOfflineMixin` (#42267), split offline inference APIs/utils (#43553).

### Build & Dependencies
* CUDA 12.9 wheel builds switched to PyTorch `manylinux_2_28` base (#41668).
* FlashInfer bumped to v0.6.11.post2 (#41711); `nvidia-cutlass-dsl` to 4.5.2 (#42991, #43230, #43745); llguidance to 1.7 (#42150); `triton_kernels` downgraded to v3.5.1 for gpt-oss (#43135).
* Rust frontend build: `setuptools-rust` dependency (#43287, #43377), pinned `protoc` in rust-build stages (#43292).
* Docker: non-root `vllm-openai` target (#40275), build `mooncake-transfer-engine` from source (#42114), AINIC & Thor NIC support (#40453); Python-only installation made optional (#42293).
* vllm-tpu: disable build isolation for CUDA deps (#43038), tpu-inference docker build fix (#43360).
* `humming` MoE backend dependency added, reverted, then restored with CuPy runtime fix (#42540, #43492, #43530).

### Deprecations & Removals
* Removed old locations of `get_tokenizer` and `resolve_hf_chat_template` (#35024).
* Marked env vars now covered by `--moe-backend` / `--linear-backend` (#43148).
* Removed deprecated MLA prefill arguments (#42555).
* Removed dead CUDA kernels and dead code (#42767, #42889, #43144).

## Contributors

@yewentao256, @haosdent, @njhill, @mgoin, @jeejeelee, @AndreasKaratzas, @NickLucche, @sfeng33, @noooop, @WoosukKwon, @khluu, @taneem-ibrahim, @Dao007forever, @vadiklyutiy, @bnellnm, @ivanium, @tjtanaa, @mmangkad, @hmellor, @DarkLight1337, @hickeyma, @zhenwei-intel, @jikunshang, @ronensc, @benchislett, @hao-aaron, @arpera, @zyongye, @gau-nernst, @frida-andersson, @ZhanqiuHu, @cleonard530, @akii96, @bedeks, @Isotr0py, @JasonKeyiL, @bigPYJ1151, @zhewenl, @weizhoublue, @zxd1997066, @gnovack, @chaojun-zhang, @majian4work, @chaunceyjiang, @pschlan-amd, @amitz-nv, @yma11, @dsikka, @tc-mb, @shanjiaz, @jperezdealgaba, @yzong-rh, @viktorpusTT, @TheEpicDolphin, @MatthewBonanni, @shen-shanshan, @hallerite, @zufangzhu, @bbrowning, @divakar-amd, @ianliuy, @esmeetu, @rasmith, @louie-tsai, @pmaybank, @liulanze, @ZJY0516, @TheDuyIT, @wzhao18, @jinzhen-lin, @BugenZhao, @ashwing, @fuergaosi233, @hqhq1025, @shaharmor98, @pisceskkk, @lkm2835, @noa-neria, @Rohan138, @whx-sjtu, @vrdn-23, @alexagriffith, @Flink-ddd, @jeffreywang-anyscale, @skyloevil, @ymoslem, @Lucaskabela, @kg6-sleipnir, @woernfl, @tdoublep, @GOavi101, @jmamou, @PeaBrane, @KaivalyaMDabhadkar, @BWAAEEEK, @MrZ20, @afierka-intel, @JoursBleu, @hissu-hyvarinen, @mwawrzos, @CynicDora, @NoeliaBentancor, @johncalesp, @fynnsu, @fxmarty-amd, @walterbm, @liangel-02, @lgeiger, @he-yufeng, @abinggo, @KrxGu, @hks-9697-v2, @Sarah-Salah, @rebklee, @aoshen02, @haic0, @libinta, @Zhenzhong1, @xhx1022, @b-mu, @WindChimeRan, @tpopp, @charlifu, @chengyinie, @ricky-chaoju, @lyd1992, @daniel-devlab, @paulyu12, @bobofang11235, @laudney, @BadrBasowid, @maeehart, @PatchouliTIS, @chunxiaozheng, @blake-snc, @southfreebird, @rbrugaro-amd, @rasdani, @dusthunter, @qizzzh, @ProExpertProg, @qianlihuang, @alec-flowers, @JisoLya, @gaozihao-shy, @rishaps, @xyang16, @wendyliu235, @hlin99, @tianmu-li, @yuwenzho, @inisis, @kfirtoledo, @roikoren755, @liranschour, @vllm-agent, @blancsw, @netanel-haber, @BowenBao, @czhu-cohere, @amitport, @tuukkjs, @revit13, @ofirzaf, @qyYue1389, @junyanxu, @gracie-guo, @sagearc, @xinyu-intel, @yiwen101, @DomBrown, @tomeras91, @Dogacel, @maxdebayser, @fadara01, @Terrencezzj, @izikgo, @wangrui6, @kebe7jun, @rishitdholakia13, @j9smith, @meena-at-work, @dllehr-amd, @alexeldeib, @sonusflow, @lucianommartins, @AAISSJ, @DaoyuanLi2816, @zexplorerhj, @zhangxin81, @velonica0, @fuscof-ibm, @anishesg, @zhengluo-nv, @ylangtsou, @fangyuchu, @zx3xyy, @simondanielsson, @ruizhang99, @zixi-qi, @xwu-intel, @yufufi, @wdhongtw, @mrjunwan-lang, @wangxiyuan, @wasnertobias, @ilmarkov, @sychen52, @zhandaz, @russellb, @SandishKumarHN, @juhi10071998, @itayalroy, @djmmoss, @SumanthRH, @mayuyuace, @zhougit86, @meenchen, @lucifer1004, @popkart-EZ, @jzakrzew, @ffggs, @huanghua1994, @orozery, @danisereb, @rshavitt, @Yihuki, @QingZhou-YangHY, @Jie-Fang, @bbartels

## New Contributors

* @abinggo made their first contribution in https://github.com/vllm-project/vllm/pull/42128
* @afierka-intel made their first contribution in https://github.com/vllm-project/vllm/pull/40327
* @alexagriffith made their first contribution in https://github.com/vllm-project/vllm/pull/41987
* @alexeldeib made their first contribution in https://github.com/vllm-project/vllm/pull/43255
* @amitport made their first contribution in https://github.com/vllm-project/vllm/pull/41666
* @anishesg made their first contribution in https://github.com/vllm-project/vllm/pull/43079
* @bedeks made their first contribution in https://github.com/vllm-project/vllm/pull/40269
* @blake-snc made their first contribution in https://github.com/vllm-project/vllm/pull/35568
* @blancsw made their first contribution in https://github.com/vllm-project/vllm/pull/41154
* @bobofang11235 made their first contribution in https://github.com/vllm-project/vllm/pull/42604
* @BWAAEEEK made their first contribution in https://github.com/vllm-project/vllm/pull/42233
* @CynicDora made their first contribution in https://github.com/vllm-project/vllm/pull/39487
* @daniel-devlab made their first contribution in https://github.com/vllm-project/vllm/pull/42479
* @DaoyuanLi2816 made their first contribution in https://github.com/vllm-project/vllm/pull/42905
* @Dogacel made their first contribution in https://github.com/vllm-project/vllm/pull/42764
* @DomBrown made their first contribution in https://github.com/vllm-project/vllm/pull/42080
* @dusthunter made their first contribution in https://github.com/vllm-project/vllm/pull/42594
* @ffggs made their first contribution in https://github.com/vllm-project/vllm/pull/43414
* @frida-andersson made their first contribution in https://github.com/vllm-project/vllm/pull/41825
* @fuergaosi233 made their first contribution in https://github.com/vllm-project/vllm/pull/43488
* @gaozihao-shy made their first contribution in https://github.com/vllm-project/vllm/pull/42869
* @gracie-guo made their first contribution in https://github.com/vllm-project/vllm/pull/42626
* @haic0 made their first contribution in https://github.com/vllm-project/vllm/pull/40453
* @hks-9697-v2 made their first contribution in https://github.com/vllm-project/vllm/pull/42521
* @hlin99 made their first contribution in https://github.com/vllm-project/vllm/pull/42740
* @inisis made their first contribution in https://github.com/vllm-project/vllm/pull/41710
* @izikgo made their first contribution in https://github.com/vllm-project/vllm/pull/42938
* @j9smith made their first contribution in https://github.com/vllm-project/vllm/pull/41215
* @junyanxu made their first contribution in https://github.com/vllm-project/vllm/pull/42671
* @KaivalyaMDabhadkar made their first contribution in https://github.com/vllm-project/vllm/pull/42333
* @libinta made their first contribution in https://github.com/vllm-project/vllm/pull/41689
* @lucifer1004 made their first contribution in https://github.com/vllm-project/vllm/pull/43433
* @meena-at-work made their first contribution in https://github.com/vllm-project/vllm/pull/40082
* @mrjunwan-lang made their first contribution in https://github.com/vllm-project/vllm/pull/43360
* @MrZ20 made their first contribution in https://github.com/vllm-project/vllm/pull/42394
* @mwawrzos made their first contribution in https://github.com/vllm-project/vllm/pull/42498
* @NoeliaBentancor made their first contribution in https://github.com/vllm-project/vllm/pull/42250
* @ovidiusm made their first contribution in https://github.com/vllm-project/vllm/pull/42542
* @paulyu12 made their first contribution in https://github.com/vllm-project/vllm/pull/42306
* @QingZhou-YangHY made their first contribution in https://github.com/vllm-project/vllm/pull/43579
* @qizzzh made their first contribution in https://github.com/vllm-project/vllm/pull/41680
* @qyYue1389 made their first contribution in https://github.com/vllm-project/vllm/pull/42289
* @rasdani made their first contribution in https://github.com/vllm-project/vllm/pull/42481
* @rebklee made their first contribution in https://github.com/vllm-project/vllm/pull/42098
* @revit13 made their first contribution in https://github.com/vllm-project/vllm/pull/42926
* @ruizhang99 made their first contribution in https://github.com/vllm-project/vllm/pull/43260
* @Sarah-Salah made their first contribution in https://github.com/vllm-project/vllm/pull/42441
* @sonusflow made their first contribution in https://github.com/vllm-project/vllm/pull/36329
* @TheDuyIT made their first contribution in https://github.com/vllm-project/vllm/pull/40131
* @tuukkjs made their first contribution in https://github.com/vllm-project/vllm/pull/42880
* @vllm-agent made their first contribution in https://github.com/vllm-project/vllm/pull/42913
* @wangrui6 made their first contribution in https://github.com/vllm-project/vllm/pull/40326
* @wasnertobias made their first contribution in https://github.com/vllm-project/vllm/pull/43001
* @weizhoublue made their first contribution in https://github.com/vllm-project/vllm/pull/42830
* @woernfl made their first contribution in https://github.com/vllm-project/vllm/pull/42397
* @xwu-intel made their first contribution in https://github.com/vllm-project/vllm/pull/37888
* @Yihuki made their first contribution in https://github.com/vllm-project/vllm/pull/42933
* @yiwen101 made their first contribution in https://github.com/vllm-project/vllm/pull/42654
* @ylangtsou made their first contribution in https://github.com/vllm-project/vllm/pull/43038
* @yufufi made their first contribution in https://github.com/vllm-project/vllm/pull/42972
* @zhengluo-nv made their first contribution in https://github.com/vllm-project/vllm/pull/43105
* @zhougit86 made their first contribution in https://github.com/vllm-project/vllm/pull/42739
* @zx3xyy made their first contribution in https://github.com/vllm-project/vllm/pull/42855

---

## v0.21.0  (2026-05-15T08:44:26Z)

## Highlights

This release features 367 commits from 202 contributors (49 new)!

* **Transformers v4 deprecated**: This release formally deprecates `transformers` v4 support (#40389). Users should migrate to `transformers` v5.
* **C++20 build requirement**: vLLM now requires a C++20-compatible compiler for compatibility with PyTorch (#40380). This is a **breaking build change**.
* **KV Offload + Hybrid Memory Allocator (HMA)**: The KV offloading subsystem now integrates with the Hybrid Memory Allocator, including scheduler-side sliding window group support and full HMA enablement (#41228, #41445, #39571).
* **Speculative decoding with thinking budget**: Speculative decoding now respects reasoning/thinking budgets, enabling correct spec decode for reasoning models (#34668).
* **TOKENSPEED_MLA backend on Blackwell**: A new TOKENSPEED_MLA attention backend is available for DeepSeek-R1/Kimi-K25 prefill + decode on Blackwell GPUs (#41778).

### Model Support
* New architectures: MiMo-V2.5 (#40967), Laguna XS.2 (#41129, #41880), Moondream3 (#32325), Qianfan-OCR (#40136), Cohere MoE (#40817), Cohere Eagle (#42078).
* Speculative decoding: EAGLE for Mistral (#41024), Gemma4 MTP (#41745), MTP for MiMo-V2.5 (#41905), Cohere Eagle (#42078).
* DeepSeek V4: AMD/ROCm support (#40871), pipeline parallelism (#41694), `max` reasoning effort (#40982), disaggregated serving fixes (#41957).
* Tool calling: Cohere reasoning and tool parsers (#40422), LFM2/2.5 tool parser (#39243).
* Gemma3/Gemma4: `hidden_act` variant support (#40588), pipeline parallelism fix (#40786), MoE fixes (#41206, #41574, #41401), tool parser crash fix (#41991, #42188).
* Model Runner V2: Qwen3.5/Mamba hybrid model support (#35520), `logprob_token_ids` support (#40559).
* CUDA graph: ViT CUDA graph support for Qwen2.5-VL (#40830).
* Compatibility: Vendor HCXVisionConfig for Transformers v5 (#38447), legacy `rope_type` checkpoint support (#41734).

### Engine Core
* KV offloading + HMA: Scheduler-side sliding window groups (#41228), full HMA enablement (#41445), multi-connector HMA (#39571), per-job store completion (#39186), DCP/PCP support in OffloadingConnector (#41549), MooncakeStoreConnector for distributed KV offloading (#40900).
* Speculative decoding: Thinking budget support (#34668), independent drafter attention backend selection (#39930), multimodal model support with warning (#41752), per-step allocation elimination (#41043).
* Model Runner V2: Rejection sampling acceptance rate fix (#40651), skip metadata rebuild before draft prefill (#40410), rebuild metadata between draft decode steps (#41162), Qwen3.5/Mamba hybrid support (#35520).
* Routing: Replace routing replay with device cache and async D2H pipeline (#39917).
* Ray: RayExecutorV2 enabled by default (#41421), actor name collision fix for DP > 1 (#40398).
* Stability: Two-phase pause to prevent scheduler deadlock (#39366), thread-safe HF tokenizer wrappers (#41181), OOM prevention via `max_split_size_mb` during model loading (#41268).
* IndexCache support for DSA models (#37735).

### Hardware & Performance
* **NVIDIA Blackwell**: TOKENSPEED_MLA backend for DSR1/Kimi-K25 (#41778), faster per-token FP8 group quant packed kernel (#41326), FP8 on NVIDIA Thor/SM110 (#39712), CUTLASS scaled mm for non-compatible sizes (#41868).
* **Performance**: FlashInfer top-k/top-p sampler enabled by default (#40376), FP8 FlashInfer attention for ViT (#38065), TurboQuant shared dequant buffers (#40941), `AllPool.forward` 51% faster (#41163), GPU<->CPU sync elimination in pooling (#41433) and attention (#41434), numpy zero-copy embedding serialization (#41681), multimodal processor skip for text-only (#41246), FlashInfer FP8 async TP fusion (#39505), NVFP4 all-gather GEMM fusion for AsyncTP (#41882), re-enable allreduce+RMS fusion for DP/PP (#41458), DeepSeek bf16→fp32 via `torch.mm` (#41300), persistent MLA for sparse backend (#41990), configurable safetensors checkpoint prefetch (#41499), fused mhc_post_pre kernel (#41536), 2D-grid W8W8 group quant kernel (#42153), relaxed memory ordering for KV cache swaps (#39306).
* **AMD ROCm**: ROCm 7.2.2 (#41386), DBO (Dynamic Batch Optimization) (#34726), AITER Fused Allreduce+RMSNorm (#37646), Fused Shared Expert (FSE) for Qwen3-Next (#39280), DeepSeek V3.2 TP4 AITER MLA (#41835), GDN linear attention fusion (#40711), eliminate redundant MoE buffer copies in AITER (#41713), CPU offloading support (#40549), DeepEP API update (#39721), cap Triton paged attention block size to fix shared memory OOM (#38502).
* **CPU**: FP8 attention for AMX/AVX-512 (#39445), FP8 W8A16 linear (#41186), FP8 W8A16 MoE (#41314), DNNL AVX2 W8A8 Int8 (#41318), Gated DeltaNet Attention for Qwen 3.5/3.6 (#41025), RISC-V OMP thread auto-binding (#40569).
* **Intel XPU**: Top-k/top-p sample kernel (#39285), out-of-place all-reduce (#41808), LoRA support (#38206).
* **IBM Power**: VSX attention backend (#40451).
* **FlexAttention**: Re-enabled for batch invariant mode (#40842).
* **MLA**: Abstracted MLA prefill backends, eliminated cuDNN dependency (#32623).

### Large Scale Serving
* Disaggregated serving: Bi-directional KV cache transfers between P and D (#32553), NIXL transfer redesign (#40731), EPLB memory overhead optimization (#40013), NIXL connector bumped to 1.x (#42364), Mooncake KVConnectorStats for transfer observability (#40414), NIXL P-node pre-admission rejection notification (#41269), KV block release for skipped P-ranks (#40449).
* DCP: Pack output and LSE in DCP A2A (#41160).
* MoE: PluggableLayer interface for out-of-tree MoE runners (#35178).
* LoRA: Initial expert parallel (EP) support (#40867), Qwen3.5 LoRA fusion fix (#37912).

### Quantization
* **NVFP4**: KV cache support (#40177), Triton dequant/QDQ emulation kernels for Hopper and AMD (#40033), GELU on TRT-LLM NvFP4 fused MoE for Gemma4 (#41050), ModelOpt NVFP4 W4A16 (#41769), NVFP4 all-gather GEMM fusion for AsyncTP (#41882), GLM4-MoE NVFP4 loading fix (#41755).
* **MXFP4**: Humming MXFP4 MoE backend (#41083), FlashInfer CUTLASS MXFP4-MXFP8 MoE fix (#42089).
* **TurboQuant**: Hybrid model and uniform quantization support (#39931).
* **Compressed tensors**: Allow configs with non-explicit ignores (#41965).
* **FP8**: Bias loading fix (#41424), FlashInfer autotune temporarily disabled for correctness (#41524).
* **DSV4**: Improved fused Indexer Q quant kernel (#41428).

### API & Frontend
* **Responses API**: Streaming tool/function calling with `required` (#40700) and named tool/function choice (#41110), resubmitting output items with missing fields (#41355).
* **OpenAI compatibility**: `system_fingerprint` field in responses (#40537), `prompt_embeds` content part support (#40720), `defer_loading` and `tool_reference` support (#40190), rendered prompt text in chat completion response (#42052), tolerate empty content in forced tool choice (#40148).
* **Tool calling**: XGrammar 0.2.0 with structural tags for strict tool calling + reasoning (#40894), Cohere reasoning/tool parsers (#40422), LFM2/2.5 tool parser (#39243).
* **Tokenizer**: Fastokens support (#41741).
* **RLHF**: Explicit `/start_weight_update` and `/finish_weight_update` APIs (#39212).
* **ASR**: Engine request abort on cancellation (#41266).
* **Configuration**: `VLLM_SKIP_MODEL_NAME_VALIDATION` env var (#34676), configurable model weights loading tracking (#41086), Triton JIT compilation monitor (#40137).

### Build & Dependencies
* **Breaking**: C++20 required for PyTorch compatibility (#40380).
* **Breaking**: Transformers v4 deprecated (#40389).
* Docker image size reduced by ~2.5 GB via deferred FlashInfer cubin download (#41134).
* CUDA 13.0 wheels switched to PyTorch manylinux_2_28 base (#41416).
* DeepGEMM bundled wheel built per-Python for CPython compatibility (#41516).
* Container image provenance metadata embedded (#40653).
* tpu-inference upgraded to v0.19.0 (#41844).
* NIXL connector bumped to 1.x (#42364).
* ROCm 7.2.2 (#41386).

## Contributors

@AndreasKaratzas, @haosdent, @khluu, @yewentao256, @stecasta, @mgoin, @Isotr0py, @hmellor, @chaunceyjiang, @jeejeelee, @noooop, @MatthewBonanni, @njhill, @zyongye, @yzong-rh, @ronensc, @NickLucche, @chaojun-zhang, @dzhengAP, @chfeng-cs, @TheEpicDolphin, @esmeetu, @wzhao18, @ZJY0516, @juliendenize, @kylesayrs, @fadara01, @Etelis, @tianmu-li, @arpera, @ekagra-ranjan, @orozery, @wxsIcey, @jikunshang, @izhuhaoran, @rasmith, @russellb, @Lucaskabela, @Harry-Chen, @alec-flowers, @pmaybank, @Terrencezzj, @hickeyma, @Baekpica, @itej89, @fxmarty-amd, @WoosukKwon, @juhi10071998, @sychen52, @baonudesifeizhai, @vllmellm, @johncalesp, @the-david-oy, @lucianommartins, @bittoby, @Dao007forever, @lyd1992, @yuwenzho, @lesj0610, @sfeng33, @micah-wil, @akii96, @yma11, @SoluMilken, @mmangkad, @SiluPanda, @ojhaanshika, @zhandaz, @bhoomit, @simon-mo, @msanft, @angelayi, @anthonsu, @artem-spector, @zhangxin81, @benoittgt, @joerowell, @yangrz7, @chelnnexy, @liangel-02, @walterbm, @rishitdholakia13, @SKRohit, @BugenZhao, @JaredforReal, @amd-lalithnc, @frgossen, @h-avsha, @DarkLight1337, @danisereb, @laithsakka, @Bortlesboat, @wangluochao902, @Rohan138, @hao-aaron, @puririshi98, @roikoren755, @heachary, @UranusSeven, @dsingal0, @ChenxiQ, @snadampal, @ilmarkov, @wendyliu235, @lequytra, @JisoLya, @LuisRobaina, @sniper35, @eicherseiji, @Yuyi-Ao, @raviguptaamd, @sungsooha, @ganyi1996ppo, @andylolu2, @FredericOdermatt, @ProExpertProg, @rbrugaro-amd, @mcsantiago, @hnt2601, @jinzhen-lin, @taneem-ibrahim, @tomeras91, @alex-jw-brooks, @Aktsvigun, @HanFa, @netanel-haber, @JasonKeyiL, @gshtras, @joa-stdn, @Seven-Streams, @JartX, @xuechendi, @BowenBao, @Akashcodes732, @jeffreywang-anyscale, @czhu-cohere, @zhewenl, @marvinzh, @Lidang-Jiang, @gcanlin, @whx-sjtu, @S1ro1, @liulanze, @Dhruvilbhatt, @laviier, @wi-adam, @aaab8b, @yuankaichen-amd, @ZhanqiuHu, @QwertyJack, @viktorpusTT, @divakar-amd, @starkwj, @benchislett, @jcyang43, @JLiu4Coding, @xy3xy3, @hongxiayang, @amd-mghanimi, @wenyili, @bigPYJ1151, @s-yanev, @AlonKejzman, @noobHappylife, @TomerBN-Nvidia, @MeganEFlynn, @liuzijing2014, @jbuchananr, @lokashrinav, @ssam18, @dllehr-amd, @gmagogsfm, @tpopp, @tjtanaa, @simondanielsson, @zhenwei-intel, @HiroakiMikami, @nholmber, @SumanthRH, @LucasWilkinson, @maeehart, @rishaps, @r-barnes, @gau-nernst, @Kermit-C, @tdoublep, @aoshen02, @Naveassaf, @wangxingran222, @cvan20191, @AbhiOnGithub, @abdulrahman-cohere, @jmamou, @Flink-ddd, @bnellnm, @hqhq1025, @gnovack, @wangxiyuan, @princepride, @jiahanc, @LCAIZJ, @ovidiusm

## New Contributors

* @abdulrahman-cohere made their first contribution in https://github.com/vllm-project/vllm/pull/41266
* @AbhiOnGithub made their first contribution in https://github.com/vllm-project/vllm/pull/42180
* @Aktsvigun made their first contribution in https://github.com/vllm-project/vllm/pull/40788
* @amd-mghanimi made their first contribution in https://github.com/vllm-project/vllm/pull/41713
* @Baekpica made their first contribution in https://github.com/vllm-project/vllm/pull/41206
* @benoittgt made their first contribution in https://github.com/vllm-project/vllm/pull/41134
* @bittoby made their first contribution in https://github.com/vllm-project/vllm/pull/41690
* @chelnnexy made their first contribution in https://github.com/vllm-project/vllm/pull/40754
* @ChenxiQ made their first contribution in https://github.com/vllm-project/vllm/pull/40956
* @chfeng-cs made their first contribution in https://github.com/vllm-project/vllm/pull/42066
* @cvan20191 made their first contribution in https://github.com/vllm-project/vllm/pull/40951
* @dzhengAP made their first contribution in https://github.com/vllm-project/vllm/pull/41423
* @ghphotoframe made their first contribution in https://github.com/vllm-project/vllm/pull/40859
* @HiroakiMikami made their first contribution in https://github.com/vllm-project/vllm/pull/40588
* @itej89 made their first contribution in https://github.com/vllm-project/vllm/pull/39721
* @JasonKeyiL made their first contribution in https://github.com/vllm-project/vllm/pull/41068
* @jbuchananr made their first contribution in https://github.com/vllm-project/vllm/pull/39243
* @JisoLya made their first contribution in https://github.com/vllm-project/vllm/pull/41363
* @JLiu4Coding made their first contribution in https://github.com/vllm-project/vllm/pull/41832
* @juhi10071998 made their first contribution in https://github.com/vllm-project/vllm/pull/41050
* @Kermit-C made their first contribution in https://github.com/vllm-project/vllm/pull/42076
* @lequytra made their first contribution in https://github.com/vllm-project/vllm/pull/41401
* @Lidang-Jiang made their first contribution in https://github.com/vllm-project/vllm/pull/38099
* @liulanze made their first contribution in https://github.com/vllm-project/vllm/pull/41571
* @lokashrinav made their first contribution in https://github.com/vllm-project/vllm/pull/41681
* @LuisRobaina made their first contribution in https://github.com/vllm-project/vllm/pull/40720
* @maeehart made their first contribution in https://github.com/vllm-project/vllm/pull/42061
* @marvinzh made their first contribution in https://github.com/vllm-project/vllm/pull/40136
* @mcsantiago made their first contribution in https://github.com/vllm-project/vllm/pull/41492
* @MeganEFlynn made their first contribution in https://github.com/vllm-project/vllm/pull/41880
* @nholmber made their first contribution in https://github.com/vllm-project/vllm/pull/39280
* @pmaybank made their first contribution in https://github.com/vllm-project/vllm/pull/41012
* @raviguptaamd made their first contribution in https://github.com/vllm-project/vllm/pull/34726
* @s-yanev made their first contribution in https://github.com/vllm-project/vllm/pull/41755
* @S1ro1 made their first contribution in https://github.com/vllm-project/vllm/pull/39213
* @Seven-Streams made their first contribution in https://github.com/vllm-project/vllm/pull/40894
* @SiluPanda made their first contribution in https://github.com/vllm-project/vllm/pull/40907
* @SKRohit made their first contribution in https://github.com/vllm-project/vllm/pull/40786
* @snadampal made their first contribution in https://github.com/vllm-project/vllm/pull/32553
* @sniper35 made their first contribution in https://github.com/vllm-project/vllm/pull/32325
* @ssam18 made their first contribution in https://github.com/vllm-project/vllm/pull/41486
* @the-david-oy made their first contribution in https://github.com/vllm-project/vllm/pull/40737
* @wangluochao902 made their first contribution in https://github.com/vllm-project/vllm/pull/41043
* @wenyili made their first contribution in https://github.com/vllm-project/vllm/pull/41901
* @wi-adam made their first contribution in https://github.com/vllm-project/vllm/pull/40749
* @xy3xy3 made their first contribution in https://github.com/vllm-project/vllm/pull/40820
* @yangrz7 made their first contribution in https://github.com/vllm-project/vllm/pull/40449
* @yuankaichen-amd made their first contribution in https://github.com/vllm-project/vllm/pull/40390
* @zhangxin81 made their first contribution in https://github.com/vllm-project/vllm/pull/39904

---

## v0.20.2  (2026-05-10T07:37:57Z)

# vLLM v0.20.2

## Highlights
This release features 6 commits from 6 contributors (0 new)!

This is a small patch release with bug fixes for DeepSeek V4, gpt-oss, and Qwen3-VL

### Bug Fixes
* **DeepSeek V4 sparse attention**: Re-enable the persistent topk path on Hopper and ensure the memset kernel runs at CUDA graph capture time regardless of `max_seq_len`, fixing the MTP=1 hang on DeepSeek V4 (#41665, revert of #41605).
* **DeepSeek V4 KV cache**: Fixed a "failure to allocate KV blocks" error in the V1 engine KV cache manager (#41282).
* **gpt-oss MXFP4 + torch.compile**: Plumbed `hidden_dim_unpadded` through the `moe_forward` fake op so MXFP4 works under `torch.compile` on v0.20.x (#42002, backport of #41646).
* **Qwen3-VL**: Removed an invalid deepstack boundary check that could fail under heavy load (#40932).

## Contributors
@ywang96, @zyongye, @stecasta, @wzhao18, @Isotr0py, @khluu

---

## v0.20.1  (2026-05-04T10:36:26Z)

# vLLM v0.20.1

This is a patch release on top of `v0.20.0` primarily focused on **DeepSeek V4 stabilization and performance improvements**, along with several important bug fixes.

### DeepSeek V4
* Base model support (#41006).
* Multi-stream pre-attention GEMM (#41061), configurable pre-attn GEMM knob (#41443), and tuned default `VLLM_MULTI_STREAM_GEMM_TOKEN_THRESHOLD` (#41526).
* BF16 and MXFP8 all-to-all support for FlashInfer one-sided communication (#40960).
* PTX `cvt` instruction for faster FP32->FP4 conversion (#41015).
* Integrated tile kernels (`head_compute_mix_kernel`) for optimized head computation (#41255).
* Guard megamoe flag with Pure TP (#41522).
* Fixed persistent topk cooperative deadlock at TopK=1024 (#41189) and inter-CTA init race on RadixRowState (#41444), with temporary disable of persistent topk as a workaround (#41442).
* Fixed import error due to AOT compile cache loading (#41090).
* Fixed torch inductor error (#41135).
* Fixed repeated RoPE cache initialization (#41148).
* Fixed missing type conversion for non-streaming tool calls in DSV3.2/V4 (#41198).

### Bug Fixes
* Fixed `max_num_batched_token` not being captured in CUDA graph (#40734).
* Fixed `num_gpu_blocks_override` not accounted for in `max_model_len` checks (#41069).
* Auto-disable `expandable_segments` around cumem memory pool (#40812).
* Fixed BailingMoE linear layer (#40859) and MLA RoPE rotation for BailingMoE V2.5 (#41185).
* Fixed reasoning parser kwargs not being passed to structured output (#41199).
* [ROCm] Fixed `input_ids` and `expert_map` args for Quark W4A8 GPT-OSS (#41165).

## List of contributors
@BugenZhao, @chaunceyjiang, @gau-nernst, @ghphotoframe, @Isotr0py, @jeejeelee, @khluu, @njhill, @Rohan138, @wzhao18, @youkaichao, @ywang96, @ZJY0516, @zixi-qi, @zyongye

---

## v0.20.0  (2026-04-27T21:20:28Z)

# vLLM v0.20.0

## Highlights
This release features 752 commits from 320 contributors (123 new)!

* **DeepSeek V4**: Initial DeepSeek V4 support landed (#40860), with DSML token-leakage fix in DSV4/3.2 (#40806), DSA + MTP IMA fix (#40772), and a silu clamp limit on the shared expert (#40950).
* **CUDA 13.0 default**: Default CUDA wheel on PyPI and `vllm/vllm-openai:v0.20.0` image switched to CUDA 13.0; architecture lists and build-args cleaned up (#39878), and CUDA bumped to 13.0.2 to match PyTorch 2.11.0 (#40669). As a general rule of thumb, our CUDA version policy follows PyTorch's. We highly recommend to install vLLM with `uv` and use `--torch-backend=cu129` if you are on CUDA 12.9.
* **PyTorch 2.11 upgrade** (#34644): vLLM ships on torch 2.11 for CUDA, and XPU is now also on torch 2.11 (#37947) — XPU is no longer pinned to 2.10. This is a breaking change for environment dependency.
* **Python 3.14**: Added to the supported Python version list (#34770).
* **Transformers v5**: vLLM now runs on HuggingFace `transformers>=5` (#30566), with vision-encoder torch.compile bypass (#30518) and continued v4/v5 compat fixes including PaddleOCR-VL image processor `max_pixels` (#38629), Mistral YaRN warning (#37292), and Jina ColBERT rotary inv_freq recompute (#39176).
* **New large models**: Hunyuan v3 (Hy3) preview (#40681) with HYV3 reasoning parser (#40713); Granite 4.1 Vision as a built-in multimodal model (#40282).
* **FlashAttention 4 as default MLA prefill**: FA4 re-enabled as the default MLA prefill backend (#38819) with head-dim 512 and paged-KV support on SM90+ (#38835), plus an upstream FA4 sync (#38690).
* **TurboQuant 2-bit KV cache**: New attention backend delivering 2-bit KV cache compression with 4× capacity (#38479), now with FA3/FA4 prefill support (#40092).
* **Online quantization frontend**: New end-to-end online quantization frontend (#38138), with docs (#39736); experts_int8 consolidated into the FP8 online path (#38463); MXFP8 online quant moved to the new frontend (#40152).
* **vLLM IR**: Initial IR skeleton with rms_norm op (#33825), OOT-platform kernel imports (#38807), gemma_rms_norm reworked on IR (#39014), and IR op testing/benchmarking infra added (#40167) — foundation for future kernel work.
* **Model Runner V2 advances**: Eagle prefill full-CUDA-graph (#37588), auto-resolve cudagraph mode/sizes from attention backend (#32936), fused probabilistic rejection sample kernels (#38496), config validation for unsupported features (#38758), piecewise-fallback disabled for eagle draft decodes (#39773), multiple prompt-logprobs support (#39937), prefill warmup coverage (#40746), and a fix for accuracy regression caused by stale sampled/draft tokens (#39833).
* **MoE refactor series**: Unquantized migrated to Full Oracle Flow (#36286), CT W8A8 to Oracle (#39187), SharedExperts class (#35153), `SharedFusedMoE` removed (#35782), DefaultMoERunner split (#35326) and later combined back into `MoERunnerBase` (#40560), shared/fused expert output sum moved into `MoERunnerBase` (#35949), ZeroExpertFusedMoE in new framework (#35549), `compressed_tensors_moe.py` split (#38960), `GPTQMarlinMoEMethod` reworked with MK (#37990), XPU & CUTLASS MoE relocated to `fused_moe/experts/` (#40568, #40574), `make_expert_params_mapping` renamed (#40671), MoE LoRA refactor (#40338), and MoE DP chunking removed (#39107).
* **Performance**: Optimize batch invariant with fused rms norm — 2.1% E2E latency improvement (#40413); avoid `seq_lens_cpu` GPU→CPU sync (#40654); cache `InductorPass.hash_source` (#39328); skip FX-graph deserialization on loading for faster warm compile (#40151); CUDAGraph memory profiling enabled by default for clearer startup memory accounting (#38284).

### Model Support
* New architectures: DeepSeek V4 (#40860), Hunyuan v3 preview (#40681), Granite 4.1 Vision (#40282), EXAONE-4.5 (#39388), BharatGen Param2MoE (#38000), Phi-4-reasoning-vision-15B (#38306), Cheers multimodal (#38788), telechat3 (#38510), FireRedLID (#39290), jina-reranker-v3 (#38800), Jina Embeddings v5 (#39575), Nemotron-v3 VL Nano/Super (#39747).
* Gemma4 series: fast prefill (#38879), quantized MoE (#39045), Eagle3 (#39450), block-local attention + YaRN for Gemma3 (#39823), bidirectional vision attention for sliding layers (#40534), token-repetition fix via dynamic BOS (#39842), multimodal embedder norm-order fix (#40411), plus a string of streaming/tool-call fixes (#38844, #38909, #38992, #39114, #39679, #39027).
* Quantization formats: GGUF support for MiniMax-M2.1 (#36965), non-standard GGUF quant types with prefix such as UD-IQ1_S (#39471).
* Speculative decoding: Eagle3 for MiniMax-M2 (#37512), Eagle3 for Gemma4 (#39450).
* LoRA: Qwen3ASRForConditionalGeneration (#37247), Gemma4ForConditionalGeneration (#39291, #38844), DeepSeek V3.2 (#35077), Qwen3.5 / Step3.x expert base_layer extension (#37114), MoE LoRA refactor (#40338), dual-CUDA-streams linear layer (#35721).
* Multimodal MRoPE refresh: mm_features-based MRoPE for Ernie-4.5 VL (#39753), Keye-VL / Keye-1.5-VL (#39869), PaddleOCR-VL (#39888).
* Other: Nano-Nemotron-VL static image inputs fix (#40724); Qwen3 MoE no longer calls gate twice (#40664); DeepSeek V2-Lite accuracy drop fix (#40673); Parakeet UX / perf enhancements (#39423); ColModernVBERT updated for latest HF checkpoint (#39307); NemotronH default `mamba_ssm_cache_dtype=float32` with NemotronHNanoVLV2 auto-hook (#39032); new TP plan styles for the Transformers backend (#40467); GLM-5.1 fix on ROCm (#40763).

### Engine Core
* **Model Runner V2**: Full CUDA graph for eagle prefill (#37588), auto cudagraph mode/sizes based on attention backend (#32936), fused probabilistic rejection-sample kernels (#38496), config validation (#38758), eagle-draft piecewise fallback disabled (#39773), multiple prompt logprobs (#39937), prefill warmup coverage (#40746), stale sampled/draft tokens accuracy fix (#39833).
* **vLLM IR**: IR skeleton + rms_norm (#33825), OOT kernel import hooks (#38807), gemma_rms_norm on IR (#39014), IR op testing/benchmarking infra (#40167).
* **torch.compile**: Opaque Objects on torch 2.11 (#39286), AOT compile with batch-invariance mode (#39201), Inductor cache nested under AOT dir (#39718), split FX graph via codegen (#38657), Inductor pre-grad passes re-enabled for torch≥2.12 (#38944), strings in custom ops without compile regressions (#38123), MLA + group FP8 fusion (#38877), SiluMul activation+quant fusion refactor (#39684), `donate_graph_module=True` for `standalone_compile` (#39733), skip FX graph deserialization on loading (#40151), include Inductor & functorch configs in compile-cache key (#40627), respect `TORCH_COMPILE_DISABLE` at vLLM config level (#40715), disable Sequence Parallelism for piecewise compilation (#38373).
* **Attention**: FA4 as default MLA prefill (#38819), head-dim 512 + paged-KV on sm90+FA4 (#38835), FA4 upstream sync (#38690), full CUDA graph for FlexAttention (#36298), FlexAttention non-causal support (#40394), unified 2D/3D triton_unified_attention (#40631), TRTLLM minimax_allreduce_rms ported (#37045), `concat_mla_q` half-types only (#37892), batch-invariance-aware backend auto-selection (#40193), avoid `seq_lens_cpu` GPU→CPU sync (#40654).
* **Helion kernels**: torch.compile support for Helion kernels (#38592).
* **HMA / KV offload**: GPU-side KV events for HMA (#37688), group block hashes/IDs tracked (#37109), unified memory layout for offloading workers (#37206), `shutdown()` on OffloadingConnector (#39182), request context passed through KV offload (#39185), sliding-window lookup (#36645), multi-group worker transfer (#38453), multi-KV-group lookup/load/store (#39401, #39402, #39403).
* **Features**: NUMA binding for GPU workers (#38635), opt-in `VLLM_MEDIA_CACHE` media URL caching (#37123), safe request abort when FSM fails to advance (#38663), KV connector prioritized over internal registry (#38301), CUDAGraph memory profiling on by default (#38284), shared-expert overlap restored (#39222), `CONFIG_REGISTRY` config-class lookup fix when on-disk model_type differs (#39554), workspace-resize GPU memory leak fix (#39226), SWA/chunked-local runtime admission capped to startup pool-sizing bound (#40946).
* **Pluggable layers**: Applied to llm_head / vocab embedding (#33465) and MoE layers (#33556).
* **Mamba**: Stochastic rounding (#35753), different Conv state layouts (#37416), FlashInfer `selective_state_update` (#36162).
* **Metrics & scheduling**: Labeled waiting-breakdown (capacity/deferred) metric (#38435), API server handshake simplified (#39364), mm-scheduler `get_num_embed` overhead reduced (#40143), `request_id` on `FinishedRequestStats` (#39710).
* **Executor**: RayExecutorV2 introduced (#36836); unified engine process monitoring with Ray backend (#35862).

### Hardware & Performance
* **NVIDIA**: swapAB support for SM120 CUTLASS blockwise FP8 GEMM (#38325), MXFP4 W4A4 CUTLASS MoE for SM100 (#37463), TRTLLM GEN NVFP4 MoE with non-512-aligned hidden dims via weight padding (#39510), TRTLLM FP8 MoE with shuffled weights + BlockMajorK layout (#38993), fused qknorm+rope kernel on SM9.0 (#37376), tuned fused_moe config for RTX PRO 6000 Blackwell (#39183), ViT full CUDA graph for Qwen3-VL video (#38061), `--enable-vit-cuda-graph` for VLM examples (#40580), default `max_frames_per_batch` auto-infer for ViT CG video (#40445), fused FP8 output quantization into `merge_attn_states` (#36518), batched KV-cache swap via `cuMemcpyBatchAsync` (#38460), sm_110 (Jetson Thor) added to CUDA 13.0 build targets (#39233).
* **AMD ROCm**: ZenCPU / AMD Zen CPU backend via zentorch (#39967), RDNA 3.5/4 device IDs (gfx1150/1151/1201) (#38455), gfx1102/gfx1103 added (#40037), MORI EP for unquantized MoE with AITER (#37529), MoRI build with AMD AINIC stack (#38371), MoRI-IO message format aligned with P2pNcclConnector and vllm-router (#39565), MORI prefill/decode API correction (#39835), AITER gemm w8a8 ptpc integration (#33773), TritonW4A16LinearKernel (#37352), asymmetric INT8 in `TritonInt8ScaledMMLinearKernel` (#38501), `fused_silu_mul_block_quant` enabled (#38817), KV-cache shuffle for `paged_attention_common` (#32914), MLA decode output zero-fill removed in AITER (#37539), MLA dual RMS norm fusion pass for DeepSeek/Kimi-K2 (#39242, with older-AITer guard #40386), AITER MLA + Eagle3 spec decode (#39616), DFlash on ROCm (#39703), wvSplitK FP8 path for RDNA (#37712), GPU↔NUMA-node detection (#40015), non-causal attention in `ROCM_ATTN` (#40176), engine-shutdown GPU memory leak fix (#38503), score-correction-bias dtype cast for DeepSeek/Kimi-K2 (#39999).
* **Intel XPU**: torch 2.11 upgrade for XPU (#37947) — no longer pinned to 2.10, initial GDN attention for Qwen3-Next / Qwen3.5 (#33657), torch.compile for XPU GDN attention (#39466), XPU MXFP8 quant op (#38682), XPU MXFP4 quant op (#39857), per-channel FP8 linear (#38316), FP8 KV cache on XPU (#37731), `round_int8` for Intel Triton (#38825), MoE Triton in online FP8 quantization fix (#40109), `current_platform.supports_fp8()` updated for TritonExperts (#40132), NIXL import on XPU fix (#40430), fusion-pattern support disabled on XPU (#39789).
* **CPU**: CPU draft-model speculative decoding (#32662), CPU int8 compute mode in AWQ (#35697), head_size 512 in `cpu_attn` (#38676), gelu in `cpu_fused_moe` (#38770), OMP replacement (#36487), BF16 GELU LUT on ARM (#37469), W4A16 Autoround on CPU (#38192), CPU affinity/memory mgmt refactor (#39781), IBM Z s390x torch 2.11 builds (#39910), faster exp routine for lower-precision dtypes (#38112), inter-node pipeline parallel fix (#40150), RISC-V multiple RVV VLEN targets (#39478), RISC-V platform detection fix (#40427), exp() input clamp to prevent NaN on CPU/RISC-V (#40428).
* **TPU**: tpu-inference upgraded to 0.18.0 (#40395).
* **DeepSeek / MLA / Indexer**: Persistent TopK scheduler for DSV3.2 DSA decode (#37421), DSV3.2 indexer fused weights projection (#38684), Triton MLA perf fixes (#33529), indexer WK upcast to BF16 for fusion (#38928), MLA indexer uniform-decode optimization for MTP>1 (#39458), DSA + MTP IMA fix (#40772).
* **GDN / Mamba**: Kernel fusion in GDN (#37813), TMA aligned with upstream FLA (#38981), GPU↔CPU syncs eliminated in prefill and spec-decode paths (#38361, #38047).
* **Other**: DeepGEMM integrated into the vLLM wheel via CMake (#37980), Lustre FS checkpoint prefetching enabled by default (#39422), Gemma4 fused routing Triton kernel (#39083), Gemma4 embed_input_ids GPU/CPU sync removed (#39234), Nemotron VL image/video preprocessing optimized (#40283), SiLU block-quant fusion v1 (#32996), bilinear_pos_embed Triton kernel for ViT (#37948), mean-pooling optimization (~5.9% throughput) (#38559), redundant-sync removal for pooling (~3.7% throughput) (#39113), H2D pageable-memory copy reduction (#38794), fused zero initializer for FP8 DeepGemm block-quant (#39547), batch-invariant fused-rms-norm 2.1% E2E latency improvement (#40413), `InductorPass.hash_source` cached (#39328), humming quantization kernel (#34556).

### Large Scale Serving
* **EPLB**: Alternative communication for EPLB weight exchange (#33176), nixl-based EPLB communicator (#36276), mapping optimization with router record for prefill (#36261), `TransferMetadata` consolidation (#37341), Async EPLB synchronization refactor (#37601), asyncio infrastructure removed from Async EPLB (#40730), replica-selection bias fix in fused_moe router (#40810), Async EPLB integration test added (#40168).
* **WideEP**: Naive all2all replaced by allgather + reducescatter (#33728).
* **KV Offload / Connector**: 3FS KVConnector (#37636), unified memory layout for offloading workers (#37206), cache_salt propagated through MP connector for per-user isolation (#39837), multi-connector metrics of same type (#40010), LMCache block-allocation event (#38856), LMCache MP save optimization with MLA (#38810), `num_lmcache_extra_cached_token` in KVTransferParams (#39843), offload all KV blocks during prefill in P/D (#40346), DP control bundle pinned to first GPU's node on Ray (#39167), FlashInfer NVLink MNNVL workspace sized to EP group (#40893).
* **Disaggregated / NIXL / Mamba**: Full PD support for Mamba2-like models on Heterogeneous TP deployments (#37635), Nixl bumped to 0.10.1 (#39922), `TpKVTopology` + `HeteroTPTransferConfig` unified into `TransferTopology` (#39529), NIXL EP treated as batched experts in fused_moe (#40412).

### Quantization
* **New formats & methods**: TurboQuant 2-bit KV cache compression (#38479) with FA3/FA4 prefill (#40092), per-token-head INT8/FP8 KV cache quantization (#38378), fused FP8/NVFP4 output quantization in MLA attention (#35792), NVFP4 dense models on MI300/MI355X and Hopper via emulation (#35733), NVFP4 MoE emulation fallback for H100/MI300/MI350 (#35737), humming quantization kernel (#34556).
* **Kernels**: MXFP8 in Marlin GEMM/MoE with Mxfp8LinearOp refactor (#34664), MXFP4 W4A4 CUTLASS MoE for SM100 (#37463), NVFP4 in `reshape_and_cache_flash` (#37332), batch-invariant NVFP4 linear (#39322), FlashInfer CuteDSL batched-experts backend for NVFP4 MoE (#38251), special `GptOssMxfp4MoeMethod` (#39604), W4A8_FP8 MoE TP>1 correctness fix (#40310), NVFP4 CUTLASS MoE OOB-read fix for non-multiple-of-4/16 expert counts (#40351), RMS norm + quant fusion fix on DeepGEMM UE8M0 path for B200 (#40552), Gemma4 quantized MoE (#39045).
* **Compressed tensors**: W8A8 MXFP8 linear/MoE (`CompressedTensorsW8A8Mxfp8`) (#38815), CT W8A8 in Oracle structure (#39187), layerwise reloading of attention/KV quantized models (#38995), experts_int8 consolidated with FP8 online quant (#38463), MXFP8 online quant on the new frontend (#40152).
* **Online quant**: Quantized model init failure fix with prefetch offloading (#40432), `current_platform.supports_fp8()` updated for TritonExperts on XPU/ROCm (#40132).
* **XPU / CPU / AMD**: XPU MXFP4 (#39857), XPU MXFP8 GEMM + compressed-tensor schema (#38707), XPU FP8 per-channel linear (#38316), FP8 KV cache on XPU (#37731), CPU W4A16 Autoround (#38192), XPU W4A16 Autoround (#37986), asymmetric INT8 `TritonInt8ScaledMMLinearKernel` on ROCm (#38501), Quark W8A8 INT8 MoE inference (#36320).
* **Deprecations**: Petit NVFP4 removed (#32694).

### API & Frontend
* **OpenAI / Anthropic API**: `presence_penalty` / `frequency_penalty` on Responses API (#38613), Responses API streaming migrated to unified parser (#38755), `tool_choice` / `tools` validation on Responses to match OpenAI (#40399), Mistral Grammar factory (#38150), multimodal support on `/inference/v1/generate` (#38405), `max_tokens_per_doc` in rerank (#38827), Generative Scoring (#34539), MaxSim re-enabled on GPU (#38620), `chat_template_kwargs` on Anthropic `/v1/messages` (#40125), auto-detection of `reasoning_config` when only `reasoning_parser` is set (#38214), reasoning parsers can access model config via `adjust_request` (#37848, #39027), effective chat-template kwargs passed to reasoning parsers (#40460), reasoning parsers expose `reasoning_start_str`/`reasoning_end_str` (#40566).
* **Pooling ecosystem**: Pooling entrypoints overhauled across scoring (#28631), pooling (#39153), and cleanup (#39675); preprocessing/postprocessing offloaded to thread pool (#39763); async scheduling disabled by default for pooling (#39592); `logit_scale` added to PoolerConfig (#39435), then renamed `logit_bias`/`logit_scale` → `logit_mean`/`logit_sigma` for affine score calibration (#39530) — breaking. `LLM.reward` deprecated; use `LLM.encode` instead (#40688).
* **gRPC / streaming**: Streaming on token-generation endpoint (#37171); gRPC periodic stats logging + servicer log forwarding (#38333); standard `grpc.health.v1` health check for Kubernetes-native probes (#38016).
* **Tool / reasoning parsers**: Treat `<tool_call>` as implicit reasoning end in Qwen3 (#35687), `is_reasoning_end_streaming()` override for GptOssReasoningParser (#35745), Mistral tool parser HF-tokenizer fix (#39294), Mistral pre-v11 tool parser trailing-output fix (#40531), Gemma4 streaming HTML duplication / JSON corruption / null-as-string fixes (#38909, #38992, #39114, #39679), HF tokenizer concurrent-borrow fix in tool parsers (#40059), `HYV3ReasoningParser` no longer mutates `chat_template_kwargs` (#40713).
* **Multimodal**: Externally processed `mm_kwargs` with cache injection (#39502), PyAV video backend for concurrent decoding (#39986), custom video metadata for pre-extracted frame sequences (#40133), image+video mixed inputs (per prompt) for VLM examples (#40335), deepstack buffer optimized for Qwen3 multimodal (#40145), readonly multimodal processor warmup during renderer startup (#40797), `mm_processor_kwargs` forwarded in offline `generate` APIs (#40251), normalize malformed dict prompts that carry token IDs in `prompt` (#40339), hotwords for FunASR (#39674), bundle `get_generation_prompt()` params into `SpeechToTextParams` (#36268).
* **Frontend / vLLM Omni**: `--omni` delegates to vLLM Omni (#40744); avoid eager import of `mistral_common` (#40043).
* **LLM / CLI**: Structured-output special tokens preserved in offline `LLM.chat` (#39352), `use_audio_in_video` passable at `vllm serve` for nemotron-nano-vl (#38538), deferred imports save ~2s CLI startup (#40056), improved MM-input-too-long error message (#39409), warning when FP8 KV cache misses prefill query quant (#39752), clearer DCP error message (#28443), `--model` deprecation warning updated (#39518), Mimo reasoning/tooling parsers mapped (#40089), human-readable `k/K/m/M…` suffix in JSON CLI args (#40473).

### Spec Decode
* Eagle3 for MiniMax-M2 (#37512), Eagle3 for Gemma4 (#39450), AITER MLA + Eagle3 on ROCm (#39616).
* TurboQuant FA3/FA4 for prefill paths (#40092).
* Mamba: default to `'align'` cache mode for Mamba-based models when speculative decoding is enabled (#40454).
* Unified Synthetic Acceptance Rate for V1 and V2 (#40662); `SpecDecodeBaseProposer` moved out of `eagle.py` (#40732); DSA + MTP IMA fix (#40772).

### Security
* SSRF fix in batch runner `download_bytes_from_url` (#38482).

### Dependencies
* **PyTorch 2.11** for CUDA (#34644) and XPU (#37947) — XPU no longer pinned to 2.10.
* **CUDA 13.0** default with updated architecture lists and cleaned build-args (#39878); CUDA bumped to 13.0.2 to match PyTorch 2.11.0 (#40669); sm_110 (Jetson Thor) added (#39233).
* **Python 3.14** added to supported versions (#34770).
* **Transformers v5** (#30566), with vision-encoder torch.compile bypass (#30518) and continued v4/v5 compat fixes.
* **FlashAttention 4** upstream sync (#38690) and symlink-on-install behavior (#38814).
* **FlashInfer** bumped to 0.6.8 (#39959).
* **AITER** triton BUFFER_OPS fix + version updates (#38580), AITER reverted to v0.1.10.post3 (#39509); **Nixl** bumped to 0.10.1 (#39922) and pinned per CUDA major in CI (#39851); **DeepGEMM** integrated into the wheel via CMake (#37980); **fastsafetensors** added to NVIDIA Dockerfile (#38950); Helion bumped 0.3.2 → 0.3.3 (#38062).
* **Removed / moved**: `resampy` dependency dropped (#39524), `librosa` direct dependency dropped (#39079), `pyav` and `soundfile` moved to common requirements (#39997).

### Breaking Changes
1. **PyTorch 2.11 + CUDA 13.0(.2) default** — environment dependency change, now applied to XPU as well.
2. **Transformers v5** is the supported baseline (#30566).
3. **Metrics rework**: `vllm:prompt_tokens_recomputed` removed (#38709); `num_cached_tokens` / `num_external_computed_tokens` replaced with `PrefillStats` (#37460).
4. **Pooler config rename**: `logit_bias`/`logit_scale` → `logit_mean`/`logit_sigma` (#39530).
5. **Async scheduling default OFF for pooling models** (#39592).
6. **CUDAGraph memory profiling now ON by default** (#38284) — startup memory accounting changes.
7. **Petit NVFP4 quantization removed** (#32694); `LLM.reward` deprecated, use `LLM.encode` (#40688); `cprofile` / `cprofile_context` deprecated (#39100); V0 `accept output buffer` deprecated (#39125).

### V0 Deprecation
* Petit NVFP4 (#32694), `accept output buffer` in attention (#39125), `cprofile` / `cprofile_context` (#39100), `LLM.reward` offline API (#40688).

## New Contributors
* @1096125073 made their first contribution in https://github.com/vllm-project/vllm/pull/38510
* @2imi9 made their first contribution in https://github.com/vllm-project/vllm/pull/38970
* @AAISSJ made their first contribution in https://github.com/vllm-project/vllm/pull/37831
* @abatilo made their first contribution in https://github.com/vllm-project/vllm/pull/38987
* @aditi-amd made their first contribution in https://github.com/vllm-project/vllm/pull/39953
* @aeon-x made their first contribution in https://github.com/vllm-project/vllm/pull/39843
* @Alchuang22-dev made their first contribution in https://github.com/vllm-project/vllm/pull/40339
* @aleksandaryanakiev made their first contribution in https://github.com/vllm-project/vllm/pull/40125
* @aliialsaeedii made their first contribution in https://github.com/vllm-project/vllm/pull/38253
* @artem-spector made their first contribution in https://github.com/vllm-project/vllm/pull/40282
* @bai made their first contribution in https://github.com/vllm-project/vllm/pull/39959
* @bhargav-patel-29 made their first contribution in https://github.com/vllm-project/vllm/pull/38000
* @bingshuailiu made their first contribution in https://github.com/vllm-project/vllm/pull/38788
* @Bortlesboat made their first contribution in https://github.com/vllm-project/vllm/pull/39123
* @BugenZhao made their first contribution in https://github.com/vllm-project/vllm/pull/40460
* @carlyou made their first contribution in https://github.com/vllm-project/vllm/pull/36205
* @Chinmay-Kulkarni-AMD made their first contribution in https://github.com/vllm-project/vllm/pull/39967
* @crawfordxx made their first contribution in https://github.com/vllm-project/vllm/pull/38722
* @daiyu1111 made their first contribution in https://github.com/vllm-project/vllm/pull/40011
* @dalistarh made their first contribution in https://github.com/vllm-project/vllm/pull/40194
* @daniebrill made their first contribution in https://github.com/vllm-project/vllm/pull/36934
* @dhonnappa-amd made their first contribution in https://github.com/vllm-project/vllm/pull/38238
* @dondetir made their first contribution in https://github.com/vllm-project/vllm/pull/38455
* @efortin made their first contribution in https://github.com/vllm-project/vllm/pull/39183
* @elenalil-aws made their first contribution in https://github.com/vllm-project/vllm/pull/38927
* @elwhyjay made their first contribution in https://github.com/vllm-project/vllm/pull/39526
* @EricccYang made their first contribution in https://github.com/vllm-project/vllm/pull/37376
* @evezhier made their first contribution in https://github.com/vllm-project/vllm/pull/36540
* @ezylopx5 made their first contribution in https://github.com/vllm-project/vllm/pull/37051
* @fergusfinn made their first contribution in https://github.com/vllm-project/vllm/pull/35745
* @foreverlms made their first contribution in https://github.com/vllm-project/vllm/pull/31113
* @frgossen made their first contribution in https://github.com/vllm-project/vllm/pull/38944
* @Galigator made their first contribution in https://github.com/vllm-project/vllm/pull/40161
* @ganeshr10 made their first contribution in https://github.com/vllm-project/vllm/pull/32662
* @hangy-amd made their first contribution in https://github.com/vllm-project/vllm/pull/39703
* @heachary made their first contribution in https://github.com/vllm-project/vllm/pull/39999
* @hhk7734 made their first contribution in https://github.com/vllm-project/vllm/pull/37171
* @hnt2601 made their first contribution in https://github.com/vllm-project/vllm/pull/39892
* @hospedales made their first contribution in https://github.com/vllm-project/vllm/pull/38847
* @huangzhilin-hzl made their first contribution in https://github.com/vllm-project/vllm/pull/40092
* @ianliuy made their first contribution in https://github.com/vllm-project/vllm/pull/39473
* @ibifrost made their first contribution in https://github.com/vllm-project/vllm/pull/37636
* @ibrahim1023 made their first contribution in https://github.com/vllm-project/vllm/pull/39169
* @ichbinblau made their first contribution in https://github.com/vllm-project/vllm/pull/38371
* @jackcfwang made their first contribution in https://github.com/vllm-project/vllm/pull/38794
* @jaseelmohd2 made their first contribution in https://github.com/vllm-project/vllm/pull/39986
* @jatseng-ai made their first contribution in https://github.com/vllm-project/vllm/pull/37352
* @JeanPaulShapo made their first contribution in https://github.com/vllm-project/vllm/pull/35736
* @jefp made their first contribution in https://github.com/vllm-project/vllm/pull/39435
* @jesus-talavera-ibm made their first contribution in https://github.com/vllm-project/vllm/pull/38714
* @jigangz made their first contribution in https://github.com/vllm-project/vllm/pull/39780
* @JoursBleu made their first contribution in https://github.com/vllm-project/vllm/pull/36965
* @khairulkabir1661 made their first contribution in https://github.com/vllm-project/vllm/pull/38388
* @khushali9 made their first contribution in https://github.com/vllm-project/vllm/pull/40409
* @kibitzing made their first contribution in https://github.com/vllm-project/vllm/pull/37501
* @KimuGenie made their first contribution in https://github.com/vllm-project/vllm/pull/39679
* @kkyyxhll made their first contribution in https://github.com/vllm-project/vllm/pull/38517
* @kot-begemot-uk made their first contribution in https://github.com/vllm-project/vllm/pull/36487
* @krishung5 made their first contribution in https://github.com/vllm-project/vllm/pull/39502
* @KyleMylonakisProtopia made their first contribution in https://github.com/vllm-project/vllm/pull/38699
* @lalit10 made their first contribution in https://github.com/vllm-project/vllm/pull/38955
* @larryli2-amd made their first contribution in https://github.com/vllm-project/vllm/pull/39616
* @lesj0610 made their first contribution in https://github.com/vllm-project/vllm/pull/40359
* @liuchenbing2026 made their first contribution in https://github.com/vllm-project/vllm/pull/37512
* @lyd1992 made their first contribution in https://github.com/vllm-project/vllm/pull/40428
* @MekayelAnik made their first contribution in https://github.com/vllm-project/vllm/pull/39085
* @menogrey made their first contribution in https://github.com/vllm-project/vllm/pull/37989
* @mieshkiwrk made their first contribution in https://github.com/vllm-project/vllm/pull/38825
* @misaAle made their first contribution in https://github.com/vllm-project/vllm/pull/39554
* @Monishver11 made their first contribution in https://github.com/vllm-project/vllm/pull/32996
* @mukesh-hai made their first contribution in https://github.com/vllm-project/vllm/pull/38435
* @namgyu-youn made their first contribution in https://github.com/vllm-project/vllm/pull/38799
* @nemanjaudovic made their first contribution in https://github.com/vllm-project/vllm/pull/38114
* @nithinvc made their first contribution in https://github.com/vllm-project/vllm/pull/38405
* @noobHappylife made their first contribution in https://github.com/vllm-project/vllm/pull/38519
* @pedramr made their first contribution in https://github.com/vllm-project/vllm/pull/39650
* @petern48 made their first contribution in https://github.com/vllm-project/vllm/pull/37247
* @philip-essential made their first contribution in https://github.com/vllm-project/vllm/pull/39823
* @pinsiangamd made their first contribution in https://github.com/vllm-project/vllm/pull/37529
* @Prathmesh234 made their first contribution in https://github.com/vllm-project/vllm/pull/36466
* @puririshi98 made their first contribution in https://github.com/vllm-project/vllm/pull/39206
* @qiching made their first contribution in https://github.com/vllm-project/vllm/pull/39752
* @qmx made their first contribution in https://github.com/vllm-project/vllm/pull/35687
* @rbrugaro-amd made their first contribution in https://github.com/vllm-project/vllm/pull/39242
* @rishaps made their first contribution in https://github.com/vllm-project/vllm/pull/39092
* @Roy214 made their first contribution in https://github.com/vllm-project/vllm/pull/39575
* @San-Nguyen made their first contribution in https://github.com/vllm-project/vllm/pull/40324
* @SandishKumarHN made their first contribution in https://github.com/vllm-project/vllm/pull/35431
* @SeraphimSerapis made their first contribution in https://github.com/vllm-project/vllm/pull/39861
* @ShubyM made their first contribution in https://github.com/vllm-project/vllm/pull/38844
* @shunting314 made their first contribution in https://github.com/vllm-project/vllm/pull/36298
* @skavulya made their first contribution in https://github.com/vllm-project/vllm/pull/40430
* @starkwj made their first contribution in https://github.com/vllm-project/vllm/pull/38726
* @stevenkuang-tencent made their first contribution in https://github.com/vllm-project/vllm/pull/40681
* @storyicon made their first contribution in https://github.com/vllm-project/vllm/pull/40133
* @talorabr made their first contribution in https://github.com/vllm-project/vllm/pull/36029
* @thomasmaindron made their first contribution in https://github.com/vllm-project/vllm/pull/39293
* @TihoElek made their first contribution in https://github.com/vllm-project/vllm/pull/38849
* @triangleXIV made their first contribution in https://github.com/vllm-project/vllm/pull/39102
* @ultranationalism made their first contribution in https://github.com/vllm-project/vllm/pull/40191
* @USTCKAY made their first contribution in https://github.com/vllm-project/vllm/pull/39181
* @V2arK made their first contribution in https://github.com/vllm-project/vllm/pull/38016
* @vedantjh2 made their first contribution in https://github.com/vllm-project/vllm/pull/34539
* @velonica0 made their first contribution in https://github.com/vllm-project/vllm/pull/39478
* @vibhavagarwal5 made their first contribution in https://github.com/vllm-project/vllm/pull/39064
* @VinayakMishra95 made their first contribution in https://github.com/vllm-project/vllm/pull/40729
* @Wangxiaoxiaoa made their first contribution in https://github.com/vllm-project/vllm/pull/40455
* @wincent8 made their first contribution in https://github.com/vllm-project/vllm/pull/37841
* @wojciech-wais made their first contribution in https://github.com/vllm-project/vllm/pull/34844
* @wufann made their first contribution in https://github.com/vllm-project/vllm/pull/38615
* @wuyingjun-lucky made their first contribution in https://github.com/vllm-project/vllm/pull/40251
* @YifanLi3 made their first contribution in https://github.com/vllm-project/vllm/pull/40266
* @yintong-lu made their first contribution in https://github.com/vllm-project/vllm/pull/35697
* @YM2132 made their first contribution in https://github.com/vllm-project/vllm/pull/38427
* @yoke233 made their first contribution in https://github.com/vllm-project/vllm/pull/38909
* @yubofredwang made their first contribution in https://github.com/vllm-project/vllm/pull/39160
* @yurun00 made their first contribution in https://github.com/vllm-project/vllm/pull/37766
* @yuwenzho made their first contribution in https://github.com/vllm-project/vllm/pull/39466
* @Yuyi-Ao made their first contribution in https://github.com/vllm-project/vllm/pull/38052
* @z1ying made their first contribution in https://github.com/vllm-project/vllm/pull/39518
* @zhangj1an made their first contribution in https://github.com/vllm-project/vllm/pull/40629
* @Zhenzhong1 made their first contribution in https://github.com/vllm-project/vllm/pull/38192
* @zxd1997066 made their first contribution in https://github.com/vllm-project/vllm/pull/38899

---

## v0.19.1  (2026-04-18T05:44:42Z)

This is a patch release on top of `v0.19.0` with Transformers v5.5.3 upgrade and bug fixes for Gemma4:
- Update to transformers v5 (#30566)
- [Bugfix] Fix invalid JSON in Gemma 4 streaming tool calls by stripping partial delimiters (#38992)
- [Bugfix][Frontend] Fix Gemma4 streaming HTML duplication after tool calls (#38909)
- [Bugfix] Fix Gemma4 streaming tool call corruption for split boolean/number values (#39114)
- [Tool] adjust_request to reasoning parser, and Gemma4 fixes (#39027)
- [Gemma4] Support quantized MoE (#39045)
- Add Gemma4 Eagle3 support (#39450)
- [Gemma4][Bugfix]: Enable Gemma4ForCasualLM to load lora adapters correctly (#38844)
- [Bugfix] Fix Gemma4 tool parser converting bare null to string "null" (#39679)
- [Model] Fix Gemma 4 token repetition by dynamic BOS injection for PT models (#39842)
- fix(kimi_k25): resolve media_placeholder_token_id from tokenizer (#39344)

---

## v0.19.0  (2026-04-03T02:19:12Z)

# vLLM v0.19.0

## Highlights
This release features 448 commits from 197 contributors (54 new)!

* **Gemma 4 support**: Full Google Gemma 4 architecture support including MoE, multimodal, reasoning, and tool-use capabilities (#38826, #38847). Requires `transformers>=5.5.0`. We recommend using pre-built docker image `vllm/vllm-openai:gemma4` for out of box usage.
* **Zero-bubble async scheduling + speculative decoding**: Async scheduling now supports speculative decoding with zero-bubble overlap, significantly improving throughput (#32951).
* **Model Runner V2 maturation**: MRV2 gains piecewise CUDA graphs for pipeline parallelism (#35162), spec decode rejection sampler with greedy/logprobs support (#37238, #37237), multi-modal embeddings for spec decode (#36097), streaming inputs (#37028), and EPLB support (#37488).
* **ViT Full CUDA Graphs**: Vision encoders (ViT) now support full CUDA graph capture for reduced overhead (#35963).
* **General CPU KV cache offloading**: A simple yet general CPU KV cache offloading mechanism for V1, with pluggable cache policy and block-level preemption handling (#37160, #37874, #34805, #36642, #37853).
* **DBO (Dual-Batch Overlap) generalization**: The microbatch optimization (DBO) now works with general models, not just specific architectures (#37926).
* **NVIDIA B300/GB300 (SM 10.3) support**: Allreduce fusion enabled by default with tuned all-reduce communicator (#37755, #37756).
* **Transformers v5 compatibility**: Broad compatibility fixes across many models for HuggingFace Transformers v5 (#37681, #38127, #38090, #38247, #38410).

### Model Support
* New architectures: Gemma 4 (#38826), Cohere ASR (#35809), Cohere Transcribe (#38120), ColQwen3.5 4.5B (#36887), LFM2-ColBERT-350M (#37528), Granite 4.0 1B Speech (#38019), Qwen3-ForcedAligner (#35367).
* Speculative decoding: Eagle3 for Pixtral (#37182), EagleMistralLarge3 fix (#37232).
* LoRA expansion: H2OVL tower/connector LoRA (#31696), `--lora-target-modules` to restrict LoRA to specific modules (#34984), `language_model_only` respected (#37375), Mistral3 fix (#36928), Qwen3.5 fix (#36976), out-of-tree ops replacement (#37181).
* Model fixes: NemotronH MTP + Chunked Prefill (#35447), Qwen3-VL video timestamps (#37439), Qwen3.5 GDN quantized models (#37448), Qwen3Next A_log FP32 (#37810), JAIS ALiBi (#37820), RoBERTa CUDA graph position IDs (#37873), AudioFlamingo3/MusicFlamingo (#37643), Music Flamingo loading (#35535), bge-m3 task selection (#37632), Nemotron Parse loading (#37407), GLM OCR patch merger (#37962), PaddleOCR checkpoint compat (#38232), DeepSeek v3.2 params (#33703), MiniMax NVFP4 weight loading (#37214), gated model HF token (#37920), Parakeet OOM on long audio (#36671).
* Features: Temporal compression for Nemotron-3-VL videos (#36808), NemotronH Puzzle + MTP (#37803), torch.compile for InternVL vision encoder (#38049), multiple embedding types in single call (#35829).
* Performance: GLM-4.xv ViT optimization (#37779).

### Engine Core
* **Zero-bubble async scheduling + speculative decoding** (#32951).
* **Model Runner V2**: PP CUDA graphs (#35162), spec decode rejection sampler greedy (#37238) + logprobs (#37237), multimodal embeddings for spec decode (#36097), streaming inputs (#37028), configurable acceptance rate (#38045), FP32 draft logits (#37526), FP64 Gumbel noise (#37798), warmup with spec decode (#37812).
* **ViT Full CUDA Graph** capture (#35963).
* **General CPU KV cache offloading** with pluggable CachePolicy (#37160, #37874), block-level preemption (#34805), multiple KV groups (#36642), hybrid model support (#37853).
* **DBO for general models**: Microbatch optimization generalized beyond specific architectures (#37926).
* **Compilation**: Mega AOT artifact for torch 2.12+ (#37198), lazy graph module to defer recompile (#37609), remove model tag requirement for compile cache (#37345), Triton autotuning disk cache enabled by default (#37188), inductor runtime asserts disabled by default (#37485).
* **FlexAttention**: Custom mask modification support (#37692).
* **Attention**: Distinguish short extends vs decodes (#37303), allow qk_nope_head_dim=192 in FlashInfer MLA (#37475), skip sliding window attention layers with FP8 KV cache (#33695).
* **Scheduling**: Schedule requests based on full input sequence length (#37307).
* **Spec decode**: Per-draft-model MoE backend via `--speculative-config` (#37880), Eagle3 drafter quant_config propagation (#37280), Eagle3 norm_before_fc propagation (#38111).
* **Extensibility**: PluggableLayer for CustomQwen2Decoder (#37293), tensor IPC transfer for multimodal data (#32104).
* **Performance**: Optimize top-k in Triton sampler (#37225), optimize token_embed for pooling models with 1% improvement (#37347), fix slow hasattr in CUDAGraphWrapper (#37425), NFS prefetch auto-enabled with RAM guard (#37673), pybase64 replacement (#37290), optimize swap_states for hybrid models (#34733).
* **Bugfixes**: Fix gibberish from FP8 MLA KV scale inconsistency (#37054), Mamba state corruption (#37728), deadlock with pause/resume (#37024), FlashInfer MNNVL socket collisions (#36674), multimodal prefix cache key collisions (#36708), DP coordinator ZMQ TOCTOU (#37452), CUDA graph memory double-counting (#37426), pooling non-determinism (#37775), AllReduce Fusion shutdown crash (#36955), FlashInfer allreduce workspace (#37461), async spec decoding with hybrid models (#38556), MLA sparse indexer prefill chunking (#36178), KV offloading + MLA (#37536), async scheduling extra CUDA context (#37449), DP MTP dummy run (#35243), offloading+prefetch for GLM-4.7-FP8 (#37178), max memory for multiple KV-cache groups (#36030).

### Hardware & Performance
* **NVIDIA**:
  * B300/GB300 (SM 10.3): Allreduce fusion enabled by default (#37755), tuned all-reduce communicator (#37756).
  * Blackwell: Optimized SM120 CUTLASS blockwise FP8 GEMM (#37970), fix NVFP4 NaN on desktop Blackwell (#37725), fix DeepGEMM E8M0 accuracy for Qwen3.5 FP8 (#38083), restore FP8 FlashMLA CUDA graph persistent buffers (#35175), DGX Spark fix (#38126).
  * FlashInfer sparse MLA as default for FP8 KV cache (#37252).
  * Tuned prefill configs for FP8 FA3 (#36265), tuned Triton MoE config for Qwen3.5 on H200 with 9.9% E2E improvement (#37340), H800 MoE configs (#31201).
  * GPT-OSS: Router GEMM kernel (#37205), eliminate padding with FlashInfer MXFP4/MXFP8 MoE (#30647), reduce redundant SparseMatrix creation (#37683).
  * NVFP4 CUTLASS MoE non-gated support (#37320), fuse pack topk in TRTLLM MoE via torch.compile (#37695).
  * Non-contiguous KV cache in TRTLLM FP8 dequant kernel (#36867), Qwen3 dual stream input projection (#36795).
* **AMD ROCm**:
  * ROCm 7.2.1, torch 2.10, triton 3.6 (#38252).
  * DeepEP as all2all backend (#34692).
  * Persistent MLA kernel from AITER (#36574), FP8xFP8 attention in AITER (#36927).
  * AWQ Marlin support (#36505), wvSplitK skinny GEMM for RDNA4/gfx1x (#34709).
  * Nightly Docker image and wheel releases (#37283).
  * Bugfixes: Sleep mode memory leak (#37533), hybrid model stride (#37228), qwen3_next crash (#36795).
* **Intel XPU**: MLA model support (#37143), CompressedTensor W4A8 (#37207), auto-detect XPU build platform (#37634).
* **TPU**: Async scheduling interface (#36924), Qwen3.5 FP8 weight loading fix (#37348).
* **CPU**: Enable tcmalloc by default (#37607), graceful degradation without tcmalloc/libiomp (#37561), 48.9% throughput improvement for pooling models (#38139), OpenMP thread fix for torch.compile (#37538), structured output crash fix (#37706), KV cache block zeroing crash fix (#37550), slot mapping kernel (#37987), W4A16 compressed tensors (#38219).
* **Performance fixes**: FP8 DeepGEMM batch invariance (#37718), Triton autotuning for Qwen3.5 (#37338), TRTLLM NVFP4 routing precision (#36725).

### Large Scale Serving
* **Disaggregated serving**: PD kv_transfer_params for Anthropic Messages (#37535) and Responses API (#37424), Mooncake heterogeneous TP (#36869), Mamba N-1 prefill for P/D (#37310).
* **EPLB**: MRV2 support (#37488), improved responsiveness (#36271), EP weight filter fix (#37322).
* **Elastic EP**: Fix repeated scale up/down cycles (#37131), fix stateless group port races (#36330).
* **DBO**: Generalized to work with all models (#37926).
* **Multi-node**: Fix allreduce fusion (#38136).
* **KV connector**: Plugin-overridable metadata build (#37336).
* **Constraints**: Cap API servers to 1 with Elastic EP (#37466).

### Quantization
* **Online MXFP8** quantization for MoE and dense models (#35448).
* **FP8**: WoQ kernel abstraction (#32929), Marlin FP8 for compressed tensors fix (#38092).
* **NVFP4**: Rescale weight scales to fix BF16 dequant underflow (#34577), fix Marlin NaN/Inf with float16 (#33972).
* **QeRL**: Online quantization composed with quantized reloading for RLHF (#38032).
* **CPU**: W4A16 compressed tensors (#38219).
* **XPU**: CompressedTensor W4A8 (#37207).
* **ROCm**: AWQ Marlin support (#36505).
* **MXFP8 + DeepGEMM**: Fix crash when both are active (#37358).
* **Removals**: Per-tensor-per-channel FP8 removed (#32700), Sparse24 integration and kernels removed (#36799).

### API & Frontend
* **New endpoints**: `/v1/chat/completions/batch` for batched chat completions (#38011).
* **Features**: Limit thinking tokens (hard limit) (#20859), multiple embedding types in single call (#35829), numpy array embeddings for multimodal (#38119), `--lora-target-modules` (#34984), `-sc` shorthand for `--speculative-config` (#38380).
* **Tool parsing**: GigaChat 3.1 parser (#36664), Kimi-K2.5 reasoning/tool parser (#37438), Gemma 4 tool parser (#38847), tools passed to parser constructor (#38029), fix Mistral parser (#37209), fix DeepSeek v3.2 streaming (#36056), fix GLM-4.7 parsing (#37386), fix Hermes streaming (#38168), fix OpenAI tool parser IndexError (#37958), fix Anthropic streaming (#37510).
* **Responses API**: Fix crash with tool_choice=required exceeding max_output_tokens (#37258), fix TTFT recording (#37498), fix Anthropic serving template kwargs (#37899).
* **Performance**: Offload blocking tokenizer ops to thread pool (#34789).
* **Deprecations**: `--calculate-kv-scales` (#37201), `score` task (#37537), pooling multi-task support (#37956), `reasoning_content` message field removed (#37480).
* **Bugfixes**: Embed/classify task routing (#37573), Cohere embed task instruction (#38362), renderer workers restricted to 1 with MM cache (#38418).
* **UX**: Log once per node by default (#37568), torch profiler with stack enabled (#37571).

### Security
* Add `VLLM_MAX_N_SEQUENCES` environment variable to enforce sequence limits (#37952).
* Enforce frame limit in VideoMediaIO to prevent resource exhaustion (#38636).

### Dependencies
* Transformers v5 compatibility across many models (#37681, #38127, #38247, #38410, #38090).
* ROCm 7.2.1, torch 2.10, triton 3.6 for ROCm builds (#38252).
* compressed-tensors bumped to 0.14.0.1 (#36988).
* Python OpenAI package bumped (#32316).
* flashinfer-cubin added as default CUDA dependency (#37233).
* librosa removed from audio dependencies (#37058).

### V0 Deprecation
* Deprecate virtual engine (#37195).
* Deprecate `--disable-frontend-multiprocessing` (#37612).
* Refactor KV cache from list to element (#37487).

### New Contributors
* @aaab8b made their first contribution in #37533
* @aasgaonkar made their first contribution in #35386
* @allgather made their first contribution in #38410
* @avinashsingh77 made their first contribution in #37100
* @b-mu made their first contribution in #35963
* @bongwoobak made their first contribution in #37424
* @brandonpelfrey made their first contribution in #32104
* @ccrhx4 made their first contribution in #37634
* @cdpath made their first contribution in #37510
* @cemigo114 made their first contribution in #37064
* @cnyvfang made their first contribution in #37439
* @DanBlanaru made their first contribution in #37307
* @DorBernsohn made their first contribution in #37438
* @dsingal0 made their first contribution in #37923
* @fxdawnn made their first contribution in #36038
* @grYe99 made their first contribution in #38074
* @guillaumeguy made their first contribution in #38119
* @gxd3 made their first contribution in #36924
* @he-yufeng made their first contribution in #37301
* @javierdejesusda made their first contribution in #37920
* @jetxa made their first contribution in #37899
* @jhsmith409 made their first contribution in #37448
* @jrplatin made their first contribution in #37348
* @kjiang249 made their first contribution in #37475
* @laudney made their first contribution in #34709
* @lcskrishna made their first contribution in #34692
* @li-liwen made their first contribution in #38108
* @Liangyx2 made their first contribution in #37523
* @MatejRojec made their first contribution in #38011
* @Nekofish-L made their first contribution in #37970
* @pjo256 made their first contribution in #34733
* @r266-tech made their first contribution in #37820
* @RobTand made their first contribution in #37725
* @scyyh11 made their first contribution in #34789
* @SherryC41 made their first contribution in #37519
* @shwetha-s-poojary made their first contribution in #31696
* @siewcapital made their first contribution in #36955
* @SKPsanjeevi made their first contribution in #36574
* @thillai-c made their first contribution in #37231
* @tianrengao made their first contribution in #34389
* @tmm77 made their first contribution in #37694
* @utsumi-fj made their first contribution in #38328
* @vineetatiwari27 made their first contribution in #37998
* @Wangbei25 made their first contribution in #37293
* @WindChimeRan made their first contribution in #35007
* @wjhrdy made their first contribution in #37706
* @XLiu-2000 made their first contribution in #37371
* @xueliangyang-oeuler made their first contribution in #37536
* @yanghui1-arch made their first contribution in #37873
* @yassha made their first contribution in #37369
* @yeahdongcn made their first contribution in #37840
* @Young-Leo made their first contribution in #37565
* @ZeldaHuang made their first contribution in #37425
* @zhejiangxiaomai made their first contribution in #37259

---

## v0.18.1  (2026-03-31T00:53:26Z)

This is a patch release on top of v0.18.0 to address a few issues:
- Change default SM100 MLA prefill backend back to TRT-LLM (#38562)
- Fix mock.patch resolution failure for standalone_compile.FakeTensorMode on Python <= 3.10 (#37158)
- Disable monolithic TRTLLM MoE for Renormalize routing #37605
- Pre-download missing FlashInfer headers in Docker build #38391
- Fix DeepGemm E8M0 accuracy degradation for Qwen3.5 FP8 on Blackwell (#38083)

---

## v0.18.0  (2026-03-20T21:31:36Z)

# vLLM v0.18.0

## Known issues
- Degraded accuracy when serving Qwen3.5 with FP8 KV cache on B200 (#37618)
- If you previously ran into `CUBLAS_STATUS_INVALID_VALUE` and had to use a workaround in `v0.17.0`, you can reinstall `torch 2.10.0`. PyTorch published an updated wheel that addresses this bug.

## Highlights

This release features 445 commits from 213 contributors (61 new)!

* **gRPC Serving Support**: vLLM now supports gRPC serving via the new `--grpc` flag (#36169), enabling high-performance RPC-based serving alongside the existing HTTP/REST interface.
* **GPU-less Render Serving**: New `vllm launch render` command (#36166, #34551) enables GPU-less preprocessing and rendering, allowing separation of multimodal preprocessing from GPU inference.
* **NGram GPU Speculative Decoding**: NGram speculative decoding now runs on GPU and is compatible with the async scheduler (#29184), significantly reducing spec decode overhead.
* **KV Cache Offloading Improvements**: Smart CPU offloading that stores only frequently-reused blocks (#35342), plus FlexKV as a new offloading backend (#34328) and support for multiple KV groups in offloading spec (#36610).
* **Elastic Expert Parallelism Milestone 2**: NIXL-EP integration (#35627) enables dynamic GPU scaling for MoE experts, with new `--enable-ep-weight-filter` CLI option (#37351) for faster EP model loading.
* **FlashInfer 0.6.6**: Updated FlashInfer dependency (#36768) with numerous performance and correctness improvements.
* **Responses API Streaming Tool Calls**: The OpenAI Responses API now supports tool/function calling with streaming (#29947).
* **Online Beam Search for ASR**: Beam search support for encoder/decoder models both offline (#36153) and online transcriptions (#36160).
* **Ray No Longer a Default Dependency**: Ray has been removed as a default dependency (#36170) — install it explicitly if needed.

### Model Support
* **New architectures**: Sarvam MoE (#33942), OLMo Hybrid (#32550), HyperCLOVAX-SEED-Think-32B VLM (#31471), HyperCLOVAX-SEED-Think-14B (#37107), Kimi-Audio-7B-Instruct (#36127), ColPali late-interaction retrieval (#36818), ERNIE pooling models (#36385).
* **Speculative decoding**: Eagle3 for Qwen3.5 (#36658), Eagle3 for Kimi K2.5 MLA (#36361), Eagle for Mistral Large 3 with dense layers (#36163).
* **LoRA**: Whisper LoRA (#29856), FP8 LoRA dense kernel (#35242).
* **Multimodal**: Online use_audio_in_video (#36319), audio extraction from MP4 for Nemotron Nano VL (#35539), audio transcription for MP4/M4A/WebM (#35109), expose media_io_kwargs at runtime (#34778), fast media preprocessing for Nano Nemotron VL (#35657).
* **Compatibility**: Gemma/Gemma2 inputs_embeds (#36787), SigLIP/CLIP Transformers v5 (#37200), fused expert weights in Transformers backend (#36997).
* **Performance**: Qwen3 Next fused GDN kernel (#35777), LFM2 tuned H100 MoE configs (#36699).
* **Fixes**: DeepSeek-V3.2 tokenizer space stripping (#37004), Qwen3.5 tool calling (#36774), Qwen3-VL timestamp mismatch (#36136), Qwen3-Next TP>1 weight sharding (#36242), Qwen3-ASR torch.compile (#35869), MiniCPM-V audio inference (#36751), MiniCPM-O 4.5 ViT attention (#34127), routed experts for hybrid models (#35744), Qwen2.5-Omni/Qwen3-Omni multi-video audio_in_video (#37147), DeepSeek-OCR empty images crash (#36670).

### Engine Core
* **Model Runner V2**: Probabilistic rejection sampling for spec decode (#35461), pooling models (#36019), extensible CUDA graph dispatch (#35959), WhisperModelState (#35790), XD-RoPE (#36817), model_state CUDA graph capture (#36544).
* **KV cache offloading**: Reuse-frequency-gated CPU stores (#35342), FlexKV offloading backend (#34328), multiple KV groups (#36610), async scheduling fix (#33881).
* **Speculative decoding**: NGram GPU implementation with async scheduler (#29184), fused EAGLE step slot mapping (#33503).
* **Performance**: Remove busy loop from idle buffer readers (#28053), 2.7% E2E throughput for pooling via worker-side maxsim (#36159), 3.2% via batched maxsim (#36710), CUDA graph memory accounting during profiling (#30515), checkpoint prefetch to OS page cache (#36012), InstantTensor weight loader (#36139), sporadic stall fix via pin_memory removal (#37006).
* **Stability**: VLM concurrent throughput degradation fix (#36557), DP deadlock fix (#35194), DeepSeek V3.2 OOM during CG profiling (#36691), Ray DP startup crash (#36665), NCCL rank calculation fix (#36940), zero-init MLA output buffers for NaN prevention (#37442), CUDA OOM fix (#35594).
* **Defaults**: Cascade attention disabled by default (#36318).
* **Extensibility**: OOT linear method registration (#35981), custom collective ops registration for non-CUDA platforms (#34760).

### Kernel
* **FA4 for MLA prefill** (#34732).
* **FlashInfer Sparse MLA**: FP8 KV cache support (#35891), CUDA graphs on ROCm (#35719), MTP lens > 1 on ROCm (#36681).
* **TRTLLM FP8 MoE modular kernel** (#36307).
* **FP8 KV cache for Triton MLA decode** (#34597).
* **FlashInfer MoE A2A kernel** (#36022).
* **Remove chunking from FusedMoE** for full batch processing (#34086).
* **CustomOp FusedRMSNormGated** for torch.compile compatibility (#35877).
* **Mamba2 SSD prefill Triton kernel** optimization (#35397).
* **DeepSeek-V3.2**: Vectorized MLA query concat kernel (#34917), optimized FP8 KV cache gather for context parallel (#35290).
* **320-dimension MLA head size** support (#36161).
* **Packed recurrent fast path** for decode (#36596).
* **EP scatter race condition** fix (#34991).

### Hardware & Performance
* **NVIDIA**: FA4 for MLA prefill (#34732), DeepSeek-V3.2 MLA kernel optimizations (#34917, #35290).
* **AMD ROCm**: Sparse MLA CUDA graphs (#35719), MTP lens > 1 in Sparse MLA (#36681), MLA with nhead<16 + FP8 KV for TP=8 (#35850), RoPE+KV cache fusion for AITER FA (#35786), AITER MLA CPU sync avoidance (#35765), Quark W4A8 MXFP4/FP8 (#35316), gfx1152/gfx1153 Krackan support (#36499), fused_topk_bias AITER optimization (#36253), skinny GEMM improvements (#34304), DeepEP in ROCm Dockerfile (#36086), startup OOM fix (#36720).
* **Intel XPU**: Model Runner V2 enabled (#36078), MLA Sparse backend for DeepSeek V3.2 (#33230), LoRA via torch.compile (#36962), block FP8 MoE fallback (#36458), deepseek_scaling_rope fused kernel (#36612).
* **CPU**: aarch64 int8 matmul via OneDNN upgrade (#36147), AMD Zen CPU backend via zentorch (#35970).
* **RISC-V**: CPU backend support (#36578).
* **Performance**: 5% E2E improvement for PD disaggregation scheduling (#35781), packed recurrent decode fast path (#36596), pooling model maxsim 2.7%+3.2% throughput (#36159, #36710).
* **torch.compile**: FakeTensors instead of real GPU tensors for single-size compilation (#36093), non-contiguous fused RMSNorm + group quant (#36551), stop lazy compiling (#35472).

### Large Scale Serving
* **Elastic EP Milestone 2**: NIXL-EP integration (#35627), `--enable-ep-weight-filter` for faster EP loading (#37351).
* **PD Disaggregation**: ~5% scheduler overhead reduction (#35781), KV transfer fix with spec decode (#35158), P/D for hybrid SSM-FA models via NIXL (#36687), PP for multimodal models on Transformers backend (#37057).
* **KV Connectors**: HMA + NIXL connector (#35758), FlexKV offloading (#34328), worker→scheduler metadata (#31964), All-to-All DCP backend (#34883).
* **LMCache**: Fault tolerance mechanism (#36586), memory leak fix (#35931), race condition fix (#35831), TP size for MLA multi-reader locking (#36129).
* **EP loading**: Skip non-local expert weights (#37136).

### Quantization
* **ModelOpt MXFP8 MoE** support (#35986).
* **MXFP4 MoE routing simulation** override for accuracy (#33595).
* **FP8 LoRA dense kernel** (#35242).
* **ROCm**: Quark W4A8 MXFP4/FP8 for LinearLayer (#35316), compressed-tensors fix for DeepSeek-R1 on MI300x (#36247).
* **Fixes**: MLA crash with AWQ/GPTQ quantized models (#34695), score layer quantization for reranker models (#35849), GLM-4.1V non-default quantization (#36321), FP8 k_scale/v_scale loading for Qwen3-MoE (#35656).

### API & Frontend
* **gRPC**: New `--grpc` flag for gRPC serving (#36169).
* **GPU-less serving**: `vllm launch render` for preprocessing-only serving (#36166), `vllm launch` for GPU-less preprocessing (#34551).
* **Responses API**: Streaming tool/function calling (#29947), reasoning item fixes (#34499, #36516).
* **Anthropic API**: Accept redacted thinking blocks (#36992).
* **ASR**: Online beam search transcriptions (#36160), offline beam search (#36153), audio transcription for MP4/M4A/WebM (#35109), realtime endpoint metrics (#35500).
* **Tool calling**: Granite4 tool parser (#36827), Qwen3Coder anyOf double encoding fix (#36032).
* **New options**: `--distributed-timeout-seconds` (#36047), `--attention-backend auto` (#35738), `reasoning_effort=none` (#36238), PyTorch profiler schedule (#35240).
* **Cohere Embed v2 API** support (#37074).
* **Azure Blob Storage** support for RunAI Model Streamer (#34614).
* **Graceful shutdown** timeout for in-flight requests (#36666).
* **Fixes**: tool_choice=required exceeding max_tokens crash (#36841), negative max_tokens with long prompts (#36789), concurrent classify/token_classify race (#36614), Anthropic billing header prefix cache miss (#36829), render endpoint crash for multimodal requests (#35684), xgrammar dtype mismatch on macOS CPU (#32384), minimax_m2 tool parser with stream interval > 1 (#35895).

### Security
* Respect user `trust_remote_code` setting in NemotronVL and KimiK25 (#36192).
* Upgrade xgrammar for security fix (#36168).
* Guard RLHF weight sync deserialization behind insecure serialization flag (#35928).

### Dependencies
* **FlashInfer 0.6.6** (#36768).
* **Ray removed from default dependencies** (#36170).
* `kaldi_native_fbank` made optional (#35996).
* OpenAI dependency bounded to 2.24.0 (#36471).
* Deprecated items from v0.18 removed (#36470, #36006).
* Mistral common v10 (#36971).

### Breaking Changes
1. **Ray no longer a default dependency** — install explicitly if needed (#36170).
2. **Deprecated items removed** — items deprecated in v0.18 have been removed (#36470, #36006).
3. **Cascade attention disabled by default** (#36318).
4. **swap_space parameter removed** (V0 deprecation, #36216).
5. **Monolithic TRTLLM MoE disabled for renormalize routing** — late fix cherry-picked (#37591).


## New Contributors 🎉

* @11happy made their first contribution in https://github.com/vllm-project/vllm/pull/35481
* @12010486 made their first contribution in https://github.com/vllm-project/vllm/pull/36782
* @abhishkh made their first contribution in https://github.com/vllm-project/vllm/pull/32454
* @AjAnubolu made their first contribution in https://github.com/vllm-project/vllm/pull/35976
* @alvinttang made their first contribution in https://github.com/vllm-project/vllm/pull/36397
* @amd-asalykov made their first contribution in https://github.com/vllm-project/vllm/pull/35093
* @amd-lalithnc made their first contribution in https://github.com/vllm-project/vllm/pull/35970
* @arlo-scitix made their first contribution in https://github.com/vllm-project/vllm/pull/36139
* @benenzhu made their first contribution in https://github.com/vllm-project/vllm/pull/36253
* @ChuanLi1101 made their first contribution in https://github.com/vllm-project/vllm/pull/35893
* @cluster2600 made their first contribution in https://github.com/vllm-project/vllm/pull/34882
* @cong-or made their first contribution in https://github.com/vllm-project/vllm/pull/36164
* @daje0601 made their first contribution in https://github.com/vllm-project/vllm/pull/29856
* @davzaman made their first contribution in https://github.com/vllm-project/vllm/pull/32441
* @eellison made their first contribution in https://github.com/vllm-project/vllm/pull/35877
* @fangyuchu made their first contribution in https://github.com/vllm-project/vllm/pull/35194
* @feiqiangs made their first contribution in https://github.com/vllm-project/vllm/pull/34328
* @fenypatel99 made their first contribution in https://github.com/vllm-project/vllm/pull/35240
* @gambletan made their first contribution in https://github.com/vllm-project/vllm/pull/36402
* @giulio-leone made their first contribution in https://github.com/vllm-project/vllm/pull/36937
* @gkswns0531 made their first contribution in https://github.com/vllm-project/vllm/pull/35849
* @grimulkan made their first contribution in https://github.com/vllm-project/vllm/pull/34597
* @hai-meh-cs made their first contribution in https://github.com/vllm-project/vllm/pull/36684
* @hasethuraman made their first contribution in https://github.com/vllm-project/vllm/pull/34614
* @Hongbin10 made their first contribution in https://github.com/vllm-project/vllm/pull/36713
* @jeonsworld made their first contribution in https://github.com/vllm-project/vllm/pull/34499
* @jjmiao1 made their first contribution in https://github.com/vllm-project/vllm/pull/35994
* @Kaonael made their first contribution in https://github.com/vllm-project/vllm/pull/36818
* @ketyi made their first contribution in https://github.com/vllm-project/vllm/pull/36670
* @KevinZonda made their first contribution in https://github.com/vllm-project/vllm/pull/36209
* @leo-cf-tian made their first contribution in https://github.com/vllm-project/vllm/pull/36022
* @lisperz made their first contribution in https://github.com/vllm-project/vllm/pull/34531
* @mitre88 made their first contribution in https://github.com/vllm-project/vllm/pull/35933
* @nkm-meta made their first contribution in https://github.com/vllm-project/vllm/pull/34760
* @nvnbagrov made their first contribution in https://github.com/vllm-project/vllm/pull/35657
* @rahul-sarvam made their first contribution in https://github.com/vllm-project/vllm/pull/33942
* @royyhuang made their first contribution in https://github.com/vllm-project/vllm/pull/35931
* @sbeurnier made their first contribution in https://github.com/vllm-project/vllm/pull/37006
* @seanmamasde made their first contribution in https://github.com/vllm-project/vllm/pull/35109
* @sergey-zinchenko made their first contribution in https://github.com/vllm-project/vllm/pull/35684
* @shaunkotek made their first contribution in https://github.com/vllm-project/vllm/pull/36149
* @shubhra made their first contribution in https://github.com/vllm-project/vllm/pull/36545
* @simone-dotolo made their first contribution in https://github.com/vllm-project/vllm/pull/36000
* @sladyn98 made their first contribution in https://github.com/vllm-project/vllm/pull/33503
* @slin1237 made their first contribution in https://github.com/vllm-project/vllm/pull/36938
* @SoluMilken made their first contribution in https://github.com/vllm-project/vllm/pull/36511
* @Srinivasoo7 made their first contribution in https://github.com/vllm-project/vllm/pull/35342
* @stecasta made their first contribution in https://github.com/vllm-project/vllm/pull/35871
* @sungsooha made their first contribution in https://github.com/vllm-project/vllm/pull/34883
* @SunMarc made their first contribution in https://github.com/vllm-project/vllm/pull/36896
* @TQCB made their first contribution in https://github.com/vllm-project/vllm/pull/36165
* @tunglinwood made their first contribution in https://github.com/vllm-project/vllm/pull/36127
* @tusharshetty61 made their first contribution in https://github.com/vllm-project/vllm/pull/36243
* @typer-J made their first contribution in https://github.com/vllm-project/vllm/pull/36578
* @weiguangli-io made their first contribution in https://github.com/vllm-project/vllm/pull/35815
* @wuxun-zhang made their first contribution in https://github.com/vllm-project/vllm/pull/33230
* @XingLiu1 made their first contribution in https://github.com/vllm-project/vllm/pull/35197
* @yanhong-lbh made their first contribution in https://github.com/vllm-project/vllm/pull/32550
* @yitingw1 made their first contribution in https://github.com/vllm-project/vllm/pull/36612
* @yuanheng-zhao made their first contribution in https://github.com/vllm-project/vllm/pull/36106
* @zihaoanllm made their first contribution in https://github.com/vllm-project/vllm/pull/35973

---

## v0.17.1  (2026-03-11T10:24:34Z)

This is a patch release on top of `v0.17.0` to address a few issues:
- New Model: Nemotron 3 Super
- Fix passing of activation_type to trtllm fused MoE NVFP4 and FP8 (#36017)
- Fix/resupport nongated fused moe triton (#36412)
- Re-enable EP for trtllm MoE FP8 backend (#36494)
- [Mamba][Qwen3.5] Zero freed SSM cache blocks on GPU (#35219)
- Fix TRTLLM Block FP8 MoE Monolithic (#36296)
- [DSV3.2][MTP] Optimize Indexer MTP handling (#36723)

---

## v0.17.0  (2026-03-07T00:46:41Z)

# vLLM v0.17.0

**Known Issue**: If you are on CUDA 12.9+ and encounter a `CUBLAS_STATUS_INVALID_VALUE` error, this is caused by a CUDA library mismatch. To resolve, try one of the following:
1. Remove the path to system CUDA shared library files (e.g. `/usr/local/cuda`) from `LD_LIBRARY_PATH`, or simply `unset LD_LIBRARY_PATH`.
2. Install vLLM with `uv pip install vllm --torch-backend=auto`.
3. Install vLLM with `pip install vllm --extra-index-url https://download.pytorch.org/whl/cu129` (change the CUDA version to match your system).

## Highlights

This release features 699 commits from 272 contributors (48 new)!

* **PyTorch 2.10 Upgrade**: This release upgrades to **PyTorch 2.10.0**, which is a breaking change for environment dependencies.
* **FlashAttention 4 Integration**: vLLM now supports the **FlashAttention 4** backend (#32974), bringing next-generation attention performance.
* **Model Runner V2 Maturation**: Model Runner V2 has reached a major milestone with **Pipeline Parallel** (#33960), **Decode Context Parallel** (#34179), **Eagle3 speculative decoding with CUDA graphs** (#35029, #35040), **pooling model support** (#35120), piecewise & mixed CUDA graph capture (#32771), DP+EP for spec decoding (#35294), and a new ModelState architecture. Design docs are now available (#35819).
* **Qwen3.5 Model Family**: Full support for the **Qwen3.5** model family (#34110) featuring GDN (Gated Delta Networks), with FP8 quantization, MTP speculative decoding, and reasoning parser support.
* **New `--performance-mode` Flag**: A new `--performance-mode {balanced, interactivity, throughput}` flag (#34936) simplifies performance tuning for common deployment scenarios.
* **Anthropic API Compatibility**: Added support for **Anthropic thinking blocks** (#33671), **`count_tokens` API** (#35588), `tool_choice=none` (#35835), and streaming/image handling fixes.
* **Weight Offloading V2 with Prefetching**: The weight offloader now **hides onloading latency via prefetching** (#29941), plus **selective CPU weight offloading** (#34535) and CPU offloading without pinned memory doubling (#32993).
* **Elastic Expert Parallelism Milestone 2**: Initial support for elastic expert parallelism enabling dynamic GPU scaling for MoE models (#34861).
* **Quantized LoRA Adapters**: Users can now load **quantized LoRA adapters** (e.g. QLoRA) directly (#30286).
* **Transformers v5 Compatibility**: Extensive work to ensure compatibility with HuggingFace Transformers v5 across models and utilities.
* **CPU release supports AVX2, AVX-512, VNNI, AVX512BF16, and AMX** (#35466). The multi-ISA CPU dispatcher was originally implemented by @MekayelAnik (https://github.com/dtrifiro/vllm/pull/9, merged December 22, 2025) in collaboration with Willy Hardy, and later reimplemented in C++ in #35466.

### Model Support
* **New architectures**: Qwen3.5 (#34110), COLQwen3 (#34398), ColModernVBERT (#34558), Ring 2.5 (#35102), skt/A.X-K1 (#32407), Ovis 2.6 (#34426), nvidia/llama-nemotron-embed-vl-1b-v2 (#35297), nvidia/llama-nemotron-rerank-vl-1b-v2 (#35735), nvidia/nemotron-colembed (#34574).
* **ASR models**: FunASR (#33247), FireRedASR2 (#35727), Qwen3-ASR realtime streaming (#34613).
* **Multimodal**: OpenPangu-VL video input (#34134), audio chunking for offline LLM (#34628), Parakeet audio encoder for nemotron-nano-vl (#35100), MiniCPM-o flagos (#34126).
* **LoRA**: LFM2 (#34921), Llama 4 Vision tower/connector (#35147), max vocab size increased to 258048 (#34773), quantized LoRA adapters (#30286).
* **Task expansion**: ColBERT extended to non-standard BERT backbones (#34170), multimodal scoring for late-interaction models (#34574).
* **Performance**: Qwen3.5 GDN projector fusion (#34697), FlashInfer cuDNN backend for Qwen3 VL ViT (#34580), Step3.5-Flash NVFP4 (#34478), Qwen3MoE tuned configs for H200 (#35457).
* **Fixes**: DeepSeek-VL V2 simplified loading (#35203), Qwen3/Qwen3.5 reasoning parser (#34779), Qwen2.5-Omni/Qwen3-Omni mixed-modality (#35368), Ernie4.5-VL garbled output (#35587), Qwen-VL tokenizer (#36140), Qwen-Omni audio cache (#35994), Nemotron-3-Nano NVFP4 accuracy with TP>1 (#34476).

### Engine Core
* **Model Runner V2**: Pipeline Parallel (#33960), Decode Context Parallel (#34179), piecewise & mixed CUDA graphs (#32771), Eagle3 with CUDA graphs (#35029, #35040), pooling models (#35120), DP+EP for spec decoding (#35294), bad_words sampling (#33433), ModelState architecture (#35350, #35383, #35564, #35621, #35774), design docs (#35819).
* **Weight offloading**: V2 prefetching to hide latency (#29941), selective CPU weight offloading (#34535), CPU offloading without pinned memory doubling (#32993).
* **Sleep level 0** mode with enqueue/wait pattern (#33195), pause/resume moved into engine (#34125).
* **Fixes**: allreduce_rms_fusion disabled by default with PP > 1 (#35424), DCP + FA3 crash (#35082), prefix caching for Mamba "all" mode (#34874), num_active_loras fix (#34119), async TP reduce-scatter reduction fix (#33088).
* Repetitive token pattern detection flags (#35451).

### Kernel
* **FlashAttention 4** integration (#32974).
* **FlashInfer Sparse MLA** backend (#33451).
* **Triton-based top-k and top-p** sampler kernels (#33538).
* Faster topKperRow decode kernel for DeepSeek-V3.2 sparse attention (#33680).
* Optimized grouped topk kernel (#34206).
* TRTLLM DSV3 Router GEMM kernel, **6% batch-1 speedup** (#34302).
* FA3 swizzle optimization (#34043).
* 256-bit LDG/STG activation kernels (#33022).
* TMA support for fused_moe_lora kernel (#32195).
* **Helion kernel framework**: silu_mul_fp8 kernel (#33373), autotuning infrastructure (#34025), num_tokens autotuning (#34185), fx tracing via HOP (#34390), GPU variant canonicalization (#34928).
* FlashInfer TRTLLM fused MoE non-gated FP8 & NVFP4 (#33506).
* Optimized sample_recovered_tokens kernel (#34974).
* KV cache update ops extraction from FlashInfer forward (#35422) and MLA backends (#34627).

### Hardware & Performance
* **NVIDIA**: SM100 FMHA FP8 prefill for MLA (#31195), SM100 MXFP8 blockscaled grouped MM and quant kernels (#34448), SM100 Oink RMSNorm path (#31828), SM120 FP8 GEMM optimization (#34424), FlashInfer DeepGEMM swapAB on SM90 by default (#34924), DeepSeek R1 BF16 min latency QKV GEMM 0.5% E2E speedup (#34758), Cublas BF16 gate with FP32 output (#35121), FlashInfer All Reduce default to TRTLLM backend (#35793).
* **AMD ROCm**: AITER fused RoPE+KVCache (#33443), MXFP4 MoE weight pre-shuffling on gfx950 (#34192), bitsandbytes quantization (#34688), CK backend for MoE quantization (#34301), dynamic MXFP4 for DeepSeek V2 (#34157), GPT-OSS Quark format (#29008), GPT-OSS WMXFP4_AFP8 static scales (#30357), encoder/encoder-decoder on AITER (#35334), device capability derivation without CUDA init (#35069), `aiter` package renamed to `amd-aiter` (#35198).
* **Intel XPU**: CUDA graph support (#34482), GPUDirect RDMA via NIXL (#35270), TORCH_SDPA/TRITON_ATTN as ViT backend (#35010), vllm-xpu-kernels v0.1.3 (#35984).
* **CPU**: ARM BF16 cross-compilation (#33079), FP16 for s390x (#34116), KleidiAI INT8_W4A8 for all input dtypes (#34890), s390x vector intrinsics for attention (#34434), prefix caching for ppc64le (#35081), CPU release supports both AVX2 and AVX512 (#35466).
* **Performance**: Pipeline Parallel async send/recv 2.9% E2E throughput (#33368), pooling maxsim **13.9% throughput improvement** (#35330), Triton ViT attention backend (#32183), Mamba1 kernel-level chunk alignment for prefix caching (#34798), detokenizer optimization (#32975), pooling model copy optimization 1.8% throughput (#35127).

### Large Scale Serving
* **Pipeline Parallel** async send/recv, **2.9% throughput improvement** (#33368).
* **Elastic EP Milestone 2** (#34861).
* **EPLB**: Async rebalance algorithm (#30888), sync enforcement for NCCL backend (#35212).
* **Native weight syncing API** via IPC for RL workflows (#34171).
* Decode Context Parallel in Model Runner V2 (#34179).
* Ray env var propagation to workers (#34383).
* **Breaking**: KV load failure policy default changed from "recompute" to "fail" (#34896).
* Cross-node data parallelism message queue fix (#35429).
* NIXL: Token-based IPC API (#34175), version bound (#35495), NUMA core binding (#32365).

### Speculative Decoding
* **Nemotron-H MTP** and Mamba speculative decoding (#33726).
* **Eagle3** on Model Runner V2 with CUDA graphs (#35029, #35040), Eagle3 + disaggregated serving (#34529).
* Hidden states extraction system (#33736).
* `min_tokens` support with speculative decoding (#32642).
* Reduced TP communication for draft generation (#34049).
* MTP num_speculative_tokens > 1 with sparse MLA (#34552).
* Sparse MLA + MTP with full CUDA graphs (#34457).
* Spec decoding in Mamba cache align mode (#33705).
* DP+EP for spec decoding in Model Runner V2 (#35294).

### MoE Refactor
* **MoERunner abstraction** (#32344) with modular kernel architecture.
* MXFP4 Cutlass Experts to modular kernel (#34542), MXFP4 Marlin to modular kernel format (#34588), TRTLLM Kernels MK (#32564).
* MoEActivation enum (#33843).
* Improved default Triton fused MoE configs (#34846).
* Fused MoE + LoRA shared expert dual stream, **1.07x throughput** (#34933).
* DSV3 QKVAProj GEMM custom op for torch.compile (#35751).
* Fix routing for models without expert groups (MiniMax-M2.1) (#34673).

### torch.compile
* **AOT compile** with PyTorch 2.10 (#34155).
* **AR+RMSNorm fusion** by default at -O2 (#34299).
* **SiLU+FP4 quant fusion** by default at O1+ (#34718).
* Sequence parallelism threshold compile ranges (#28672).
* Various compile fixes: recursive pre_grad_passes (#34092), FakeTensorProp elimination (#34093), time discrepancy logging (#34912), artifact load errors (#35115), atomic artifact saving (#35117), pytree slice caching (#35308), fast_moe_cold_start undo for torch>=2.11 (#35475).

### Quantization
* **Quantized LoRA adapters** (#30286).
* **Per-head KV cache scales** in attention selector (#34281).
* FP8 MoE bias for GPT-OSS (#34906).
* SM100 MXFP8 blockscaled grouped MM and quant kernels (#34448).
* Mixed precision support for ModelOpt (#35047).
* Llama-4 attention quantization (int8, fp8) (#34243).
* Sparse24 compressed tensors fix (#33446).
* KV scale loading fix for MLA models (#35430).
* Compressed tensors as ground-truth for quant strategies (#34254).
* **AMD**: CK backend for MoE (#34301), dynamic MXFP4 for DeepSeek V2 (#34157), bitsandbytes on ROCm (#34688), GPT-OSS Quark format (#29008).
* **CPU**: KleidiAI INT8_W4A8 for all input dtypes (#34890).
* **Qwen3.5**: FP8 weight loading fix (#35289), mlp.gate not quantizable (#35156).
* int4_w4a16 fused_moe benchmark and tuning (#34130).
* FlashInfer integrate mm_mxfp8 in ModelOpt MXFP8 (#35053).

### API & Frontend
* **Anthropic API**: Thinking blocks (#33671), count_tokens (#35588), tool_choice=none (#35835), tool call streaming fix (#34887), base64 image handling (#35557).
* **Responses API**: Structured outputs (#33709), reasoning_tokens fix (#33513), reasoning_part streaming events (#35184).
* **UX**: `--performance-mode {balanced, interactivity, throughput}` (#34936), `--moe-backend` for explicit kernel selection (#33807), `--language-model-only` for hybrid models (#34120), `--enforce-eager` clarification (#34523).
* Whisper automatic language detection (#34342).
* MFU Prometheus counters (#30950).
* Unrecognized environment variable warnings (#33581).
* `generation_config` max_tokens treated as default not ceiling (#34063).
* Structured output bugfix for completions (#35237).
* Structured output JSON feature validation (#33233).
* Validate non-text content in system messages (#34072).
* Explicit validation error for tool calls (#34438).
* IO Processor plugin simplification (#34236).
* Sparse embedding IO process plugin (#34214).
* Pooling entrypoint improvements (#35604).

### Security
* Fix SSRF bypass via backslash-@ URL parsing inconsistency (#34743).

### Dependencies
* **PyTorch 2.10.0 upgrade** — breaking change requiring environment updates. ROCm torch also updated to official 2.10 release (#34387).
* OpenTelemetry libraries included by default (#34466).
* Bound NIXL upper bound version (#35495).
* mooncake-transfer-engine added to kv_connectors requirements (#34826).
* openai bounded to under 2.25.0.
* lm-eval bumped for Transformers v5 compatibility (#33994).
* mamba-ssm bumped for Transformers v5 (#34233).
* PyPI source distribution (sdist) now included (#35136).
* amd-quark package added for ROCm (#35658).

### V0 Deprecation
* Removed per-request logits processors (#34400).
* Removed unused MM placeholders in request output (#34944).
* Removed Swin model (#35821).
* Scheduled v0.17 deprecations applied (#35441).

### Transformers v5 Compatibility
* Model fixes: Qwen3VL (#34262), JAIS (#34264), MiniCPM-V, GLM-ASR, Qwen3.5.
* Xet high-performance mode (#35098).
* Custom processor import fixes (#35101, #35107).
* padding_index removal for compatibility (#35189).
* lm-eval (#33994) and mamba-ssm (#34233) version bumps.

## New Contributors 🎉

* @2ez4bz made their first contribution in https://github.com/vllm-project/vllm/pull/33607
* @Alibaba-HZY made their first contribution in https://github.com/vllm-project/vllm/pull/35289
* @aykoppol made their first contribution in https://github.com/vllm-project/vllm/pull/35451
* @bhoomit made their first contribution in https://github.com/vllm-project/vllm/pull/34773
* @charlesashby made their first contribution in https://github.com/vllm-project/vllm/pull/34169
* @chengyinie made their first contribution in https://github.com/vllm-project/vllm/pull/35457
* @EdalatiAli made their first contribution in https://github.com/vllm-project/vllm/pull/34448
* @ehfd made their first contribution in https://github.com/vllm-project/vllm/pull/33992
* @flutist made their first contribution in https://github.com/vllm-project/vllm/pull/35838
* @fort726 made their first contribution in https://github.com/vllm-project/vllm/pull/32407
* @fynnsu made their first contribution in https://github.com/vllm-project/vllm/pull/33736
* @gante made their first contribution in https://github.com/vllm-project/vllm/pull/35281
* @hallerite made their first contribution in https://github.com/vllm-project/vllm/pull/35834
* @hujia177 made their first contribution in https://github.com/vllm-project/vllm/pull/34982
* @itayalroy made their first contribution in https://github.com/vllm-project/vllm/pull/34861
* @jasonozuzu-cohere made their first contribution in https://github.com/vllm-project/vllm/pull/34715
* @jcaip made their first contribution in https://github.com/vllm-project/vllm/pull/35327
* @jhaotingc made their first contribution in https://github.com/vllm-project/vllm/pull/34933
* @jjmiao1 made their first contribution in https://github.com/vllm-project/vllm/pull/35994
* @jonoillar made their first contribution in https://github.com/vllm-project/vllm/pull/34513
* @koush made their first contribution in https://github.com/vllm-project/vllm/pull/33646
* @lailoo made their first contribution in https://github.com/vllm-project/vllm/pull/35616
* @Laurawly made their first contribution in https://github.com/vllm-project/vllm/pull/31828
* @Li-Yongwen made their first contribution in https://github.com/vllm-project/vllm/pull/34336
* @lichuang made their first contribution in https://github.com/vllm-project/vllm/pull/34679
* @lin-shh made their first contribution in https://github.com/vllm-project/vllm/pull/35645
* @majian4work made their first contribution in https://github.com/vllm-project/vllm/pull/35466
* @ojhaanshika made their first contribution in https://github.com/vllm-project/vllm/pull/34986
* @PatrykWo made their first contribution in https://github.com/vllm-project/vllm/pull/35307
* @pi314ever made their first contribution in https://github.com/vllm-project/vllm/pull/35434
* @pkousha made their first contribution in https://github.com/vllm-project/vllm/pull/33839
* @pks made their first contribution in https://github.com/vllm-project/vllm/pull/35237
* @qianlihuang made their first contribution in https://github.com/vllm-project/vllm/pull/32642
* @simonreginis made their first contribution in https://github.com/vllm-project/vllm/pull/31025
* @stakeswky made their first contribution in https://github.com/vllm-project/vllm/pull/35230
* @SteadfastAsArt made their first contribution in https://github.com/vllm-project/vllm/pull/34888
* @stingoChen made their first contribution in https://github.com/vllm-project/vllm/pull/35352
* @sychen52 made their first contribution in https://github.com/vllm-project/vllm/pull/35047
* @thepushkarp made their first contribution in https://github.com/vllm-project/vllm/pull/32114
* @Tib-Gridello made their first contribution in https://github.com/vllm-project/vllm/pull/35423
* @umut-polat made their first contribution in https://github.com/vllm-project/vllm/pull/35510
* @voipmonitor made their first contribution in https://github.com/vllm-project/vllm/pull/35615
* @wangxingran222 made their first contribution in https://github.com/vllm-project/vllm/pull/33088
* @wenshuai-xiaomi made their first contribution in https://github.com/vllm-project/vllm/pull/34424
* @wjabbour made their first contribution in https://github.com/vllm-project/vllm/pull/35672
* @yashwantbezawada made their first contribution in https://github.com/vllm-project/vllm/pull/31057
* @yoonsnowdev made their first contribution in https://github.com/vllm-project/vllm/pull/35382
* @ZhongsJie made their first contribution in https://github.com/vllm-project/vllm/pull/35835
* @MekayelAnik made their first contribution in https://github.com/vllm-project/vllm/pull/35466

---

## v0.16.0  (2026-02-25T19:58:49Z)

# vLLM v0.16.0
Please note that this release was branch cut on Feb 8, so any features added to vLLM after that date is not included.

## Highlights

This release features 440 commits from 203 contributors (7 new)!

* **Async scheduling + Pipeline Parallelism** is now fully supported, delivering **30.8% E2E throughput improvement** and **31.8% TPOT improvement** (#32618).
* **Realtime API**: A new WebSocket-based Realtime API enables streaming audio interactions (#33187), building on the Voxtral realtime infrastructure.
* **RLHF workflow improvements**: Native NCCL-based weight syncing API (#31943), layerwise weight reloading for QeRL (#32133), and engine pause/resume with request preservation (#32351).
* **Unified Parallel Drafting** for speculative decoding (#32887), plus spec decode now works with structured outputs (#33374) and penalty application in Model Runner V2 (#33251).
* **Major XPU platform overhaul**: Deprecated IPEX in favor of vllm-xpu-kernels (#33379), adding MoE (#33659), MXFP4 MoE (#33679), WNA16 (#33973), scaled_mm (#34117), and FP8 MoE (#34202) support.

### Model Support
* New architectures: GLM-OCR with MTP (#33005), Qwen3-ASR (#33312), DeepSeek-OCR-2 (#33165), Intern-S1-Pro (#33636), MiniCPM-o 4.5 (#33431), openPangu7B-VL (#32449), NemotronHPuzzle heterogeneous (#32549), MusicFlamingo (#32696), FunAudioChat (#2), ColBERT late interaction (#33686), voyage-4-nano (#33720), GLM-5 (#34124).
* Speculative decoding: EAGLE3 for Hunyuan/HunyuanVL (#33035), AFMoE (#33111), Mistral3 (#33939).
* LoRA expansion: Gemma3 vision components (#32764), Nemotron-H MTP models (#32265), Qwen3 output embedding (#29816). Optimized fused MoE-LoRA kernel indexing (#32770, #32774), unpermute-aware fused MoE LoRA path (#32655), reduced kernel overhead for fewer active LoRAs with multiple CUDA graphs (#32005).
* Features: Qwen3-Omni transcription (#29828), Mistral Large 3 with FlashInfer MoE (#33174), LFM2 SigLIP2 intermediate encoder layers (#33370), Qwen3-Omni/GLM-4.xV MRoPE positioning fixes (#33010, #33039), embedding input for disabled modalities (#32493).
* Performance: GLM-4.7-GPTQ decode and MTP acceptance rate regression fix (#33771), DeepSeek V3.2 fast detokenization (#33855), DeepSeek V3.2 tokenizer fix (#33832), GLM-5 MTP accuracy fix (#34385).

### Engine Core
* Async scheduling + Pipeline Parallelism: Full support with 30.8% throughput improvement (#32618), optimized spec decode + async scheduling with 1.5% throughput improvement (#33612), deadlock fix for torchrun PP broadcast (#33701).
* Speculative decoding: Unified Parallel Drafting (#32887), structured output support (#33374), penalty application in MRV2 (#33251), skip softmax for all-greedy rejection sampling (#32852), correctness fix for spec tokens with prefill chunks (#33652).
* RLHF: Native NCCL weight syncing API (#31943), layerwise reloading for QeRL (#32133), engine pause/resume with request preservation (#32351).
* Helion kernel framework: ConfigManager (#32740), kernel wrapper (#32964), kernel registry (#33203).
* PluggableLayer: Applied to linear layers (#33152) and Mamba layers (#33660).
* Batch invariance: Disable Cascade Attention (#32561), enable Triton attention (#33688).
* Performance: Grammar bitmask H2D copy on separate stream (#33059), zero-copy GQA for multimodal and CPU (#33732), early-reject oversized MM requests (#33502), CPU memory leak fix from Request reference cycle in prefix caching (#34183).

### Hardware & Performance
* **NVIDIA**: FlashInfer TRTLLM BF16 MoE integration (#32954), SM100 INT4 W4A16 kernel (#32437), SM121 (DGX Spark) CUTLASS support (#33517), MNNVL protocol for GB series (#33540), FlashInfer MLA concat optimization (#31171), GDN attention layout optimization (#33291), DeepGEMM FP8 MLA performance (#33568), wvSplitK_fp8 performance (#33527, #33493), B200 MoE configs for Nemotron Nano (#32804), Super B200 TP2 (#33510), GLM 4.6 (#32958), Mamba selective scan tuning for B200 (#32873). Fix: DeepSeek R1 CUTLASS MLA on B200 (#33637), QK Norm+RoPE fusion on B200+FP8 (#33967), CUTLASS FP8 blockwise on SM103a (#32224).
* **AMD ROCm**: QWEN3-NEXT FP8 tunings (#32042), AITER attention backend for Qwen3-Next (#32492), fused_add_rmsnorm_pad for GPT-OSS (#30976), Qwen3-Omni startup fix (#33077).
* **Intel XPU**: Platform overhaul - deprecated IPEX, switched to vllm-xpu-kernels (#33379). New: unquantized MoE (#33659), MXFP4 MoE (#33679), WNA16 kernel (#33973), scaled_mm kernel (#34117), FP8 MoE (#34202).
* **ARM CPU**: KleidiAI INT4 dynamic quant with BF16 activations (#33122), NEON BFMMLA BF16 paged attention (#32263), vectorization backend optimization (#30329), attention dispatch by head_dim alignment (#32161).
* **IBM Z**: BF16 kernel type for s390x (#33788).
* **torch.compile**: Stop compiling identical artifacts (#34003), MoE cold start optimization option (#33735), fix 32-bit indexing assumption (#33113), attention fusion pass fix (#33945).
* **Performance**: Chat completion streaming optimization (#33782), ORJSONResponse for faster API responses (#33548), MoE permute optimization for CUTLASS FP8 (#32892), shared/routed overlap for latent MoE on Nemotron-H (#32790), FlashInfer autotune control flag (#34006).

### Large Scale Serving
* Disaggregated serving: Mooncake connector rework with bootstrap server (#31034), cross-layer KV cache layout at NIXL Connector V2 (#33339), delay freeing blocks for aborted async loads (#32255), async double-free fix (#33377), Ray multi-replica single-instance fix (#33604).
* EPLB: Capture logical experts with router replay (#33013), DP metadata fix for dense models (#32739).
* Metrics: KV offloading connector metrics (#27942), labeled prompt token metrics for P/D disaggregation (#33290).

### Quantization
* New: FP8 block quant for CompressedTensorsW8A16Fp8 (#33280), ModelOpt MXFP8 for dense models (#33786), NVFP4/FP8 on Turing GPUs (#33076), TP > 4 for FP4 Gemm (#31099).
* Bugfixes: FP8 online quantization memory fix (#31914), asymmetric W4A16 (ConchLinear) for CT (#33200), DeepSeek V3.2 NVFP4 (#33932), LoRA FP8 (#33879), quantized Falcon-H1 model loading (#32728), quantized Mamba TP with n_groups=1 (#33257), CPU W8A8 with bias (#33582), CPU W8A8 3D input support (#33727).
* **Deprecation**: Removed BitBlas (#32683) and Marlin 24 (#32688).

### API & Frontend
* **Realtime API**: WebSocket-based streaming API (#33187) with Voxtral realtime support.
* **Responses API**: Sampling parameters (#32609), return token IDs (#33212), return prompt token IDs (#33378), parser implementation (#32712).
* Pooling API: Request schema consensus for ScoreRequest (#33060) and final standardization (#31127).
* Tool calling: Fix multi-turn tool call ID preservation (#32768), fix indexing double-counting (#33141), GLM-4 incremental string streaming (#33218), DSV3.2 fast detokenization fix (#33964), MCP tools non-streaming fix (#32762).
* Structured outputs: Performance optimization with reasoning (#33557), guidance vocab size fix (#33509).
* CLI: `--disable-access-log-for-endpoints` option (#30011).
* UX: Nested configs in YAML files (#33193), GGUF `repo_id:quant_type` syntax (#33371), DeepSeek ReasoningParser with thinking enabled by default (#33221), remove noisy CT warning (#33273), early tokenization validation (#31366), reasoning_content backward compatibility (#33635), only include Authorization header when OPENAI_API_KEY is set (#33488).
* Features: run_batch transcription/translation support (#33934), /server_info collect_env (#33246), OTEL tracing during model loading (#31162), clear MM and encoder cache (#33452), HF Hub LoRA resolver (#20320).
* Scoring: Fix multi-document scoring returning single result (#33837).

### Security
* Patch protobuf for CVE-2026-0994 (#34253).

### Dependencies
* huggingface-hub updates for Transformers v5 preparation (#33473).
* Transformers v5 compatibility fixes across multiple models (#33977, #33683).

### Deprecation & Breaking Changes
* Removed BitBlas quantization (#32683) and Marlin 24 (#32688).
* Removed deprecated `reasoning_content` message field (#33402).
* Removed deprecated pooling items (#33477).
* Removed deprecated `VLLM_ALL2ALL_BACKEND` environment variable (#33535).
* Deprecated IPEX for XPU, switched to vllm-xpu-kernels (#33379).

---
## New Contributors 🎉

* @aabbccddwasd made their first contribution in https://github.com/vllm-project/vllm/pull/33771
* @Code4me2 made their first contribution in https://github.com/vllm-project/vllm/pull/33517
* @ikchifo made their first contribution in https://github.com/vllm-project/vllm/pull/33967
* @jiangwu300 made their first contribution in https://github.com/vllm-project/vllm/pull/33604
* @pjs102793 made their first contribution in https://github.com/vllm-project/vllm/pull/33963
* @sleepcoo made their first contribution in https://github.com/vllm-project/vllm/pull/33978
* @TundeAtSN made their first contribution in https://github.com/vllm-project/vllm/pull/33939

---

## v0.15.1  (2026-02-04T20:48:08Z)

v0.15.1 is a patch release with security fixes, RTX Blackwell GPU fixes support, and bug fixes.

## Security

- **CVE-2025-69223**: Updated aiohttp dependency (#33621)
- **CVE-2026-0994**: Updated Protobuf dependency (#33619)

## Highlights

### Bugfix Hardware Support
- **RTX Blackwell (SM120)**: Fixed NVFP4 MoE kernel support for RTX Blackwell workstation GPUs. Previously, NVFP4 MoE models would fail to load on these GPUs (#33417)
- **FP8 kernel selection**: Fixed FP8 CUTLASS group GEMM to properly fall back to Triton kernels on SM120 GPUs (#33285)

### Model Support
- **Step-3.5-Flash**: New model support (#33523)

### Bugfix Model Support
- **Qwen3-VL-Reranker**: Fixed model loading (#33298)
- **Whisper**: Fixed FlashAttention2 with full CUDA graphs (#33360)

### Performance
- **torch.compile cold-start**: Fixed regression that increased cold-start compilation time (Llama3-70B: ~88s → ~22s) (#33441)
- **MoE forward pass**: Optimized by caching layer name computation (#33184)

### Bug Fixes
- Fixed prefix cache hit rate of 0% with GPT-OSS style hybrid attention models (#33524)
- Enabled Triton MoE backend for FP8 per-tensor dynamic quantization (#33300)
- Disabled unsupported Renormalize routing methods for TRTLLM per-tensor FP8 MoE (#33620)
- Fixed speculative decoding metrics crash when no tokens generated (#33729)
- Disabled fast MoE cold start optimization with speculative decoding (#33624)
- Fixed ROCm skinny GEMM dispatch logic (#33366)

### Dependencies
- Pinned LMCache >= v0.3.9 for API compatibility (#33440)

## New Contributors 🎉
* @zaristei2 made their first contribution in https://github.com/vllm-project/vllm/pull/33621

**Full Changelog**: https://github.com/vllm-project/vllm/compare/v0.15.0...v0.15.1

---

## v0.15.0  (2026-01-29T10:21:01Z)

## Highlights

This release features 335 commits from 158 contributors (39 new)!

### Model Support
* **New architectures**: Kimi-K2.5 (#33131), Molmo2 (#30997), Step3vl 10B (#32329), Step1 (#32511), GLM-Lite (#31386), Eagle2.5-8B VLM (#32456).
* **LoRA expansion**: Nemotron-H (#30802), InternVL2 (#32397), MiniMax M2 (#32763).
* **Speculative decoding**: EAGLE3 for Pixtral/LlavaForConditionalGeneration (#32542), Qwen3 VL MoE (#32048), draft model support (#24322).
* **Embeddings**: BGE-M3 sparse embeddings and ColBERT embeddings (#14526).
* **Model enhancements**: Voxtral streaming architecture (#32861), SharedFusedMoE for Qwen3MoE (#32082), dynamic resolution for Nemotron Nano VL (#32121), Molmo2 vision backbone quantization (#32385).

### Engine Core
* **Async scheduling + Pipeline Parallelism**: `--async-scheduling` now works with pipeline parallelism (#32359).
* **Mamba prefix caching**: Block-aligned prefix caching for Mamba/hybrid models with `--enable-prefix-caching --mamba-cache-mode align`. Achieves ~2x speedup by caching Mamba states directly (#30877).
* **Session-based streaming input**: New incremental input support for interactive workloads like ASR. Accepts async generators producing `StreamingInput` objects while maintaining KV cache alignment (#28973).
* **Model Runner V2**: VLM support (#32546), architecture improvements.
* **LoRA**: Inplace loading for memory efficiency (#31326).
* **AOT compilation**: torch.compile inductor artifacts support (#25205).
* **Performance**: KV cache offloading redundant load prevention (#29087), FlashAttn attention/cache update separation (#25954).

### Hardware & Performance

#### NVIDIA
* **Blackwell defaults**: FlashInfer MLA is now the default MLA backend on Blackwell, with TRTLLM as default prefill (#32615).
* **MoE performance**: 1.2-2% E2E throughput improvement via grouped topk kernel fusion (#32058), NVFP4 small-batch decoding improvement (#30885), faster cold start for MoEs with torch.compile (#32805).
* **FP4 kernel optimization**: Up to 65% faster FP4 quantization on Blackwell (SM100F) using 256-bit loads, ~4% E2E throughput improvement (#32520).
* **Kernel improvements**: topk_sigmoid kernel for MoE routing (#31246), atomics reduce counting for SplitK skinny GEMMs (#29843), fused cat+quant for FP8 KV cache in MLA (#32950).
* **torch.compile**: SiluAndMul and QuantFP8 CustomOp compilation (#32806), Triton prefill attention performance (#32403).

#### AMD ROCm
* **MoRI EP**: High-performance all2all backend for Expert Parallel (#28664).
* **Attention improvements**: Shuffle KV cache layout and assembly paged attention kernel for AiterFlashAttentionBackend (#29887).
* **FP4 support**: MLA projection GEMMs with dynamic quantization (#32238).
* **Consumer GPU support**: Flash Attention Triton backend on RDNA3/RDNA4 (#32944).

#### Other Platforms
* **TPU**: Pipeline parallelism support (#28506), backend option (#32438).
* **Intel XPU**: AgRsAll2AllManager for distributed communication (#32654).
* **CPU**: NUMA-aware acceleration for TP/DP inference on ARM (#32792), PyTorch 2.10 (#32869).
* **Whisper**: torch.compile support (#30385).
* **WSL**: Platform compatibility fix for Windows Subsystem for Linux (#32749).

### Quantization
* **MXFP4**: W4A16 support for compressed-tensors MoE models (#32285).
* **Non-gated MoE**: Quantization support with Marlin, NVFP4 CUTLASS, FP8, INT8, and compressed-tensors (#32257).
* **Intel**: Quantization Toolkit integration (#31716).
* **FP8 KV cache**: Per-tensor and per-attention-head quantization via llmcompressor (#30141).

### API & Frontend
* **Responses API**: Partial message generation (#32100), `include_stop_str_in_output` tuning (#32383), `prompt_cache_key` support (#32824).
* **OpenAI API**: `skip_special_tokens` configuration (#32345).
* **Score endpoint**: Flexible input formats with `data_1`/`data_2` and `queries`/`documents` (#32577).
* **Render endpoints**: New endpoints for prompt preprocessing (#32473).
* **Whisper API**: `avg_logprob` and `compression_ratio` in verbose_json segments (#31059).
* **Security**: FIPS 140-3 compliant hash option for enterprise/government users (#32386), `--ssl-ciphers` CLI argument (#30937).
* **UX improvements**: Auto `api_server_count` based on `dp_size` (#32525), wheel variant auto-detection during install (#32948), custom profiler URI schemes (#32393).

### Dependencies
* FlashInfer v0.6.1 (#30993)
* Transformers 4.57.5 (#32287)
* PyTorch 2.10 for CPU backend (#32869)
* DeepGEMM newer version (#32479)

### Breaking Changes & Deprecations
* **Metrics**: Removed deprecated `vllm:time_per_output_token_seconds` metric - use `vllm:inter_token_latency_seconds` instead (#32661).
* **Environment variables**: Removed deprecated environment variables (#32812).
* **Quantization**: DeepSpeedFp8 removed (#32679), RTN removed (#32697), HQQ deprecated (#32681).

### Bug Fixes
* **Speculative decoding**: Eagle draft_model_config fix (#31753).
* **DeepSeek**: DeepSeek-V3.1 + DeepGEMM incompatible scale shapes fix (#32361).
* **Distributed**: DP+MoE inference fix via CpuCommunicator (#31867), P/D with non-MoE DP fix (#33037).
* **EPLB**: Possible deadlock fix (#32418).
* **NIXL**: UCX memory leak fix by exporting UCX_MEM_MMAP_HOOK_MODE=none (#32181).
* **Structured output**: Outlines byte fallback handling fix (#31391).

---

## New Contributors 🎉
* @YunzhuLu made their first contribution in https://github.com/vllm-project/vllm/pull/32126
* @emricksini-h made their first contribution in https://github.com/vllm-project/vllm/pull/30784
* @dsfaccini made their first contribution in https://github.com/vllm-project/vllm/pull/32289
* @ofirzaf made their first contribution in https://github.com/vllm-project/vllm/pull/32312
* @seekskyworld made their first contribution in https://github.com/vllm-project/vllm/pull/32321
* @brian033 made their first contribution in https://github.com/vllm-project/vllm/pull/31715
* @TomerBN-Nvidia made their first contribution in https://github.com/vllm-project/vllm/pull/32257
* @vanshilshah97 made their first contribution in https://github.com/vllm-project/vllm/pull/32448
* @George-Polya made their first contribution in https://github.com/vllm-project/vllm/pull/32385
* @T1mn made their first contribution in https://github.com/vllm-project/vllm/pull/32411
* @mritunjaysharma394 made their first contribution in https://github.com/vllm-project/vllm/pull/31492
* @randzero made their first contribution in https://github.com/vllm-project/vllm/pull/32511
* @DemingCheng made their first contribution in https://github.com/vllm-project/vllm/pull/32556
* @iboiko-habana made their first contribution in https://github.com/vllm-project/vllm/pull/32471
* @honglyua-il made their first contribution in https://github.com/vllm-project/vllm/pull/32462
* @hyeongyun0916 made their first contribution in https://github.com/vllm-project/vllm/pull/32473
* @DanielMe made their first contribution in https://github.com/vllm-project/vllm/pull/32560
* @netanel-haber made their first contribution in https://github.com/vllm-project/vllm/pull/32121
* @longregen made their first contribution in https://github.com/vllm-project/vllm/pull/28784
* @jasonyanwenl made their first contribution in https://github.com/vllm-project/vllm/pull/32749
* @Wauplin made their first contribution in https://github.com/vllm-project/vllm/pull/32788
* @ikaadil made their first contribution in https://github.com/vllm-project/vllm/pull/32775
* @alexsun07 made their first contribution in https://github.com/vllm-project/vllm/pull/28664
* @liranschour made their first contribution in https://github.com/vllm-project/vllm/pull/30207
* @AuYang261 made their first contribution in https://github.com/vllm-project/vllm/pull/32844
* @diviramon made their first contribution in https://github.com/vllm-project/vllm/pull/32393
* @RishabhSaini made their first contribution in https://github.com/vllm-project/vllm/pull/32884
* @MatteoFari made their first contribution in https://github.com/vllm-project/vllm/pull/32397
* @peakcrosser7 made their first contribution in https://github.com/vllm-project/vllm/pull/30877
* @orionr made their first contribution in https://github.com/vllm-project/vllm/pull/30443
* @marksverdhei made their first contribution in https://github.com/vllm-project/vllm/pull/32614
* @joninco made their first contribution in https://github.com/vllm-project/vllm/pull/32935
* @monajafi-amd made their first contribution in https://github.com/vllm-project/vllm/pull/32944
* @ruizcrp made their first contribution in https://github.com/vllm-project/vllm/pull/32988
* @sjhddh made their first contribution in https://github.com/vllm-project/vllm/pull/32983
* @HirokenOvo made their first contribution in https://github.com/vllm-project/vllm/pull/32646
* @Chenhao-Guan made their first contribution in https://github.com/vllm-project/vllm/pull/32763
* @joshuadeng made their first contribution in https://github.com/vllm-project/vllm/pull/28973
* @ZhanqiuHu made their first contribution in https://github.com/vllm-project/vllm/pull/33016

**Full Changelog**: https://github.com/vllm-project/vllm/compare/v0.14.1...v0.15.0

---

## v0.14.1  (2026-01-24T20:29:27Z)

This is a patch release on top of `v0.14.0` to address a few security and memory leak fixes.

---