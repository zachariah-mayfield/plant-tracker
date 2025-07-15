#!/bin/bash

# Exit on error
set -e

echo "Testing Docker builds..."

# Test backend build
echo "Building backend image..."
docker build -t plant-tracker-backend:test ./backend

# Test frontend build
echo "Building frontend image..."
docker build -t plant-tracker-frontend:test ./frontend

# Test backend container
echo "Testing backend container..."
docker run -d --name backend-test -p 8000:8000 plant-tracker-backend:test
sleep 5  # Wait for the server to start

# Test backend health endpoint
echo "Testing backend health endpoint..."
curl -f http://localhost:8000/ || { echo "Backend health check failed"; exit 1; }

# Test frontend container
echo "Testing frontend container..."
docker run -d --name frontend-test -p 3000:3000 plant-tracker-frontend:test
sleep 5  # Wait for nginx to start

# Test frontend container
echo "Testing frontend container..."
curl -f http://localhost:3000/ || { echo "Frontend health check failed"; exit 1; }

# Cleanup
echo "Cleaning up test containers..."
docker stop backend-test frontend-test
docker rm backend-test frontend-test

echo "Docker tests completed successfully!" 