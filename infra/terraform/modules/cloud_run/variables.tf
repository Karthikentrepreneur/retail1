variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "image" {
  type = string
}

variable "service_account" {
  type = string
  description = "Existing service account email for Cloud Run. Leave empty to create one."
  default = ""
}

variable "vpc_connector" {
  type = string
}

variable "database_url" {
  type = string
  default = ""
}

variable "redis_url" {
  type = string
  default = ""
}
