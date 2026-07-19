# ggml-org/llama.cpp - last 20 releases (latest: b9999)


## b9999  (2026-07-14T11:23:47Z)

<details open>

kleidiai : add SME2 f32 kernel (#24414)

* kleidiai : add SME2 f32 kernel

* enable dynamic scheduling for SME2 f32 kernel

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9999/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9999/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9999/llama-b9999-ui.tar.gz)

---

## b9996  (2026-07-14T10:41:38Z)

<details open>

arg: Flush log before exiting after usage() (#25504)

Under certain conditions, it's possible for messages emitted via LOG()
to get lost before exit, apparently because they are emitted by another
thread. common_params_print_usage() uses printf directly, and is not
affected.

Flushing the log before exit seems to resolve this.

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9996/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9996/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9996/llama-b9996-ui.tar.gz)

---

## b9995  (2026-07-14T09:44:45Z)

<details open>

sycl: set fattn_vec_nthreads to 256 for Battlemage (#25205)

Currently detects lunarlake + battlemage / xe2 and
sets the value to 256.

Keeps default at 128, Intel's ARC Alchemist's prefered value.

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9995/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9995/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9995/llama-b9995-ui.tar.gz)

---

## b9994  (2026-07-14T05:29:11Z)

<details open>

metal : add Q2_0 support (#25419)

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9994/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9994/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9994/llama-b9994-ui.tar.gz)

---

## b10012  (2026-07-14T21:34:17Z)

<details open>

hexagon: fix hmx-queue signal enum-narrowing problem (#25677)

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10012/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10012/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10012/llama-b10012-ui.tar.gz)

---

## b10011  (2026-07-14T20:55:37Z)

<details open>

server : refactor prompt cache state ownership (#25649)

* server : clear checkpoints upon prompt clear

* server : move the prompt state data to the server_prompt_cache

Assisted-by: pi:llama.cpp/Qwen3.6-27B

* server : handle batched slot being cleared

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10011/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10011/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10011/llama-b10011-ui.tar.gz)

---

## b10010  (2026-07-14T20:26:04Z)

<details open>

server: add --cors-* options (#25655)

* server: add --cors-* options

* add special "localhost" value

* add tests

* fix test

* add link to PR

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10010/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10010/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10010/llama-b10010-ui.tar.gz)

---

## b10007  (2026-07-14T19:42:26Z)

<details open>

opencl: fix a dp4a bug for devices where cl_khr_integer_dot_product is unavailable (#25639)

* opencl: do not fail backend init on devices without cl_khr_integer_dot_product

* opencl: do not call dp4 kernels when dp is unavailable

---------

Co-authored-by: Li He <lih@qti.qualcomm.com>

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10007/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10007/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10007/llama-b10007-ui.tar.gz)

---

## b10005  (2026-07-14T18:57:52Z)

<details open>

DeepseekV4: fix seq_rm (#25588)

* DeepseekV4: fix seq_rm

* implement proper seq_cp

* create actual update context

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10005/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10005/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10005/llama-b10005-ui.tar.gz)

---

## b10004  (2026-07-14T18:17:12Z)

<details open>

vulkan/cpu: Support f16 as SET_ROWS src. (#25432)

* vulkan/cpu: Support f16 as SET_ROWS src.

This adds full support for f16 SET_ROWS (equivalent to f32) to vulkan and CPU
backends, and adds more backend tests.

* Set DenormPreserve 16 when supported, to try to fix failures on Intel

* tune error threshold

* update metal supports_op

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10004/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10004/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10004/llama-b10004-ui.tar.gz)

---

## b10003  (2026-07-14T17:42:45Z)

<details open>

tokenize : align usage by using common args (#25516)

Migrate the tokenize tool to common_params_parse, replacing its
hand-rolled argv parsing, Windows UTF-8 handling and file reading
with the shared common helpers.

Expose the model-sourcing flags (-m, -mu, -dr, -hf, -hff, --offline,
HF_TOKEN) to LLAMA_EXAMPLE_TOKENIZE, and register --ids, --stdin,
--no-bos, --no-parse-special and --show-count as common args.
parse_special defaults to true for TOKENIZE to preserve the old
behavior. Errors now go through LOG_ERR instead of fprintf(stderr).

Signed-off-by: Adrien Gallouët <angt@huggingface.co>

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10003/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10003/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10003/llama-b10003-ui.tar.gz)

---

## b10002  (2026-07-14T15:19:55Z)

<details open>

ggml : add a set of functions for checking contiguity of inner tensor dimensions (#25650)

Co-authored-by: Stanisław Szymczyk <sszymczy@gmail.com>

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10002/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10002/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10002/llama-b10002-ui.tar.gz)

---

## b10001  (2026-07-14T12:46:17Z)

<details open>

tests: export-graph-ops: exit gracefully when called w/o arguments (#25619)

Fixes a segfault when `test-export-graph-ops` is called without any
arguments.

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10001/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10001/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10001/llama-b10001-ui.tar.gz)

---

## b10000  (2026-07-14T12:06:19Z)

<details open>

ggml: uniformize im2col dst_type for all conv ops (#23660)

* ggml: uniformize im2col dst_type for all conv ops

* Update ggml/src/ggml.c

Co-authored-by: Georgi Gerganov <ggerganov@gmail.com>

* ggml : uniformize im2col casting logic across all conv ops

* fix : allow im2col_f16 to accept any kernel type

---------

Co-authored-by: Georgi Gerganov <ggerganov@gmail.com>

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10000/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b10000/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b10000/llama-b10000-ui.tar.gz)

---

## b9993  (2026-07-13T23:09:16Z)

