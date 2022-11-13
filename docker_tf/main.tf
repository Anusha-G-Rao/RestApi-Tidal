# Start a container
resource "docker_container" "restapi-tidal" {
  name  = "grao2701/restapi-tidal"
  image = docker_image.restapi-tidal.latest
  ports {
    internal = "8080"
    external = "8080"
  }
}

# Find the latest Ubuntu precise image.
resource "docker_image" "grao2701" {
  name = "restapi-tidal"
}