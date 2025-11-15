output "vpc_network" {
  value = module.network.network_name
}

output "cloud_run_url" {
  value = module.cloud_run.url
}

output "cloud_sql_instance" {
  value = module.cloud_sql.instance_connection_name
}
