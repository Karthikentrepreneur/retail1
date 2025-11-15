variable "project_id" {
  type    = string
  default = "pos-staging"
}

variable "region" {
  type    = string
  default = "asia-south1"
}

variable "database_password" {
  type      = string
  sensitive = true
  default   = "staging-password"
}

variable "api_image" {
  type    = string
  default = "gcr.io/example-project/pos-api:staging"
}

variable "run_service_account" {
  type    = string
  default = ""
}

