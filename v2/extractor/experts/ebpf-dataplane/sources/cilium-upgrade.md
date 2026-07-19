# Cilium Upgrade Guide — consolidated upgrade notes (stable/1.19, 1.15, 1.14)

Source pages:
- https://docs.cilium.io/en/stable/operations/upgrade/ (Cilium 1.19)
- https://docs.cilium.io/en/v1.15/operations/upgrade/
- https://docs.cilium.io/en/v1.14/operations/upgrade/

---

## Cilium 1.19 Upgrade Guide — Key Changes

### Critical Pre-Upgrade Actions

Before upgrading to Cilium 1.19, you must:

1. Read version-specific notes — the guide explicitly warns: "Do not upgrade to 1.19 before reading the section 1.19 Upgrade Notes and completing the required steps."
2. Run preflight checks — execute the CNP validator and image pre-pull to prevent downtime.
3. Update to latest patch first — "Always update to the latest patch release of your current version before attempting an upgrade."

### Major Breaking Changes

#### Network Policy
- DNS wildcard `**` now matches multiple subdomains (previously treated as single `*`).
- `FromRequires` and `ToRequires` fields are no longer permitted in `CiliumNetworkPolicy` and `CiliumClusterwideNetworkPolicy`.
- Kafka policy support deprecated, removal planned for v1.20.
- Mesh auth flag (`authentication.enabled`) now defaults to disabled.

#### ClusterMesh Configuration
- Policy Default Local Cluster: Network policies now select endpoints from local cluster only by default (major behavioral shift). Use `policy-default-local-cluster: false` to retain prior behavior, though this option will be deprecated.
- `clustermesh.apiserver.tls.authMode` defaults to `migration` mode.
- MCS-API CRDs now installed by default; set `clustermesh.mcsapi.installCRDs: false` to opt-out.

#### Custom Resource Versions
- `CiliumLoadBalancerIPPool` v2alpha1 deprecated; migrate to `apiVersion: cilium.io/v2`.
- `CiliumBGPPeeringPolicy` CRD and BGPv1 control plane removed; migrate to v2 CRDs.

### Configuration Changes

#### Removed Flags (previously deprecated, now removed in 1.19)
- `--bpf-lb-proto-diff`
- `--enable-recorder`, `--hubble-recorder-*` (PCAP feature)
- `--enable-session-affinity`
- `--enable-internal-traffic-policy`
- `--enable-svc-source-range-check`
- `--enable-node-port`, `--enable-host-port`, `--enable-external-ips`
- `--enable-custom-calls`
- `--enable-ipv4-egress-gateway`
- `--egress-multi-home-ip-rule-compat`
- `--l2-pod-announcements-interface`

#### Deprecated Flags
- `--aws-pagination-enabled` → replaced by `--aws-max-results-per-call`
- `--enable-ipsec-encrypted-overlay` (no effect; removal planned v1.20)
- `--enable-encryption-strict-mode` → use egress-specific variants
- `clustermesh.enableMCSAPISupport` → use `clustermesh.mcsapi.enabled`
- `encryption.strictMode.*` → use `encryption.strictMode.egress.*`

#### Changed Options
- `--unmanaged-pod-watcher-interval` changed from integer (seconds) to duration format (e.g., `15s`). Before: `--unmanaged-pod-watcher-interval=15`; After: `--unmanaged-pod-watcher-interval=15s`.
- `clustermesh.config.clusters` now accepts dict format in addition to list format.

#### New Options
- `enable-remote-node-masquerade: "true"` (requires BPF masquerading)
- `encryption-strict-mode-ingress` (drops unencrypted pod-to-pod traffic; requires WireGuard)
- `packetization-layer-pmtud-mode` (enables packet-layer MTU discovery by default)

### Metrics Changes (1.19)

#### Renamed Metrics (workqueue consolidated under `cilium_operator_` namespace)
- `workqueue_adds_total` → `cilium_operator_k8s_workqueue_adds_total`
- `workqueue_depth` → `cilium_operator_k8s_workqueue_depth`
- `workqueue_longest_running_processor_seconds` → `cilium_operator_k8s_workqueue_longest_running_processor_seconds`
- `workqueue_queue_duration_seconds` → `cilium_operator_k8s_workqueue_queue_duration_seconds`
- `workqueue_retries_total` → `cilium_operator_k8s_workqueue_retries_total`
- `workqueue_unfinished_work_seconds` → `cilium_operator_k8s_workqueue_unfinished_work_seconds`
- `workqueue_work_duration_seconds` → `cilium_operator_k8s_workqueue_work_duration_seconds`

All renamed workqueue metrics changed label `queue_name` to `name`.

