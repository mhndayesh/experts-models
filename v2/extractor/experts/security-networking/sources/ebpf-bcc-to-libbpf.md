# BCC to libbpf + CO-RE conversion (eBPF API changes)

The `BPF_HASH(name, ktype, vtype)` map macro is replaced by an explicit struct with `__uint(type, BPF_MAP_TYPE_HASH)` annotated `SEC(".maps")`.
The `BPF_ARRAY(name, type, size)` macro is replaced by an explicit `BPF_MAP_TYPE_ARRAY` struct annotated `SEC(".maps")`.
The `BPF_PERF_OUTPUT(name)` macro is replaced by an explicit `BPF_MAP_TYPE_PERF_EVENT_ARRAY` struct annotated `SEC(".maps")`.
The `map.lookup(&key)` method is replaced by `bpf_map_lookup_elem(&map, &key)`.
The `map.update(&key, &val)` method is replaced by `bpf_map_update_elem(&map, &key, &val, 0)`.
The `events.perf_submit(ctx, data, len)` method is replaced by `bpf_perf_event_output(ctx, &events, BPF_F_CURRENT_CPU, data, len)`.
BCC's implicit `#include <linux/...>` kernel headers are replaced by a single `#include "vmlinux.h"`.
libbpf requires explicit `#include <bpf/bpf_helpers.h>` and `#include <bpf/bpf_core_read.h>` (BCC needed none).
Direct kernel struct field access `ptr->field->subfield` is replaced by `BPF_CORE_READ(ptr, field, subfield)`.
The BCC kprobe form `int kprobe__func(struct pt_regs *ctx, args)` is replaced by `SEC("kprobe/func") int BPF_KPROBE(kprobe__func, args)`.
BCC's implicit section naming is replaced by an explicit `SEC("...")` annotation on every program.
BCC's compile-time `#define` config substitution is replaced by global `const volatile` variables.
BCC runtime compilation is replaced by a generated skeleton loaded via `name__open()`, `name__load()`, and `name__attach()`.
User space reads global variables via `skel->rodata`, `skel->bss`, or `skel->data`.
`bpf_trace_printk()` is replaced by `bpf_printk()` (with a 3-argument limit).
Static helper functions must be marked `static __always_inline`.
