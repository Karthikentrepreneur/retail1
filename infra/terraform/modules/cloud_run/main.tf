resource "google_service_account" "run" {
  account_id   = "pos-api-sa"
  display_name = "POS API Service Account"
}

resource "google_cloud_run_service" "api" {
  name     = "pos-api"
  location = var.region

  template {
    spec {
      service_account_name = var.service_account
      containers {
        image = var.image
        env {
          name  = "DATABASE_URL"
          value = var.database_url
        }
        env {
          name  = "REDIS_URL"
          value = var.redis_url
        }
      }
    }
  }

  traffic {
    percent         = 100
    latest_revision = true
  }
}

resource "google_cloud_run_service_iam_member" "invoker" {
  service  = google_cloud_run_service.api.name
  location = google_cloud_run_service.api.location
  role     = "roles/run.invoker"
  member   = "allUsers"
}

resource "google_compute_security_policy" "waf" {
  name        = "pos-waf"
  description = "Basic WAF rules"
}

output "url" {
  value = google_cloud_run_service.api.status[0].url
}