<details open>

model: add Hy3 (hy_v3) support with MTP speculative decoding (#25395)

* model: add Hy3 (hy_v3) architecture support

Adds Tencent Hunyuan 3 (HF architecture HYV3ForCausalLM, GGUF arch
hy_v3): a MoE decoder stack with per-head Q/K RMSNorm, a sigmoid
router with expert selection bias, an always-active ungated shared
expert, and leading dense block(s) (first_k_dense_replace).

The base implementation is ported from charlie12345's fork
(https://github.com/charlie12345/ROCmFPX, src/models/hyv3.cpp),
adapted to current mainline APIs (hparams.n_layer(), build_qkv,
build_moe_ffn with fused gate_up + scale tensors, output_s).

Note: blk.N.exp_probs_b is stored without a .bias suffix for
compatibility with existing hy_v3 GGUFs produced by that fork.

Co-Authored-By: charlie12345 <charlie12345@users.noreply.github.com>
Co-authored-by: Piotr Wilkin <ilintar@gmail.com>
Assisted-by: Claude Fable 5

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9993/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9993/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9993/llama-b9993-ui.tar.gz)

---

## b9992  (2026-07-13T21:04:47Z)

<details open>

CUDA: refactor MMQ kernel configuration (#24127)

* CUDA: refactor MMQ kernel configuration

* fix Blackwell config

* remove legacy code

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9992/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9992/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9992/llama-b9992-ui.tar.gz)

---

## b9990  (2026-07-13T19:51:41Z)

<details open>

spec: add Minimax2 eagle3 support

* Fix nullptr in minimax2 EAGLE3

* minor : add newline

---------

Co-authored-by: Georgi Gerganov <ggerganov@gmail.com>

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9990/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9990/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9990/llama-b9990-ui.tar.gz)

---

## b9988  (2026-07-13T19:10:17Z)

<details open>

tests: Harmonize header use (#25616)

* tests: Harmonize the use of private ggml includes

* tests: In test-backend-ops, use quoted includes

As with all other tests. This is to ensure that the build uses shipped
headers over possibly system-installed ones.

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9988/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9988/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9988/llama-b9988-ui.tar.gz)

---

## b9987  (2026-07-13T15:40:41Z)

<details open>

gguf : add tensor shape accessor (#24405)

* gguf : add tensor shape accessors

* gguf : return tensor shape as const int64_t *

* gguf : remove n_dims accessor, keep only gguf_get_tensor_ne

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9987/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9987/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9987/llama-b9987-ui.tar.gz)

---

## b9986  (2026-07-13T09:06:33Z)

<details open>

chat : fix reasoning leak with force-opened bare <think> templates (#24674)

* chat : fix reasoning leak with force-opened bare <think> templates

The reasoning start tag inferred from prior turns can carry trailing
whitespace (e.g. <think>\n) while a force-open template prefills a bare
<think>. Trim the tag used for the prefix split so the bare prefill is
matched instead of being swallowed into content.

* chat : fix Nemotron Nano v2 regression

---------

Co-authored-by: Alde Rojas <hello@alde.dev>

</details>

**macOS/iOS:**
- [macOS Apple Silicon (arm64)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-macos-arm64.tar.gz)
- macOS Apple Silicon (arm64, KleidiAI enabled) [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23780)
- [macOS Intel (x64)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-macos-x64.tar.gz)
- [iOS XCFramework](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-xcframework.zip)

**Linux:**
- [Ubuntu x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-x64.tar.gz)
- [Ubuntu arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-arm64.tar.gz)
- [Ubuntu s390x (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-s390x.tar.gz)
- [Ubuntu x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-vulkan-x64.tar.gz)
- [Ubuntu arm64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-vulkan-arm64.tar.gz)
- [Ubuntu x64 (ROCm 7.2)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-rocm-7.2-x64.tar.gz)
- [Ubuntu x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-openvino-2026.2.1-x64.tar.gz)
- [Ubuntu x64 (SYCL FP32)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-sycl-fp32-x64.tar.gz)
- [Ubuntu x64 (SYCL FP16)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-ubuntu-sycl-fp16-x64.tar.gz)

**Android:**
- [Android arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-android-arm64.tar.gz)

**Windows:**
- [Windows x64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-cpu-x64.zip)
- [Windows arm64 (CPU)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-cpu-arm64.zip)
- [Windows arm64 (OpenCL Adreno)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-opencl-adreno-arm64.zip)
- [Windows x64 (CUDA 12)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-cuda-12.4-x64.zip) - [CUDA 12.4 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9986/cudart-llama-bin-win-cuda-12.4-x64.zip)
- [Windows x64 (CUDA 13)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-cuda-13.3-x64.zip) - [CUDA 13.3 DLLs](https://github.com/ggml-org/llama.cpp/releases/download/b9986/cudart-llama-bin-win-cuda-13.3-x64.zip)
- [Windows x64 (Vulkan)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-vulkan-x64.zip)
- [Windows x64 (OpenVINO)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-openvino-2026.2.1-x64.zip)
- [Windows x64 (SYCL)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-sycl-x64.zip)
- [Windows x64 (HIP)](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-bin-win-hip-radeon-x64.zip)

**openEuler:**
- [DISABLED](https://github.com/ggml-org/llama.cpp/pull/23705)
- openEuler x86 (310p)
- openEuler x86 (910b, ACL Graph)
- openEuler aarch64 (310p)
- openEuler aarch64 (910b, ACL Graph)

**UI:**
- [UI](https://github.com/ggml-org/llama.cpp/releases/download/b9986/llama-b9986-ui.tar.gz)

---