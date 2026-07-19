# huggingface/transformers - last 20 releases (latest: v5.13.1)


## v5.13.1  (2026-07-11T09:15:36Z)

# Patch release v5.13.1 

This patch is focused on enabling `transformers` for the latest release of vllm! 

- Be more defensive with remap_legacy_layer_types for custom models (#47245) from @hmellor 
- Fix custom code which doesn't know about the new linear layer type names (#47174) from @hmellor 
- Fix case where _LazyAutoMapping.register is passed a str key (#47148) from @hmellor

---

## v5.13.0  (2026-07-03T16:06:27Z)

# Release v5.13.0


## New Model additions

### KimiK 2.5, 2.6, and 2.7

<img width="1097" height="400" alt="image" src="https://github.com/user-attachments/assets/c24d2232-a9b4-413b-a2c8-58d013b6dfbd" />

This release includes the architecture for Kimi 2.5 which is used by 2.5-2.7:

Kimi K2.5 is an open-source, native multimodal agentic model that advances practical capabilities in long-horizon coding, coding-driven design, proactive autonomous execution, and swarm-based task orchestration. The model was proposed in [Kimi K2.5: Visual Agentic Intelligence](https://www.kimi.com/en/blog/kimi-k2-5) and further improved in [Kimi K2.6: Advancing Open-Source Coding](Kimi K2.5: Visual Agentic Intelligence).

Kimi K2.5 achieves significant improvements on complex, end-to-end coding tasks, generalizing robustly across programming languages (Rust, Go, Python) and domains spanning front-end, DevOps, and performance optimization. The model is capable of transforming simple prompts and visual inputs into production-ready interfaces and lightweight full-stack workflows, generating structured layouts, interactive elements, and rich animations with deliberate aesthetic precision.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/kimi_k25)
* Add new model: Kimi2-6 (#45630) by @zucchini-nlp in [#45630](https://github.com/huggingface/transformers/pull/45630)

### MiMo-V2-Flash

<img width="6900" height="904" alt="image" src="https://github.com/user-attachments/assets/8bd8d5f0-0381-4f8c-8ada-0203e11ff494" />

**MiMo-V2-Flash** is a Mixture-of-Experts (MoE) language model developed by the Xiaomi MiMo team. Designed to establish a new balance between long-context modeling capabilities and inference efficiency, the model is built for strong performance in complex reasoning and agentic tasks. Trained on 27T tokens with native 32k sequence lengths, MiMo-V2-Flash seamlessly supports an extended **256K context window** while significantly reducing KV-cache storage compared to standard global attention models.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/mimo_v2_flash)
* Add Xiaomi MiMo-V2 (#45144) by @casinca in [#45144](https://github.com/huggingface/transformers/pull/45144)

### Nemotron 3.5 ASR

<img width="1632" height="735" alt="image" src="https://github.com/user-attachments/assets/597bbb9c-b046-4e47-b9fd-f242e0a5b04d" />

Nemotron 3.5 ASR is a 600M-parameter multilingual speech recognition model from NVIDIA, built for high-quality transcription in both low-latency streaming and high-throughput batch settings, with native punctuation and capitalization. For streaming, it offers configurable chunk sizes—80ms, 160ms, 560ms, and 1120ms, letting users trade off latency against accuracy to suit their application. Its cache-aware FastConformer-RNNT architecture is central to this capability: unlike traditional buffered streaming, which repeatedly reprocesses overlapping audio windows, the model processes only each new incoming chunk while reusing cached encoder context from prior chunks. This eliminates redundant computation, significantly improves efficiency, and minimizes end-to-end delay without sacrificing accuracy, making it well suited to real-time transcription workloads.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/nemotron3_5_asr)
* Add Nemotron 3.5 ASR Streaming (#46565) by @eustlb in [#46565](https://github.com/huggingface/transformers/pull/46565)

### NemotronAsrStreaming

Nemotron ASR Streaming is a 600M-parameter English speech recognition model from NVIDIA, built for high-quality transcription in both low-latency streaming and high-throughput batch settings, with native punctuation and capitalization. For streaming, it offers configurable chunk sizes—80ms, 160ms, 560ms, and 1120ms, letting users trade off latency against accuracy to suit their application. Its cache-aware FastConformer-RNNT architecture is central to this capability: unlike traditional buffered streaming, which repeatedly reprocesses overlapping audio windows, the model processes only each new incoming chunk while reusing cached encoder context from prior chunks. This eliminates redundant computation, significantly improves efficiency, and minimizes end-to-end delay without sacrificing accuracy, making it well suited to real-time transcription workloads.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/nemotron_asr_streaming)
* Add Nemotron ASR Streaming (#46332) by @eustlb in [#46332](https://github.com/huggingface/transformers/pull/46332)

### Qwen3 ASR

<img width="3646" height="2036" alt="image" src="https://github.com/user-attachments/assets/41ed13e3-a0bf-463a-8473-bc6beb8ebd73" />

Qwen3 ASR is an automatic speech recognition model from Alibaba's Qwen team that combines a Whisper-style audio encoder with a Qwen3 language model decoder for speech-to-text transcription. The model supports automatic language detection and multilingual transcription.

A forced aligner model is also included. It can be used to timestamp a provided transcript and its audio. It uses the same audio encoder model with a classification head that predicts a word's length. This model can be used with the transcript from any ASR model (see the example below with Parakeet CTC).

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/qwen3_asr)
* Qwen3 ASR and Forced Aligner (#43838) by @mbtariq82 in [#43838](https://github.com/huggingface/transformers/pull/43838)

### ZAYA

<img width="1200" height="628" alt="image" src="https://github.com/user-attachments/assets/2935eba8-ab74-455c-9d44-f088636b2785" />

ZAYA1 is a 760M active / 8.4B total parameter MoE language model trained by Zyphra. It combines Compressed
Convolutional Attention (CCA), a nonlinear ZAYA1 router, and residual scaling.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/zaya)
* [new model] Add Zyphra/ZAYA1-8B (#45862) by @JJJYmmm in [#45862](https://github.com/huggingface/transformers/pull/45862)

### VideoPrism

The VideoPrism model was proposed in the paper [VideoPrism: A Foundational Visual Encoder for Video Understanding](https://huggingface.co/papers/2402.13217) by Google DeepMind ([blog post](https://research.google/blog/videoprism-a-foundational-visual-encoder-for-video-understanding/)).

VideoPrism is a general-purpose video encoder that tackles diverse video understanding tasks with a single frozen model. The model is pretrained on a large-scale heterogeneous corpus containing 36M high-quality video-caption pairs and 582M video clips with noisy parallel text (e.g., ASR transcripts). The pretraining approach improves upon masked autoencoding through global-local distillation of semantic video embeddings and a token shuffling scheme, enabling the model to focus primarily on the video modality while leveraging text associated with videos. VideoPrism achieves state-of-the-art performance on 31 out of 33 video understanding benchmarks across four broad task groups, from web video question answering to computer vision for science.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/videoprism)
* Add Videoprism (#39895) by @MHRDYN7 in [#39895](https://github.com/huggingface/transformers/pull/39895)

### RADIO

[RADIO](https://huggingface.co/papers/2312.06709) (Reduce All Domains Into One) is a family of vision foundation models from NVIDIA trained by multi-teacher distillation (e.g. CLIP, DINOv2, SAM) into a single ViT backbone. It produces both an image-level `summary` embedding and dense spatial `features`, and supports variable input resolutions through a Cropped Position Embedding (CPE) patch generator.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/radio)
* Add support for RADIO models (#46425) by @meatybobby in [#46425](https://github.com/huggingface/transformers/pull/46425)

### MiniCPM3

MiniCPM3 is the third-generation MiniCPM dense language model from OpenBMB. The 4B variant
([`openbmb/MiniCPM3-4B`](https://huggingface.co/openbmb/MiniCPM3-4B)) outperforms many 7B–9B open
models on standard benchmarks while remaining lightweight enough for on-device usage.

MiniCPM3 combines several architectural ideas:

- **Multi-head Latent Attention (MLA)** from DeepSeek-V2, which compresses the key/value cache
  into a low-rank latent representation while still using rotary embeddings on a portion of the
  query/key heads.
- A standard SwiGLU MLP (no MoE).
- Three scalar scaling factors that govern signal flow:
  - `scale_emb` — scales input embeddings.
  - `scale_depth / sqrt(num_hidden_layers)` — scales residual connections.
  - `hidden_size / dim_model_base` — scales hidden states before the language model head.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/minicpm3)
* Add MiniCPM3 (#41116) by @bzantium in [#41116](https://github.com/huggingface/transformers/pull/41116)



## Breaking changes

A broad set of modeling changes have been made to standardize layer declarations, mask/cache construction, and hybrid-attention handling, making many models cleanly exportable (ONNX, `torch.export`, ExecuTorch) and fullgraph-compilable — users relying on internal modeling APIs may need to update their code accordingly.
* 🚨 Modeling changes for export, compile, and hybrid-attention standardization (#46738) by @IlyasMoutawwakil

Attention masking for image tokens in Gemma 3/4 models has been fixed to correctly respect sliding window boundaries in local layers, which changes model behavior and may affect reproducibility of previous results.
* 🚨 [gemma 3/4] Fix bidirectional attention masking crossing sliding window boundaries (#46850) by @douglas-reid

The Expert Parallelism (EP) router contract has been corrected across many models and FP8 scale format handling has been fixed, requiring users of EP or FP8 quantization with affected models to verify their configurations and potentially update conversion mappings.
* 🚨 EP: fix EP router contract for many models + honor FP8 scale format (#46818) by @IlyasMoutawwakil

The `Kernels` integration has been synced to the latest version, which includes a breaking change where model-type repositories are no longer accepted by the kernels interface — users must migrate to the updated kernel repository format as shown in the updated tests.
* :rotating_light: [`Kernels`] Sync to latest version (#46039) by @vasqu


## HfExporters: Native, Unified export for PyTorch / ONNX / ExecuTorch

<img alt="thumbnail" src="https://github.com/user-attachments/assets/3ba5751b-c99e-4945-b5a8-b2b29231f5df" />

A native, in-Transformers export pipeline — one base class (`HfExporter`), three subclasses for the runtimes we care about, one unified API:

| Exporter | Output | Runtime |
|---|---|---|
| `DynamoExporter` | `ExportedProgram` | Any PyTorch runtime, AOT compilation |
| `OnnxExporter` | `ONNXProgram` | Any ONNX runtime (ORT, TensorRT, OpenVINO, …) |
| `ExecutorchExporter` | `ExecutorchProgramManager` | Mobile and edge (ExecuTorch) |

Same call shape across all three. Dynamic shapes by default. Generation-style models split automatically into prefill + decode (+ vision/audio sub-encoders for VLMs).

```python
from transformers import AutoModelForMaskedLM, AutoTokenizer
from transformers.exporters import OnnxExporter, OnnxConfig

model_id = "hf-internal-testing/tiny-random-BertForMaskedLM"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForMaskedLM.from_pretrained(model_id).eval()
inputs = tokenizer(["Hello, my dog is cute"] * 2, return_tensors="pt")
onnx_program = OnnxExporter().export(model, inputs, config=OnnxConfig(dynamic=True))

new_input = tokenizer("Hello, my cat is so adorable!", return_tensors="pt")
torch.testing.assert_close(
    onnx_program.call_reference(**new_input)[0],   # numpy reference
    onnx_program(**new_input)[0],                  # onnxruntime
    rtol=1e-4, atol=1e-4,
)
```

Swap one line for another runtime — `DynamoExporter()` / `DynamoConfig` or `ExecutorchExporter()` / `ExecutorchConfig(backend=...)`.

For generative models the prefill/decode split is captured automatically:

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from transformers.exporters import OnnxExporter, OnnxConfig

model_id = "hf-internal-testing/tiny-random-LlamaForCausalLM"
tokenizer = AutoTokenizer.from_pretrained(model_id)
model = AutoModelForCausalLM.from_pretrained(model_id).eval()
inputs = tokenizer(["Hello, my dog is cute"] * 2, return_tensors="pt")

artifacts = OnnxExporter().export_for_generation(model, inputs, config=OnnxConfig(dynamic=True))
# {"prefill": ONNXProgram, "decode": ONNXProgram}
# For VLMs: also vision_encoder, audio_encoder, multi_modal_projector, language_model, lm_head
```


## Kernels

**Kernels:** Fixed a silent SDPA math-kernel fallback for GQA models with `head_dim > 256` (e.g., Gemma4) that caused O(S²) memory materialization, and resolved a regression where `use_kernels=True` failed to apply kernel mappings. Additional improvements include lazy loading of the default kernel mapping to prevent import failures with incompatible kernel versions, ROCm routing to AITER Triton kernels for AMD GPUs, GB10/SM121 Hub-kernel support for Qwen3.6 Gated DeltaNet, and expanded documentation for the kernel API.


* Fix silent SDPA math-kernel fallback for GQA when key/value head_dim > 256 or differ (#46960) by @Butterfingrz in [#46960]
* [docs] AITER kernels (#46871) by @stevhliu in [#46871]
* Documentation for the kernel API (#46754) by @michaelbenayoun in [#46754]
* update kernels-community/aiter-rope version (#46810) by @Abdennacer-Badaoui in [#46810]
* Add GB10/SM121 Hub-kernel path for Qwen3.6 Gated DeltaNet (#46423) by @AzeezIsh in [#46423]
* [`Kernels`] Trigger proper kernelization on `use_kernels=True` (#46755) by @vasqu in [#46755]
* Lazily build the default kernel mapping to decouple `kernels` from normal transformers usage (#46681) by @jiqing-feng in [#46681]
* Add some AITER kernel routing for ROCm (#46268) by @Abdennacer-Badaoui in [#46268]
* fix: position ids does not exist in upstream rotary kernel (#46619) by @NanoCode012 in [#46619]
* docs(zh): add Chinese translation of kernels.md (#46621) by @shoushinya123 in [#46621]


## Generation

Several generation bugs were fixed, including Mamba2 chunked-prefill and speculative decoding for hybrid models (Zamba2, Nemotron-H, Bamba, FalconH1, GraniteMoeHybrid), beam search for Mamba models, prompt lookup decoding crashes with no EOS token, and incorrect stateful model handling for LFM2. Additional improvements include reduced unnecessary generation warnings, a fix for continuous batching output mutation, and a new option to keep input tensors on CPU during generation to avoid retracing on Neuron/TPU devices.


* Fix Mamba2 chunked-prefill / speculative decoding for Zamba2, Nemotron-H, Bamba, FalconH1 and GraniteMoeHybrid (#46741) by @Sunt-ing in [#46741]
* Remove some unnecessary generate warnings (#46955) by @Cyrilvallez in [#46955]
* Reject assisted generation for LFM2 and LFM2-MoE (set _is_stateful) (#46937) by @Sunt-ing in [#46937]
* Fix beam search for mamba models (#46819) by @Cyrilvallez in [#46819]
* Fix prompt lookup decoding crash when no EOS token is configured (#46790) by @Sunt-ing in [#46790]
* [Continuous Batching] Snapshot generation outputs without mutating request state (#46670) by @Incheonkirin in [#46670]
* [docs] keep generation tensors on cpu (#46675) by @stevhliu in [#46675]
* feat(generation): allow user to keep input tensors on cpu (#46590) by @dacorvo in [#46590]


## Attention

Several attention-related bugs were fixed in this release, including silent SDPA math-kernel fallbacks for GQA with large head dimensions, broken Flash Attention with `StaticCache`, incorrect causal masking in Xcodec2, a cross-attention reshape regression in Blip2, and eager GQA support in Evolla. Accelerate hook handling was also corrected for models using linear attention to prevent silently wrong results during offloading.


* Fix accelerate hooks for all models using linear attention (#46978) by @Cyrilvallez in [#46978]
* Fix Xcodec2 attention to be non-causal. (#46963) by @ebezzam in [#46963]
* Fix flash attention with StaticCache (#46914) by @Cyrilvallez in [#46914]
* Fix Evolla eager attention for the GQA text decoder (#46860) by @jiqing-feng in [#46860]
* [docs] metal flash attention (#46349) by @stevhliu in [#46349]
* [`Blip2`] Fix cross attention reshape (#46695) by @vasqu in [#46695]


## Cache

Cache APIs were improved by consolidating redundant getters into a cleaner `get_max_length` method and updating documentation accordingly. Several bug fixes were also applied, including correcting mask generation beyond sliding windows, fixing a dimension issue in cumulative length tracking, resolving device mismatches in offloaded cache for hybrid models, and fixing crashes when loading trust_remote_code models from symlinked local caches.


* [docs] update cache apis (#46892) by @stevhliu in [#46892]
* Rework some old cache getters/properties (#46862) by @Cyrilvallez in [#46862]
* Fix expanded dim in the cache's cumulative length (#46856) by @Cyrilvallez in [#46856]
* Fix mask when generating beyond sliding window (#46839) by @zucchini-nlp in [#46839]
* Fix offloaded cache device mismatch on hybrid models (#46748) by @Sunt-ing in [#46748]
* Fix dynamic module symlinked cache on trust_remote_code models (#46618) by @ldkhang1201 in [#46618]


## Serve

Several fixes and improvements were made to the Serve functionality, including lazy imports to prevent CLI crashes when the optional `serve` extra is not installed, a fix for dropped attributes during serialization of subclassed Pydantic models, and added documentation for the kernel API.


* fix(cli/serve): import serve handlers lazily so the CLI works without the `serve` extra (#46473) by @<NOT FOUND> in [#46473]
* [Fix] Serve drops some attributes at serialization (#46680) by @remi-or in [#46680]
* Reduce per_page from 100 to 50 in GitHub API calls to avoid server errors (#46678) by @ydshieh in [#46678]


## Quantization

Fixed dtype casting bugs in Gemma4's vision and audio multimodal embedders when using BitsAndBytes quantization, where inputs were incorrectly cast to integer storage dtypes (`uint8`/`int8`) instead of the actual compute dtype. Also corrected FP8 quantization to round block scales before quantizing weights, ensuring dequantization produces correct values for `ue8m0` (DeepSeek-V4 style) format.


* [Gemma4] Fix dtype casting for quantized vision/audio embedders (#46933) by @sharmax-vikas in [#46933]
* Fix dtype casting for quantized multimodal embedders (#46904) by @praful-srinivasan-027 in [#46904]
* Round the ue8m0 FP8 scale before quantizing so dequant matches the stored inverse (#46763) by @Incheonkirin in [#46763]


## Bugfixes and improvements

* Update workflow callers to use `transformers-ci` (#47040) by @ydshieh in [#47040]
* Add HunYuan VL model (#46417) by @Mi-Jiazhi in [#46417]
* Add tiny_model_id support to ProcessorTesterMixin for memory-sensitive tests (#47005) by @ydshieh in [#47005]
* chore(linter): add TRF018 modeling rule (#46259) by @tarekziade in [#46259]
* [PoC] HF exporters (#41992) by @IlyasMoutawwakil in [#41992]
* TST Skip PEFT tests if PEFT version is too low (#47027) by @BenjaminBossan in [#47027]
* CI Add PEFT integration tests (#47021) by @BenjaminBossan in [#47021]
* [glm-mode-dsa] Indexer uses interleaved rope (#46842) by @pcuenca in [#46842]
* Use standard arg names in Mllama (#46977) by @zucchini-nlp in [#46977]
* Bump min peft 0.19.1 remove weight conversion duplicate code (#46442) by @BenjaminBossan in [#46442]
* Raise a loud error for missing prefix (#46980) by @Rocketknight1 in [#46980]
* Fix typo in Qwen3 ASR no_split_module (#47002) by @ebezzam in [#47002]
* only in the original repo (#46982) by @tarekziade in [#46982]
* Fix typos in Gemma 4 Assistant documentation (#46975) by @RaunaqDavidNath in [#46975]
* the CI status should be a comment (#46976) by @tarekziade in [#46976]
* QwenVL model conversion (#46881) by @zucchini-nlp in [#46881]
* Remove default dtype in FusedRMSNormGated modules (#46953) by @Cyrilvallez in [#46953]
* FIX PEFT test changed error type (#46959) by @BenjaminBossan in [#46959]
* Fix path traversal via vocab-file arguments in tokenizer_config.json (#46279) by @LinZiyuu in [#46279]
* docs(conditional_detr): fix num_queries default in docstring (100 -> 300) (#46939) by @Kropiunig in [#46939]
* Use common floats_list method for feature extractor tests. (#46956) by @ebezzam in [#46956]
* Fix RT-DETR indexing error when num_feature_levels exceeds backbone o… (#46833) by @c1prk in [#46833]
* Fix Florence2 training-loss double-shift (same pattern as Moonshine #… (#46898) by @sharmax-vikas in [#46898]
* [Olmo3] different RoPE per layer type (#46911) by @zucchini-nlp in [#46911]
* Use inspect.getsource instead of open() for source-reading in _can_set_*_implementation (#46207) by @rasmi in [#46207]
* Don't pin the gated delta net norm to `cuda:0` with a hardcoded device (#46817) by @Sunt-ing in [#46817]
* Fix auto-mappings registration for remote code & fixes a few custom code issues (#46876) by @Cyrilvallez in [#46876]
* Fix broken internal documentation links (#46945) by @sezer-muhammed in [#46945]
* Insert a Grafana badge in the PR (#46774) by @tarekziade in [#46774]
* [NemotronAsrStreaming] fix pipeline (#46870) by @eustlb in [#46870]
* [NemotronAsrStreaming] processor without modular (#46865) by @eustlb in [#46865]
* [`Dia`] Fix docs (#46923) by @vasqu in [#46923]
* [Docs] Fix full disk offloading docs (#46905) by @kylesayrs in [#46905]
* [CB] Changes to increase max_batch_tokens (#46712) by @remi-or in [#46712]
* Redirect to diffusers pipe in docs for experimental features (#46875) by @zucchini-nlp in [#46875]
* Install in docker (#46910) by @ydshieh in [#46910]
* [CI] Use pre-computed `_OLD_MODELS` in `test_new_models_require_torchvision_backend` (#46882) by @ydshieh in [#46882]
* call transformers-ci in a nightly run (#46811) by @tarekziade in [#46811]
* [docs] full disk offloading (#46893) by @stevhliu in [#46893]
* TST Run fast PEFT tests in normal CI (#45679) by @BenjaminBossan in [#45679]
* nemotron_asr_streaming: set _supports_flex_attn to False (#46878) by @kaixuanliu in [#46878]
* Add native masked MSE loss for Sapiens2ForPoseEstimation (#46764) by @Sainava in [#46764]
* blip 2 fix (#46816) by @itazap in [#46816]
* Use meshgrid for brevity (#46861) by @zucchini-nlp in [#46861]
* Add xcodec2 model (#44178) by @ebezzam in [#44178]
* Prevent auto-class from being modified for all models (#46844) by @zucchini-nlp in [#46844]
* Add Spanish translation of the torch.compile page (#46852) by @delcenjo in [#46852]
* docs: Update NeMo AutoModel doc examples (#46857) by @adil-a in [#46857]
* [docs] distributed training (#44420) by @stevhliu in [#44420]
* [docs] require trust_remote_code for custom_generate (#46677) by @stevhliu in [#46677]
* add distributed config (#46705) by @3outeille in [#46705]
* [Offloading] [Bugfix] Fix disk offloading of models with explicit tensor dtypes (#46849) by @kylesayrs in [#46849]
* Streamable chat parsing (#45847) by @Rocketknight1 in [#45847]
* Fix BitNet packed-weight unpacking dtype (`F.linear` dtype mismatch) (#46808) by @jiqing-feng in [#46808]
* Fix typos in code (#46579) by @cyyever in [#46579]
* Fix Moonshine training-loss double-shift (train against labels, not labels[..., 1:]) (#46784) by @Incheonkirin in [#46784]
* [CB] Fix issues with FA read / writes (#46765) by @remi-or in [#46765]
* Switch decorator order (#46853) by @Cyrilvallez in [#46853]
* docs(trainer): add JIT checkpointing to trainer recipes (#46826) by @efazal in [#46826]
* Import diffusion_gemma in models init (#46841) by @boringcrypto in [#46841]
* [skills] help your agent get started (#45732) by @stevhliu in [#45732]
* Fix use_cache with seq_len > 1 ( #46032) (#46084) by @Ramshankar07 in [#46084]
* [Offloading] Support full disk offloading (#46749) by @kylesayrs in [#46749]
* fix: raise `ValueError` for empty conversation in `apply_chat_template` (#46753) by @sharmax-vikas in [#46753]
* Fix VideoPrismForVideoClassification returning last_hidden_state as h… (#46830) by @sharmax-vikas in [#46830]
* Avoid NumPy 2.0 `__array__` copy-keyword deprecation in `create_mm_token_type_ids` (#46827) by @qgallouedec in [#46827]
* docs: update apple silicon doc with safetensors `0.8.0` benefits (#46744) by @McPatate in [#46744]
* [`CB`] Add FA2 to the fast path (#46729) by @vasqu in [#46729]
* Fix flex_attention block mask creation when `get_seq_length` returns a tensor (#46802) by @jiqing-feng in [#46802]
* Fix left-padding token selection in `BioGptForSequenceClassification` (#46782) by @Sunt-ing in [#46782]
* Fix broken internal links in model documentation (#46807) by @ShamSaleem in [#46807]
* DiffusionGemma: mask layout and CI (#46654) by @zucchini-nlp in [#46654]
* Use cached added-token dicts in per-token decode loops (#46535) by @ishan-1010 in [#46535]
* fix another flaky test (#46767) by @zucchini-nlp in [#46767]
* Fix secondary rate limit when downloading artifacts in slack report (#46796) by @ydshieh in [#46796]
* docs: move SmolLM3 to Text models category in _toctree.yml (#46770) by @yyouretoast in [#46770]
* Fix several bugs in `cache_implementation=static` (#46446) by @dacorvo in [#46446]
* [CI] Fix artifact download path in self-comment-ci workflow (#46769) by @ydshieh in [#46769]
* fixes per head minimaxm3 (#46719) by @ArthurZucker in [#46719]
* [`CI`] Fix some failures introduced by myself :grimacing:  (#46751) by @vasqu in [#46751]
* Fix regression in ProcessorMixin._load_tokenizer_from_pretrained for tokenizers at root (#46592) by @<NOT FOUND> in [#46592]
* fix(aria): use math.ceil in get_number_of_image_patches to match actual patch count (#46732) by @arnavkewalram in [#46732]
* Return logits from semantic segmentation post-process (#46163) by @guarin in [#46163]
* Fall back to the for-loop grouped_mm on CPU (#46743) by @Sunt-ing in [#46743]
* Kernelize refactor (#46520) by @michaelbenayoun in [#46520]
* ci: add comment explaining why secrets are not inherited in security gate (#46750) by @ydshieh in [#46750]
* ci: trigger PR CI on ci-* branches (#46746) by @ydshieh in [#46746]
* finegrained v3 (#46742) by @IlyasMoutawwakil in [#46742]
* Improve AutoImageProcessor error for unavailable backends (#46727) by @sisaman in [#46727]
* skip decorators must appear after @parameterized.expand in pytest (#46737) by @rasmi in [#46737]
* [RecurrentGemma] Support attn_implementation dispatch (#46320) by @YangKai0616 in [#46320]
* [docs] clarify initialization module usage (#46698) by @stevhliu in [#46698]
* feat: bump safetensors to `0.8.0` (#46523) by @McPatate in [#46523]
* ci: disable CircleCI by replacing config with no-op (#46721) by @ydshieh in [#46721]
* [CB] Fix offloading (#46587) by @remi-or in [#46587]
* [`Templates`] Update members (#46720) by @vasqu in [#46720]
* feat[vLLM x v5]: Expose max_source_positions on VibeVoiceAsrConfig (#46472) by @harshaljanjani in [#46472]
* Laguna: support per-element output gating (#46690) by @joerowell in [#46690]
* ci: grant pull-requests:write to the security gate caller (#46715) by @ydshieh in [#46715]
* Multi-gpu loading when the whole backbone is tied (#46625) by @zucchini-nlp in [#46625]
* Delete docstring if same as in auto-doc (#46284) by @zucchini-nlp in [#46284]
* Update GLM-5.2 docs (#46703) by @Dovis01 in [#46703]
* add conversion scripts for EUPE (#46691) by @molbap in [#46691]
* [docs] compile level and batch/scheduling limits (#46676) by @stevhliu in [#46676]
* [blip_2] Support attn_implementation dispatch (#46401) by @YangKai0616 in [#46401]
* [CTRL] Support attn_implementation dispatch (#46073) by @YangKai0616 in [#46073]
* Lfm2: also thread `seq_idx` through ShortConv.slow_forward (non-fast-path) (#46633) by @ChangyiYang in [#46633]
* feat(pipelines): accept numpy arrays and tensors in ImageClassificationPipeline (#39607) (#46573) by @kamran-nizamani in [#46573]
* Smovlm: pad videos up to max frames (#46662) by @zucchini-nlp in [#46662]
* mistral common backend fix (#46667) by @itazap in [#46667]
* [pr template] update (#46606) by @stevhliu in [#46606]
* Fix AttributeError in auto_factory when model_class lacks config_class (#46669) by @atharv1945 in [#46669]
* [CB] Slice logits inside the model (#46660) by @remi-or in [#46660]
* ci: add NO_COLOR=1 to suppress ANSI color codes in CI output (#46659) by @ydshieh in [#46659]
* Fix dynamic RoPE not resetting inv_freq when layer_type is None (#46624) by @Incheonkirin in [#46624]
* Better processing tests (#46374) by @zucchini-nlp in [#46374]
* ci: add merge_group trigger to pr-ci-caller.yml (#46668) by @ydshieh in [#46668]
* skip invalid quant_cache test for nemotron_h (#46368) by @kaixuanliu in [#46368]
* Revert "Disable PR CI workflow for PRs from forked repo. during the weekend" (#46652) by @ydshieh in [#46652]
* [CB] Fix seqlens and use TypedDict (#46593) by @remi-or in [#46593]
* Disable PR CI workflow for PRs from forked repo. during the weekend (#46609) by @ydshieh in [#46609]
* Update post release (#46608) by @vasqu in [#46608]
* Fix `peft` lower bound (#46605) by @hmellor in [#46605]
* Fix docstring formatting issues causing Sphinx autodoc warnings (#46596) by @kurtmckee in [#46596]

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @ydshieh
    * Update workflow callers to use `transformers-ci` (#47040)
    * Add tiny_model_id support to ProcessorTesterMixin for memory-sensitive tests (#47005)
    * Install in docker (#46910)
    * [CI] Use pre-computed `_OLD_MODELS` in `test_new_models_require_torchvision_backend` (#46882)
    * Fix secondary rate limit when downloading artifacts in slack report (#46796)
    * [CI] Fix artifact download path in self-comment-ci workflow (#46769)
    * ci: add comment explaining why secrets are not inherited in security gate (#46750)
    * ci: trigger PR CI on ci-* branches (#46746)
    * ci: disable CircleCI by replacing config with no-op (#46721)
    * ci: grant pull-requests:write to the security gate caller (#46715)
    * Reduce per_page from 100 to 50 in GitHub API calls to avoid server errors (#46678)
    * ci: add NO_COLOR=1 to suppress ANSI color codes in CI output (#46659)
    * ci: add merge_group trigger to pr-ci-caller.yml (#46668)
    * Revert "Disable PR CI workflow for PRs from forked repo. during the weekend" (#46652)
    * Disable PR CI workflow for PRs from forked repo. during the weekend (#46609)
* @Mi-Jiazhi
    * Add HunYuan VL model (#46417)
* @tarekziade
    * chore(linter): add TRF018 modeling rule (#46259)
    * only in the original repo (#46982)
    * the CI status should be a comment (#46976)
    * Insert a Grafana badge in the PR (#46774)
    * call transformers-ci in a nightly run (#46811)
* @casinca
    * Add Xiaomi MiMo-V2 (#45144)
* @JJJYmmm
    * [new model] Add Zyphra/ZAYA1-8B (#45862)
* @ebezzam
    * Fix typo in Qwen3 ASR no_split_module (#47002)
    * Fix Xcodec2 attention to be non-causal. (#46963)
    * Use common floats_list method for feature extractor tests. (#46956)
    * Add xcodec2 model (#44178)
* @meatybobby
    * Add support for RADIO models (#46425)
* @douglas-reid
    * 🚨 [gemma 3/4] Fix bidirectional attention masking crossing sliding window boundaries (#46850)
* @Sunt-ing
    * Fix Mamba2 chunked-prefill / speculative decoding for Zamba2, Nemotron-H, Bamba, FalconH1 and GraniteMoeHybrid (#46741)
    * Reject assisted generation for LFM2 and LFM2-MoE (set _is_stateful) (#46937)
    * Don't pin the gated delta net norm to `cuda:0` with a hardcoded device (#46817)
    * Fix prompt lookup decoding crash when no EOS token is configured (#46790)
    * Fix left-padding token selection in `BioGptForSequenceClassification` (#46782)
    * Fix offloaded cache device mismatch on hybrid models (#46748)
    * Fall back to the for-loop grouped_mm on CPU (#46743)
* @eustlb
    * Add Nemotron 3.5 ASR Streaming (#46565)
    * [NemotronAsrStreaming] fix pipeline (#46870)
    * [NemotronAsrStreaming] processor without modular (#46865)
    * Add Nemotron ASR Streaming (#46332)
    * [fix] enable base64 str audio in load_audio (#46694)
* @vasqu
    * [`Dia`] Fix docs (#46923)
    * [`CB`] Add FA2 to the fast path (#46729)
    * [`Kernels`] Trigger proper kernelization on `use_kernels=True` (#46755)
    * [`CI`] Fix some failures introduced by myself :grimacing:  (#46751)
    * :rotating_light: [`Kernels`] Sync to latest version (#46039)
    * [`Templates`] Update members (#46720)
    * [`Blip2`] Fix cross attention reshape (#46695)
    * Update post release (#46608)
* @mbtariq82
    * Qwen3 ASR and Forced Aligner (#43838)
* @remi-or
    * [CB] Changes to increase max_batch_tokens (#46712)
    * [CB] Fix issues with FA read / writes (#46765)
    * [CB] Fix offloading (#46587)
    * [Fix] Serve drops some attributes at serialization (#46680)
    * [CB] Slice logits inside the model (#46660)
    * [CB] Fix seqlens and use TypedDict (#46593)
* @jiqing-feng
    * Fix BitNet packed-weight unpacking dtype (`F.linear` dtype mismatch) (#46808)
    * Fix Evolla eager attention for the GQA text decoder (#46860)
    * Fix flex_attention block mask creation when `get_seq_length` returns a tensor (#46802)
    * Lazily build the default kernel mapping to decouple `kernels` from normal transformers usage (#46681)
* @bzantium
    * Add MiniCPM3 (#41116)
* @MHRDYN7
    * Add Videoprism (#39895)
* @YangKai0616
    * [RecurrentGemma] Support attn_implementation dispatch (#46320)
    * [blip_2] Support attn_implementation dispatch (#46401)
    * [CTRL] Support attn_implementation dispatch (#46073)

---

## v5.12.1  (2026-06-15T17:29:59Z)

# Patch release v5.12.1
Updated the lower bound for PEFT and a fix for auto tokenizer to properly resolve the mistral tokenizer (when `mistral-common` is installed). This is similar to v.5.10.3 minus the fixes that were already included in the main release - vLLM will first target 5.10.3 :hugs: 

* Fix `peft` lower bound #46605 by @hmellor (#46605)
* mistral common backend fix #46667 by @itazap (#46667)


**Full Changelog**: https://github.com/huggingface/transformers/compare/v5.12.0...v5.12.1

---

## v5.10.3  (2026-06-15T17:29:39Z)

# Patch release v5.10.4
Update: Note that on pypi `5.10.3` doesn't exist and this this saved under `5.10.4` (so essentially a minor version skipped). Sorry about that, that's on me. Just wanted to clarify to make this less confusing!

A few fixes needed for vLLM to sync with transformers :hugs: 

* [fix] regression introduced by #45534 #46456 by @eustlb (#46456)
* Fix {image/video/audio}_token_ids in ProcessorMixin #46500 by @hmellor (#46500)
* Fix InternVL models #46524 by @hmellor (#46524)
* Fix the offsets in processing #46525 by @zucchini-nlp (#46525)
* Fix `peft` lower bound #46605 by @hmellor (#46605)
* mistral common backend fix #46667 by @itazap (#46667)


**Full Changelog**: https://github.com/huggingface/transformers/compare/v5.10.2...v5.10.3

---

## v5.12.0  (2026-06-12T14:39:40Z)

# Release v5.12.0


## New Model additions

### MiniMax-M3-VL

<img width="886" height="583" alt="image" src="https://github.com/user-attachments/assets/ae9dd96f-6877-4531-a06b-a756686f24e5" />

MiniMax-M3-VL is the vision-language member of the MiniMax-M3 family that pairs a CLIP-style vision tower with 3D rotary position embeddings with the MiniMax-M3 text backbone. It uses a mixed dense/sparse Mixture-of-Experts decoder with SwiGLU-OAI gated experts and a lightning indexer for block-sparse attention. The model processes images through a Conv3d patch embedding system and includes specialized components for efficient multimodal understanding and generation.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/minimax_m3_vl)
* Add minimax m3vl (#46600) by @ArthurZucker in [#46600](https://github.com/huggingface/transformers/pull/46600)


### PP-OCRv6: update documentation and slow tests (#46576)

<img width="3840" height="1494" alt="image" src="https://github.com/user-attachments/assets/e62284ec-78bf-49cb-8aa2-deccc665372f" />

The official weights for PP-OCRv6 are out: PP-OCRv6 is a lightweight OCR system that combines architectural innovation with data-centric optimization. It redesigns the backbone, detection neck, and recognition neck around a unified MetaFormer-style building block with structural reparameterization. Three model tiers (medium, small, tiny) share the same block primitives, covering deployment scenarios from server to edge.

* PP-OCRv6: update documentation and slow tests (#46576) by @ zhang-prog


### Add Parakeet-RNNT (#46331)

ParakeetForRNNT: a Fast Conformer Encoder + an RNN-T (RNN Transducer) decoder

- RNN-T Decoder: Standard neural transducer:
    - LSTM prediction network maintains language context across token predictions.
       - Joint network combines encoder and decoder outputs.
       - Greedy transducer decoding for inference: a blank emission advances the encoder frame by one, a non-blank emission stays on the same frame.

* Add Parakeet-RNNT (#46331) by @eustlb


## Bugfixes and improvements

* [CI] don't export OTELs within the tests (#46602) by @tarekziade in [#46602]
* [CI] capture checkers output in OTEL (#46601) by @tarekziade in [#46601]
* Lfm2: thread `seq_idx` through ShortConv for packed/varlen inputs (#46588) by @ChangyiYang in [#46588]
* put output_hidden_states into filter_output_hidden_states (#46422) by @molbap in [#46422]
* a11 for checkers (#46599) by @tarekziade in [#46599]
* Fix stop string matching for byte-fragment tokens (#46530) by @Incheonkirin in [#46530]
* [DiffusionGemma] better docs and links (#46569) by @gante in [#46569]
* Require `trust_remote_code` to run a local-directory `custom_generate` (#46483) by @LinZiyuu in [#46483]
* Fix torchaudio version not tied to torch version in docker file  (#46594) by @ydshieh in [#46594]
* [CI] Enable PR CI for all fork PRs via security gate (#46591) by @ydshieh in [#46591]
* [CB] [Minor] Add parameter to tune default compile level (#46533) by @remi-or in [#46533]
* Make DiffusionGemma trainable (#46568) by @kashif in [#46568]
* docs: 🌐 add Turkish translation for README file (#46312) by @onuralpszr in [#46312]
* fix-trainer-tests (#46541) by @SunMarc in [#46541]
* Remove unnecessary expand_as in get_placeholder_mask across VLMs (#44907) by @syncdoth in [#44907]
* [CI] Catch all shell/process execution issues in security gate via Bandit JSON report (#46560) by @ydshieh in [#46560]
* Honor a concrete dtype in AutoModel for composite checkpoints (#46514) by @qflen in [#46514]
* [CI] Implement real security check in PR CI security gate (#46557) by @ydshieh in [#46557]
* [CI] Add 60s delay in security gate for flow observation (#46555) by @ydshieh in [#46555]
* [TBC] [CI] Auto-approve PR CI for fork PRs via security gate (#46553) by @ydshieh in [#46553]
* [CI] fix and make less flaky (#46543) by @zucchini-nlp in [#46543]
* Fix hf_hub_download not placing file in current dir for url_to_local_path (#46545) by @ydshieh in [#46545]

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @ArthurZucker
    * Add minimax m3vl (#46600)
* @eustlb
    * Add Parakeet-RNNT (#46331)

---

## v5.11.0  (2026-06-10T16:32:44Z)

# Release v5.11.0


## New Model additions

### DiffusionGemma

<img width="1240" height="700" alt="image" src="https://github.com/user-attachments/assets/5081e449-6374-4076-bd96-d295c8334ca4" />

DiffusionGemma is engineered to reduce the sequential bottlenecks of standard causal language models by employing an encoder-decoder architecture specifically optimized for inference speed. During inference, DiffusionGemma leverages multi-canvas sampling, where rather than generating one token at a time, the model iteratively denoises a full block of tokens using a diffusion sampler. This block-autoregressive approach facilitates text generation at higher speeds compared to traditional sequential generation methods.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/diffusion_gemma)
* GPU go brr (#46540) by @gante in [#46540](https://github.com/huggingface/transformers/pull/46540)



### DeepSeek-V3.2

<img width="1135" height="671" alt="image" src="https://github.com/user-attachments/assets/24c9694d-eeae-402c-9a98-f7a3971dd9d0" />

DeepSeek-V3.2-Exp is an experimental model from DeepSeek-AI that introduces DeepSeek Sparse Attention (DSA), a trainable, fine-grained sparse attention mechanism designed to improve training and inference efficiency in long-context scenarios. Built on top of DeepSeek-V3.1-Terminus with a 685B-parameter Mixture-of-Experts backbone, it reduces the quadratic cost of attention over long sequences by attending only to a selected subset of past tokens while maintaining virtually identical benchmark performance. The work was extended in DeepSeek-V3.2 which pairs DSA with scalable reinforcement learning and achieves gold-medal level results on competition math and competitive programming benchmarks.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/deepseek_v32) | [Paper](https://huggingface.co/papers/2512.02556)
* Add deepseek 3.2 exp (#41251) by @ArthurZucker in [#41251](https://github.com/huggingface/transformers/pull/41251)


## Kernels

The `KernelConfig` API was extended to support n-to-1 module fusion and parameter transformation, simplifying how custom kernels are integrated with Transformers modules. Additional fixes include resolving a dtype mismatch in the Mamba2 CUDA kernel path for NemotronH/Zamba2, adding fine-grained fp8/fp4 Triton kernel support, and correcting the FalconMamba fast-path warning to recommend `pip install kernels` instead of `mamba-ssm`.


* Extended & simplified n-to-1 kernel fusion via KernelConfig (#46339) by @michaelbenayoun in [#46339]
* Triton finegrained fp8/fp4 (#46407) by @IlyasMoutawwakil in [#46407]
* Fix dtype mismatch in NemotronH/Zamba2 Mamba2 CUDA-kernel path (`out_proj`) (#46487) by @yuekaizhang in [#46487]
* fix(falcon_mamba): recommend `pip install kernels` in fast-path warning (#46343) by @Anai-Guo in [#46343]


## Parallelization

Fixed model parallel beam search bugs in the Qwen2-VL, Qwen2.5-VL, and Qwen3-VL MoE model families, and added documentation for tensor parallelism support with continuous batching.


* [docs] tp for continuous batching (#46019) by @stevhliu in [#46019]
* revisit history parallel beam search tests to avoid unnecessary fix (#46495) by @kaixuanliu in [#46495]
* fix qwen series VL model's model parallel bug (#46316) by @kaixuanliu in [#46316]


## Bugfixes and improvements

* Fix the offsets in processing (#46525) by @zucchini-nlp in [#46525]
* Fix buggy action sha pin (#46534) by @ydshieh in [#46534]
* Fix trailing comma bug in DataCollatorForLanguageModeling example (#46527) by @JemmaUZH in [#46527]
* Fix missing Gemma4Processor._compute_audio_num_tokens (#46416) by @csantosbh in [#46416]
* Fix InternVL models (#46524) by @hmellor in [#46524]
* fix(afmoe): reduce tokens in test_compile_static_cache to avoid flaky bfloat16 drift (#46521) by @ydshieh in [#46521]
* [CB] Add a "max_requests_per_batch" parameter (#46434) by @remi-or in [#46434]
* revamp cv docs and fix rf-detr (#46219) by @merveenoyan in [#46219]
* Update hub metadata (#46379) by @zucchini-nlp in [#46379]
* extend DeepseekV4FlashIntegrationTest to non-cuda device (#46517) by @sywangyi in [#46517]
* [docs] deepgemm (#46361) by @stevhliu in [#46361]
* [fix] regression introduced by #45534 (#46456) by @eustlb in [#46456]
* Use torchvision's native LANCZOS interpolation instead of PIL fallback (#46496) by @NicolasHug in [#46496]
* Add debugging info in `pr-ci-caller.yml` (#46505) by @ydshieh in [#46505]
* Fix tests: 'Cohere2MoeModel' object has no attribute 'hf_device_map' (#46337) by @kaixuanliu in [#46337]
* Bump the actions group across 1 directory with 19 updates (#46414) by @dependabot[bot] in [#46414]
* Log some information in `.github/workflows/pr-ci-post-dashboard-link.yml` (#46499) by @ydshieh in [#46499]
* feat(quantizers): support non-weight param names in TorchAo safetensors loading (#46325) by @agesf in [#46325]
* docs: fix typo in make_list_of_images docstring (#46469) by @ramkumar27072006 in [#46469]
* add XPU expectation for deepseek_ocr2 model tests (#46492) by @kaixuanliu in [#46492]
* Fix sapiens2 tests: add XPU device expectations (#46488) by @kaixuanliu in [#46488]
* Add vLLM smoke test to CI (#46383) by @hmellor in [#46383]
* extend deepseek v4 test to xpu (#46366) by @sywangyi in [#46366]
* Added cosmos3 model (#46146) by @MaciejBalaNV in [#46146]
* fbgemm_fp8:Keep the current device aligned with the input tensor (#46403) by @kaixuanliu in [#46403]
* [Modular] Add `no_inherit_decorators` and fixup wrong RoPE related inheritances  (#46440) by @Bissmella in [#46440]
* skip deepgemm test except cuda (#46090) by @jiqing-feng in [#46090]
* Fix/video classification pipeline video processor (#46256) by @J3r3myPerera in [#46256]
* ci: less flaky test_assisted_decoding_matches_greedy_search_1_same (#46445) by @ydshieh in [#46445]
* Fix flip_back graph break (#46344) by @guarin in [#46344]
* Add the other processors to auto-mappings (#46046) by @zucchini-nlp in [#46046]
* fix: compatibility with torch<=2.7 (#46393) by @andylin-hao in [#46393]
* fix: remove dynamic per-actor Slack ID lookup in ssh-runner workflow (#46327) by @ydshieh in [#46327]
* [docs] Romanian translation of `pipeline_tutorial.md`, `pipeline_gradio.md`, `pipeline_webserver.md` and `add_new_pipeline.md`. (#46388) by @filipinescu in [#46388]
* [docs] gemma4 typos (#46351) by @stevhliu in [#46351]
* [docs] padding-free training (#46333) by @stevhliu in [#46333]
* fix[vLLM x v5]: Default untied embeddings in AudioFlamingo3 and VibeVoice (#46400) by @harshaljanjani in [#46400]
* Fix deepspeed docker (#46108) by @SunMarc in [#46108]
* Fix conversion for clip models (#46406) by @zucchini-nlp in [#46406]
* ci: mention code quality failure in CI dashboard comment (#46415) by @ydshieh in [#46415]
* Fix noisy logging from image_processing module aliases issue - 46298 (#46350) by @skshmjn in [#46350]
* Raise tqdm minimum to 4.60 to match tqdm.contrib.logging import (#46397) by @n0gu-furiosa in [#46397]
* fix(gemma4_unified): conversion script and config bugs (#46398) by @douglas-reid in [#46398]
* [docs] remove sparsity from compressed-tensors (#46387) by @stevhliu in [#46387]
* [CB] Fix crashes when fork is not possible (#46251) by @remi-or in [#46251]
* Improve CI dashboard comment: rename and deduplicate (#46412) by @ydshieh in [#46412]
* Fix missing f-string prefixes in error messages (#46354) by @joaopedroassad in [#46354]
* Add workflow to post CI Grafana dashboard link to PR (#46410) by @ydshieh in [#46410]
* [docs] Romanian translation of `fast_tokenizers.md`, `custom_tokenizers.md`, `tokenizer_summary.md`, `image_processors.md` and `video_processors.md`. (#46356) by @filipinescu in [#46356]
* Clean up new models after release (#46092) by @zucchini-nlp in [#46092]

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @ArthurZucker
    * Add deepseek 3.2 exp (#41251)
* @gante
    * GPU go brr (#46540)
* @merveenoyan
    * revamp cv docs and fix rf-detr (#46219)
* @sgerrard
    * Quantization for small models (#46449)
* @MaciejBalaNV
    * Added cosmos3 model (#46146)
* @J3r3myPerera
    * Fix/video classification pipeline video processor (#46256)
* @filipinescu
    * [docs] Romanian translation of `pipeline_tutorial.md`, `pipeline_gradio.md`, `pipeline_webserver.md` and `add_new_pipeline.md`. (#46388)
    * [docs] Romanian translation of `fast_tokenizers.md`, `custom_tokenizers.md`, `tokenizer_summary.md`, `image_processors.md` and `video_processors.md`. (#46356)

---

## v5.10.2  (2026-06-04T18:43:06Z)

# Patch release v5.10.2
There was a big bug in the model conversion of models related to clip, this affected models like sam3 and others. Please make sure to update :pray: 

* Fix conversion for clip models by @zucchini-nlp (#46406)


**Full Changelog**: https://github.com/huggingface/transformers/compare/v5.10.1...v5.10.2

---

## v5.10.1  (2026-06-03T15:37:41Z)

# Release v5.10.1
v5.10.0 was yanked as we publish on a corrupted branch. Sorry everyone, this happens when we rush a release!!! 

## New Model additions

### Gemma4 unified+ Gemma4 MTP
<img width="2000" height="400" alt="image" src="https://github.com/user-attachments/assets/5e3ee940-f78d-4343-ac7a-889930800aa6" />

Gemma 4 12B Unified is an **encoder-free** multimodal model with pretrained and instruction-tuned variants. Unlike [standard Gemma 4](./gemma4), which uses dedicated encoder towers, Gemma 4 12B Unified projects raw inputs directly into the language model's embedding space through lightweight linear pipelines. This results in a simpler architecture while maintaining strong multimodal performance.

Key differences from standard Gemma 4:
- **No Vision Tower**: Raw pixel patches are projected directly into LM space via a `Dense + LayerNorm` pipeline with factorized 2D positional embeddings, replacing the vision encoder.
- **No Audio Tower**: Raw 16 kHz waveform samples are chunked into fixed-length frames and projected through a simple `RMSNorm → Linear` pipeline, replacing the mel spectrogram + Conformer encoder.
- **Shared Multimodal Pipeline**: Both vision and audio use the same `Gemma4UnifiedMultimodalEmbedder` (RMSNorm → Linear) for the final projection to text hidden space.

You can find the original Gemma 4 12B Unified checkpoints under the [Gemma 4](https://huggingface.co/collections/google/gemma-4) release.

* who needs encoders? (#46385) by @douglas-reid @sgerrard @vasqu @molbap

### Sapiens2

Sapiens2 is a family of high-resolution vision transformers pretrained on ~1 billion curated human images, designed for human-centric computer vision tasks including pose estimation, body-part segmentation, surface normal estimation, and pointmap estimation. The models scale from 0.4B to 5B parameters and train at native 1K resolution, with hierarchical 4K variants for extended spatial reasoning. Sapiens2 achieves substantial improvements over its predecessor with +4 mAP in pose estimation, +24.3 mIoU in body-part segmentation, and 45.6% error reduction in normal estimation.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/sapiens2) | [Paper](https://huggingface.co/papers/2604.21681)
* Add Sapiens2 Model (#45919) by @guarin in [#45919](https://github.com/huggingface/transformers/pull/45919)

### DeepSeek-OCR-2

DeepSeek-OCR-2 is an OCR-specialized vision-language model built on a distinctive architecture that combines a SAM ViT-B vision encoder with a Qwen2 hybrid attention encoder, connected through an MLP projector to a DeepSeek-V2 Mixture-of-Experts (MoE) language model. The model features a hybrid attention mechanism that applies bidirectional attention over image tokens and causal attention over query tokens, enabling efficient and accurate document understanding. It supports both plain OCR tasks and grounding capabilities with coordinate-aware output for document conversion to markdown format.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/deepseek_ocr2)
* Add Deepseek-OCR-2 model (#45075) by @thisisiron in [#45075](https://github.com/huggingface/transformers/pull/45075)

### Mellum

Mellum is a code-focused Mixture-of-Experts language model developed by JetBrains. It is derived from the Qwen3-MoE architecture with per-layer-type RoPE and interleaved sliding window attention. The model has 12B total parameters with 2.5B active parameters per token, using 64 routed experts with 8 activated per token across 28 layers.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/mellum)
* feat: Add support for JetBrains' `Mellum` v2 code generation model (#46112) by @shadeMe in [#46112](https://github.com/huggingface/transformers/pull/46112)



## Breaking changes

The Gemma4 vision pooler now casts inputs to float32 before scaling to prevent float16 overflow (inf saturation) with large checkpoints, which may cause minor numerical differences in outputs for users running Gemma-4 vision models in float16.
* 🚨 Fix float16 overflow in Gemma4 vision pooler (#46277) by @Bluear7878

Audio Language Models (ALMs) now have a dedicated base model class without a language modeling head, aligning them with the design of Vision Language Models (VLMs); users relying on the previous model class structure should update their code to use the new base model class where appropriate.
* 🚨 [ALM] Add base model without head (#45534) by @eustlb



## Parallelization

This release includes numerous bug fixes for model parallelism across multiple models (Gemma4, AltCLIP, ChineseClip, Blip-2, Whisper, Ovis2, Moshi) and parallel execution strategies, including fixes for tensor parallelism (TP), expert parallelism (EP), beam search under model parallel settings, and loss over-counting under TP/EP configurations. The continuous batching manager was also reworked for clearer control flow and improved TP race condition handling, and FSDP initialization via `from_pretrained` was introduced.


* Fix dsv4 dequant + tp/ep (#46378) by @IlyasMoutawwakil in [#46378]
* [CB] [Major] Rework manager to have clearer control flow + handle TP (#46070) by @remi-or in [#46070]
* fix series of bugs for model parallel beam search (#46280) by @kaixuanliu in [#46280]
* Fix model parallel issue for altclip model and ChineseClip model (#45487) by @kaixuanliu in [#45487]
* Model parallel fix (#46230) by @kaixuanliu in [#46230]
* [`Revert`] FSDP+Dtensor refactor related changes (#46246) by @vasqu in [#46246]
* Fix model parallel bugs for Gemma4 (#45817) by @kaixuanliu in [#45817]
* init FSDP through from_pretrained (#46102) by @3outeille in [#46102]
* fix model parallel device mismatch issue in `create_bidirectional_mask` (#46221) by @kaixuanliu in [#46221]
* Trainer.compute_loss: fix loss over-counting under TP and EP-as-TP (#45994) by @AmineDiro in [#45994]
* Fix caching allocator warmup byte estimation for EP model loading (#46149) by @sywangyi in [#46149]


## Cache

Fixed a regression in encoder-decoder cache initialization where the decoder config was incorrectly applied to the cross-attention cache, and resolved a `RuntimeError` caused by buffer size limits when warming up the cache on MPS devices. Additional test infrastructure improvements were made to support read-only cache environments used in CI.


* fix: cache warmup `RuntimeError` on mps (#46239) by @McPatate in [#46239]
* Make more tests work with read-only cache (#46299) by @ydshieh in [#46299]
* Update a test to avoid writing to the default xet cache (#46250) by @ydshieh in [#46250]
* Fix a regression in encoder-decoder generation cache initialization (#46111) by @kaixuanliu in [#46111]


## Quantization

Added support for DeepGEMM BF16, mixed FP8/FP4, and MegaMoE quantization via a grouped linear refactor, while fixing two bugs: an FP8 MoE reverse substring issue affecting DSv4 initialization, and a BitsAndBytes 4-bit/8-bit quantization bug that silently dropped chunked tensors from one-to-many weight converters.


* DeepGEMM BF16 + mixed FP8/FP4 + MegaMoE + refactor (#45634) by @IlyasMoutawwakil in [#45634]
* Fix fp8 moe reverse substring (#46265) by @ArthurZucker in [#46265]
* Fix bnb 4bit/8bit quantization drop chunked tensors bug (#46210) by @kaixuanliu in [#46210]


## Bugfixes and improvements

* Fix wrong changes produced by style/repo. check bot (#46371) by @ydshieh in [#46371]
* Fix path traversal when saving Bark voice preset embeddings (#46237) by @LinZiyuu in [#46237]
* Pass library_name/version to Hub calls via a shared HfApi (#46318) by @Wauplin in [#46318]
* docs: update ACL Anthology URL in CITATION.cff (#46352) by @irfaan101 in [#46352]
* [docs] contributing (#45465) by @stevhliu in [#45465]
* [docs] Romanian translation of `contributing.md`, `modular_transformers.md`, `multimodal_processing.md`, `add_vision_processing_components.md`, `add_audio_processing_components.md`, `modeling_rules.md`, `model_output_tracing.md`, `auto_docstring.md`, `testing.md`, `pr_checks.md` and `add_new_model.md` . (#46345) by @filipinescu in [#46345]
* [docs] xpu continuous batching (#46334) by @stevhliu in [#46334]
* Fix incorrect attribute mapping relationships in GLM MoE DSA Config (#46338) by @Dovis01 in [#46338]
* Fix grammar typos in Whisper documentation (#46336) by @calliec-1223 in [#46336]
* [docs] update num_items_in_batch for causal LMs (#46335) by @stevhliu in [#46335]
* Update compressed tensors minimum version (#46342) by @SunMarc in [#46342]
* Fix _is_package_available reporting available without a version (#46125) by @blipbyte in [#46125]
* remove sec (#46346) by @ydshieh in [#46346]
* fix: include transitive relative imports when loading from local directory (#46022) by @trducng in [#46022]
* perf(feature_extraction_sequence): skip re-splitting already-batched numpy arrays in pad() (#46329) by @Anai-Guo in [#46329]
* [Zamba] Support attn_implementation dispatch (#46317) by @YangKai0616 in [#46317]
* Fix TestAppRoutes test failures caused by deprecated asyncio.get_event_loop() on Python 3.10+ (#46340) by @ydshieh in [#46340]
* [Qwen3VL] Fix video token placeholder: use self.video_token instead of hardcoded "<|placeholder|>" (#46296) by @kpal002 in [#46296]
* chore(linter): fixes for rule 16 (#46023) by @tarekziade in [#46023]
* [docs] Romanian translation of  `weightconverter.md`,  `models.md`,  `custom_models.md`,  `monkey_patching.md`,  `fusion_mapping.md`, `how_to_hack_models.md`, `model_sharing.md` and `serialization.md`. (#46309) by @filipinescu in [#46309]
* Normalize CUDA OOM errors when comparing commit failures in check_bad_commit (#46322) by @ydshieh in [#46322]
* Fix unhandled exception noise from background safetensors conversion thread (#45752) by @dhruv7477 in [#45752]
* Add Expectations for pipeline token classification tests (#46151) by @kaixuanliu in [#46151]
* [docs] fix auto-add release dates (#46283) by @zucchini-nlp in [#46283]
* Separate pip command syntax for notebook and CLI tabs in Quickstart (#46243) by @pvelayudhan in [#46243]
* Romanian translation of README.md, index.md, installation.md, _config.py and quicktour.md. (#46166) by @filipinescu in [#46166]
* Fall back to flat kwarg when modality dict is passed without it (#46195) by @Ace3Z in [#46195]
* Fix load_adapter OOM caused by full-model warmup sizing (#46145) by @Yooniel in [#46145]
* Replace assert with raise ImportError for optuna/ray dependency checks (#46263) by @SebTardif in [#46263]
* chore(linter): respect TRF017 modeling rule (#46260) by @tarekziade in [#46260]
* Delete dead code in qwen-vl series (#45827) by @zucchini-nlp in [#45827]
* qa: fix ty caching and align CI with local run (#46278) by @tarekziade in [#46278]
* Guard DeviceMesh import in continuous batching (#46205) by @danyalahmed1995 in [#46205]
* Processor compatibility with vLLM  (#46258) by @zucchini-nlp in [#46258]
* Fix PR CI workflow cancellation condition (#46276) by @ydshieh in [#46276]
* [fix] toctree (#46106) by @stevhliu in [#46106]
* add more generic support for distributed trainer tests (#46109) by @kaixuanliu in [#46109]
* add XPU Expectations for florence2 and lfm2_vl model test (#46275) by @kaixuanliu in [#46275]
* Fix `StaticCache` building an empty layer list when `num_kv_shared_layers == 0` (#46235) by @tengomucho in [#46235]
* Fix inverted assertion in remove_handler (#46227) by @SebTardif in [#46227]
* [ShieldGemma2] Support attn_implementation dispatch (#46069) by @YangKai0616 in [#46069]
* [Gemma4] Replace one-hot matmul with F.embedding in position embeddings (#46176) by @Sriniketh24 in [#46176]
* fix: kosmos2.5: properly expand embeddings table (#45835) by @nunq in [#45835]
* find pytest launch error in torch 2.13.0.dev20260526 (#46252) by @sywangyi in [#46252]
* [Test][Kosmos2.5] Add XPU expectations for integration tests (#46135) by @YangKai0616 in [#46135]
* Support FA2 flash_attn_with_kvcache for XPU continuous batching (#46028) by @YangKai0616 in [#46028]
* [`Configs`] Fix layer type validation to include its mlp counterpart (#46220) by @vasqu in [#46220]
* Fix `num_items_in_batch` over-counting for causal LM losses (#46204) by @qgallouedec in [#46204]
* RF-DETR doc fixes (#46244) by @merveenoyan in [#46244]
* Use `main` instead of commit SHA for now (#46241) by @ydshieh in [#46241]
* Enable push event (to main) for PR CI workflow (#46240) by @ydshieh in [#46240]
* fix(hrm_text): Add XPU Expectations for tests (#46214) by @kaixuanliu in [#46214]
* [deepseek_v4] keep hc_head / sinks / position_bias in fp32 (#46198) by @ArthurZucker in [#46198]
* Fix FSDP2 and distributed checkpointing imports for older PyTorch versions (#46141) by @ryota-komatsu in [#46141]
* Fix Gemma4 Array Mask Indexing (#46203) by @petecao in [#46203]
* utils: handle flash_attn missing from importlib packages_distributions without crashing (#45524) by @SAY-5 in [#45524]
* [AMD CI] revert AMD mi325 hf-workflows ref from SHA back to @main (#46213) by @Abdennacer-Badaoui in [#46213]
* [GLM-4.6V] Update with GLM-GA Processor (#46184) by @zRzRzRzRzRzRzR in [#46184]
* update xpu expectation for falcon mamba (#46086) by @sywangyi in [#46086]
* chore: enable Dependabot weekly GitHub Actions bumps (#46157) by @hf-dependantbot-rollout[bot] in [#46157]
* Fix Gemma4 use_bidirectional_attention="all" mask behavior (#46079) by @oliverholworthy in [#46079]
* Fix loading with only 1 device or distributed config (#46197) by @Cyrilvallez in [#46197]
* Fix TypeError on list-typed ignore_keys_at_rope_validation in RoPE config (#46142) by @Charly21r in [#46142]
* Support XPU autocast dtype fallback for FlashAttention (#46199) by @YangKai0616 in [#46199]
* Fix path traversal when saving named chat templates (#46191) by @LinZiyuu in [#46191]
* Fix is_last off-by-one in MaskGenerationPipeline for partial batches (#46136) by @J3r3myPerera in [#46136]
* Fix wrong variable in check_model_type isinstance check (#46080) by @SebTardif in [#46080]
* Enable passing kwargs through RoFormer models (#46171) by @ir2718 in [#46171]
* Update cohere2_moe tp_plan (#46189) by @Cyrilvallez in [#46189]
* Update release tool (#46193) by @Cyrilvallez in [#46193]
* [loading] Fix base_model_prefix issues in conversions (#46067) by @Cyrilvallez in [#46067]
* Bump dev version (#46188) by @Cyrilvallez in [#46188]
* Update self-comment-ci (#46137) by @guarin in [#46137]

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @filipinescu
    * [docs] Romanian translation of `contributing.md`, `modular_transformers.md`, `multimodal_processing.md`, `add_vision_processing_components.md`, `add_audio_processing_components.md`, `modeling_rules.md`, `model_output_tracing.md`, `auto_docstring.md`, `testing.md`, `pr_checks.md` and `add_new_model.md` . (#46345)
    * [docs] Romanian translation of  `weightconverter.md`,  `models.md`,  `custom_models.md`,  `monkey_patching.md`,  `fusion_mapping.md`, `how_to_hack_models.md`, `model_sharing.md` and `serialization.md`. (#46309)
    * Romanian translation of README.md, index.md, installation.md, _config.py and quicktour.md. (#46166)
* @remi-or
    * [CB] [Major] Rework manager to have clearer control flow + handle TP (#46070)
* @thisisiron
    * Add Deepseek-OCR-2 model (#45075)
* @kaixuanliu
    * Add Expectations for pipeline token classification tests (#46151)
    * fix series of bugs for model parallel beam search (#46280)
    * add more generic support for distributed trainer tests (#46109)
    * add XPU Expectations for florence2 and lfm2_vl model test (#46275)
    * Fix model parallel issue for altclip model and ChineseClip model (#45487)
    * Model parallel fix (#46230)
    * fix(hrm_text): Add XPU Expectations for tests (#46214)
    * Fix model parallel bugs for Gemma4 (#45817)
    * Fix bnb 4bit/8bit quantization drop chunked tensors bug (#46210)
    * fix model parallel device mismatch issue in `create_bidirectional_mask` (#46221)
    * Fix a regression in encoder-decoder generation cache initialization (#46111)
* @shadeMe
    * feat: Add support for JetBrains' `Mellum` v2 code generation model (#46112)
* @vasqu
    * [`Revert`] FSDP+Dtensor refactor related changes (#46246)
    * [`Configs`] Fix layer type validation to include its mlp counterpart (#46220)
* @zRzRzRzRzRzRzR
    * [GLM-4.6V] Update with GLM-GA Processor (#46184)
* @eustlb
    * 🚨 [ALM] Add base model without head (#45534)

---

## v5.9.0  (2026-05-20T14:12:54Z)

# Release v5.9.0


## New Model additions

### Cohere2Moe

Command A+ is a Mixture-of-Experts (MoE) language model from Cohere that features a hybrid attention pattern combining sliding window and full attention layers. The model incorporates both shared and routed experts and supports a very large context window for processing extensive text sequences.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/cohere2_moe)
* Add new cohere2_moe model (#46115) by @Cyrilvallez in [#46115](https://github.com/huggingface/transformers/pull/46115)

### Parakeet tdt (#44171)

* Parakeet tdt (#44171) by @lmaksym

### HRM-Text

HRM-Text is an improved autoregressive language-modeling variant of the Hierarchical Reasoning Model (HRM) that uses a hierarchical recurrent forward pass with two transformer stacks - one for slow, abstract planning (H) and one for fast, detailed computation (L) - reused inside a nested recurrence. It features PrefixLM attention where instruction tokens attend bidirectionally while response tokens attend causally, per-head sigmoid output gates, and parameterless RMSNorm. The model is designed as a base language model without instruction tuning or chat templates.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/hrm_text) | [Paper](https://huggingface.co/papers/2506.21734)
* Add hrm text (#46025) by @abcd1927 in [#46025](https://github.com/huggingface/transformers/pull/46025)



## Breaking changes

The `text_embeds` input for SAM3, EdgeTAM, and SAM3-Lite-Text models now expects full text embeddings instead of just pooler outputs, aligning with other models in the library — users must update their inputs accordingly.
* 🚨Fix memory leaks caused by lru decorators in vision models (#45922) by @yonigozlan



## Audio

Audio support was expanded with the addition of AudioFlamingoNext model checkpoints and improved compilability of audio/vision encoders via standalone pure functions. Additional improvements include better error messaging when loading audio from video files and new documentation for audio/video processors.


* user friendly error when loading audio from video (#45221) by @eustlb in [#45221]
* [docs] adding audio/video processors (#45795) by @stevhliu in [#45795]
* Support Audio Flamingo Next checkpoints (#44830) by @lashahub in [#44830]
* Extract dynamic vision/audio tensors into standalone pure functions (#45396) by @IlyasMoutawwakil in [#45396]


## Generation

Fixed generation issues including `inputs_embeds` and `per_layer_inputs` handling for Gemma4, an `AttributeError` in RAG's `generate()` caused by missing config fields, and flaky VLM generation tests by blocking special image tokens during sampling.


* Fix Gemma4 generation from inputs_embeds and per_layer_inputs (#46049) by @Cyrilvallez in [#46049]
* Fix AttributeError in RAG generate() for missing config fields (#46035) by @Sriniketh24 in [#46035]
* Block image_start/end_token_id in generation test sampling (#45914) by @Rocketknight1 in [#45914]


## Bugfixes and improvements

* Remove mask visualization tool from `masking_utils.py` (#46066) by @Cyrilvallez in [#46066]
* fix: owned_by field in GET /v1/models returns list instead of string (#46006) by @nileshpatil6 in [#46006]
* [CB] Remove OpenTelemetry (#45984) by @remi-or in [#45984]
* docs(readme): use canonical `huggingface.co` domain in prose links (#46042) by @kiwigitops in [#46042]
* Fix remaining RAG doc examples that crash on current transformers (#46044) by @Sriniketh24 in [#46044]
* Init the actual tensor, not a copy (#46030) by @Rocketknight1 in [#46030]
* docs: sync legacy ACL anthology URLs and update metrics across i18n READMEs (#46027) by @irfaan101 in [#46027]
* [MultimodalLM] add language_model to the get/set_input_embeddings logic (#46029) by @eustlb in [#46029]
* [`HRM Text`] Add integration tests (#46033) by @vasqu in [#46033]
* hy_v3: add XPU expectations (#45858) by @kaixuanliu in [#45858]
* exaone4_5: add XPU expectations (#45890) by @kaixuanliu in [#45890]
* hyperclovax: add XPU Expectations for CI test (#45926) by @kaixuanliu in [#45926]
* chore(ci): remove dead env vars from circleci-failure-summary-comment.yml (#45972) by @XciD in [#45972]
* [CB] [Major] Add tensor paralellism (#45821) by @remi-or in [#45821]
* docs: update models architecture count and sync ACL anthology URLs (#46001) by @irfaan101 in [#46001]
* bugfix(ci): avoid E2BIG in pr_slow_ci_suggestion  (#45983) by @tarekziade in [#45983]
* RFDetr - use correct Roboflow org for release (#45946) by @sbucaille in [#45946]
* docs: Fix formatting issues in weightconverter.md (#45988) by @ArjunSrivastava1 in [#45988]
* Fix colqwen2 test (#45981) by @IlyasMoutawwakil in [#45981]
* Fix M-RoPE device mismatch in Qwen3VL family under FSDP2 CPU offload (#45861) by @jamesbraza in [#45861]
* [docs] chat template prefill (#45947) by @stevhliu in [#45947]
* [docs] decode fast path (#45899) by @stevhliu in [#45899]
* fix: restore `_attn_implementation `and fix request offset in `generate_batch()` (#45943) by @sergiopaniego in [#45943]
* Expose `per_layer_inputs` for every Gemma4 variants (#45927) by @Cyrilvallez in [#45927]
* chore: update benchmark_v2.yml (#45966) by @hf-security-analysis[bot] in [#45966]
* fix(ci): set persist-credentials: false on actions/checkout and close remaining template injection findings (#45964) by @XciD in [#45964]
* chore(ci): set default workflow permissions to contents: read (#45961) by @XciD in [#45961]
* fix(ci): remove template injection on pull_request_target workflows (#45956) by @XciD in [#45956]
* chore(ci): pin all GitHub Actions and reusable workflows by SHA (#45955) by @XciD in [#45955]
* [docs] ALMModelTest (#45900) by @stevhliu in [#45900]
* Enhance apply_chat_template to support custom field prefilling (reasoning_content, thinking, etc.) (#45896) by @Mamiglia in [#45896]
* BUGFIX: Support hubert models that don't have conv_pos_batch_norm configured (#45921) by @igordertigor in [#45921]
* Revert 45777 (#45942) by @Rocketknight1 in [#45942]
* pass the otel secrets (#45933) by @tarekziade in [#45933]
* Add initial torch_tpu backend support (#45918) by @tengomucho in [#45918]
* [CB] Hide activation footprint by using the CUDA graph pool (#45911) by @remi-or in [#45911]
* Require input_ids for repetition penalty (#45389) by @ruben-aghayan in [#45389]
* Fix undefined 'input' variable (#45895) by @fullyz in [#45895]
* Fix post processing RF-DETR (#46041) by @yonigozlan (direct commit on v5.9.0)
* [loading] Free up tensors faster inside ConversionOps (#46110) by @Cyrilvallez (direct commit on v5.9.0)
* Add new cohere2_moe model (#46115) by @Cyrilvallez (direct commit on v5.9.0)
* Fix cohere2 tp_plan for release by @Cyrilvallez (direct commit on v5.9.0)
* Release v5.9.0 by @Cyrilvallez (direct commit on v5.9.0)

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @lmaksym
    * Parakeet tdt (#44171)
* @eustlb
    * user friendly error when loading audio from video (#45221)
    * [MultimodalLM] add language_model to the get/set_input_embeddings logic (#46029)
* @remi-or
    * [CB] Remove OpenTelemetry (#45984)
    * [CB] [Major] Add tensor paralellism (#45821)
    * [CB] Hide activation footprint by using the CUDA graph pool (#45911)
* @abcd1927
    * Add hrm text (#46025)

---

## v5.8.1  (2026-05-13T03:21:23Z)

# Patch release v5.8.1 
This release is mainly to fix the Deepseek V4 integration!!! 

<img width="714" height="774" alt="image" src="https://github.com/user-attachments/assets/0d85e891-a0ff-436e-a9d4-b6633096f2b5" />


* [fix] Add fatal_error to ContinuousBatchingManager so the serving... by @qgallouedec, @remi-or
* Fix WeightConverter regex incorrectly matching shared_experts as experts by @silencelamb, @claude
* Fix deepseek v4 by @ArthurZucker (#45892)
* Deepseek v4 csa mask collapse by @ArthurZucker, @Sawyer117 (#45928)

---

## v5.8.0  (2026-05-05T16:52:21Z)

# Release v5.8.0


## New Model additions

### DeepSeek-V4

<img width="6604" height="3574" alt="image" src="https://github.com/user-attachments/assets/4c0fdb29-f770-463c-a97b-d24438896a4c" />

DeepSeek-V4 is the next-generation MoE (Mixture of Experts) language model from DeepSeek that introduces several architectural innovations over DeepSeek-V3. The architecture replaces Multi-head Latent Attention (MLA) with a hybrid local + long-range attention design, swaps residual connections for Manifold-Constrained Hyper-Connections (mHC), and bootstraps the first few MoE layers with a static token-id → expert-id hash table. This implementation covers DeepSeek-V4-Flash, DeepSeek-V4-Pro, and their -Base pretrained variants, which share the same architecture but differ in width, depth, expert count and weights.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/deepseek_v4) | [Paper](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash/blob/main/DeepSeek_V4.pdf)
* Add DeepSeek V4 (#45643) by @ArthurZucker in [#45643](https://github.com/huggingface/transformers/pull/45643)

### Gemma 4 Assistant

<img width="2000" height="400" alt="image" src="https://github.com/user-attachments/assets/02c79b0b-a172-4495-b09d-a6a4b625ee66" />

Gemma 4 Assistant is a small, text-only model that enables speculative decoding for Gemma 4 models using the Multi-Token Prediction (MTP) method and associated candidate generator. The model shares the same Gemma4TextModel backbone as other Gemma 4 models but uses KV sharing throughout the entire model, allowing it to reuse the KV cache populated by the target model and skip the pre-fill phase entirely. This architecture includes cross-attention to make the most of the target model's context, allowing the assistant to accurately predict more drafted tokens per drafting round.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/gemma4_assistant)
* First model (#45788) by @SindhuRaghuram97 in [#45788](https://github.com/huggingface/transformers/pull/45788)

### GraniteSpeechPlus

<img width="1310" height="930" alt="image" src="https://github.com/user-attachments/assets/94fc3730-742c-4b9e-ab6a-ed2e5c75d0bf" />

Granite Speech Plus is a variant of Granite Speech that enhances the projector by consuming the concatenation of the encoder's final hidden states with an arbitrary subset of its intermediate hidden states along the feature dimension. It is a multimodal speech-to-text model that can transcribe audio, provide speaker annotation and word level timestamps by responding to text prompts. The model inherits the same architecture components as Granite Speech including the speech encoder, query transformer projector, language model, and optional LoRA adapter.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/granite_speech_plus)
* Support for a new Granite-Speech-Plus model (#45695) by @zvik in [#45695](https://github.com/huggingface/transformers/pull/45695)

### Granite4Vision

Granite Vision 4.1 is a vision-language model from IBM Research designed for enterprise-grade document data extraction. It specializes in chart extraction (Chart2CSV, Chart2Summary, Chart2Code), table extraction (JSON, HTML, OTSL), and semantic key-value pair extraction. The model builds on LLaVA-NeXT with architectural innovations including SigLIP2 Vision Encoder, Window Q-Former Projectors, and DeepStack Feature Injection with 8 vision-to-LLM injection points.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/granite4_vision)
* Add Granite 4.1 Vision (granite4_vision) (#45597) by @artem-spector in [#45597](https://github.com/huggingface/transformers/pull/45597)

### EXAONE-4.5

<img width="3840" height="2160" alt="image" src="https://github.com/user-attachments/assets/55eb732d-f9da-4f97-8226-2cd3f6476ca0" />

EXAONE 4.5 is the first open-weight vision language model developed by LG AI Research, integrating a dedicated visual encoder into the existing EXAONE 4.0 framework to expand multimodal capabilities. The model features 33 billion parameters in total, including 1.2 billion parameters from the vision encoder, and achieves competitive performance in general benchmarks while outperforming similar-sized models in document understanding and Korean contextual reasoning. It builds on EXAONE 4.0 with key enhancements including an expanded vocabulary of 153,600 tokens, support for up to 256K token context windows, and a Multi-Token Prediction (MTP) mechanism.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/exaone4_5) | [Paper](https://huggingface.co/papers/2604.08644) | [Blog Post](https://www.lgresearch.ai/blog/view?seq=641)
* Add EXAONE 4.5 implementations (#45471) by @nuxlear in [#45471](https://github.com/huggingface/transformers/pull/45471)

### PP-FormulaNet

PP-FormulaNet-L and PP-FormulaNet_plus-L are lightweight models designed for table structure recognition, focusing on accurately recognizing table structures in documents and natural scenes. The models are part of the SLANet series and can be used for image-to-text tasks, specifically for detecting and processing mathematical formulas and table structures from images.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/pp_formulanet)
* [Model] Add PP-FormulaNet Model Support (#45626) by @zhang-prog in [#45626](https://github.com/huggingface/transformers/pull/45626)



## Breaking changes

Apex integration has been removed from the library (including RMSNorm usage in T5 and related models), so users relying on Apex for mixed precision or fused ops should migrate to PyTorch's native equivalents instead.
* 🚨 Get rid of most Apex references (#45723) by @Rocketknight1



## Tokenization

Fixed tokenizer mapping issues for DeepSeek R1 distilled (Qwen2) and DeepSeek OCR models, and resolved a significant performance regression in `PreTrainedTokenizer.convert_ids_to_tokens` where `skip_special_tokens=True` was rebuilding the special token set on every iteration, resulting in a ~300x speedup for that code path.


* deepseek r1 distilled tokenizer fix for qwen2 mapping (#45741) by @itazap in [#45741]
* DeepSeek OCR specifies an incorrect tokenizer class on the Hub (#45739) by @hmellor in [#45739]
* PythonBackend slow tokenizer convert_ids_to_tokens fix (#45728) by @i3hz in [#45728]


## Bugfixes and improvements

* fix: correct spelling in continuous_api docstring (#45749) by @Dhruv908615 in [#45749]
* Fix link to modular transformers documentation (#45746) by @SangbumChoi in [#45746]
* Gemma4: fix failed test cases (#45568) by @kaixuanliu in [#45568]
* Fix CI: Allow more artifacts to be download in CI (#45785) by @ydshieh in [#45785]
* Add `concurrency` to `PR CI` workflow file (`pr-ci-caller.yml`) (#45786) by @ydshieh in [#45786]
* Reorder decorators for autodoc and dataclass (#45702) by @zucchini-nlp in [#45702]
* Unwrap `text_config` in `AutoModelFor*.from_config` (#45770) by @jamesbraza in [#45770]
* fix: Added Mps support in float fallback backends list  (#45687) by @rigen1048 in [#45687]
* Github Actions PR CI (caller) (#45476) by @ydshieh in [#45476]
* make sure we call check_auto in CI (#45775) by @tarekziade in [#45775]
* Fix auto mapping script (#45774) by @Cyrilvallez in [#45774]
* [MINISTRAL3] Fix conversion script yarn's apply_scale support. (#45744) by @juliendenize in [#45744]
* [nemotron_h] respect _no_reinit flag on dt_bias and out_proj.weight (#45591) by @vai-minzhou in [#45591]
* fix(utils): Resolve backbone utils test regressions (#45594) by @harshaljanjani in [#45594]
* [CB] Better overall script and decode bucketting (#45653) by @remi-or in [#45653]
* [docs] model testing (#45152) by @stevhliu in [#45152]
* update dev (#45726) by @vasqu in [#45726]
* Doc translate to Persian(farsi)  (#45664) by @zeoses in [#45664]
* [`OAI Privacy Filter`] Add integration test (#45725) by @vasqu in [#45725]
* Speedup Qwen2VLImageProcessor (#45719) by @lgeiger in [#45719]
* Remove dead beam-search dummies from dummy_pt_objects.py (#45722) by @jw9603 in [#45722]
* chore(typing): add ty type checking for 10 utility files (#45703) by @moonbogi in [#45703]
* Llama3 video fix (#45040) by @sywangyi in [#45040]
* Fix custom-module copies inheriting read-only permissions (#45686) by @nurpax in [#45686]
* Python code in model docs (#45608) by @zucchini-nlp in [#45608]
* fix failed test cases for blt model (#45596) by @kaixuanliu in [#45596]
* chore(typing): add ty type checking for 3 pipeline files (#45667) by @moonbogi in [#45667]

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @artem-spector
    * Add Granite 4.1 Vision (granite4_vision) (#45597)
* @SindhuRaghuram97
    * First model (#45788)
* @nuxlear
    * Add EXAONE 4.5 implementations (#45471)
* @ArthurZucker
    * Add DeepSeek V4 (#45643)
* @remi-or
    * [CB] Better overall script and decode bucketting (#45653)
* @zhang-prog
    * [Model] Add PP-FormulaNet Model Support (#45626)
* @zvik
    * Support for a new Granite-Speech-Plus model (#45695)

---

## v5.7.0  (2026-04-28T18:32:50Z)

# Release v5.7.0


## New Model additions

### Laguna

<img width="699" height="176" alt="image" src="https://github.com/user-attachments/assets/d3bae269-bea7-4ddf-a53f-d4718befdb17" />

Laguna is Poolside's mixture-of-experts language model family that extends standard SwiGLU MoE transformers with two key innovations. It features per-layer head counts allowing different decoder layers to have different query-head counts while sharing the same KV cache shape, and implements a sigmoid MoE router with auxiliary-loss-free load balancing that uses element-wise sigmoid of gate logits plus learned per-expert bias for router scoring.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/laguna)
* Laguna XS.2 implementation (#45673) by @joerowell in [#45673](https://github.com/huggingface/transformers/pull/45673)

### DEIMv2

<img width="2874" height="908" alt="image" src="https://github.com/user-attachments/assets/fc8c59fe-f964-42ce-ae8e-c7fcace9beb7" />

DEIMv2 (DETR with Improved Matching v2) is a real-time object detection model that extends DEIM with DINOv3 features and spans eight model sizes from X to Atto for diverse deployment scenarios. It uses a Spatial Tuning Adapter (STA) for larger variants to convert DINOv3's single-scale output into multi-scale features, while ultra-lightweight models employ pruned HGNetv2 backbones. The unified design achieves superior performance-cost trade-offs, with DEIMv2-X reaching 57.8 AP with only 50.3M parameters and DEIMv2-S being the first sub-10M model to exceed 50 AP on COCO.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/deimv2) | [Paper](https://huggingface.co/papers/2509.20787)
* model: Add DEIMv2 to Transformers (#44339) by @harshaljanjani in [#44339](https://github.com/huggingface/transformers/pull/44339)



## Attention

Several attention-related bugs were fixed across multiple models, including a cross-attention cache type error in T5Gemma2 for long inputs, incorrect cached forward behavior in Qwen3.5's gated-delta-net linear attention, and a crash in GraniteMoeHybrid when no Mamba layers are present. Attention function dispatch was also updated to align with the latest model implementations.


* Fix cross-attention cache layer type for T5Gemma2 long inputs (#45540) by @Beichen-Ma in [#45540]
* [Qwen3.5] Fix GDN linear attention multi-token cached forward (#45513) by @kashif in [#45513]
* Fix GraniteMoeHybrid _update_mamba_mask crash on attention-only models (#45514) by @tianhaocui in [#45514]
* Align latest model attention function dispatch (#45598) by @Cyrilvallez in [#45598]



## Tokenizers

There was a bug in AutoTokenizer that caused the wrong tokenizer class to be initialized. This caused regressions in models like DeepSeek R1. 

* change got reverted (#45680) by @itazap in [#45680]


## Generation

Continuous batching generation received several fixes and improvements, including correcting KV deduplication and memory estimation for long sequences (16K+), and removing misleading warnings about `num_return_sequences` and other unsupported features that were incorrectly firing even when functionality worked correctly. Documentation for per-request sampling parameters was also added.


* generate: drop stale num_return_sequences warning on continuous batching path (#45582) by @joaquinhuigomez in [#45582]
* Remove unnecessary generate warnings (#45619) by @Cyrilvallez in [#45619]
* [CB] Changes for long generation (#45530) by @remi-or in [#45530]
* [docs] per-request sampling params (#45553) by @stevhliu in [#45553]


## Kernels

Improved kernel support by fixing configuration reading and error handling for FP8 checkpoints (e.g., Qwen3.5-35B-A3B-FP8), enabling custom expert kernels registered from the HF Hub to be properly loaded, and resolving an incompatibility that prevented Gemma3n and Gemma4 from using the rotary kernel.


* Fix configuration reading and error handling for kernels (#45610) by @hmellor in [#45610]
* Allow for registered experts from kernels hub (#45577) by @winglian in [#45577]
* Gemma3n and Gemma4 cannot use rotary kernel (#45564) by @Cyrilvallez in [#45564]


## Bugfixes and improvements

* fixing more typos (#45689) by @vasqu in [#45689]
* [docs] cb memory management (#45587) by @stevhliu in [#45587]
* [docs] cpu offloading (#45660) by @stevhliu in [#45660]
* docs(README_zh-hans): clarify conditions for not using Transformers (#45688) by @GuaiZai233 in [#45688]
* fix padding side issue for fast_vlm tests (#45592) by @kaixuanliu in [#45592]
* Fix `x_clip`: 8 failed test cases (#45394) by @kaixuanliu in [#45394]
* zero_shot_object_detection ValueError fix for python 3.13 (#45669) by @AnkitAhlawat7742 in [#45669]
* Fix pageable H2D copies in Gated DeltaNet PyTorch fallback (#45665) by @ruixiang63 in [#45665]
* Fix UnboundLocalError in shard_and_distribute_module for replicated parameters (#45675) by @Abdennacer-Badaoui in [#45675]
* [MistralCommonBackend] Soften validation mode and apply_chat_template arguments check (#45628) by @juliendenize in [#45628]
* Fix `NameError: PeftConfigLike` triggered by `PreTrainedModel.__init_subclass__` (#45658) by @qgallouedec in [#45658]
* chore(typing): added modeling_utils to ty (#45425) by @tarekziade in [#45425]
* [gemma4] infer from config instead of hardcoding (#45606) by @eustlb in [#45606]
* Update quants tests  (#45480) by @SunMarc in [#45480]
* 🔴🔴🔴 fix: skip `clean_up_tokenization` for BPE tokenizers in `PreTrainedTokenizerFast` (#44915) by @maxsloef-goodfire in [#44915]
* Fix colmodernvbert tests (#45652) by @Cyrilvallez in [#45652]
* [CB] [Major] Add CPU request offloading (#45184) by @remi-or in [#45184]
* Fix peft constructors (#45622) by @Cyrilvallez in [#45622]
* chore: speedup modular converter (~30%) (#45046) by @tarekziade in [#45046]
* Fix whisper return language (#42227) by @FredHaa in [#42227]
* Add `supports_gradient_checkpointing` to `NemotronHPreTrainedModel` (#45625) by @sergiopaniego in [#45625]
* Raise clear error for `problem_type="single_label_classification"` with `num_labels=1` (#45611) by @gaurav0107 in [#45611]
* CircleCI with torch 2.11 (#45633) by @ydshieh in [#45633]
* chore: bump doc-builder SHA for main doc build workflow (#45631) by @rtrompier in [#45631]
* Allow more artifacts to be download in CI (#45629) by @ydshieh in [#45629]
* chore(qa): split pipeline and add type checking (#45432) by @tarekziade in [#45432]
* Skip failing offloading tests (#45624) by @Cyrilvallez in [#45624]
* fix: compute auxiliary losses when denoising is disabled in D-FINE (#45601) by @Abineshabee in [#45601]
* qa: bumped mlinter and allow local override (#45585) by @tarekziade in [#45585]
* Processing Utils: continue when content is a string (#45605) by @RyanMullins in [#45605]
* SonicMoe (#45433) by @IlyasMoutawwakil in [#45433]
* fix transformers + torchao nvfp4 serialization (#45573) by @vkuzo in [#45573]
* [AMD CI] Fix expectations for Gemma3n (#45602) by @Abdennacer-Badaoui in [#45602]
* [docs] multi-turn tool calling (#45554) by @stevhliu in [#45554]
* Fix `AttributeError` on `s_aux=None` in `flash_attention_forward` (#45589) by @jamesbraza in [#45589]
* do not index past decoded chars with special tokens (#45435) by @itazap in [#45435]
* Update dev version (#45583) by @vasqu in [#45583]
* Update torchao usage for XPU and CPU (#45560) by @jiqing-feng in [#45560]

## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @vasqu
    * fixing more typos (#45689)
    * Update dev version (#45583)
* @joerowell
    * Laguna XS.2 implementation (#45673)
* @tarekziade
    * chore(typing): added modeling_utils to ty (#45425)
    * chore: speedup modular converter (~30%) (#45046)
    * chore(qa): split pipeline and add type checking (#45432)
    * qa: bumped mlinter and allow local override (#45585)
* @harshaljanjani
    * model: Add DEIMv2 to Transformers (#44339)
* @remi-or
    * [CB] [Major] Add CPU request offloading (#45184)
    * [CB] Changes for long generation (#45530)

---

## v5.6.2  (2026-04-23T18:36:03Z)

# Patch release v5.6.2

Qwen 3.5 and 3.6 MoE (text-only) were broken when using with FP8. It should now work again with this :saluting_face: 

* Fix configuration reading and error handling for kernels (https://github.com/huggingface/transformers/pull/45610) by @hmellor 

**Full Changelog**: https://github.com/huggingface/transformers/compare/v5.6.1...v5.6.2

---

## v5.6.1  (2026-04-23T08:20:03Z)

# Patch release v5.6.1

Flash attention path was broken! Sorry everyone for this one 🤗 

* Fix AttributeError on s_aux=None in flash_attention_forward (https://github.com/huggingface/transformers/pull/45589) by @jamesbraza

---

## v5.6.0  (2026-04-22T15:52:30Z)

# Release v5.6.0


## New Model additions

### OpenAI Privacy Filter

OpenAI Privacy Filter is a bidirectional token-classification model for personally identifiable information (PII) detection and masking in text. It is intended for high-throughput data sanitization workflows where teams need a model that they can run on-premises that is fast, context-aware, and tunable. The model labels an input sequence in a single forward pass, then decodes coherent spans with a constrained Viterbi procedure, predicting probability distributions over 8 privacy-related output categories for each input token.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/openai_privacy_filter)
* [`Privacy Filter`] Add model (#45580) by @vasqu in [#45580](https://github.com/huggingface/transformers/pull/45580)

### QianfanOCR

Qianfan-OCR is a 4B-parameter end-to-end document intelligence model developed by Baidu that performs direct image-to-text conversion without traditional multi-stage OCR pipelines. It supports a broad range of prompt-driven tasks including structured document parsing, table extraction, chart understanding, document question answering, and key information extraction all within one unified model. The model features a unique "Layout-as-Thought" capability that generates structured layout representations before producing final outputs, making it particularly effective for complex documents with mixed element types.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/qianfan_ocr) | [Paper](https://huggingface.co/papers/2603.13398)
* add Qianfan-OCR model definition (#45280) by @marvinzh in [#45280](https://github.com/huggingface/transformers/pull/45280)

### SAM3-LiteText

SAM3-LiteText is a lightweight variant of SAM3 that replaces the heavy SAM3 text encoder (353M parameters) with a compact MobileCLIP-based text encoder optimized through knowledge distillation, while keeping the SAM3 ViT-H image encoder intact. This reduces text encoder parameters by up to 88% while maintaining segmentation performance comparable to the original model. The model enables efficient vision-language segmentation by addressing the redundancy found in text prompting for segmentation tasks.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/sam3_lite_text) | [Paper](https://huggingface.co/papers/2602.12173)
* Add SAM3-LiteText (#44320) by @NielsRogge in [#44320](https://github.com/huggingface/transformers/pull/44320)

### SLANet

SLANet and SLANet_plus are lightweight models designed for table structure recognition, focusing on accurately recognizing table structures in documents and natural scenes. The model improves accuracy and inference speed by adopting a CPU-friendly lightweight backbone network PP-LCNet, a high-low-level feature fusion module CSP-PAN, and a feature decoding module SLA Head that aligns structural and positional information. SLANet was developed by Baidu PaddlePaddle Vision Team as part of their table structure recognition solutions.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/slanet)
* [Model] Add SLANet Model Support (#45532) by @zhang-prog in [#45532](https://github.com/huggingface/transformers/pull/45532)


## Breaking changes

The internal `rotary_fn` is no longer registered as a hidden kernel function, so any code referencing `self.rotary_fn(...)` within an Attention module will break and must be updated to call the function directly instead.
* :rotating_light: [`Kernels`] Fix kernel function registration (#45420) by @vasqu



## Serve

The `transformers serve` command received several enhancements, including a new `/v1/completions` endpoint for legacy text completion, multimodal support for audio and video inputs, improved tool-calling via `parse_response`, proper forwarding of `tool_calls`/`tool_call_id` fields, a 400 error on model mismatch when the server is pinned to a specific model, and fixes for the response API. Documentation was also updated to cover new serving options such as `--compile` and `--model-timeout`.


* Add /v1/completions endpoint (OpenAI legacy completions API) to `transformers serve` (#44558) by @rain-1 in [#44558]
* Updated the image cache for Paddle models according to the latest API (#45562) by @zhang-prog in [#45562]
* Raise 400 on model mismatch when `transformers serve` is pinned (#45443) by @qgallouedec in [#45443]
* [serve] Update tool call to switch to `parse_response` (#45485) by @SunMarc in [#45485]
* Fix response api support  (#45463) by @SunMarc in [#45463]
* [serve] Forward `tool_calls`/`tool_call_id` in processor inputs (#45418) by @qgallouedec in [#45418]
* refactor(qa): extend extras so ty can run on server modules (#45456) by @tarekziade in [#45456]
* Multimodal serve support  (#45220) by @SunMarc in [#45220]
* [docs] transformers serve (#45174) by @stevhliu in [#45174]


## Vision

Several vision-related bug fixes were applied in this release, including correcting Qwen2.5-VL temporal RoPE scaling for still images, fixing missing/mismatched image processor backends for Emu3 and BLIP, resolving modular image processor class duplication, and preventing accelerate from incorrectly splitting vision encoders in PeVideo/PeAudioVideo models. Image loading performance was also improved by leveraging torchvision's native `decode_image` in the torchvision backend, yielding up to ~17% speedup over PIL-based loading.


* Revert "Fix: modular image processors (#45492)" (#45531) by @tarekziade in [#45531]
* Fix: modular image processors (#45492) by @zucchini-nlp in [#45492]
* fix: prevent accelerate from splitting vision encoder by setting _no_… (#43047) by @<NOT FOUND> in [#43047]
* Fix Qwen2.5-VL temporal RoPE scaling applied to still images (#45330) by @Kash6 in [#45330]
*  Use torchvision `decode_image` to load images in the torchvision backend (#45195) by @yonigozlan in [#45195]
* Fix missing image processors backends (#45165) by @zucchini-nlp in [#45165]


## Parallelization

Fixed several bugs affecting distributed training, including silently wrong results or NaN loss with Expert Parallelism, NaN weights on non-rank-0 FSDP processes, and a resize failure in PP-DocLayoutV3; additionally added support for loading adapters with Tensor Parallelism, added MoE to the Gemma4 TP plan, and published documentation for TP training.


* Fix EP: RouterParallel shape, tp_plan property, grouped_mm sentinels (#45473) by @AmineDiro in [#45473]
* Fix NaN weights on non-rank-0 FSDP processes (#45050) by @albertvillanova in [#45050]
* Load adapter with TP (#45155) by @michaelbenayoun in [#45155]
* [docs] tp training (#44613) by @stevhliu in [#44613]
* Fix resize failure caused by zero-sized masks in PP-DocLayoutV3 (#45281) by @zhang-prog in [#45281]
* Add MoE to Gemma4 TP plan (#45219) by @sywangyi in [#45219]


## Tokenization

Fixed a docstring typo in streamer classes, resolved a Kimi-K2.5 tokenizer regression and `_patch_mistral_regex` AttributeError, and patched a streaming generation crash for `Qwen3VLProcessor` caused by incorrect `_tokenizer` attribute access. Additional housekeeping included moving the GPT-SW3 instruct tokenizer to an internal testing repo and fixing a global state leak in the tokenizer registry during tests.


* [Doc] Fix 'tokenized' -> 'tokenizer' typo in streamer docstrings (#45508) by @avasis-ai in [#45508]
* Fix Kimi-K2.5 tokenizer regression and _patch_mistral_regex AttributeError (#45359) by @ArthurZucker in [#45359]
* fix(serving): resolve rust tokenizer from ProcessorMixin in streaming generation (#45368) by @sharziki in [#45368]
* [`Tokenizers`] Move gpt sw3 tokenizer out (#45404) by @vasqu in [#45404]
* fix: leak in tokenizer registry for `test_processors` (#45318) by @tarekziade in [#45318]


## Cache

Cache handling was improved for Gemma4 and Gemma3n models by dissociating KV state sharing from the Cache class, ensuring KV states are always shared regardless of whether a Cache is used. Additionally, the image cache for Paddle models was updated to align with the latest API.


* Align gemma3n cache sharing to gemma4 (#45489) by @Cyrilvallez in [#45489]
* remove cache file from tree (#45392) by @tarekziade in [#45392]
* [gemma4] Dissociate kv states sharing from the Cache (#45312) by @Cyrilvallez in [#45312]


## Audio

Audio models gained vLLM compatibility through targeted fixes across several model implementations, while reliability improvements were also made including exponential back-off retries for audio file downloads, a crash fix in the `text-to-speech` pipeline when generation configs contain `None` values, and corrected test failures for Kyutai Speech-To-Text.


* feat[vLLM × v5]: Add vLLM compatibility for audio models (#45326) by @harshaljanjani in [#45326]
* http retries on audio file downloads (#45126) by @tarekziade in [#45126]
* fix(testing): Fix Kyutai Speech-To-Text and LongCatFlash test failures on main CI (#44695) by @harshaljanjani in [#44695]
* Fix `text-to-speech` pipeline crash when generation config contains `None` values (#45107) by @jiqing-feng in [#45107]


## Bugfixes and improvements

* [`Privacy Filter`] Add model (#45580) by @vasqu in [#45580]
* Add ForSequenceClassification heads for the OLMo family (#45551) by @earino in [#45551]
* Add IndexCache support for GLM5 DSA (#45424) by @louzongzhi in [#45424]
* Fix redundant logic in video processing SmolVLM (#45272) by @yonigozlan in [#45272]
* Fix typos (#45574) by @vasqu in [#45574]
* [Model] Add SLANet Model Support (#45532) by @zhang-prog in [#45532]
* refactor(Dots1): drop Dots1MoE override to `pass` (inherits from DSV3 MoE) (#45572) by @casinca in [#45572]
* perf: avoid recomputing rotary_emb for each layer in some Google and ModernBERT models (#45555) by @casinca in [#45555]
* Gemma4 training with text-only samples (#45454) by @zucchini-nlp in [#45454]
* [nemotron_h] Add support for MLP mixers (#44763) by @xenova in [#44763]
* add expert parallelism for gemma-4-26B-A4B-it (#45279) by @sywangyi in [#45279]
* Add full GGUF loading support for GPT‑OSS (fixes #43366, supersedes #43757) latest (#45506) by @sirzechs66 in [#45506]
* Update Gemma4 weight conversion script (#45328) by @RyanMullins in [#45328]
* Move some conversion mappings to PrefixChange (#45567) by @Cyrilvallez in [#45567]
* fix table update versions (#45544) by @tarekziade in [#45544]
* Add disable_mmap kwarg to from_pretrained with hf-mount auto-detection (#45547) by @rtrompier in [#45547]
* fix(DSV3): parity between native `DeepseekV3MoE` and remote official implementation (#45441) by @casinca in [#45441]
* [modular] Fix modular logic broken in #45045 (#45539) by @Cyrilvallez in [#45539]
* Fix: propagate quantization_config to text sub-config for composite models in AutoModelForCausalLM (#45494) by @lvliang-intel in [#45494]
* T5Gemma2: fix `prepare_decoder_input_ids_from_labels` (#45516) by @Tokarak in [#45516]
* [Trainer] Add ddp_static_graph option (#45519) by @KeitaW in [#45519]
* Add dtype config options for Four Over Six (#45367) by @jackcook in [#45367]
* [Sam3LiteText] Remove unnecessary modules/configs (#45535) by @yonigozlan in [#45535]
* Fix conditional check for float formatting (#44425) by @qgallouedec in [#44425]
* Fix AMD CI: rebuild torchvision with libjpeg + refresh expectations (#45533) by @Abdennacer-Badaoui in [#45533]
* Reapply modular to examples (#45527) by @Cyrilvallez in [#45527]
* qa: re-run modular converter when the script itself is modified (#45528) by @tarekziade in [#45528]
* [GGUF] Reduce peak RAM usage by casting dequantized tensors early during load (#45386) by @UsamaKenway in [#45386]
* Fix CSM `TextToAudioPipeline` missing `<bos>` token (#45525) by @jiqing-feng in [#45525]
* [`Conversion Mapping`] Small fixups (#45483) by @vasqu in [#45483]
* fix: return empty tuple from import_protobuf_decode_error when protobuf is unavailable (#45486) by @jw9603 in [#45486]
* throw error when conversion required (#45078) by @itazap in [#45078]
* chore: bump doc-builder SHA for PR upload workflow (#45450) by @rtrompier in [#45450]
* xpu output align with cuda in test case (#45526) by @sywangyi in [#45526]
* chore(qa): split out mlinter (#45475) by @tarekziade in [#45475]
* [loading] Clean way to add/remove full parts in checkpoint names (#45448) by @Cyrilvallez in [#45448]
* Fix Zamba2MambaMixer ignoring use_mamba_kernels=False (#44853) by @sergiopaniego in [#44853]
* revert sha commit pointing to main for transformers_amd_ci_  workflows (#45495) by @paulinebm in [#45495]
* Fix ZeRO-3 from_pretrained: load registered buffers in _load_state_dict_into_zero3_model (#45402) by @saslifat-gif in [#45402]
* Remove redundant condition checks in `get_image_size` method (#45461) by @JiauZhang in [#45461]
* Add check-auto in repo-consistency and fix sorting (#45481) by @zucchini-nlp in [#45481]
* Fix typos in src/transformers/utils/output_capturing.py (#45269) by @ryota-komatsu in [#45269]
* typing: rule 15 - checks for tie_word_embeddings presence (#44988) by @tarekziade in [#44988]
* [CB] Fix capture of max_seqlen (#45323) by @remi-or in [#45323]
* Minor update (#45484) by @ydshieh in [#45484]
* Add Neuron to auto-compile hardware list (#44757) by @dacorvo in [#44757]
* Allow loading Qwen Thinker 'base' models without generative head (#45457) by @tomaarsen in [#45457]
* [`fix`] Always early return for non-Mistral models in _patch_mistral_regex (#45444) by @tomaarsen in [#45444]
* Fix spurious position_ids warnings for at least 40 architectures (#45437) by @tomaarsen in [#45437]
* [`fix`] Make Qwen2_5OmniProcessor warning a lot less noisy via warning_once (#45455) by @tomaarsen in [#45455]
* Dynamic auto mapping (#45018) by @zucchini-nlp in [#45018]
* [docs] vlm addition (#45271) by @stevhliu in [#45271]
* fix: dont download artifacts from the test hub (#45319) by @tarekziade in [#45319]
* fix(clipseg): fix 2 failing tests (#45403) by @kaixuanliu in [#45403]
* [docs] @auto_docstring decorator (#45130) by @stevhliu in [#45130]
* Fix Sam3Processor missing input_boxes_labels for padded None entries (#45171) by @Kash6 in [#45171]
* better grad acc tests (#45434) by @SunMarc in [#45434]
* Add example for iterative chatting with MLLMs (#45398) by @zucchini-nlp in [#45398]
* Gemma4 resizing per layer inputs (#45324) by @zucchini-nlp in [#45324]
* Add `step3_vl` to `MODELS_WITH_INCORRECT_HUB_TOKENIZER_CLASS` (#45449) by @hmellor in [#45449]
* Update workflow references to new commit hash (#45442) by @paulinebm in [#45442]
* [Gemma4] Add docstrings for Per-Layer Embeddings (PLE) pipeline (#45207) by @w4nderlust in [#45207]
* [Doc] Correct checkpoint path in Dinov2 model_docs  (#45430) by @ambroiseodt in [#45430]
* Fix ty for transformers cli (#45190) by @SunMarc in [#45190]
* fix(models): Resolve regressions in Wav2Vec2PhonemeCTCTokenizer (wav2vec2-lv-60-espeak-cv-ft) (#45199) by @harshaljanjani in [#45199]
* Fix Qwen2.5VL temporal grid positions (#45400) by @zucchini-nlp in [#45400]
* [`fix`] PEFT integration fixes preventing save/load & integration (#45428) by @tomaarsen in [#45428]
* Fix the response schema for the gemma4 converter (#45411) by @Rocketknight1 in [#45411]
* [Doc]  MoE routing capture and replay recipe  (#44925) by @kashif in [#44925]
* Fix `apply_chat_template` crash on `tool_call` messages without content (#45348) by @qgallouedec in [#45348]
* [AMD CI] Fix torch.compile/export failures on AMD CI due to untraceable set.__contains__  (#45282) by @Abdennacer-Badaoui in [#45282]
* [inference_fusion] convert conv3d patch embed to linear (#45041) by @JJJYmmm in [#45041]
* Fix #45305 + add regression test GAS (#45349) by @florian6973 in [#45349]
* Update `trackio` integration to use Buckets and "freeze" Space after training (#45329) by @abidlabs in [#45329]
* fix(qwen3_moe): correct return type annotation on Qwen3MoeSparseMoeBlock.forward (#45352) by @RudrenduPaul in [#45352]
* Fix: NotebookProgressCallback crash when evaluating with the Trainer (#44949) by @Charly21r in [#44949]
* docs: fix 5 docstring errors in Gemma3nTextConfig (typos, grammar, formatting) (#45370) by @RudrenduPaul in [#45370]
* Less unnecessary RoPE warnings (#45289) by @zucchini-nlp in [#45289]
* Fix unintended Hub metadata calls from _patch_mistral_regex (#43603) by @vaibhav-research in [#43603]
* Fix MoE routers returning probabilities instead of logits (#45131) by @yacinemebarki in [#45131]
* [docs] training on specific hardware (#44799) by @stevhliu in [#44799]
* [docs] zero + sequence parallelism (#44605) by @stevhliu in [#44605]
* Fix vlm weight mappings (#45358) by @Cyrilvallez in [#45358]
* Copy the template resolution logic from the base apply_chat_template to Voxtral (#45117) by @Rocketknight1 in [#45117]
* add kwargs to all methods in the CallbackHandler class (#45353) by @wilnn in [#45353]
* Close file handler (#45187) by @ydshieh in [#45187]
* fix: restore mypy type checking for PreTrainedConfig subclasses (#45071) (#45240) by @shhKnight30 in [#45240]
* `cohere_asr`: fix device issue for `test_model_parallel_beam_search` (#45214) by @kaixuanliu in [#45214]
* Fix AttributeError in Gemma3ForConditionalGeneration and Gemma3ForSequenceClassification when config.return_dict=False (#45277) by @kamalrajkannan78 in [#45277]
* fix bug for videomt model device mismatch (#45204) by @kaixuanliu in [#45204]
* fix gemma4 gradient accumulation loss and last token incorrect labels (#45354) by @winglian in [#45354]
* Logger has `[transformers]` prefix in non-verbose mode (#45316) by @zucchini-nlp in [#45316]
* Fix AttributeError in AssistantToTargetTranslator.unmap_input_ids with cross-vocab models (#45320) by @Regata3010 in [#45320]
* musicflamingo: add test support for Intel XPU device (#45212) by @kaixuanliu in [#45212]
* nomic_bert: make the test suitable for general device. (#45209) by @kaixuanliu in [#45209]
* Skip invalid flash-attn tests for `pi0` model (#45011) by @kaixuanliu in [#45011]
* Add cuda compatibility check for using `grouped_mm` (#45001) by @Sai-Suraj-27 in [#45001]
* [docs] optimizers, hyperparam search, training features (#44290) by @stevhliu in [#44290]
* Remove unused parameters and improve add_tensor_parallel_hooks_t… (#44768) by @michaelbenayoun in [#44768]
* [gemma4] Fix device map auto (#45347) by @Cyrilvallez in [#45347]
* Refactor CLIP-like models (#44431) by @zucchini-nlp in [#44431]
* refactor: display test duration (#45344) by @tarekziade in [#45344]
* Fix `Wav2Vec2Config.vocab_size` type to allow `None` (#45108) by @jiqing-feng in [#45108]
* Add THD support in ESM (#44145) by @balvisio in [#44145]
* [gemma4] Remove all shared weights, and silently skip them during loading (#45336) by @Cyrilvallez in [#45336]
* Fix conversion mappings for vlms (#45340) by @Cyrilvallez in [#45340]
* chore: added circleci python script to ruff and ty checkers (#45339) by @tarekziade in [#45339]
* tweak checkers output on errors (#45163) by @tarekziade in [#45163]
* chore: remove test_hub for now (#45337) by @tarekziade in [#45337]
* [docs] pipeline cleanup (#44954) by @stevhliu in [#44954]
* Fix export for gemma4 and add Integration tests (#45285) by @Cyrilvallez in [#45285]
* Fix vllm cis (#45139) by @ArthurZucker in [#45139]
* [docs] static model rules (#45232) by @stevhliu in [#45232]
* fix(security): prevent untrusted users from triggering TRL CI dispatch (#45302) by @jagwar in [#45302]
* [AMD CI] Fix Qwen2 expectations (#45284) by @Abdennacer-Badaoui in [#45284]
* Add `hasattr(torch.backends.cudnn, "conv")` to `conftest.py` (#45263) by @ydshieh in [#45263]
* Fix `SmolVLM` video processor `resize` using wrong interpolation after backend refactor (#45258) by @ydshieh in [#45258]
* Fix `Qwen2IntegrationTest` (#45268) by @ydshieh in [#45268]
* doc: fix TokenizersBackend.convert_to_native_format docstring (#45262) by @lowzhao in [#45262]
* empty (#45261) by @ydshieh in [#45261]
* Fix unexpected TF32 being enabled in testing (#45252) by @ydshieh in [#45252]
* Fix tf32 issue: set `torch.backends.cudnn.conv.fp32_precision` explicitly. (#45248) by @ydshieh in [#45248]
* Nvidia CI with `torch 2.11` (#45243) by @ydshieh in [#45243]
* Update tiny model creation script (#45241) by @ydshieh in [#45241]
* Update `get_test_info.py` (related to tiny model creation) (#45238) by @ydshieh in [#45238]
* More fix for tiny model creation (#45228) by @ydshieh in [#45228]
* remove unnecessary entries in some auto model mappings (#45224) by @ydshieh in [#45224]
* fix: hf-doc-builder insallation was failing (#45225) by @tarekziade in [#45225]
* [CB] Add per-request logits processors (#45026) by @remi-or in [#45026]
* [docs] formatting (#45196) by @stevhliu in [#45196]
* fix `test_register_result_handler` (#45188) by @SunMarc in [#45188]
* [CB] Tweaks to update and minor fixes (#45179) by @remi-or in [#45179]
* Fix pypi release (#45210) by @ArthurZucker in [#45210]
* fix(docs): correct gemma4 docs and examples (#45197) by @douglas-reid in [#45197]
* Add Turkish (tr) translation for Get Started section (#45158) by @onwp in [#45158]
*
 
## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @vasqu
    * [`Privacy Filter`] Add model (#45580)
    * Fix typos (#45574)
    * [`Conversion Mapping`] Small fixups (#45483)
    * :rotating_light: [`Kernels`] Fix kernel function registration (#45420)
    * [`Tokenizers`] Move gpt sw3 tokenizer out (#45404)
* @rain-1
    * Add /v1/completions endpoint (OpenAI legacy completions API) to `transformers serve` (#44558)
* @zhang-prog
    * Updated the image cache for Paddle models according to the latest API (#45562)
    * [Model] Add SLANet Model Support (#45532)
    * Fix resize failure caused by zero-sized masks in PP-DocLayoutV3 (#45281)
* @tarekziade
    * fix table update versions (#45544)
    * qa: re-run modular converter when the script itself is modified (#45528)
    * Revert "Fix: modular image processors (#45492)" (#45531)
    * chore(qa): split out mlinter (#45475)
    * typing: rule 15 - checks for tie_word_embeddings presence (#44988)
    * fix: dont download artifacts from the test hub (#45319)
    * refactor(qa): extend extras so ty can run on server modules (#45456)
    * remove cache file from tree (#45392)
    * refactor: display test duration (#45344)
    * http retries on audio file downloads (#45126)
    * chore: added circleci python script to ruff and ty checkers (#45339)
    * tweak checkers output on errors (#45163)
    * fix: leak in tokenizer registry for `test_processors` (#45318)
    * chore: remove test_hub for now (#45337)
    * fix: hf-doc-builder insallation was failing (#45225)
* @marvinzh
    * add Qianfan-OCR model definition (#45280)
* @remi-or
    * [CB] Fix capture of max_seqlen (#45323)
    * [CB] Add per-request logits processors (#45026)
    * [CB] Tweaks to update and minor fixes (#45179)
* @ydshieh
    * Minor update (#45484)
    * Close file handler (#45187)
    * Add `hasattr(torch.backends.cudnn, "conv")` to `conftest.py` (#45263)
    * Fix `SmolVLM` video processor `resize` using wrong interpolation after backend refactor (#45258)
    * Fix `Qwen2IntegrationTest` (#45268)
    * empty (#45261)
    * Fix unexpected TF32 being enabled in testing (#45252)
    * Fix tf32 issue: set `torch.backends.cudnn.conv.fp32_precision` explicitly. (#45248)
    * Nvidia CI with `torch 2.11` (#45243)
    * Update tiny model creation script (#45241)
    * Update `get_test_info.py` (related to tiny model creation) (#45238)
    * More fix for tiny model creation (#45228)
    * remove unnecessary entries in some auto model mappings (#45224)
* @NielsRogge
    * Add SAM3-LiteText (#44320)
* @ArthurZucker
    * Fix IndexError with DeepSpeed ZeRO-3 when kernels rotary is active (#45414)
    * Fix Kimi-K2.5 tokenizer regression and _patch_mistral_regex AttributeError (#45359)
    * Fix vllm cis (#45139)
    * Fix pypi release (#45210)
    * update to dev version 5.6.0-dev0
* @JJJYmmm
    * [inference_fusion] convert conv3d patch embed to linear (#45041)
* @balvisio
    * Add THD support in ESM (#44145)
* @onwp
    * Add Turkish (tr) translation for Get Started section (#45158)

---

## v5.5.4  (2026-04-13T16:58:06Z)

# Patch release v5.5.4

This is mostly some fixes that are good to have asap, mostly for tokenizers;
** Fix Kimi-K2.5 tokenizer regression and _patch_mistral_regex Attribute… (#45305) by ArthurZucker

For training:
** Fix #45305 + add regression test GAS (#45349) by florian6973, SunMarc
** Fix IndexError with DeepSpeed ZeRO-3 when kernels rotary is active (#…) by ArthurZucker

And for Qwen2.5-VL :
** Fix Qwen2.5-VL temporal RoPE scaling applied to still images (#45330) by Kash6, zucchini-nlp

---

## v5.5.3  (2026-04-09T15:53:11Z)

Small patch release to fix `device_map` support for Gemma4! It contains the following commit:

- [gemma4] Fix device map auto (#45347) by @Cyrilvallez

---

## v5.5.2  (2026-04-09T14:05:16Z)

Small patch dedicated to optimizing gemma4, fixing inference with `use_cache=False` due to k/v states sharing between layers, as well as conversion mappings for some models that would inconsistently serialize their weight names. It contains the following PRs:

- Add MoE to Gemma4 TP plan (#45219) by @sywangyi and @Cyrilvallez
- [gemma4] Dissociate kv states sharing from the Cache (#45312) by @Cyrilvallez
- [gemma4] Remove all shared weights, and silently skip them during loading (#45336) by @Cyrilvallez
- Fix conversion mappings for vlms (#45340) by @Cyrilvallez

---

## v5.5.1  (2026-04-09T05:53:03Z)

# Patch release v5.5.1

This patch is very small and focuses on vLLM and Gemma4! 

** Fix export for gemma4 and add Integration tests (#45285) by @Cyrilvallez 
** Fix vllm cis (#45139) by @ArthurZucker

---

## v5.5.0  (2026-04-02T16:15:33Z)

# Release v5.5.0

<img width="2786" height="1504" alt="image" src="https://github.com/user-attachments/assets/6c8c878f-042b-4858-9f64-73fd9ccd7e4b" />

## New Model additions

### Gemma4

[Gemma 4](INSET_PAPER_LINK) is a multimodal model with pretrained and instruction-tuned variants, available in 1B, 13B, and 27B parameters. The architecture is mostly the same as the previous Gemma versions. The key differences are a vision processor that can output images of fixed token budget and a spatial 2D RoPE to encode vision-specific information across height and width axis.

<img width="1478" height="1374" alt="image" src="https://github.com/user-attachments/assets/9d88bd1b-02ea-4829-b7d0-fac0e347d436" />


You can find all the original Gemma 4 checkpoints under the [Gemma 4](https://huggingface.co/collections/google/gemma-4-release-67c6c6f89c4f76621268bb6d) release.

The key difference from previous Gemma releases is the new design to process **images of different sizes** using a **fixed-budget number of tokens**. Unlike many models that squash every image into a fixed square (like 224×224), Gemma 4 keeps the image's natural aspect ratio while making it the right size. There a a couple constraints to follow:
- The total number of pixels must fit within a patch budget
- Both height and width must be divisible by **48** (= patch size 16 × pooling kernel 3)

> [!IMPORTANT]
> Gemma 4 does **not** apply the standard ImageNet mean/std normalization that many other vision models use. The model's own patch embedding layer handles the final scaling internally (shifting values to the [-1, 1] range).

The number of "soft tokens" (aka vision tokens) an image processor can produce is configurable. The supported options are outlined below and the default is **280 soft tokens** per image.


| Soft Tokens | Patches (before pooling) | Approx. Image Area |
|:-----------:|:------------------------:|:-------------------:|
| 70          | 630                      | ~161K pixels        |
| 140         | 1,260                    | ~323K pixels        |
| **280**     | **2,520**                | **~645K pixels**    |
| 560         | 5,040                    | ~1.3M pixels        |
| 1,120       | 10,080                   | ~2.6M pixels        |


To encode positional information for each patch in the image, Gemma 4 uses a learned 2D position embedding table. The position table stores up to 10,240 positions per axis, which allows the model to handle very large images. Each position is a learned vector of the same dimensions as the patch embedding. The 2D RoPE which Gemma 4 uses independently rotate half the attention head dimensions for the x-axis and the other half for the y-axis. This allows the model to understand spatial relationships like "above," "below," "left of," and "right of."

### NomicBERT

NomicBERT is a BERT-inspired encoder model that applies Rotary Position Embeddings (RoPE) to create reproducible long context text embeddings. It is the first fully reproducible, open-source text embedding model with 8192 context length that outperforms both OpenAI Ada-002 and OpenAI text-embedding-3-small on short-context MTEB and long context LoCo benchmarks. The model generates dense vector embeddings for various tasks including search, clustering, and classification using specific instruction prefixes.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/nomic_bert) | [Paper](https://arxiv.org/abs/2402.01613)
* Internalise the NomicBERT model (#43067) by @ed22699 in [#43067](https://github.com/huggingface/transformers/pull/43067)

### MusicFlamingo

Music Flamingo is a fully open large audio–language model designed for robust understanding and reasoning over music. It builds upon the Audio Flamingo 3 architecture by including Rotary Time Embeddings (RoTE), which injects temporal position information to enable the model to handle audio sequences up to 20 minutes. The model features a unified audio encoder across speech, sound, and music with special sound boundary tokens for improved audio sequence modeling.

**Links:** [Documentation](https://huggingface.co/docs/transformers/main/en/model_doc/musicflamingo) | [Paper](https://huggingface.co/papers/2511.10289)
* Add Music Flamingo (#43538) by @lashahub in [#43538](https://github.com/huggingface/transformers/pull/43538)



## Breaking changes

Mamba and hybrid model caches are now first-class native citizens in the library, so users working with Mamba-based or hybrid (Mamba + attention) models should update their code to use the new native cache classes instead of any previous workarounds.
* 🚨 [Cache] Native mamba & hybrid cache (#44950) by @Cyrilvallez

Remote code execution support has been removed from the native `LightGlue` integration, so users who were loading `LightGlue` with `trust_remote_code=True` must remove that argument and use the model directly through the standard native API.
* :rotating_light: [`LightGlue`] Remove remote code execution (#45122) by @vasqu



## Vision

Several vision-related bugs were fixed in this release, including correcting the Gemma vision mask to support video inputs, resolving a dependency issue that incorrectly required torchvision for PIL-based image processors, and patching bugs in the Janus image generation model and image loading. Local code resolution for tokenizers and image processors was also corrected.


* Generalize gemma vision mask to videos (#45185) by @zucchini-nlp in [#45185]
* Fix explicit local code resolution for tokenizers and image processors (#45169) by @hmellor in [#45169]
* fix bug for janus model image generation (#45044) by @kaixuanliu in [#45044]
* [Bugfix] Remove incorrect torchvision requirement from PIL backend image processors (#45045) by @Lidang-Jiang in [#45045]
* Avoid `Image.open` failure (#44645) by @sywangyi in [#44645]


## Cache

Improved the performance of repository checks (`check-repo`) by introducing file-level and AST-level disk caching, achieving up to a 27x speedup (from ~46s to ~1.6s with a warm cache), and fixed the mlinter cache location in `.gitignore`.


* refactoring: speedup static checks with disk cache (#44992) by @tarekziade in [#44992]
* refactor: added cache in check_repo (#45012) by @tarekziade in [#45012]
* chore: Fix mlinter cache location (#45052) by @tarekziade in [#45052]


## Bugfixes and improvements

* Fix resized LM head weights being overwritten by post_init (#45079) by @javierdejesusda in [#45079]
* [Qwen3.5 MoE] Add _tp_plan to ForConditionalGeneration (#45124) by @danielquintas8 in [#45124]
* fix(models): Fix dtype mismatch in SwitchTransformers and TimmWrapperModel (#45074) by @harshaljanjani in [#45074]
* [misc] fix qwen35 tests: correct the text model type and skip reverse_mapping (#45173) by @JJJYmmm in [#45173]
* 🔒 Pin GitHub Actions to commit SHAs (#45180) by @paulinebm in [#45180]
* Use doc-builder runnable example for GLM-ASR (#44277) by @tarekziade in [#44277]
* CI] Small T5 expectations updated (#45138) by @Abdennacer-Badaoui in [#45138]
* fix: correct type annotations across config classes for @strict validation (#45007) by @Krishnachaitanyakc in [#45007]
* Fix T5Attention shape mismatch under Tensor Parallelism (#45109) by @aws-zhanxun in [#45109]
* [refactor] Serving into proper modules (#44796) by @SunMarc in [#44796]
* Re-add regex substitutions to the response parsing spec (#45166) by @Rocketknight1 in [#45166]
* Fix incorrect TrainingArguments example in training.md (#45150) by @maanas1234 in [#45150]
* Add parse_response to Processor, make it a bit more official (#45143) by @Rocketknight1 in [#45143]
* DeepGEMM (#44832) by @IlyasMoutawwakil in [#44832]
* fix: prefer registered config over remote code in AutoConfig.from_pretrained (#45094) by @HanFa in [#45094]
* [serving] Fix continuous batching JSON response serialization (#45057) by @NathanHB in [#45057]
* Fix stupid test fetcher (#45140) by @ydshieh in [#45140]
* [CB] Add warmup feature (#45112) by @remi-or in [#45112]
* feature: added import complexity checker (#45013) by @tarekziade in [#45013]
* Fix tests for `janus` model (#44739) by @kaixuanliu in [#44739]
* CB improvements for serving  (#45063) by @SunMarc in [#45063]
* [docs] continuous batching (#44896) by @stevhliu in [#44896]
* Fix few issues in Qwen_3_Omni_Moe (#44848) by @Sai-Suraj-27 in [#44848]
* Fix TypeError in rope validation when ignore_keys is a list (#45069) by @Fr0do in [#45069]
* Remove unused TensorFlow env var (#45065) by @Sai-Suraj-27 in [#45065]
* fix: add identity reverse_op to dequantize ops for save_pretrained (#44983) by @Hyungkeun-Park-Nota in [#44983]
* Fix when RoPE params are in kwargs (#45049) by @zucchini-nlp in [#45049]
* chore: update update_metdata.yml (#45054) by @hf-security-analysis[bot] in [#45054]
* [`FA`] Fix BC support for a few versions + add deprecation cycle (#45061) by @vasqu in [#45061]
* fix(testing): Fix Parakeet, Evolla, Pi0, and Phi-3 test failures on main CI (#45004) by @harshaljanjani in [#45004]
* Allow advanced users to override `model_type` in `AutoConfig.from_pretrained` (#45058) by @hmellor in [#45058]
* Fix failing `SmolLM3IntegrationTest` (#45048) by @Sai-Suraj-27 in [#45048]
* chore: remove old extras (#45024) by @tarekziade in [#45024]
* Embedding VLMs don't need a head (#45000) by @zucchini-nlp in [#45000]
* Fix GraniteConfig type hints to accept int for multiplier fields (#45019) by @javierdejesusda in [#45019]
* fix: preserve rotary_pct across save/load cycle in GPTNeoX configs (#44985) by @Krishnachaitanyakc in [#44985]




## Significant community contributions

The following contributors have made significant changes to the library over the last release:

* @ed22699
    * Internalise the NomicBERT model (#43067)
* @tarekziade
    * Use doc-builder runnable example for GLM-ASR (#44277)
    * refactoring: speedup static checks with disk cache (#44992)
    * feature: added import complexity checker (#45013)
    * refactor: added cache in check_repo (#45012)
    * chore: remove old extras (#45024)
    * chore: Fix mlinter cache location (#45052)
    * refactor: speed up docstring checker (#45009)
* @Krishnachaitanyakc
    * fix: correct type annotations across config classes for @strict validation (#45007)
    * fix: preserve rotary_pct across save/load cycle in GPTNeoX configs (#44985)
* @lashahub
    * Add Music Flamingo (#43538)
* @Lidang-Jiang
    * [Bugfix] Remove incorrect torchvision requirement from PIL backend image processors (#45045)

---