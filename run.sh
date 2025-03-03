#!/bin/bash

# Step 1: Build the Docker image
echo "Building Docker image..."
docker build -t app .

# Step 2: Run the Docker container
echo "Running Docker container..."
docker run -p 5000:5000 app