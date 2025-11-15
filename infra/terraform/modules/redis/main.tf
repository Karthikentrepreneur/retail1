resource "google_redis_instance" "cache" {
  name                    = "pos-cache"
  tier                    = "STANDARD_HA"
  memory_size_gb          = 4
  region                  = var.region
  authorized_network      = var.network
  transit_encryption_mode = "SERVER_AUTHENTICATED"
}

output "host" {
  value = google_redis_instance.cache.host
}
