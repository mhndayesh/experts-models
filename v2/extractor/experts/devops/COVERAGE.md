# DevOps Expert — coverage (built 2026-07-16)

Built with the proven pipeline (FIND deprecation/upgrade guide → WebFetch → DeepSeek extract → repair →
check). All quote-grounded, integrity-checked.

## Banks
| library | facts | source |
|---|---|---|
| kubernetes | 33 | kubernetes.io deprecation guide (removed apiVersions) — the gold source, proven 96.5% |
| github-actions | 4 | GitHub Actions workflow-command deprecations |
| terraform-aws | 37 | terraform AWS provider v6 upgrade guide (HCL prose) |
| **total** | **74** | 3 banks |

Landmine examples: k8s `Ingress extensions/v1beta1`→`networking.k8s.io/v1`, `CronJob batch/v1beta1`→
`batch/v1`, `PodDisruptionBudget policy/v1beta1`→`policy/v1`, PodSecurityPolicy removed → Pod Security
Admission; Actions `set-output`→`GITHUB_OUTPUT` file, `set-env`→`GITHUB_ENV`.

## Next (not yet built)
terraform azurerm provider, ansible (porting guides, collections split), helm 2→3,
docker compose v1→v2, boto3, cloud SDKs. See `../DEPARTMENTS.md`.
