# FD.io VPP (Vector Packet Processor) Release Notes — API changes, deprecations, removals

Source: https://docs.fd.io/vpp/25.02/aboutvpp/releasenotes/ and the per-release pages
(v25.02.html, v24.10.html, v24.06.html, v24.02.html). The API-message lists below are
reproduced verbatim from each release's "API changes" section; the marker in parentheses
is the release-notes diff marker: "only in image" = newly added this release,
"only in file" = present only in the previous .api reference file and removed from the
built image this release, "definition changed" = message signature changed.

---

## VPP 25.02

"more than 269 commits since the previous release, including 100 fixes."

### Features
- Crypto (ipsecmb): Bump to ipsecmb v2.0
- DPDK: Updated to version 24.11.1 and rdma-core 55.0
- Host Stack: Added request repeating to HTTP client and UDP proxying in HTTP/1.1
- Marvell Armada: Initial DSA support
- Marvell Octeon: Hardware VLAN tagging, crypto framework, and HMAC-MD5/ChachaPoly support
- Snort: API functions for plugin integration
- BFD: Add support for multihop
- Segment Routing: Adding support to SRv6 uA behavior
- Session Layer: VCL transport attributes and auto SDL
- TLS: Async processing support
- Device Drivers: Consistent QP feature and secondary interfaces support
- Python binding for VPP API now includes asyncio support

### API changes (verbatim message list)

af_xdp_create (only in file)
af_xdp_create_reply (only in file)
af_xdp_create_v2 (only in file)
af_xdp_create_v2_reply (only in file)
auto_sdl_config (only in image)
auto_sdl_config_reply (only in image)
bfd_udp_enable_multihop (only in image)
bfd_udp_enable_multihop_reply (only in image)
dev_create_port_if (definition changed)
http_static_enable (only in file)
http_static_enable_reply (only in file)
http_static_enable_v3 (only in image)
http_static_enable_v3_reply (only in image)
ikev2_get_sleep_interval (only in image)
ikev2_get_sleep_interval_reply (only in image)
ikev2_plugin_set_sleep_interval (only in image)
ikev2_plugin_set_sleep_interval_reply (only in image)
pg_delete_interface (only in image)
pg_delete_interface_reply (only in image)
session_rules_v2_details (only in image)
session_rules_v2_dump (only in image)
session_sdl_add_del_v2 (only in image)
session_sdl_add_del_v2_reply (only in image)
session_sdl_v2_details (only in image)
session_sdl_v2_dump (only in image)
session_sdl_v3_details (only in image)
session_sdl_v3_dump (only in image)
sflow_enable_disable (only in image)
sflow_enable_disable_reply (only in image)
sflow_header_bytes_get (only in image)
sflow_header_bytes_get_reply (only in image)
sflow_header_bytes_set (only in image)
sflow_header_bytes_set_reply (only in image)
sflow_interface_details (only in image)
sflow_interface_dump (only in image)
sflow_polling_interval_get (only in image)
sflow_polling_interval_get_reply (only in image)
sflow_polling_interval_set (only in image)
sflow_polling_interval_set_reply (only in image)
sflow_sampling_rate_get (only in image)
sflow_sampling_rate_get_reply (only in image)
sflow_sampling_rate_set (only in image)
sflow_sampling_rate_set_reply (only in image)
snort_client_details (only in image)
snort_client_disconnect (only in image)
snort_client_disconnect_reply (only in image)
snort_client_get (only in image)
snort_client_get_reply (only in image)
snort_input_mode_get (only in image)
snort_input_mode_get_reply (only in image)
snort_input_mode_set (only in image)
snort_input_mode_set_reply (only in image)
snort_instance_create (only in image)
snort_instance_create_reply (only in image)
snort_instance_delete (only in image)
snort_instance_delete_reply (only in image)
snort_instance_details (only in image)
snort_instance_disconnect (only in image)
snort_instance_disconnect_reply (only in image)
snort_instance_get (only in image)
snort_instance_get_reply (only in image)
snort_interface_attach (only in image)
snort_interface_attach_reply (only in image)
snort_interface_detach (only in image)
snort_interface_detach_reply (only in image)
snort_interface_details (only in image)
snort_interface_get (only in image)
snort_interface_get_reply (only in image)
sw_interface_ip4_enable_disable (only in image)
sw_interface_ip4_enable_disable_reply (only in image)

