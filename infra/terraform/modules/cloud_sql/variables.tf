variable "project_id" {
  type = string
}

variable "region" {
  type = string
}

variable "network_self_link" {
  type = string
}

variable "database_tier" {
  type = string
}

variable "database_password" {
  type      = string
  sensitive = true
}
