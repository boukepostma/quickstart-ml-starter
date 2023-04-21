variable "environment" {
  type        = string
  description = "Name of the environment"
  default     = "dev"
}

variable "location" {
  type        = string
  description = "Location of the resources"
  default     = "{{ cookiecutter.azure_location }}"
}

variable "prefix" {
  type        = string
  description = "Prefix of the resource name"
  default     = "{{ cookiecutter.azure_prefix }}"
}

variable "prefix_alphanum" {
  type        = string
  description = "Prefix of the resource name"
  default     = "{{ cookiecutter.azure_prefix_alphanum }}"
}

variable arm_subscription_id {
  type        = string
  description = "ID of Azure subscription"
}

variable  arm_tenant_id {
  type        = string
  description = "ID of tenant in Azure"
}

variable  arm_client_id {
  type        = string
  description = "ID of service principal in Azure"
}

variable  arm_client_secret {
  type        = string
  description = "Secret of service principal in Azure"
  sensitive = true
}
