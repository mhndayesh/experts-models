# Kubernetes Deprecated API Migration Guide (removed apiVersions)

## Removed in v1.32
FlowSchema `flowcontrol.apiserver.k8s.io/v1beta3` is removed; use `flowcontrol.apiserver.k8s.io/v1`.
PriorityLevelConfiguration `flowcontrol.apiserver.k8s.io/v1beta3` is removed; use `flowcontrol.apiserver.k8s.io/v1`.

## Removed in v1.29
FlowSchema `flowcontrol.apiserver.k8s.io/v1beta2` is removed; use `flowcontrol.apiserver.k8s.io/v1`. The `assuredConcurrencyShares` field is renamed to `nominalConcurrencyShares`.
PriorityLevelConfiguration `flowcontrol.apiserver.k8s.io/v1beta2` is removed; use `flowcontrol.apiserver.k8s.io/v1`.

## Removed in v1.27
CSIStorageCapacity `storage.k8s.io/v1beta1` is removed; use `storage.k8s.io/v1`.

## Removed in v1.26
FlowSchema `flowcontrol.apiserver.k8s.io/v1beta1` is removed; use `flowcontrol.apiserver.k8s.io/v1beta2`.
PriorityLevelConfiguration `flowcontrol.apiserver.k8s.io/v1beta1` is removed; use `flowcontrol.apiserver.k8s.io/v1beta2`.
HorizontalPodAutoscaler `autoscaling/v2beta2` is removed; use `autoscaling/v2`. The `targetAverageUtilization` field is replaced with `target.averageUtilization`.

## Removed in v1.25
CronJob `batch/v1beta1` is removed; use `batch/v1`.
EndpointSlice `discovery.k8s.io/v1beta1` is removed; use `discovery.k8s.io/v1`. Use the per-Endpoint `nodeName` and `zone` fields instead of `topology`.
Event `events.k8s.io/v1beta1` is removed; use `events.k8s.io/v1`.
HorizontalPodAutoscaler `autoscaling/v2beta1` is removed; use `autoscaling/v2`.
PodDisruptionBudget `policy/v1beta1` is removed; use `policy/v1`. An empty `spec.selector` now selects all pods instead of none.
PodSecurityPolicy `policy/v1beta1` is removed; use Pod Security Admission or a third-party webhook.
RuntimeClass `node.k8s.io/v1beta1` is removed; use `node.k8s.io/v1`.

## Removed in v1.22
MutatingWebhookConfiguration `admissionregistration.k8s.io/v1beta1` is removed; use `admissionregistration.k8s.io/v1`. The default `failurePolicy` changed to `Fail`, `matchPolicy` to `Equivalent`, and `timeoutSeconds` to `10`.
ValidatingWebhookConfiguration `admissionregistration.k8s.io/v1beta1` is removed; use `admissionregistration.k8s.io/v1`. The `sideEffects` and `admissionReviewVersions` fields are now required.
CustomResourceDefinition `apiextensions.k8s.io/v1beta1` is removed; use `apiextensions.k8s.io/v1`. The `spec.scope` field and a structural schema are now required.
APIService `apiregistration.k8s.io/v1beta1` is removed; use `apiregistration.k8s.io/v1`.
Lease `coordination.k8s.io/v1beta1` is removed; use `coordination.k8s.io/v1`.

## Removed in v1.16
NetworkPolicy `extensions/v1beta1` is removed; use `networking.k8s.io/v1`.
DaemonSet `extensions/v1beta1` is removed; use `apps/v1`.
Deployment `extensions/v1beta1` is removed; use `apps/v1`.
ReplicaSet `extensions/v1beta1` is removed; use `apps/v1`.
ReplicationController `extensions/v1beta1` is removed; use `core/v1`.
Ingress `extensions/v1beta1` is removed; use `networking.k8s.io/v1`.