### Newly deprecated API messages (25.02)

http_static_enable_v2
http_static_enable_v2_reply
http_static_enable_v3
http_static_enable_v3_reply
session_rules_details
session_rules_dump
session_sdl_add_del
session_sdl_add_del_reply
session_sdl_details
session_sdl_dump
session_sdl_v2_details
session_sdl_v2_dump

Note: in 25.02 the original `http_static_enable` / `http_static_enable_reply` are removed
from the image ("only in file"); `http_static_enable_v3` is added as the current variant,
and `http_static_enable_v2` and `http_static_enable_v3` are simultaneously marked deprecated.
The `af_xdp_create` and `af_xdp_create_v2` messages appear "only in file" (removed from the image).

---

## VPP 24.10

"more than 241 commits since the previous release, including 86 fixes."

### Features
- Octeon-roc version bumped to 0.5
- Marvell CN913x platform support added
- DPDK upgraded to version 24.07 with RDMA 52.0
- New Marvell Armada device driver plugin introduced
- Marvell Octeon9 SoC support added (promiscuous mode, counters, flow types, checksum offload, pause frames)
- Packet Vector Tunnel Interface (PVTI) plugin introduced
- New Device Drivers Infrastructure with port/queue counter operations and devicetree support
- Session Layer Source Deny List feature
- Vector Library automatic core pinning improvements
- FreeBSD portability work completed

### API changes (removed messages)

builtinurl_enable (only in file)
builtinurl_enable_reply (only in file)
http_static_enable (only in file)
http_static_enable_reply (only in file)
session_enable_disable (only in file)
session_enable_disable_reply (only in file)

New messages include PVTI interface operations, session SDL (Source Deny List) operations,
and enhanced IP table/route handling with v2 versions.

### Newly deprecated API messages (24.10)

http_static_enable
http_static_enable_reply
session_enable_disable
session_enable_disable_reply

---

## VPP 24.06

### Newly deprecated API messages (24.06)

builtinurl_enable
builtinurl_enable_reply

### API changes (only in image / new)

bpf_trace_filter_set_v2
bpf_trace_filter_set_v2_reply
get_api_json
get_api_json_reply
ikev2_child_sa_v2_details
ikev2_child_sa_v2_dump
ikev2_sa_v2_details
ikev2_sa_v2_dump
ikev2_sa_v3_details
ikev2_sa_v3_dump

Total API message signature differences found: 10

---

## VPP 24.02

### Newly deprecated API messages (24.02)

rdma_create_v3

### API changes

Definition changed:
cnat_translation_details
cnat_translation_update

Only in image (new):
dev_attach
dev_attach_reply
dev_create_port_if
dev_create_port_if_reply
dev_detach
dev_detach_reply
dev_remove_port_if
dev_remove_port_if_reply
dhcp_client_detect_enable_disable
dhcp_client_detect_enable_disable_reply
gtpu_add_del_forward
gtpu_add_del_forward_reply
gtpu_add_del_tunnel_v2
gtpu_add_del_tunnel_v2_reply
gtpu_get_transfer_counts
gtpu_get_transfer_counts_reply
gtpu_tunnel_v2_details
gtpu_tunnel_v2_dump
ipsec_sa_v5_details
ipsec_sa_v5_dump
ipsec_sad_entry_add_v2
ipsec_sad_entry_add_v2_reply
lldp_details
lldp_dump
lldp_dump_reply
ping_finished_event
rdma_create_v4
rdma_create_v4_reply
sr_mobile_localsid_add_del
sr_mobile_localsid_add_del_reply
sr_mobile_policy_add
sr_mobile_policy_add_reply
urpf_interface_details
urpf_interface_dump
want_ping_finished_events
want_ping_finished_events_reply

Note: `rdma_create_v3` is deprecated in 24.02 and `rdma_create_v4` is the current variant.
`ipsec_sad_entry_add_v2` supersedes the earlier `ipsec_sad_entry_add`.
`gtpu_add_del_tunnel_v2` supersedes `gtpu_add_del_tunnel`.
