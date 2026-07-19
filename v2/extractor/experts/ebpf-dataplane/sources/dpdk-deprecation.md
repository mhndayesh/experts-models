# DPDK 24 — Deprecation, Removed Items, API Changes, ABI Changes

Source URLs:
- https://doc.dpdk.org/guides/rel_notes/deprecation.html
- https://doc.dpdk.org/guides/rel_notes/release_23_11.html
- https://doc.dpdk.org/guides/rel_notes/release_24_11.html

---

## ABI and API Deprecation Notices (deprecation.html)

kvargs: The function `rte_kvargs_process` will get a new parameter for returning key match count.

EAL commandline parameters:
- The `-c <coremask>` commandline parameter is deprecated and will be removed in a future release. Use the `-l <corelist>` or `--lcores=<corelist>` parameters instead.
- The `-s <service-coremask>` commandline parameter is deprecated and will be removed in a future release. Use the `-S <service-corelist>` parameter instead.

VFIO API: The entire VFIO API (`rte_vfio_*`) will be made internal only by DPDK 26.11, with group-based APIs removed and replaced.

Atomic operations: `rte_atomicNN_xxx`: These APIs do not take memory order parameter and should be replaced with GCC atomic builtins.

Memory barriers: `rte_smp_*mb` APIs provide full barrier functionality but should migrate to atomic operations from GCC and use `rte_atomic_thread_fence`.

Mempool: The `flushthresh` field in `struct rte_mempool_cache` and oversized object arrays will be removed in DPDK 26.11.

Flow items: `RTE_FLOW_ITEM_TYPE_VXLAN_GPE` will be removed in DPDK 25.11, replaced by `RTE_FLOW_ITEM_TYPE_VXLAN`.

ethdev queue stats: Functions `rte_eth_dev_set_tx_queue_stats_mapping` and `rte_eth_dev_set_rx_queue_stats_mapping` are deprecated.

Legacy APIs: Pipeline (`rte_pipeline_*`), table (`rte_table_*`), and port (`rte_port_*`) legacy functions deprecated for DPDK 24.11 removal.

bus/vmbus: Becoming internal in DPDK 25.11.

---

## DPDK 23.11 Release Notes

### 9.2. Removed Items

- eal: Removed deprecated `RTE_FUNC_PTR_OR_*` macros.
- ethdev: Removed deprecated macro `RTE_ETH_DEV_BONDED_SLAVE`.
- flow_classify: Removed flow classification library and examples.
- kni: Removed the Kernel Network Interface (KNI) library and driver.
- cryptodev: Removed the arrays of algorithm strings `rte_crypto_cipher_algorithm_strings`, `rte_crypto_auth_algorithm_strings`, `rte_crypto_aead_algorithm_strings` and `rte_crypto_asym_xform_strings`.
- cryptodev: Removed explicit SM2 xform parameter in asymmetric xform.
- security: Removed deprecated field `reserved_opts` from struct `rte_security_ipsec_sa_options`.
- mldev: Removed functions `rte_ml_io_input_size_get` and `rte_ml_io_output_size_get`.
- cmdline: Removed broken and unused function `cmdline_poll`.

### 9.3. API Changes

- eal: Thread API changed. Function `rte_thread_create_control()` no longer takes attributes. Thread API promoted to stable except `rte_thread_setname()` and `rte_ctrl_thread_create()`, replaced with `rte_thread_set_name()` and `rte_thread_create_control()`.
- eal: Removed `RTE_CPUFLAG_NUMFLAGS` to prevent misusage and theoretical ABI issues.
- power: Updated x86 Uncore power management API for vendor-agnostic operation.
- ethdev: `rte_eth_dev_configure` or `rte_eth_dev_rss_hash_update` now require user-provided `rss_key_len` in `rte_eth_rss_conf` when `rss_key != NULL`; no longer defaults to 40 bytes.
- bonding: Replaced master/slave terminology with main/member. Struct `rte_eth_bond_8023ad_slave_info` renamed to `rte_eth_bond_8023ad_member_info`. Removed: `rte_eth_bond_8023ad_slave_info`, `rte_eth_bond_active_slaves_get`, `rte_eth_bond_slave_add`, `rte_eth_bond_slave_remove`, `rte_eth_bond_slaves_get`. Replaced with: `rte_eth_bond_8023ad_member_info`, `rte_eth_bond_active_members_get`, `rte_eth_bond_member_add`, `rte_eth_bond_member_remove`, `rte_eth_bond_members_get`.
- cryptodev: Elliptic curve asymmetric private/public keys maintained per-session. Keys moved from `rte_crypto_ecdsa_op_param` and `rte_crypto_sm2_op_param` to `rte_crypto_ec_xform`.
- security: Structures `rte_security_ops` and `rte_security_ctx` moved to internal headers, not visible to applications.
- mldev: Updated `rte_ml_model_info` for arbitrary shape support. Modified `rte_ml_op`, `rte_ml_io_quantize`, `rte_ml_io_dequantize` to support `rte_ml_buff_seg` arrays.
- pcapng: Time parameters removed from `rte_pcapng_copy` and `rte_pcapng_write_stats`.

