variable "project_id" {
  type = string
}

variable "region" {
  type    = string
  default = "asia-south1"
}

variable "database_tier" {
  type    = string
  default = "db-custom-2-7680"
}

variable "database_password" {
  type      = string
  sensitive = true
}

variable "api_image" {
  type = string
}

variable "run_service_account" {
  type = string
}

variable "allowed_cidr_blocks" {
  type    = list(string)
  default = []
}
