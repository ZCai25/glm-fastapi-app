#!/bin/bash

# Define the image name
IMAGE_NAME="pytestimage2"

# Define port mappings (host_port:container_port)
PORTS="1313:80"

# Run the Docker container
docker run -p $PORTS $IMAGE_NAME
