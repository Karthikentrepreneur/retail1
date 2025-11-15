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
}

variable "vpc_connector" {
  type = string
}

variable "allowed_cidr_blocks" {
  type = list(string)
}

variable "database_url" {
  type = string
  default = ""
}

variable "redis_url" {
  type = string
  default = ""
}
