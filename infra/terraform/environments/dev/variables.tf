variable "project_id" {
  type    = string
  default = "pos-dev"
}

variable "region" {
  type    = string
  default = "asia-south1"
}

variable "database_password" {
  type      = string
  sensitive = true
  default   = "dev-password"
}

variable "api_image" {
  type    = string
  default = "gcr.io/example-project/pos-api:dev"
}

variable "run_service_account" {
  type    = string
  default = ""
}

