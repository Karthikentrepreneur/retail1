resource "google_sql_database_instance" "pos" {
  name             = "pos-sql"
  region           = var.region
  database_version = "POSTGRES_15"

  settings {
    tier = var.database_tier
    ip_configuration {
      ipv4_enabled    = false
      private_network = var.network_self_link
    }

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
    }

    maintenance_window {
      day          = 7
      hour         = 2
      update_track = "stable"
    }
  }
}

resource "google_sql_user" "pos" {
  instance = google_sql_database_instance.pos.name
  name     = "posapp"
  password = var.database_password
}

output "instance_connection_name" {
  value = google_sql_database_instance.pos.connection_name
}
