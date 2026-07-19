# libbpf 1.0 API migration — source corpus for FactBank extraction

Library: libbpf   Target major version: 1.0 (the 0.x -> 1.0 breaking-change / API-cleanup release)
Assembled from: the nakryiko.com libbpf-v1 change list, the libbpf wiki 1.0 Migration Guide, the
libbpf wiki 'road to v1.0' deprecation plan (full old->new API mapping), and the GitHub release notes
v0.6.0 through v1.4.0. All function names, SEC() names, struct names, and error conventions preserved verbatim.

===================================================================================
PART 1 — BLOG CHANGE LIST (nakryiko.com/posts/libbpf-v1)
===================================================================================

# libbpf 1.0 — nakryiko.com blog: "libbpf 1.0 change list" (verbatim technical reference)

Source: https://nakryiko.com/posts/libbpf-v1/

## Breaking Changes Summary

### Error Reporting Streamlining

The library standardized error handling across all APIs:

- **Pointer-returning APIs**: Return `NULL` on failure and set `errno` to positive `Exxx` error code
- **Integer-returning APIs**: Return negative `-Exxx` directly as result and set positive `errno` to `Exxx`

Destructors like `bpf_object__close()` and `btf__free()` now safely accept `NULL` pointers without requiring guards.

### SEC() Annotation Changes

Key modifications to BPF program annotations:

- **Single SEC() per type requirement removed**: Multiple programs can now share identical `SEC("xdp")` annotations
- **Random suffixes no longer supported**: Programs must use canonical annotations only (e.g., `SEC("xdp")`, not `SEC("xdp1")` or `SEC("xdp_prog1")`)
- **Program identification**: Use C function names instead of section names to uniquely identify BPF programs
- **Pinning behavior change**: BPF program names now used for pinning instead of section names
- **Optional attach targets**: Programs like kprobes can now use `SEC("kprobe")` without specifying target function

### OPTS Framework Introduction

APIs now use extensible `struct xxx_opts` parameters with `LIBBPF_OPTS()` macro:

```c
LIBBPF_OPTS(bpf_object_open_opts, opts,
    .kernel_log_buf = log_buf,
    .kernel_log_size = sizeof(log_buf),
    .kernel_log_level = 1,
);
struct bpf_object *obj = bpf_object__open_file("/path/to/file.bpf.o", &opts);
```

### API Consolidation and Removals

- **AF_XDP consolidation**: `xsk.h` APIs moved to separate `libxdp` project
- **Naming standardization**: Getters omit "get_" prefix (`bpf_program__type()`), setters include "set_" (`bpf_program__set_type()`)
- **Low-level API unification**: `bpf_prog_load()` consolidates multiple program loading APIs; `bpf_map_create()` supersedes six similar map creation functions
- **Legacy map definitions removed**: `SEC("maps")` support dropped; users must migrate to `SEC(".maps")` with BTF definitions
- **Specialized API removals**: Niche APIs used only by `perf` and BCC removed or relocated; general replacement APIs added

## Public Header Files

**User-space APIs:** `libbpf.h`, `bpf.h`, `btf.h`
**BPF-side APIs:** `bpf_helpers.h`, `bpf_tracing.h`, `bpf_core_read.h`, `usdt.bpf.h`, `bpf_endian.h`

## Transparent Kernel Compatibility Features

- `bpf_probe_read_{kernel, user}()` downgraded to `bpf_probe_read()` on older kernels
- `bpf_printk()` macro switches between `bpf_trace_printk()` and `bpf_trace_vprintk()` based on kernel capabilities
- Automatic `RLIMIT_MEMLOCK` management (set to infinity only when necessary)
- BTF sanitization for older kernel compatibility
- Auto-adjustment of BPF map parameters (e.g., ringbuf page alignment)

## New Language Support Features

- **Unrestricted BPF programs**: No limit on number of programs per `SEC()` annotation
- **Subprogram inlining**: No requirement for manual `__always_inline` directives
- **Global variables**: Full support for C global variables enabling runtime configuration from user-space
- **Static linking**: BPF object files can be linked together via `bpftool gen object` or public linking APIs

## Customization APIs

- `bpf_program__set_autoload()`: Disable auto-loading via `SEC("?...")` pattern
- `bpf_map__set_autocreate()`: Prevent automatic map creation
- `bpf_program__set_autoattach()`: Control granular program attachment
- `kernel_log_buf`, `kernel_log_size`, `kernel_log_level`: Flexible verifier log capture

## Tracing Enhancements

**USDT Support:** New `SEC("usdt")` annotation; `BPF_USDT()` macro for declarative argument specification.
**Syscall Tracing:** `SEC("ksyscall/<syscall>")` and `SEC("kretsyscall")` annotations; `BPF_KSYSCALL()` macro handling architecture/version differences.
**Uprobe Improvements:** Function tracing by name instead of manual offset; automatic system library path resolution (e.g., `SEC("uprobe/libc.so.6:malloc")`); `bpf_program__attach_uprobe()`.

## Networking APIs

**TC (Traffic Control):** `bpf_tc_hook_create()`, `bpf_tc_hook_destroy()`, `bpf_tc_attach()`, `bpf_tc_detach()`, `bpf_tc_query()`
**XDP:** `bpf_xdp_attach()`, `bpf_xdp_detach()`, `bpf_xdp_query()`, `bpf_program__attach_xdp()` (preferred link-based alternative)

===================================================================================
PART 2 — LIBBPF 1.0 MIGRATION GUIDE (wiki, verbatim)
===================================================================================

## Overview