### 9.4. ABI Changes

- ethdev: Added `recycle_tx_mbufs_reuse` and `recycle_rx_descriptors_refill` fields to `rte_eth_dev` structure.
- ethdev: Structure `rte_eth_fp_ops` modified: added `recycle_tx_mbufs_reuse` and `recycle_rx_descriptors_refill` fields, moved `rxq` and `txq` fields, changed `reserved1` and `reserved2` field sizes.
- ethdev: Added `algorithm` field to `rte_eth_rss_conf` structure for RSS hash algorithm support.
- ethdev: Added `rss_algo_capa` field to `rte_eth_dev_info` structure for RSS algorithm capability reporting.
- security: Struct `rte_security_ipsec_sa_options` updated for inline out-of-place feature addition.

---

## DPDK 24.11 Release Notes

### Removed Items

- ethdev: Removed the `__rte_ethdev_trace_rx_burst` symbol, as the corresponding tracepoint was split into two separate ones for empty and non-empty calls.

### API Changes

kvargs modifications:
- `rte_kvargs_process` now handles only `key=value` cases, rejecting key-only input.
- New function `rte_kvargs_process_opt` provided for backward compatibility with key=value and key-only handling.
- Both functions reject NULL `kvlist` parameter.

Network structures:
- `rte_ipv4_hdr` marked as two-byte aligned.
- `rte_ipv6_hdr` and extensions (`rte_ipv6_routing_ext`, `rte_ipv6_fragment_ext`) marked as two-byte aligned.
- Deprecated ICMP symbols: `RTE_IP_ICMP_ECHO_REPLY` and `RTE_IP_ICMP_ECHO_REQUEST` replaced with `RTE_ICMP_TYPE_ECHO_REPLY` and `RTE_ICMP_TYPE_ECHO_REQUEST`.

IPv6 address structure introduction affecting: `cmdline_ipaddr_t`, `rte_flow_action_set_ipv6`, `rte_flow_item_icmp6_nd_na`, `rte_flow_item_icmp6_nd_ns`, `rte_flow_tunnel`, FIB functions, hash tuple structure, IPsec structures, LPM functions, node functions, pipeline structures, security structures, table structures, and RIB functions.

Amazon ENA driver: Removed `enable_llq`, `normal_llq_hdr`, `large_llq_hdr` devargs, replaced with unified `llq_policy` devarg.

### ABI Changes

- EAL: File descriptor limit to secondary processes increased from 8 to 253.
- ethdev: Added `filter` and `names` fields to `rte_dev_reg_info`.
- cryptodev: Queue pair config updated with priority parameter; removed `RTE_CRYPTO_ASYM_XFORM_TYPE_LIST_END` and `RTE_CRYPTO_RSA_PADDING_TYPE_LIST_END`; updated `rte_crypto_asym_xform_type` and `rte_crypto_asym_op` for EdDSA; restructured RSA padding handling.
- bbdev: `rte_bbdev_stats` updated with `enqueue_depth_avail` parameter.
- dmadev: Added `nb_priorities` to `rte_dma_info` and `priority` to `rte_dma_conf`.
- eventdev: Added `preschedule_type` to `rte_event_dev_config`; removed single-event function pointers from `rte_event_fp_fps`.
- graph: Enhanced node statistics with `xstat_cntrs`, `xstat_desc`, `xstat_count`; added `rte_node_xstats`.
