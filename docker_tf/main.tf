# Start a container

resource "docker_image" "restapi-tidal" {
  name = "grao2701/restapi-tidal:latest"
}
resource "docker_container" "restapi-tidal" {
  name = "restapi-tidal"
  image = docker_image.restapi-tidal.latest
  ports {
    internal = 8080
    external = 8080
  }
}