#### Removed Labels
- `k8s_client_rate_limiter_duration_seconds` no longer includes `path` and `method` labels.
- Metrics no longer report `source_cluster` and `source_node_name` labels.

#### Renamed Metrics (Global to Per-Cluster)
- `cilium_agent_clustermesh_global_services` → `cilium_agent_clustermesh_remote_cluster_services`
- `cilium_operator_clustermesh_global_services` → `cilium_operator_clustermesh_remote_cluster_services`
- `cilium_operator_clustermesh_global_service_exports` → `cilium_operator_clustermesh_remote_cluster_service_exports`

#### Removed Metrics
- `k8s_internal_traffic_policy_enabled` (feature now enabled by default)
- `endpoint_max_ifindex` (datapath limitation no longer applies)

#### Deprecated Metrics
- `cilium_agent_bootstrap_seconds` (use `cilium_hive_jobs_oneshot_last_run_duration_seconds` instead)

### Upgrade Process (1.19)

#### Helm Commands
Standard upgrade with compatibility setting:
```
helm upgrade cilium cilium/cilium --version 1.19.6 \
   --namespace kube-system \
   --set upgradeCompatibility=1.X
```
Critical: Do NOT use `--reuse-values` flag during minor version upgrades; instead save values to file and pass via `-f`.

#### Preflight Check
```
helm template cilium/cilium --version 1.19.6 \
   --namespace kube-system \
   --set preflight.enabled=true \
   --set agent=false \
   --set operator.enabled=false \
   > cilium-preflight.yaml
kubectl create -f cilium-preflight.yaml
```
For kubeproxy-free mode, add:
```
--set k8sServiceHost=API_SERVER_IP \
--set k8sServicePort=API_SERVER_PORT
```

### Identity Migration Paths (1.19)

#### Double Write Mode (Recommended)
Allows gradual migration with rollback capability:
1. Deploy with `--identity-allocation-mode=doublewrite-readkvstore`
2. Monitor convergence via metrics: `cilium_operator_identity_crd_total_count` and `cilium_operator_identity_kvstore_total_count`
3. Switch to `--identity-allocation-mode=doublewrite-readcrd`
4. Finally switch to `--identity-allocation-mode=crd`
5. Decommission kvstore

#### Legacy Migration Script
Alternative one-off tool: `cilium preflight migrate-identity` (single point-in-time copy; cannot handle identity churn).

### Important Operational Notes (1.19)
- Only consecutive minor release upgrades/rollbacks are tested.
- User-space proxy traffic (L7 policies, Ingress/Gateway API) will experience disruption during upgrade.
- `bpf.tproxy=true` incompatible with netkit datapath mode.
- IPsec with kube-proxy replacement and BPF masquerading now auto-enables eBPF Host-Routing (requires specific kernel bugfix for CVE-2025-37959).
- LoadBalancer/ClusterIP traffic now dropped if destination port doesn't match provisioned service (north-south direction).

---

## Cilium 1.15 Upgrade Notes — Complete Reference

### Upgrade Notes Section
The following issues may occur when upgrading to Cilium 1.15:

- IPv4/IPv6 dual-stack deployments with `ToCIDR`/`ToCIDRSet` rules matching full ranges like "0.0.0.0/0" or "::/0" may experience connection breakage when switching versions. Existing connections allowed by policy may be denied until applications reconnect. This affects downgrades from 1.15.y to 1.14.x, but not upgrades to 1.15.y.
- `CiliumNetworkPolicy` resources cannot match `reserved:init` labels anymore. Convert these policies to `CiliumClusterwideNetworkPolicy` by changing the resource type.
- Cluster name and ID are no longer automatically inferred for external workloads. If different from defaults, they must be explicitly specified as parameters using Cilium CLI >=v0.15.8.
- `enable-endpoint-routes` now automatically sets `enable-local-node-route` to false, making local node routes redundant when per-endpoint routes are enabled.
- L7 visibility via Pod annotations (`policy.cilium.io/proxy-visibility`) is no longer supported. Migrate to L7 policies instead.
- Gateway API users should ensure v1 CRDs are installed and migrate resources from v1beta1 to v1 for GatewayClass, Gateway, and HTTPRoute.
- Tunnel protocol is no longer automatically set to `geneve` in native routing mode with DSR+Geneve enabled. Explicitly configure `--tunnel-protocol=geneve` or helm value `tunnelProtocol=geneve`.
- The `CILIUM_PREPEND_IPTABLES_CHAIN` environment variable renamed to `CILIUM_PREPEND_IPTABLES_CHAINS` (added trailing "S") to match the CLI flag `--prepend-iptables-chains`.
- BPF masquerade support now fails initialization with error logging if requirements aren't met (NodePort in BPF disabled or socket load-balancing disabled), rather than silently falling back to iptables.

