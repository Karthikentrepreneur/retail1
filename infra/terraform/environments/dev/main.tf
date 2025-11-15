terraform {
  backend "gcs" {
    bucket = "pos-terraform-dev"
    prefix = "state"
  }
}

module "stack" {
  source               = "../../"
  project_id           = var.project_id
  region               = var.region
  database_password    = var.database_password
  api_image            = var.api_image
  run_service_account  = var.run_service_account
  allowed_cidr_blocks  = var.allowed_cidr_blocks
}
