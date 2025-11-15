resource "google_compute_network" "pos" {
  name                    = "pos-vpc"
  auto_create_subnetworks = false
}

resource "google_compute_subnetwork" "pos" {
  name                     = "pos-subnet"
  ip_cidr_range            = "10.10.0.0/20"
  region                   = var.region
  network                  = google_compute_network.pos.id
  private_ip_google_access = true
}

resource "google_vpc_access_connector" "pos" {
  name          = "pos-connector"
  region        = var.region
  network       = google_compute_network.pos.name
  ip_cidr_range = "10.8.0.0/28"
}

output "network_name" {
  value = google_compute_network.pos.name
}

output "network_self_link" {
  value = google_compute_network.pos.self_link
}

output "vpc_connector" {
  value = google_vpc_access_connector.pos.id
}
