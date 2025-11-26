terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_network" "backend_net" {
  name = "backend_net"
}

resource "docker_image" "backend" {
  name         = "hashicorp/http-echo"
  keep_locally = true
}

resource "docker_container" "backend" {
  name  = "backend"
  image = docker_image.backend.image_id
  networks_advanced {
    name = docker_network.backend_net.name
  }
  command = ["-text={\"data\": \"from_backend\"}"]
  # No ports exposed to host
}

resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = true
}

resource "docker_container" "frontend" {
  name  = "frontend"
  image = docker_image.nginx.image_id
  networks_advanced {
    name = docker_network.backend_net.name
  }
  ports {
    internal = 80
    external = 8080
  }
  volumes {
    host_path      = abspath("${path.module}/nginx.conf")
    container_path = "/etc/nginx/conf.d/default.conf"
  }
}