### Removed Options (1.15)
- `cluster-pool-v2beta` IPAM mode removed; use `multi-pool` IPAM mode for dynamic Pod CIDR allocation.
- `install-egress-gateway-routes` flag deprecated due to datapath improvements eliminating the need for additional routes in ENI environments.
- `tunnel` option (deprecated in 1.14) removed. Use `routing-mode=native` (formerly `tunnel=disabled`) for native-routing mode or `tunnel-protocol=vxlan|geneve` (formerly `tunnel=vxlan|geneve`) to configure tunneling protocol.
- `single-cluster-route` flag removed (long defunct and undocumented).
- Deprecated options `enable-k8s-event-handover` and `cnp-status-update-interval` removed.

### Deprecated Options (1.15)
- `enable-remote-node-identity` flag deprecated; will be removed in 1.16. This flag has been enabled by default since 1.7 with no benefit to disabling.

### Helm Options Changed/Removed (1.15)
- `clustermesh.apiserver.tls.ca.cert` and `clustermesh.apiserver.tls.ca.key` removed (deprecated in 1.14); use `tls.ca.cert` and `tls.ca.key`. The `clustermesh-apiserver-ca-cert` secret no longer generated.
- `authentication.mutual.spire.install.agent.image` and `authentication.mutual.spire.install.server.image` changed type from string to structured definition decoupling repository and tag.
- Prometheus metrics now enabled by default for cilium-operator and clustermesh kvstore. Disable with `operator.prometheus.enabled=false` and `clustermesh.apiserver.metrics.etcd.enabled=false`.
- `egressGateway.installRoutes` deprecated; setting no longer necessary.
- `tunnel` helm value removed (deprecated in 1.14); use `routingMode` and `tunnelProtocol`.
- `enableK8sEventHandover` and `enableCnpStatusUpdates` helm values removed.
- `remoteNodeIdentity` helm value deprecated; removal planned for 1.16.

### Added Metrics (1.15)
- `cilium_ipam_capacity`
- `cilium_endpoint_max_ifindex`

### Removed Metrics (1.15)
- `cilium_policy_l7_parse_errors_total`, `cilium_policy_l7_forwarded_total`, `cilium_policy_l7_denied_total`, `cilium_policy_l7_received_total` (replaced by `cilium_policy_l7_total`)
- `cilium_policy_import_errors_total` (replaced by `cilium_policy_change_total`)

### Changed Metrics (1.15)
- `cilium_kvstore_operations_duration_seconds`, `cilium_clustermesh_apiserver_kvstore_operations_duration_seconds`, `cilium_kvstoremesh_kvstore_operations_duration_seconds` no longer include client-side rate-limiting latency; use corresponding `*_api_limiter_wait_duration_seconds` metrics.
- `cilium_bpf_map_pressure` for policy maps now exposed as single label `cilium_policy_*` rather than per-policy-map labels.
- `cilium_policy_l7_total` now includes `proxy_type` label distinguishing fqdn and envoy proxy requests.
- `cilium_cidrgroup_policies` renamed to `cilium_cidrgroups_referenced` for clarity.
- `cilium_cidrgroup_translation_time_stats_seconds` disabled by default.
- `cilium_api_limiter_processed_requests_total` now includes `return_code` label specifying HTTP code.

---

## Cilium 1.14 Upgrade Notes

### 1.14.2 Upgrade Notes
"`CiliumNetworkPolicy` cannot match the `reserved:init` labels any more. If you have `CiliumNetworkPolicy` resources that have a match for labels `reserved:init`, these policies must be converted to `CiliumClusterwideNetworkPolicy`."

### 1.14 Upgrade Notes — Critical Changes

Default & TTL Behavior:
- Default `--tofqdns-min-ttl` changed from 3600 seconds to zero, now honoring upstream DNS server TTLs by default.

CNI Configuration:
- Cilium now writes to `05-cilium.conflist` instead of previous `05-cilium.conf` default.

EC2 Adapter Limits:
- `--update-ec2-adapter-limit-via-api` default changed from `false` to `true`, requiring `ec2:DescribeInstances` IAM permission.

Egress Gateway Policy:
- Matching traffic now dropped when no gateway nodes available (previously allowed without rerouting).

Gateway API:
- Requires upgrade of related CRDs to v0.6.x (ReferenceGrant: v1alpha2 → v1beta1).

CiliumNetworkPolicy Authentication:
- Attribute `auth.type` renamed to `authentication.mode` in Ingress/Egress rules.
- New valid values: `disabled`, `required`, `test-always-fail`.

Cluster Mesh:
- Agents auto-cleanup stale meshed cluster information after kvstore reconnection; upgrade clustermesh-apiserver before Cilium agents to prevent connectivity disruptions.