Libbpf is moving towards v1.0 release. [This document](https://docs.google.com/document/d/1UyjTZuPFWiPFyKk1tV5an11_iaRuec6U-ZESZ54nNTY) contains a list of planned breaking changes and API deprecations planned for v1.0 release. This page contains a short guide-lines on making sure applications using libbpf can migrate smoothly with least amount of effort and no unintended breakage. Most API deprecations and other behavior changes should have a corresponding short section on this page listing the recommended new API(s) and conventions, compared to pre-1.0 API.

## Testing your application with libbpf 1.0 behavior

Whenever libbpf is attempting some breaking change, it doesn't go in effect until the official 1.0 release. Instead, libbpf provides a new API:

```c
int libbpf_set_strict_mode(enum libbpf_strict_mode mode);
```

This API allows to turn on v1.0 behavior for various aspects of libbpf. It accepts a set of flags, defined in `enum libbpf_strict_mode`:

```c
enum libbpf_strict_mode {
        /* Turn on all supported strict features of libbpf to simulate libbpf
         * v1.0 behavior.
         * This will be the default behavior in libbpf v1.0.
         */
        LIBBPF_STRICT_ALL = 0xffffffff,

        /*
         * Disable any libbpf 1.0 behaviors. This is the default before libbpf
         * v1.0. It won't be supported anymore in v1.0, please update your
         * code so that it handles LIBBPF_STRICT_ALL mode before libbpf v1.0.
         */
        LIBBPF_STRICT_NONE = 0x00,
        /*
         * Return NULL pointers on error, not ERR_PTR(err).
         * Additionally, libbpf also always sets errno to corresponding Exx
         * (positive) error code.
         */
        LIBBPF_STRICT_CLEAN_PTRS = 0x01,
        /*
         * Return actual error codes from low-level APIs directly, not just -1.
         * Additionally, libbpf also always sets errno to corresponding Exx
         * (positive) error code.
         */
        LIBBPF_STRICT_DIRECT_ERRS = 0x02,
};
```

So to turn on 1.0 behavior of consistently returning errors directly for `int`-returning APIs *and* also start returning NULL pointers on errors for pointer-returning APIs, application should do this before using any other libbpf APIs:

```c
libbpf_set_strict_mode(LIBBPF_STRICT_CLEAN_PTRS | LIBBPF_STRICT_DIRECT_ERRS);
```

Such approach allows to opt-in into new behaviors once you are sure application's usage of APIs or reliance of legacy libbpf behaviors were fixed.

For brand new users of libbpf or for those who are confident they follow best practices, it's possible to opt-in into all current and future planned changes by passing `LIBBPF_STRICT_ALL`:

```c
libbpf_set_strict_mode(LIBBPF_STRICT_ALL);
```

## NULL pointers on errors (`LIBBPF_STRICT_CLEAN_PTRS`)

Most (but not all) libbpf APIs that construct new "objects" (like `bpf_object__open_file()`, `btf__parse()`, `perf_buffer__new()`, etc) typically return a special non-NULL pointer, encoding a specific error code (e.g., `-EINVAL`). This is a convention stemming from libbpf's kernel heritage, but is quite surprising for user-space. Libbpf provides `libbpf_get_error()` API to check such pointer for error and extract error code, if any. This is the recommended way to do this, instead of relying on kernel definitions of `PTR_ERR()` and `IS_ERR()` macros:

```c
struct bpf_object *obj;
int err;

obj = bpf_object__open_file(...);
err = libbpf_get_error(obj);
if (err) {
    ...
}
```

When `LIBBPF_STRICT_CLEAN_PTRS` mode is enabled, libbpf will no longer return such special pointer. Instead NULL is returned, as one would expect. In cases when user would like to extract underlying error code, `errno` thread-local variable is set with the exact error code:

```c
struct bpf_object *obj;
int err;

obj = bpf_object__open_file(...);
if (!obj) {
    err = -errno;
    ...
}
```

Note, `libbpf_get_error()` is able to handle both modes and extract correct error code (assuming `libbpf_get_error()` is called right after the API that error out without any other function clobbering `errno`), so feel free to keep using it. But `libbpf_get_error()` is going to be eventually deprecated and removed in libbpf 1.0 release, so eventually you'd need to turn on `LIBBPF_STRICT_CLEAN_PTRS` and switch code to NULL checks and `errno` (if necessary).

## Direct error code returning (`LIBBPF_STRICT_DIRECT_ERRS`)

Pre-v1.0, some low-level libbpf APIs, wrapping `bpf()` syscalls, would return -1 on error and set `errno` with the actual error code returned by kernel. Some APIs might in some situations return the error code directly. So it's a bit of a mess.

With `LIBBPF_STRICT_DIRECT_ERRS` enabled, libbpf always sets `errno` *and* always return the actual error code directly. So if your code relies on -1 checks like below, it will become broken:

```
int err;

err = bpf_create_map(...);
if (err == -1) {
    /* wrong -1 catches only -EPERM error */
    ...
}
```

Instead, use `< 0` comparison:

```
int err;

err = bpf_create_map(...);
if (err < 0) {
    /* err might be -EPERM, but also -EINVAL or whatever other error code */
    ...
}
```

High-level APIs (mostly those that are coming from `libbpf.h` and `btf.h` headers) have always returned error codes directly, so no changes there. But now they, for uniformity, also set `errno` with a positive error code, so when returned code is `-EINVAL`, `errno` will be set to `EINVAL`. So this is possible, but discouraged given how easy it is to mis-use `errno` thread-local variable:

```
int fd, err;

fd = bpf_create_map(...);
if (fd < 0) {
  err = -errno;
  ...
}
```

## BPF program `SEC()` annotation deprecations

Some previously supported BPF program `SEC()` annotations are deprecated. See the table below for alternatives.

| Old SEC() definition  | New SEC() definition |
| --------------------- | -------------------- |
| `SEC("xdp_cpumap")`   | `SEC("xdp/cpumap")`  |
| `SEC("xdp_devmap")`   | `SEC("xdp/devmap")`  |
| `SEC("classifier")`   | `SEC("tc")`          |

===================================================================================
PART 3 — LIBBPF: THE ROAD TO V1.0 (wiki deprecation plan, full old->new API mapping)
===================================================================================

> NOTE: This wiki is adapted from the original [Google doc](https://docs.google.com/document/d/1UyjTZuPFWiPFyKk1tV5an11_iaRuec6U-ZESZ54nNTY) which also contains discussion in comments. This wiki is now source of truth, but Google doc will be kept around for historical reasons.

Libbpf has come a long way in the last few years. It became a mature and powerful library powering many BPF applications. So it’s only logical to finally reflect this maturity with the 1.0 version. 

Jump from 0.x to 1.0 is a major version bump, though, which gives libbpf an opportunity to break some backwards compatibility (within a reason, of course) and shed some of the cruft, inconsistencies, and sub-optimal (in retrospective) API choices: both to simplify developer experience through more coherent and uniform API and behavior, as well as to clean up and simplify some of the internal implementation details.

This document is attempting to document changes I have in mind for 1.0 and how API breakage and backwards compatibility is going to be handled in the transition period. The 1.0 version bump won’t happen overnight. My plan is to have a few more 0.x minor version releases to give users time and opportunity to migrate their usage of deprecated APIs to new recommended APIs. No existing functionality (with one exception for xsk.h part) is going to be removed without providing a way to achieve the same result with the new API. Deprecated APIs won’t be marked with `__attribute__((deprecated))` until replacement APIs have been released as part of an official 0.x release. This is to avoid the situation of getting deprecation warnings before there is an official libbpf version providing replacement APIs.

## Handling deprecation of APIs and functionality

There are three categories of deprecations proposed throughout this document.

1. **Deprecated APIs.** Such APIs will get marked with `__attribute__((deprecated))` some time before 1.0 release and will be completely removed in v1.0. For such APIs users are expected to migrate their code to use recommended APIs before 1.0 release. As mentioned above, we’ll go through a few more minor releases, so that gives at least a few months to perform migrations.

2. **Discouraged APIs.** Some APIs are not broken, but contribute to non-uniform API and/or sub-optimal experiences, but otherwise don’t cause extra maintenance. Often such APIs are also pretty frequently used, so it can cause a lot of unnecessary code churn for existing projects to migrate without a clear benefit. For such APIs, the plan is to move their definitions into a new **libbpf_legacy.h** header to “hide” them from the “official” APIs in libbpf.h, bpf.h, and btf.h. Eventually, we might consider removing them completely to clean up the code base. With such an approach, new users won’t be using outdated and discouraged APIs, hopefully.

3. **Stricter or changing behaviors.** Some changes and breakages are in the area of libbpf behavior and have no direct reflection in public APIs. One example is stricter handling of BPF program’s section name parsing. For such changes, where possible and appropriate, libbpf will log a warning about non-conforming behavior and recommendations on how to avoid such issues. In v1.0, instead of logging a warning, such “violations” will cause hard errors.

As we progress through API deprecation, a [Libbpf 1.0 migration guide](https://github.com/libbpf/libbpf/wiki/Libbpf-1.0-migration-guide) is populated with short instructions on how to migrate off of deprecated APIs and all the deprecation messages will give a link to corresponding sections of that wiki. This hopefully will make it as straightforward to migrate as possible.

## High-level behavior changes

### Low-level BPF APIs error reporting is changing

> Status: [done](https://patchwork.kernel.org/project/netdevbpf/list/?series=487853&state=*).
>
> Migration guidelines: [here](https://github.com/libbpf/libbpf/wiki/Libbpf-1.0-migration-guide#direct-error-code-returning-libbpf_strict_direct_errs).

Currently, some low-level BPF APIs (APIs in bpf.h, prefixed with bpf_) return errors following two different conventions:
  * -1 result and actual error set as errno (syscall convention);
  * while in other cases -Exxx is returned without setting errno (typical user-space convention, as well as kernel standard).

`errno` is notoriously inconvenient in practice and users often get it wrong (e.g., doing close(), printf(), etc, which might invalidate actual errno, before recording errno value). It’s much more convenient to get the actual error number directly. We’ll standardize on low-level APIs returning the value of -errno directly as a result. This matches the behavior of high-level API and is generally much less error-prone to handle. But, in addition, all low-level APIs will still set `errno` on every error. So if users prefer errno, they can still use it. Also, this will be compatible with high-level “constructor” APIs, returning pointers (see below).

This is potentially breaking if applications are doing exact `== -1` check, followed by `errno` check. -1 was never guaranteed (even syscall() documentation doesn’t state -1 will *always* be returned), but there is still code out there with such a pattern. Such applications would need to switch to < 0 checks. Given it’s impossible to smoothly transition from one convention to another, we’ll do our best to audit existing (open-source) code and make sure they do < 0 error checking. And after that start return `-errno` directly even before libbpf 1.0.

### All “constructor APIs” will return NULL on error

> Status: [done](https://patchwork.kernel.org/project/netdevbpf/list/?series=487853&state=*).
>
> Migration guidelines: [here](https://github.com/libbpf/libbpf/wiki/Libbpf-1.0-migration-guide#null-pointers-on-errors-libbpf_strict_clean_ptrs).

All constructor-like APIs that return a new “object”, e.g., `bpf_object__open()` variants, `btf__parse()`, `bpf_program__attach()` returning bpf_link, etc., will start returning NULL, not an error code encoded as a pointer. Current convention is extremely surprising to people not well-versed in kernel development, so leads to bad code like:

```c
struct bpf_link *link = bpf_program__attach(prog);
if (!link) { /* handle error, but not really */ }
```

In practice, if an error happens, the link won’t be NULL and the program will proceed to (most probably) crash in runtime. For a lot of such code paths, error is not very probable, so there is certainly a bunch of production code that is just a ticking bomb due to this convention. Practice shows that it’s easy to forget about this convention even for kernel developers.

While in most cases whether the operation failed with -EINVAL or -ENOMEM is not that important, libbpf will log human-friendly details on what went wrong (to the best of libbpf’s knowledge). But additionally, for cases where users do care about exact error, such constructor APIs will set errno, just like low-level APIs do. Errno is expected to be rarely needed, evidenced by BPF skeleton and perf_buffer/ring_buffer APIs, all of which return NULL on error.

As for handling the transition and minimizing the surprise factor, consider that in user-space all users of libbpf are supposed to use libbpf_get_error() API to check returned pointer for encoded error. Any application using their own PTR_ERR() implementation is technically guessing the implementation detail and is already broken in the strict sense of the word. So, taking that into account, libbpf_get_error() will start to return -EINVAL for NULL cases, handling both ERR_PTR() and NULL cases transparently. Everyone else is strongly encouraged to use libbpf_get_error() for the transition period.

`libbpf_get_error()` itself can be either deprecated and removed in v1.0 or become discouraged API and hidden away in libbpf_legacy.h. This can be discussed much later.

In summary, the error reporting approach across all APIs (low-level, high-level, both returning int and pointers) will be as follows:
  - for int-returning APIs that can fail, actual error is returned directly as -Exxx and errno is set to Exxx;
  - for pointer-returning (constructor) APIs, NULL is returned on error and errno is set to the underlying Exxx.

### xsk.{c,h} is moving into [libxdp](https://github.com/xdp-project/xdp-tools/tree/master)

> Status: [issue #270](https://github.com/libbpf/libbpf/issues/270)

AF_XDP parts of libbpf (xsk.h and xsk.c) will be removed from libbpf v1.0 and will become a part of [libxdp](https://github.com/xdp-project/xdp-tools/tree/master). The process is [underway](https://github.com/xdp-project/xdp-tools/pull/92) already. Toke Høiland-Jørgensen and Magnus Karlsson are working on this and should be done well before libbpf 1.0 is released. The intent is to make transition as painless as possible. The rationale of this change is that XSK parts of libbpf are more of a high-level user of libbpf APIs with its own high-level abstractions, rather than a fundamental BPF functionality that libbpf is striving to provide. It also is conceptually very close to XDP in general, so it will benefit users long term to have it be developed as part of libxdp.

### Stricter and more uniform BPF program section name (SEC()) handling

> Status: [issue #271](https://github.com/libbpf/libbpf/issues/271)

Libbpf is sometimes pretty lax about BPF program section names and usually cares only about a recognizable program type prefix, ignoring everything else. Historically there was one valid case when this was necessary: multiple entry-level BPF programs of the same type (e.g., two programs attaching to the same tracepoint). Since libbpf started supporting multiple BPF programs per same section, there is no more justification for such use.

On the other hand, having stricter and more uniform section name conventions is helpful to make advanced parsing easier. There are tentative plans to allow “pluggable” BPF program section name parsing to allow other libraries to inject their custom parsing logic (e.g., perf event names parsing), so standardization is important. Besides, having less variation in section names is less confusing for new users trying to infer what’s going on from open-source examples.

So the proposal is to:
  1. Use ‘/’ as a separator consistently. So no more “perf_event_whatever”, only “perf_event/whatever”.
  2. For section names not having any extra “parameters”, don’t allow anything extra beyond BPF program type. So no more “xdp_my_prog”, only “xdp”. And no “cgroup_skb/ingress/garbage”, only “cgroup_skb/ingress”.

During transition period libbpf will still handle such non-conforming section names successfully, but will emit a warning log message at runtime.

### Drop support for legacy BPF map declaration syntax

> Status: [issue #272](https://github.com/libbpf/libbpf/issues/272)

Legacy fixed-layout (through `struct bpf_map_def`) BPF map declaration in BPF code, residing in SEC("maps") will be dropped. Only BTF-defined maps will be supported starting from v1.0.

So instead of

```c
struct bpf_map_def SEC("maps") btf_map = {
        .type = BPF_MAP_TYPE_ARRAY,
        .max_entries = 4,
        .key_size = sizeof(int),
        .value_size = sizeof(struct ipv_counts),
};
```

only

```c
struct {
    __uint(type, BPF_MAP_TYPE_ARRAY);
    __uint(max_entries, 4);
    __type(key, int);
    __type(value, struct ipv_counts);
} btf_map SEC(".maps");
```
will be supported.

In the same vein, `BPF_ANNOTATE_KV_PAIR(btf_map, int, struct ipv_counts)` support will be dropped.

### Pinning path differences

> Status: [issue #273](https://github.com/libbpf/libbpf/issues/273)

Currently, BPF program pinning path is auto-derived from its section name, not its C function name. With multiple BPF programs per section it’s already broken. Further, given section name has special characters like ‘/’, it requires sanitization, making pin path still different from actual section name. All that just creates a convoluted behavior.

We’ll change this behavior to use BPF program’s C function name for the filename part of the pinning path. This matches behavior for maps and is more in line with multiple BPF programs per section. This is unfortunate potentially breaking change, but it’s almost inevitable to be really usable as a generic mechanism.

### Merging .rodata* and converged .data* + .bss

> Status: [issue #274](https://github.com/libbpf/libbpf/issues/274)

.rodata and other read-only sections (e.g., .rodata.str1.1) will be merged by libbpf into a final .rodata map (with accordingly adjusted BTF information). This will get rid of annoying warnings about .rodata.str1.1 and will allow developers to have custom .rodata sections, yet not cause multitude of BPF maps created. With BTF adjusted and BPF skeleton providing nice access to contents of .rodata, there is little downside to such approach.

Similarly, .data and .data.* will be merged together, just like .rodata.

Additionally, .bss is a historical legacy quirk of user-space static linkers (“Block Started by Symbol”…) and is quite confusing. Further, it’s annoying when BPF code changes zero initialization of a variable to non-zero value and suddenly one needs to update user-space references from `skel->bss->my_var` to `skel->data->my_var`. So to avoid such annoyances, .bss will be merged into .data by libbpf at open time (and in BPF skeleton), so all the non-read-only variables will be addressed through consistent `skel->data->my_var`.

During the transition period, `skel->bss` and `skel->data` will be the same pointer. Sometime around or after libbpf 1.0 release bpftool will be updated to stop generating skel->bss completely.

### Drop object name prefix from special map names (.rodata, .data, .kconfig)

> Status: [issue #275](https://github.com/libbpf/libbpf/issues/275)

Currently, special internal maps that libbpf creates for things like global and Kconfig variables contain (often truncated) object name along the special name suffix. E.g., “my_ob.rodata”. It has some serious inconveniences in practice. E.g., it’s almost impossible to guess the name of the resulting map (is it “my_ob.rodata” or “my_obje.rodata”, it’s almost never something logical like “my_obj.rodata”). On the other hand, that truncated object name is often insufficient in practice to match map to its BPF application. Further, with bpftool reporting PID of the “owning” process for maps and programs, it becomes quite easy and convenient to map given map to the BPF application, so name doesn’t play a big role in that.

So the proposal is to do away with this truncated prefix and settle on obvious “.rodata”, “.data”, “.kconfig” names. For the transition period, libbpf will be able to handle both conventions. In 1.0 only new-style names will be supported.

### btf.h APIs

Starting from the smaller and simpler set of APIs, let’s look at BTF-related APIs and what we want to do with them.

  - [#276](https://github.com/libbpf/libbpf/issues/276) `btf__finalize_data()` will be deprecated. It is used only for internal libbpf needs. Shouldn’t have been exposed, probably. Unlikely anyone is even relying on it.

  - [#277](https://github.com/libbpf/libbpf/issues/277) The following APIs are only used internally or by BCC. We’ll adapt BCC to not rely on these APIs and deprecate them.
    - `btf__get_map_kv_tids()` doesn’t make any sense now that BPF_ANNOTATE_KV_PAIR() is not supported;
    - `btf_ext__reloc_func_info()` is already marked deprecated and is not compatible with libbpf’s support for multiple BPF programs per section;
    - `btf_ext__reloc_line_info()` is in the similar boat;
    - `btf_ext__func_info_rec_size()` is just a specialized “extractor” of record size for specific types of .BTF.ext sections. Anyone iterating and handling .BTF.ext on their own will be able to implement this trivially;
    - `btf_ext__line_info_rec_size()`, same as above.

  - [#278](https://github.com/libbpf/libbpf/issues/278) `btf__load()` and `btf__get_from_id()` are used to “upload” and “download” BTF into/from the kernel. I propose to deprecate these two naming variants and introduce two new ones, reflecting their relationship to the kernel. E.g., `btf__load_into_kernel()` and `btf__load_from_kernel()` (or `btf__load_from_kernel_by_id()`) would be less confusing. Given they are not used that frequently, longer names don’t seem to pose a problem for usability.

  - [#279](https://github.com/libbpf/libbpf/issues/279) `btf__get_nr_types()` and `btf__get_raw_data()` don’t follow the name convention for getters of omitting “get” in the name. Appropriate names should be `btf__nr_types()` (`btf__type_cnt()`?) and `btf__raw_data()`. Further, `btf__get_nr_types()` confusingly returns number of types except VOID (or, when put alternatively, it returns type ID of the last BTF type), which leads to confusing and non-conventional iteration loop with <= instead of natural <:

```c
for (i = 0; i <= btf__get_nr_types(); i++) { ... }
```

So for the new `btf__nr_types()` I propose to fix this and return the number of all types that a user can iterate. Existing “get_” variants can stay as is as discouraged APIs in libbpf_legacy.h, they don’t need much maintenance.

  - [#280](https://github.com/libbpf/libbpf/issues/280) `libbpf_find_kernel_btf()` – its name should more correctly be `libbpf_load_vmlinux_btf()`, so the proposal is to add such a naming variant and discourage/deprecate the current one. Additionally, `libbpf_load_module_btf(const char *module_name)` will be added for completeness.

  - [#281](https://github.com/libbpf/libbpf/issues/281) `struct btf_dedup_opts` should be converted into extensible OPTS struct, similar to those used throughout most of the libbpf APIs. `dont_resolve_fwds` option will be dropped, it’s never used. `dedup_table_size` can be dropped as well, it’s only used by selftests to force hash collisions. We can drop that pretty safely. The only known user of `btf__dedup()()` API that accepts `btf_dedup_opts` is pahole, but it passes NULL for options. So there is little danger of breaking anyone. We can also use symbol versioning to introduce a new variant of `btf__dedup()`, accepting new-style opts struct. `btf_ext` argument would be supplied through opts (it rarely is provided).

  - [#283](https://github.com/libbpf/libbpf/issues/283) similarly, `struct btf_dump_opts` and `btf_dump__new()` will be converted to OPTS framework and new version of `btf_dump__new()` API will be introduced, looking like this:

```c
struct btf_dump *btf_dump__new(cosnt struct btf *btf,
                               btf_dump_printf_fn_t printf_fn, 
                               const btf_dump_opts *opts);
```

### bpf.h low-level APIs

- [#282](https://github.com/libbpf/libbpf/issues/282) Deprecate the whole zoo of `bpf_create_map_xattr()`, `bpf_create_map_node()`, `bpf_create_map_name()`, `bpf_create_map()`, `bpf_create_map_in_map_node()`, `bpf_create_map_in_map()` APIs in favor of a single unified OPTS-based one, with the name matching bpf syscall’s command (BPF_MAP_CREATE):

```c
int bpf_map_create(enum bpf_map_type map_type map_type,
                   const char *map_name,
                   unsigned int key_size,
                   unsigned int value_size,
                   unsigned int max_entries,
                   const struct bpf_map_create_opts *opts);
```

- [#284](https://github.com/libbpf/libbpf/issues/284) Similarly, deprecate `bpf_load_program_xattr()`, `bpf_load_program()`, `bpf_verify_program()` in favor of a single unified new API:

```c
int bpf_prog_load(enum bpf_prog_type type, const char *name,
                  const struct bpf_insn *insns, size_t insn_cnt,
                  const char *license,
                  const struct bpf_prog_load_opts *opts);
```

- `bpf_map_lookup_elem()` and `bpf_map_lookup_elem_flags()` would probably stay the same. While it’s a bit inconsistent to have specific _flags variant, both APIs seem to be holding up just fine and it’s not likely they would need to be extended, so to reduce the migration churn, it makes sense to leave them as is. If we ever need to extend them, adding another OPTS-based variant would be a way to go.

- Similarly, `bpf_prog_detach()` and `bpf_prog_detach2()` are not the most consistent APIs, but given they are sort of deprecated (due to `bpf_link`-based APIs), probably better to leave them as is for now.

- [#285](https://github.com/libbpf/libbpf/issues/285) `bpf_prog_attach()` and `bpf_prog_attach_xattr()` are probably OK to stay as is, but `bpf_prog_attach_xattr()`'s naming makes less and less sense with dropping all the xattr APIs. So we’ll converge to the convention used in high-level APIs and use `bpf_prog_attach_opts()` API name. We’ll end up with non-OPTS `bpf_prog_attach()` and OPTS-based `bpf_prog_attach_opts()`.

- [#286](https://github.com/libbpf/libbpf/issues/286) `bpf_prog_test_run_xattr()` and `bpf_prog_test_run()` will be deprecated in favor of already existing `bpf_prog_test_run_opts()`.

- [#419](https://github.com/libbpf/libbpf/issues/419) `bpf_load_btf()` has inconsistent naming (similar to `bpf_load_program()` and `bpf_create_map()`), and it doesn't allow to specify log level. So deprecate `bpf_load_btf()` in favor of `bpf_btf_load()` with OPTS.

- `bpf_prog_query()` and `bpf_task_fd_query()` will stay the same. They are rarely used and don’t suffer from constant expansion of API. I can be persuaded otherwise, though.

### libbpf.h high-level APIs

- [#287](https://github.com/libbpf/libbpf/issues/287) `bpf_object__open()`, `bpf_object__open_buffer()`, `bpf_object__open_xattr()` – deprecated in favor of `bpf_object__open_file()` and `bpf_object__open_mem()`.

- [#288](https://github.com/libbpf/libbpf/issues/288) Remove few options from struct bpf_object_open_opts:
  - `relaxed_core_relocs` weren’t honored for a long time now, remove it;
  - remove `attach_prog_fd`, it only works for a case of `bpf_object` containing a single BPF program or if all BPF programs are attached to the same target. Neither is a typical situation, so this option just leads to more confusion. Use `bpf_program__set_attach_target()` on individual bpf_program after bpf_object is open.

- [#289](https://github.com/libbpf/libbpf/issues/289) Deprecate `bpf_object__load_xattr()`. `bpf_object__load()` is enough. Anything else could be provided in open opts or set through setter APIs before the load.

- [#290](https://github.com/libbpf/libbpf/issues/290) Deprecate `bpf_object__unload()`. BPF objects are not re-loadable after unload. Use `bpf_object__close()` to unload and free up resources in one operation.

- [#291](https://github.com/libbpf/libbpf/issues/291) For completeness, add `bpf_object__set_name()`, to match `bpf_object__name()` getter.

- [#292](https://github.com/libbpf/libbpf/issues/292) Deprecate `bpf_object__find_program_by_title()` as an API. Searching by title (i.e., section name) is ambiguous with multiple BPF programs per section. Use `bpf_object__for_each_program()` macro to loop over all BPF programs and compare using `bpf_program__section_name()`.

- [#293](https://github.com/libbpf/libbpf/issues/293) Deprecate `bpf_object__next()` API and `bpf_object__for_each_safe()` macro. There is little utility to it, but it’s not thread-safe. Any application that needs to iterate over all its bpf_objects can keep track of them on their own easily.

- [#294](https://github.com/libbpf/libbpf/issues/294) Deprecate `bpf_object__set_priv()`/`bpf_object__priv()`, `bpf_program__set_priv()`/`bpf_program__priv()` and `bpf_map__set_priv()`/`bpf_map__priv()`. libbpf entities are not arbitrary containers for user’s private data. In cases where users should provide callbacks, they will be able to provide their own context at the time of callback registration.

- [#295](https://github.com/libbpf/libbpf/issues/295) `libbpf_find_vmlinux_btf_id()` supports only vmlinux BTF, but no kernel module support. Should we add another API that would search for types across kernel modules and return kernel module BTF FD, in addition to BTF type ID? Probably, but that could be done later. So, bottom line, just leave this API be for now.

- [#296](https://github.com/libbpf/libbpf/issues/296) `bpf_program__next()` and `bpf_program__prev()` are confusingly named. They are really “methods” of bpf_object, so should be called `bpf_object__next_program()` and `bpf_object__prev_program()`. Luckily, they are mostly used through `bpf_object__for_each_program()` macro, so deprecate confusingly named APIs and update the macro to use new ones. `bpf_map__next()` and `bpf_map__prev()` suffer from the same problem. Deal with them similarly.

- [#297](https://github.com/libbpf/libbpf/issues/297) Deprecate `bpf_program__title()` in favor of `bpf_program__section_name()`. “Title” term is confusing and unconventional, it’s `SEC()` in code and “section name” everywhere else.

- [#298](https://github.com/libbpf/libbpf/issues/298) `bpf_program__size()` is mildly confusing, though not broken by any means. Add `bpf_program__insn_cnt()` and `bpf_program__insns()` getters to get access to finalized BPF assembly of each BPF program. This will help with some cases where deprecated `bpf_program__set_prep()` might have been used, see below.

- [#299](https://github.com/libbpf/libbpf/issues/299) `bpf_program__set_prep()` is an obscure, less-known API which adds unnecessary complexity to the public API and internal implementation. Deprecate it. For cases when someone do still want to adjust and/or clone BPF programs, it could be achieved by using new `bpf_program__insns()` and `bpf_program__insn_cnt()` APIs to get raw (but libbpf-processed for CO-RE, bpf-to-bpf calls, map relocations, etc) BPF instructions and proceed with low-level `bpf_prog_load()` API.

- [#300](https://github.com/libbpf/libbpf/issues/300) Deprecate `bpf_program__pin_instance()`, `bpf_program__unpin_instance()` and `bpf_program__nth_fd()`. With no `bpf_program__set_prep()`, there is no concept of multiple bpf_program instances.

- [#301](https://github.com/libbpf/libbpf/issues/301) Deprecate `bpf_program__load()`. In general, it’s impossible for libbpf to load an individual BPF program in isolation. libbpf fully embraced the concept of bpf_object as a collection of related bpf_programs and bpf_maps (and global variables, kconfig, ksym, etc). So this API is just confusing and impossible to support properly.

- [#302](https://github.com/libbpf/libbpf/issues/302) Remove `bpf_object__find_map_by_offset()`. API created with simplistic assumptions about BPF map definitions. It hasn’t worked for a while, so just remove it finally.

- [#303](https://github.com/libbpf/libbpf/issues/303) Remove `bpf_map__for_each()` macro in favor of better named `bpf_object__for_each_map()`.

- [#304](https://github.com/libbpf/libbpf/issues/304) Discourage `bpf_map__resize()`, which is an alias to more clearly named `bpf_map__set_max_entries()`.

- [#305](https://github.com/libbpf/libbpf/issues/305) Discourage `bpf_map__def()`. It is rarely used and non-extensible. Provide individual getter APIs to compensate (if we are still missing some of them).

- [#306](https://github.com/libbpf/libbpf/issues/306) Deprecate `bpf_map__is_offload_neutral()`. It’s most probably broken already. PERF_EVENT_ARRAY isn’t the only map that’s not suitable for hardware offloading. Unlikely anyone is using this and it is a maintenance burden, if we were to make it correct.

- [#307](https://github.com/libbpf/libbpf/issues/307) Discourage `bpf_map__get_pin_path()` and use consistent naming for getter, `bpf_map__pin_path()`.

- [#308](https://github.com/libbpf/libbpf/issues/308) Deprecate `bpf_prog_load()` and `bpf_prog_load_xattr()` in favor of `bpf_object__open_{mem, file}()` and `bpf_object__load()` combo.

- [#309](https://github.com/libbpf/libbpf/issues/309) `bpf_set_link_xdp_fd()` / `bpf_set_link_xdp_fd_opts()` / `bpf_get_link_xdp_id()` / `bpf_get_link_xdp_info()` don’t follow libbpf naming guidelines. They are akin to object-less libbpf helpers, so should be called with `libbpf_` prefix. They also have a distinct low-level feel. So:
  - Discourage them (move them to libbpf_legacy.h);
  - Introduce OPTS-based `libbpf_xdp_set_prog_fd()` and `libbpf_xdp_get_info()` or something along those lines. I hope XDP-using users can make good suggestions here. And probably move them to bpf.h.

- [#310](https://github.com/libbpf/libbpf/issues/310) `bpf_perf_event_read_simple()` is a low-level and dangerous API that could be used to implement custom perf buffer consumption, but is hard to actually use correctly. Deprecate it. There is no reason to use it with `perf_buffer__poll()` and `perf_buffer__consume()` APIs available. If anyone really needs custom perf buffer consumption, re-implementing `bpf_perf_event_read_simple()` shouldn’t be a problem (for them) at that point.

- [#311](https://github.com/libbpf/libbpf/issues/311) `perf_buffer` options are not OPTS-based. Also perf_buffer constructor APIs (`perf_buffer__new()` and `perf_buffer__new_raw()`) could use a bit better design. But `perf_buffer__new()` is a very popular API used in many programs, so deprecating it will cause almost universal code churn. We also didn’t have a need to extend any of the opts yet (in more than 18 months now), so most practical approach would be to leave them as is. But if we were to change those APIs, I’d switch `perf_buffer_opts` and `perf_buffer_raw_opts` into OPTS-based ones and made constructor APIs look like this:

```c
struct perf_buffer *
perf_buffer__new(int map_fd, size_t page_cnt,
                 perf_buffer_sample_fn sample_cb,
                 perf_buffer_lost_fn lost_cb,
                 const struct perf_buffer_opts *opts);

struct perf_buffer *
perf_buffer__new_raw(int map_fd, size_t page_cnt,
                     struct perf_event_attr *attr,
                     perf_buffer_event_fn event_cb,
                     const struct struct perf_buffer_raw_opts *opts);
```

But it doesn’t seem worthwhile as it doesn’t buy as much. But I’d love to see strong opinions on this.

- [#312](https://github.com/libbpf/libbpf/issues/312) I never had to use `bpf_probe_prog_type()` / `bpf_probe_map_type()` / `bpf_probe_helper()` / `bpf_probe_large_insn_limit()` in practice, but they don’t seem to cause much maintenance issues. So I’m inclined to leave them as is, unless someone objects strongly. But we need to have a wider discussion about libbpf's convenience probing APIs. There is a niche demand for various xxx-to-string conversion APIs (e.g., to convert bpf_prog_type to string representation), so we should make a decision whether it's libbpf's first-class citizens and make appropriate implementations high-quality and complete.

- [#313](https://github.com/libbpf/libbpf/issues/313) `bpf_prog_info_linear`-related APIs. They completely fail libbpf naming guidelines (they use `bpf_program__` prefix, but they don’t operate on bpf_program objects). `bpf_program__get_prog_info_linear()` doesn’t even declare that it is expecting enum bpf_prog_info_array and just goes with generic __u64. They seem to be only used in perf and bpftool, so updating all users seems doable. At the very least, I’d fix the naming to be `libbpf_` prefixed. But I need input from Song, Arnaldo and others here.





===================================================================================
PART 4 — GITHUB RELEASE NOTES v0.6.0 .. v1.4.0 (verbatim, spanning the 1.0 transition)
===================================================================================

## libbpf v0.6.0 release notes

## Important updates towards Libbpf 1.0
  - a first big batch of deprecated APIs; compiler will let you know or grep for "LIBBPF_DEPRECATED". Please also double-check https://github.com/libbpf/libbpf/wiki/Libbpf-1.0-migration-guide.
  - documentation for a bunch of APIs added, available on https://libbpf.readthedocs.io/en/latest/api.html;
  - libbpf version APIs added: compile-time `LIBBPF_MAJOR_VERSION`/`LIBBPF_MINOR_VERSION` and runtime `libbpf_major_version()`/`libbpf_minor_version()`/`libbpf_version_string()`;
  - stricter logic for `SEC()` definition handling (opt-in until libbpf v1.0); see https://github.com/libbpf/libbpf/wiki/Libbpf:-the-road-to-v1.0#stricter-and-more-uniform-bpf-program-section-name-sec-handling for details.
  - function name will be used when pinning if `LIBBPF_STRICT_SEC_NAME` strict mode flag is specified;

## New features and APIs:
  - support custom `.rodata.*` and `.data.*` data sections;
  - `bpf_program__attach_kprobe()` and `bpf_program__attach_uprobe()` supports older kernels now (don't forget about `bpf_link__destroy()` when you are done!);
  - `BPF_MAP_TYPE_PROG_ARRAY` can be initialized statically with syntax similar to map-in-map initialization (see https://github.com/libbpf/libbpf/commit/472c0726e84d821186a315889c885b23895b155e for an example);
  - libbpf-less "light" skeleton gained new capabilities and got a bunch of fixes;
  - BTF support for `BTF_KIND_DECL_TAG` and `BTF_KIND_TYPE_TAG`;
  - new `bpf_prog_load()` and `bpf_map_create()` APIs supersede a whole zoo of to-be-deprecated APIs;
  - support for writable raw tracepoints (`SEC("raw_tp.w/...")`) added;
  - `btf__add_btf()` API for appending entire contents of BTF to another BTF object;
  - `bpf_program__insns()` and `bpf_program__insn_cnt()` to access underlying BPF assembly instructions; can be used for inspection or BPF program cloning.
  - a bunch of older APIs (`perf_buffer__new()`, `btf__dedup()`, `btf_dump__new()`, etc) were modernized to use OPTS infrastructure.

## BPF-side APIs and features:
  - unstable BPF helpers (kernel function calls) support for kernel modules;
  - `bpf_trace_vprintk()` helper and corresponding `bpf_printk()` macro enhancements. Note, `bpf_printk()` will now attempt to use static global functions, so on very old kernels this might break existing programs. Please `#define BPF_NO_GLOBAL_DATA` before `#include <bpf/bpf_helpers.h>` if that's the case for you.
  - `bpf_get_branch_snapshot()` helper;
  - `bpf_skc_to_unix_sock()` helper;
  - `bpf_find_vma()` helper;
  - `SEC("tc")` added as a replacement for `SEC("classifier")`.

## Bug fixes and compatibility improvements:
  - libbpf now guarantees that all FDs for BPF programs, maps, BTFs, and links are strictly greater than 0, which is important for some BPF UAPIs;
  - no need to use `__uint(key_size, ...)` for special BPF maps (e.g., `BPF_MAP_PERF_EVENT_ARRAY`). Libbpf automatically downgrades `__type(key, int)` into key_size, if a map doesn't support BTF types for keys and values;
  - endianness fixes in `BPF_CORE_READ_BITFIELD_PROBED()` macro;
  - `btf_dump__dump_type_data()` improvements for handling unaligned data;
  - various fixes and improvements found though fuzzing and sanitizers.


**Full Changelog**: https://github.com/libbpf/libbpf/compare/v0.5.0...v0.6.0


## libbpf v0.7.0 release notes

## Important updates towards Libbpf 1.0
  - no need for explicit `setrlimi(RLIMIT_MEMLOCK)` when `LIBBPF_STRICT_AUTO_RLIMIT_MEMLOCK` is passed to `libbpf_set_strict_mode()`. libbpf will determine whether this is necessary automatically based on kernel's support for memcg-based memory accounting for BPF;
  - legacy BPF map definitions (using `struct bpf_map_def`) are deprecated when `LIBBPF_STRICT_MAP_DEFINITIONS` is passed to `libbpf_set_strict_mode()`. Please use BTF-defined map definitions.
  - another batch of API deprecations.

## New features and APIs:
  - ability to control and capture BPF verifier log output on per-object and per-program level;
  - CO-RE support and other improvements for "light skeleton";
  - further libbpf API documentation improvements;
  - new feature-probing APIs (`libbpf_probe_bpf_helper()`, `libbpf_probe_bpf_prog_type()`, `libbpf_probe_bpf_map_type()`);
  - new streamlined low-level XDP APIs (`bpf_xdp_attach()`, `bpf_xdp_detach()`, `bpf_xdp_query()`, `bpf_xdp_query_id()`);
  - new `SEC("xdp.frags")`, `SEC("xdp.frags/cpumap")`, `SEC("xdp.frags/devmap")` section definitions;
  - new `SEC("iter.s/xxx")` section definitions for sleepable BPF iterator programs.

## BPF-side APIs and features:
  - `bpf_loop()` helper;
  - `bpf_func_arg()`, `bpf_func_ret()`, `bpf_func_arg_cnt()` helpers;
  - added syscall-specific `PT_REGS_xxx()` macros for retrieving syscall arguments;
  - added `BPF_KPROBE_SYSCALL()` helper macro for syscall kprobes;
  - `bpf_get_retval()` and `bpf_set_retval()` helpers;
  - `bpf_xdp_get_buff_len()` helper;
  - `bpf_copy_from_user_task()` helper for sleepable BPF programs.

## Bug fixes and compatibility improvements:
  - fixed compilation error for C++ due to `btf_dump__new()` macro magic;
  - improved `LINUX_VERSION_CODE` detection for Ubuntu;
  - improved multiple kprobe support for legacy kprobe mode on old kernels;
  - improved compilation when system BTF UAPI headers are outdated;
  - a bunch of fixes of `PT_REGS_PARMn*()` macros for various architectures.

**Full Changelog**: https://github.com/libbpf/libbpf/compare/v0.6.0...v0.7.0


## libbpf v0.8.0 release notes

## New features and APIs:
- major improvements for `uprobe`/`uretprobe` programs:
  - support auto-resolution of binaries and shared libraries from PATH, if necessary;
  - support attaching by function names (only by IP was supported before);
- support attaching to USDTs (`SEC("usdt/...")` and `bpf_program__attach_usdt()`) with initially supported architectures:
  - x86-64 (amd64);
  - x86 (i386);
  - s390x;
  - ARM64 (aarch64);
  - RISC V (riscv);
- improved BPF verifier log reporting for CO-RE relocation failures (no more obscure "invalid func unknown#195896080" errors);
- auto-adjust BPF ringbuf size according to host kernel's page size requirements;
- high-level BPF map APIs: `bpf_map__lookup_elem()`, `bpf_map__update_elem()`, etc that validate key/value buffer sizes;
- `bpf_link_create()` can create all bpf_link-based (including raw_tp, fentry/fexit, etc), falling back to `bpf_raw_tracepoint_open()` on old kernels transparently;
- support opting out from auto-loading BPF programs declaratively with `SEC("?...")`;
- support opting out from auto-creation of declarative BPF maps with `bpf_map__set_autocreate()`;
- support multi-kprobes (`SEC("kprobe.multi/...")` and `bpf_program__attach_kprobe_multi_opts()`);
- support target-less `SEC()` programs (e.g., `SEC("kprobe")`, `SEC("tp")`, etc);
- support BPF sub-skeletons for "incomplete" BPF object files (requires matching `bpftool` to generate `.subskel.h`);
- BPF cookie support for `fentry`/`fexit`/`fmod_ret` BPF programs (`bpf_program__attach_trace_opts()`);
- support for custom `SEC()` handlers (`libbpf_register_prog_handler()`).

## BPF-side API
- BPF-side USDT APIs. See new `usdt.bpf.h` header:
  - `BPF_USDT()` program wrapper macro;
  - `bpf_usdt_arg()`, `bpf_usdt_arg_cnt()`, `bpf_usdt_cookie()` helpers;
- new `bpf_core_field_offset()` CO-RE helper and support `bpf_core_field_size(type, field)` forms;
- `barrier()` and `barrier_var()` macros for improving BPF code generation;
- `__kptr` and `__kptr_ref` tags added;
- ARC architecture support in `bpf_tracing.h` header;
- new BPF helpers:
  - `bpf_skb_set_tstamp()`;
  - `bpf_ima_file_hash()`;
  - `bpf_kptr_xchg()`;
  - `bpf_map_lookup_percpu_elem()`.

## Bug fixes
- netlink bug fixes;
- libbpf.pc fixes to support patch releases properly;
- `BPF_MAP_TYPE_PERF_EVENT_ARRAY` map auto-pinning fix;
- minor CO-RE fixes and improvements for some corner cases;
- various other small fixes and improvements.

**Full Changelog**: https://github.com/libbpf/libbpf/compare/v0.7.0...v0.8.0


## libbpf v1.0.0 release notes

# Libbpf 1.0 is here!

## User-space-side features and APIs:
- **All deprecated APIs and features removed!**
- support for syscall-specific kprobe/kretprobe (`SEC("ksyscall/<syscall_name>")` and `SEC("kretsyscall/<syscall_name>")`);
- support for sleepable uprobe BPF programs (`SEC("uprobe.s")`);
- support for per-cgroup LSM BPF programs (`SEC("lsm_cgroup")`);
- support for new BPF CO-RE relocation `TYPE_MATCHES`;
- `bpf_prog_load()` and `bpf_map_create()` are now smarter about handling program and map name on old kernels (it will be ignored if kernel doesn't support names);
- `BTF_KIND_ENUM64` support;
- increase tracing attachment (kprobe/uprobe/tracepoint) robustness by using tracefs or debugfs, whichever is mounted;
- new APIs for converting BPF enums to their string representation:
  - `libbpf_bpf_prog_type_str()`;
  - `libbpf_bpf_map_type_str()`;
  - `libbpf_bpf_link_type_str()`;
  - `libbpf_bpf_attach_type_str()`;
- `bpf_program__set_autoattach()` and `bpf_program__autoattach()` to allow opting out from auto-attaching of BPF program by BPF skeleton;
- `perf_buffer__buffer()` API to give access to underlying per-CPU buffer for BPF ringbuf;
- `bpf_obj_get_opts()` API for more flexible fetching of BPF kernel objects' information.

## BPF-side features and APIs;
- `bpf_core_type_matches()` helper macro to emit `TYPE_MATCHES` CO-RE relocations;
- USDT support now doesn't rely on BPF CO-RE;
- new and improved `BPF_KSYSCALL()` macro for tracing syscalls, which abstracts away a lot of kernel- and architecture-specific differences;
- new BPF helpers:
  - `bpf_skc_to_mptcp_sock()`;
  - `bpf_dynptr_from_mem()`;
  - `bpf_ringbuf_reserve_dynptr()`, `bpf_ringbuf_submit_dynptr()`, `bpf_ringbuf_discard_dynptr()`;
  - `bpf_dynptr_read()`, `bpf_dynptr_write()`;
  - `bpf_dynptr_data()`;
  - `bpf_tcp_raw_gen_syncookie_ipv4()`, `bpf_tcp_raw_gen_syncookie_ipv6()`, `bpf_tcp_raw_check_syncookie_ipv4()`, `bpf_tcp_raw_check_syncookie_ipv6()`;
  - `bpf_ktime_get_tai_ns()`.

## Bug fixes
- fix power-of-2 check when adjusting BPF ringbuf map size;
- improve robustness of pointer size determination in BTF processing;
- symbol offset calculation logic fixes for uprobes and USDTs;
- fixes for clean up of legacy kprobe/uprobe attachments on partial failures;
- fix register definition for riscv architecture;
- improve robustness of reused map name handling.

**Full Changelog**: https://github.com/libbpf/libbpf/compare/v0.8.0...v1.0.0


## libbpf v1.0.1 release notes

## Fixing few issues that were reported since v1.0 release:

- fix inadvertently  changed `struct bpf_object_open_opts` memory layout;
- fix btf.h header relying on `struct enum64` type defined in kernel UAPI headers;
- fix NULL pointer exception in API btf_dump__dump_type_data;
- remove `struct btf_map_def` accidentally left in bpf_helpers.h header.

Also libbpf will attempt to load vmlinux BTF from [well known locations](https://github.com/libbpf/libbpf/commit/0420f75dbcf732e3230ae212970b33a80026e225) both ELF file (.BTF section) or as raw BTF binary data.

**Full Changelog**: https://github.com/libbpf/libbpf/compare/v1.0.0...v1.0.1


## libbpf v1.1.0 release notes

## User space-side features and APIs:

- user-space ring buffer (`BPF_MAP_TYPE_USER_RINGBUF`) support;
- new [documentation page](https://libbpf.readthedocs.io/en/latest/program_types.html) listing all recognized `SEC()` definitions;
- BTF dedup improvements:
  - unambiguous fwd declaration resolution for structs and unions;
  - better handling of some corner cases with identical structs and arrays;
  - mixed enum and enum64 forward declaration resolution logic;
- `bpf_{link,btf,pro,mapg}_get_fd_by_id_opts()` and `bpf_get_fd_by_id_opts()` APIs;
- libbpf supports loading raw BTF for BPF CO-RE from known search paths;
- support for new cgroup local storage (`BPF_MAP_TYPE_CGRP_STORAGE`);
- libbpf will only add `BPF_F_MMAPABLE` flag for data maps with *global* (i.e., non-static) vars;
- latest Linux UAPI headers with lots of changes synced into include/uapi/linux.

## BPF-side features and APIs;

- `BPF_PROG2()` macro added that supports struct-by-value arguments;
- new BPF helpers:
  - `bpf_user_ringbuf_drain()`;
  - `cgrp_storage_get()` and `cgrp_storage_delete()`.

## Bug fixes
- BTF-to-C converter fixes:
  - better handling of padding corner cases;
  - `btf__align_of()` determines packed structs better now;
  - improved handling of enums of non-standard sizes;
- USDT spec parsing improvements;
- overflow handling fixes for ringbufs;
- Makefile fixes to support cross-compilation for 32-bit targets;
- fix crash if `SEC("freplace")` programs don't have `attach_prog_fd` set;
- better handling of file existence checks when running as non-root with enhanced capabilities;
- a bunch of small fixes:
  - ELF handling improvements;
  - fix memory leak in USDT argument parsing logic;
  - fix NULL dereferences in few corner cases;
  - improved netlink attribute iteration handling.

**Full Changelog**: https://github.com/libbpf/libbpf/compare/v1.0.1...v1.1.0


## libbpf v1.2.0 release notes

## User space-side features and APIs:

- completely overhauled ["Libbpf overview"](https://libbpf.readthedocs.io/en/latest/libbpf_overview.html) landing documentation page;
- support attaching to uprobes/uretprobes to functions defined in Android APK archives;
- support for BPF link-based `struct_ops` programs:
  - `SEC(".struct_ops.link")` annotations;
  - `bpf_map__attach_struct_ops()` attach API;
  - `bpf_link__update_map()` link update API;
- support sleepable `SEC("struct_ops.s")` programs;
- improved thread-safety of libbpf print callbacks and `libbpf_set_print()`;
- improve handling and reporting of missing BPF kfuncs;
- `bpf_{btf,link,map,prog}_get_info_by_fd()` APIs;
- `bpf_xdp_query_opts()` supports fetching XDP/XSK supported features;
- `perf_buffer__new()` allows customizing notification/sampling period now;
- BPF verifier logging improvements:
  - pass-through BPF verifier log level and flags to kernel as is;
  - support `log_true_size` for getting required log buffer size to fit BPF verifier log completely;
- allow precise control over kprobe/uprobe attach mode: legacy, perf-based, link-based.


## BPF-side features and APIs;

- support for BPF open-coded iterators: `bpf_for()`, `bpf_repeat()`, `bpf_for_each()`;
- `bpf_ksym_exists()` macro to check existence of ksyms/kfuncs and kconfig values;
- `BPF_UPROBE()` and `BPF_URETPROBE()` macros;
- `BPF_KPROBE()` and `BPF_UPROBE()` macros allow fetching up to 8 passed in registers arguments, depending on architecture support;
- `BPF_KSYSCALL()` supports fetching all 6 syscall arguments now;
- LoongArch support in bpf_tracing.h;
- USDT support for 32-bit ARM architecture.


## Bug fixes

- fix legacy kprobe events names sanitization;
- fix clobbering errno in some cases;
- fix BPF map's `BPF_F_MMAPABLE` flag sanitization;
- fix BPF-side USDT support code on s390x architecture;
- fix `BPF_PROBE_READ{_STR}_INTO()` on s390x architecture;
- fix kernel version setting for Debian kernels;
- fix netlink protocol handling in some cases;
- improve robustness of attaching to legacy kprobes and uprobes;
- fix double-free during static linking empty ELF sections;
- a bunch of other small fixes here and there.


**Full Changelog**: https://github.com/libbpf/libbpf/compare/v1.1.0...v1.2.0


## libbpf v1.3.0 release notes

## User space-side features and APIs

- support for `netfilter` programs is added:
  - `SEC("netfilter")` is now available
  - API function `bpf_program__attach_netfilter()` is now available
- support for `tcx` BPF programs is added:
  - the following new SEC definitions are now available:
    - `SEC("tc/egress")`
    - `SEC("tc/ingress")`
    - `SEC("tcx/egress")`
    - `SEC("tcx/ingress")`
  - the following SEC definitions are now considered legacy:
    - `SEC("tc")`
    - `SEC("action")`
    - `SEC("classifier")`
  - functions `bpf_prog_attach_opts()` and `bpf_prog_query_opts()` are extended to work with `tcx` programs, plus two new API functions are added:
    - `bpf_prog_detach_opts()`
    - `bpf_program__attach_tcx()`
- support for multi-uprobe programs is added:
  - the following new SEC definitions are now available:
    - `SEC("uprobe.multi")`
    - `SEC("uprobe.multi.s")`
    - `SEC("uretprobe.multi")`
    - `SEC("uretprobe.multi.s")`
  - plus a new API function:
    - `bpf_program__attach_uprobe_multi()`
- support for section `SEC("usdt.s")` is added for sleepable `usdt` programs;
- support for Unix domain socket cgroup BPF programs is added the following new SEC definitions are now available:
  - `SEC("cgroup/connect_unix")`
  - `SEC("cgroup/sendmsg_unix")`
  - `SEC("cgroup/recvmsg_unix")`
  - `SEC("cgroup/getpeername_unix")`
  - `SEC("cgroup/getsockname_unix")`
- new `LIBBPF_OPTS_RESET()` utility macro;
- new `bpf_object__unpin()` function to complement existing `bpf_object__pin()`;
- new API functions for work with ring buffers:
  - `ring_buffer__ring()`
  - `ring__producer_pos()`
  - `ring__consumer_pos()`
  - `ring__avail_data_size()`
  - `ring__size()`
  - `ring__map_fd()`
  - `ring__consume()`
- `path_fd` support for `bpf_obj_pin()` and `bpf_obj_get()`;
- uprobe SEC matcher extended to allow golang symbols;
- uprobe support for symbols versioning;
- `bpf_map__set_value_size()` can now be used to resize memory mapped region for memory mapped maps;
- `struct bpf_xdp_query_opts` extended with `xdp_zc_max_segs` output field;
- basic BTF sanity check pass added to reject bogus BTF.

## BPF-side features and APIs

- triple-underscore flavors for kfunc relocation: like with CO-RE structs `___.*` suffix is ignored when kfunc relocations are resolved;
- `__percpu_kptr` macro definition in `bpf_helpers.h`;
- support for exception callbacks, use `__attribute__(btf_decl_tag("exception_callback:<func_name>"))` to specify exception callback for a program;

## Bug fixes

- fix for btf_dump__dump_type_data() when type contains bitfields;
- fix for correct work of offsetof() and container_of() macro with CO-RE;
- no longer attempt to load modules BTF when resolving CO-RE relocations if CAP_SYS_ADMIN are absent;
- regex based function search for "kprobe.multi/" programs no longer attempts to trace functions that cannot be traced;
- bpf_program__set_type() no longer resets sec_def if it is set to a custom fallback SEC handler;
- fix for memory leak possible after bpf_program__set_attach_target() call;


## libbpf v1.4.0 release notes

## User space-side features and APIs

- support for BPF token throughout low-level and high-level APIs (see also `LIBBPF_BPF_TOKEN_PATH` envvar);
- a bunch of struct_ops functionality added, mostly around handling multi-kernel compatibility using BPF CO-RE principles and approaches:
  - support struct_ops defined in kernel modules;
  - support "flavor" suffixes (`___smth`) for struct_ops types, allowing to define two incompatible definitions for the same target struct_ops kernel type;
  - support disabling/enabling auto-creation of struct_ops variables (maps):
    - `SEC("?.struct_ops")` and `SEC("?.struct_ops.link")` are now supported, default to not auto-create struct_ops map;
    - `bpf_map__set_autocreate()` is now honored for struct_ops maps;
  - disabling auto-creation of struct_ops variable (map) disables auto-loading of related BPF programs (unless they are shared between multiple struct_ops), which means that disabling struct_ops map creation behaves naturally w.r.t. related BPF programs and doesn't require explicitly disabling them from auto-loading;
  - support struct_ops "shadow type" through BPF skeleton, allowing to set/adjust custom data fields *and* also set/reset/change specific BPF programs implementing struct_ops' callbacks;
- BPF arena map support;
- BPF cookie support for raw tracepoint BPF programs in attach APIs;
- helpful error messages added to libbpf logs when attempting to use `struct bpf_program` or `struct bpf_map` instances there were not loaded or created, respectively;
- `SEC("sk_skb/verdict")` support;

## BPF-side features and APIs

- support global subprog argument tagging:
  - `__arg_ctx`, `__arg_nonnull`, `__arg_nullable`, `__arg_trusted`, and `__arg_arena` annotations added;
  - for kprobe/uprobe, and perf_event BPF program types, support fallback logic making `__arg_ctx` work on older kernels that don't yet support `__arg_ctx` (i.e., `arg:ctx` decl tag) annotation natively;
- `bpf_core_cast()` macro added, improving ergonomics of `bpf_rdonly_cast()` BPF helper;
- support `__arena` tagged global variables, which are automatically put into BPF arena map;
- `__long()` macro added for specifying 64-bit values when declaring BTF-defined maps;
- better GCC-BPF support in BPF CO-RE macros in `bpf_core_read.h` header;

## Bug fixes

- fix `faccessat()` internal usage, breaking Android versions of libbpf;
- use `OPTS_SET()` in `bpf_xdp_query()` for better backward/forward compatibility;
- fix inner map's `max_entries` setting logic;
- `btf_ext__raw_data()` and `btf__new_split()` APIs are added back, they were "lost" during libbpf v1.0 release process;
- ignore DWARF sections in BPF linker sanity checks, improving handling of some corner cases;
- fix potential NULL dereference when handling corrupted ELF files.

**Full Changelog**: https://github.com/libbpf/libbpf/compare/v1.3.0...v1.4.0
