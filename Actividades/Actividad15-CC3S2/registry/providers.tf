// providers.tf
// Configuración minima de proveedores para ejemplos de uso con un registro local.

terraform {
  required_providers {
    null = {
      source  = "hashicorp/null"
      version = "~> 3.2"
    }
    local = {
      source  = "hashicorp/local"
      version = "~> 2.5"
    }
  }
}

provider "null" {}
provider "local" {}