Policy Precedence:
- Deny policies now always take precedence over allow policies; CIDR-based deny now blocks overlapping allow policies (previously allowed).

IPv6 Host Assignment:
- `cilium_host` IPv6 now assigned from IPAM pool rather than native host interface.

### Removed Options (1.14)
- `sockops-enable` (deprecated v1.13)
- `force-local-policy-eval-at-source` (deprecated v1.13)

### New Options (1.14)
- `routing-mode=native` (replaces `tunnel=disabled`)
- `tunnel-protocol` (replaces `tunnel=vxlan`, etc.)
- `tls-relay-client-ca-files` (Hubble Relay mTLS authentication for clients)

### Deprecated Options (1.14)
- `tunnel` (removed v1.15; use `routing-mode=native` or `tunnel-protocol=geneve`)
- `disable-cnp-status-updates`, `cnp-node-status-gc-interval`, `enable-k8s-event-handover` (removed v1.15; no replacement due to scalability issues)
- `cluster-pool-v2beta` IPAM mode (removed v1.15; use `multi-pool`)
- Hubble Relay options (removed v1.15):
  - `tls-client-cert-file` → `tls-hubble-client-cert-file`
  - `tls-client-key-file` → `tls-hubble-client-key-file`
  - `tls-server-cert-file` → `tls-relay-server-cert-file`
  - `tls-server-key-file` → `tls-relay-server-key-file`
- `kube-proxy-replacement` values `strict`, `partial`, `disabled` (removed v1.15; use `true`/`false`)

### Deprecated Commands (1.14)
- `cilium endpoint regenerate` (removed v1.15)

### Added Metrics (1.14)
- `cilium_operator_ces_sync_total`
- `cilium_policy_change_total`
- `go_sched_latencies_seconds`
- `cilium_operator_ipam_available_ips`
- `cilium_operator_ipam_used_ips`
- `cilium_operator_ipam_needed_ips`
- `kvstore_sync_queue_size`
- `kvstore_initial_sync_completed`
- `cilium_endpoint_max_ifindex`

### Deprecated Metrics (1.14)
- `cilium_operator_ces_sync_errors_total` → `cilium_operator_ces_sync_total`
- `cilium_policy_import_errors_total` → `cilium_policy_change_total`
- `cilium_operator_ipam_ips` → `cilium_operator_ipam_{available,used,needed}_ips`

### Changed Metrics (1.14)
- `cilium_bpf_map_pressure` now enabled by default.
- `cilium_policy_l7_total` now includes `proxy_type` label (fqdn vs. envoy).

### Removed Metrics (1.14)
- `cilium_policy_l7_parse_errors_total`
- `cilium_policy_l7_forwarded_total`
- `cilium_policy_l7_denied_total`
- `cilium_policy_l7_received_total` (replaced by `cilium_policy_l7_total`)

### Helm Options (1.14)
- `securityContext` for Hubble Relay now applies to container (use `podSecurityContext` for pod-level).
- Hubble Relay `securityContext` defaults to drop capabilities and non-root user.
- `containerRuntime.integration` deprecated → `bpf.autoMount.enabled`.
- `tunnel` deprecated → `routingMode` and `tunnelProtocol` (removed v1.15).
- `enableCnpStatusUpdates`, `enableK8sEventHandover` deprecated (removed v1.15; no replacement).
- `encryption.keyFile`, `encryption.mountPath`, `encryption.secretName`, `encryption.interface` deprecated → `encryption.ipsec.*` counterparts (removed v1.15).
- `hubble.peerService.enabled` removed (was deprecated v1.13).
- `hubble.tls.ca`, `hubble.tls.ca.cert`, `hubble.tls.ca.key` removed (was deprecated v1.12).
- `hubble.ui.securityContext.enabled` removed (was deprecated v1.12).
- `ipam.operator.clusterPoolIPv4PodCIDR`, `ipam.operator.clusterPoolIPv6PodCIDR` removed (was deprecated v1.11).
- `clustermesh.apiserver.tls.ca.cert`, `clustermesh.apiserver.tls.ca.key` deprecated → `tls.ca.cert`, `tls.ca.key` (removed v1.15).
- `proxy.prometheus.enabled`, `proxy.prometheus.port` deprecated → `envoy.prometheus.*`.
- `disableEndpointCRD` now boolean instead of string (remove quotes).

### Cilium CLI (1.14)
"Upgrade Cilium CLI to v0.15.0 or later to switch to Helm installation mode to install and manage Cilium v1.14. Classic installation mode is not supported with Cilium v1.14." Helm and classic modes are incompatible; migration requires uninstall/reinstall.
