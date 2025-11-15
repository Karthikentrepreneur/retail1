variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-south1"
}

variable "database_password" {
  type      = string
  sensitive = true
}

variable "api_image" {
  type = string
}

variable "run_service_account" {
  type    = string
  default = ""
}

