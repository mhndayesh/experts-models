# Terraform AWS Provider v4 to v5 Upgrade (breaking changes)

## Provider arguments
`assume_role.duration_seconds` is renamed to `assume_role.duration`.
`s3_force_path_style` is renamed to `s3_use_path_style`.
`shared_credentials_file` is renamed to `shared_credentials_files` (now a list).
`skip_get_ec2_platforms` is removed.

## Resource argument renames and removals
`aws_autoscaling_attachment.alb_target_group_arn` is renamed to `lb_target_group_arn`.
`aws_autoscaling_group.tags` is removed; use the `tag` block instead.
`aws_db_instance.name` is renamed to `db_name`.
`aws_db_instance.id` now returns the DBI Resource ID instead of the DB Identifier; reference `identifier` instead.
`aws_db_instance.db_security_groups` is removed.
`aws_eip.vpc` is removed; use `domain` instead.
`aws_route.instance_id` is removed; use `network_interface_id`.
`aws_route_table` route `instance_id` is removed; use `network_interface_id`.
`aws_rds_cluster.engine` is now required (previously defaulted to `aurora`).
`aws_rds_cluster_instance.engine` is now required.
`aws_s3_object.acl` no longer defaults to `private`.
`aws_s3_object_copy.acl` no longer defaults to `private`.
`aws_elasticache_replication_group.availability_zones` is renamed to `preferred_cache_cluster_azs`.
`aws_elasticache_replication_group.number_cache_clusters` is renamed to `num_cache_clusters`.
`aws_elasticache_replication_group.replication_group_description` is renamed to `description`.
`aws_elasticache_replication_group.cluster_mode` block is removed; use top-level `num_node_groups` and `replicas_per_node_group`.
`aws_elasticache_cluster.security_group_names` is removed.
`aws_eks_addon.resolve_conflicts` is removed; use `resolve_conflicts_on_create` and/or `resolve_conflicts_on_update`.
`aws_flow_log.log_group_name` is removed; use `log_destination`.
`aws_opensearch_domain.kibana_endpoint` is removed; use `dashboard_endpoint`.
`aws_ssm_association.instance_id` is removed; use `targets`.
`aws_secretsmanager_secret.rotation_enabled`, `rotation_lambda_arn`, and `rotation_rules` are removed.
`aws_dx_gateway_association.vpn_gateway_id` is removed; use `associated_gateway_id`.
`aws_guardduty_organization_configuration.auto_enable` is removed; use `auto_enable_organization_members`.

## Data source changes
`aws_iam_policy_document.source_json` is renamed to `source_policy_documents`.
`aws_iam_policy_document.override_json` is renamed to `override_policy_documents`.
`aws_subnet_ids` data source is removed; use `aws_subnets` instead.
`aws_redshift_service_account` data source is deprecated; use the service principal name in IAM policies.

## Removed resources (EC2-Classic retirement)
`aws_db_security_group`, `aws_elasticache_security_group`, and `aws_redshift_security_group` are removed.
Non-VPC (EC2-Classic) security groups are no longer supported by `aws_security_group` and `aws_security_group_rule`.
`aws_vpc.enable_classiclink` and `enable_classiclink_dns_support` are removed.
