terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

module "network" {
  source     = "./modules/network"
  project_id = var.project_id
  region     = var.region
}

module "cloud_sql" {
  source            = "./modules/cloud_sql"
  project_id        = var.project_id
  region            = var.region
  network_self_link = module.network.network_self_link
  database_tier     = var.database_tier
  database_password = var.database_password
}

module "redis" {
  source     = "./modules/redis"
  project_id = var.project_id
  region     = var.region
  network    = module.network.network_self_link
}

module "cloud_run" {
  source          = "./modules/cloud_run"
  project_id      = var.project_id
  region          = var.region
  vpc_connector   = module.network.vpc_connector
  image           = var.api_image
  service_account = var.run_service_account
}

module "pubsub" {
  source     = "./modules/pubsub"
  project_id = var.project_id
}

