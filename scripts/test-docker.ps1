# Test Docker builds and configurations
Write-Host "Testing Docker Environment..." -ForegroundColor Cyan

# Test Docker installation
try {
    $dockerVersion = docker --version
    Write-Host "`nDocker Installation: SUCCESS" -ForegroundColor Green
    Write-Host $dockerVersion
} catch {
    Write-Host "`nDocker Installation: FAILED" -ForegroundColor Red
    Write-Host "Error: Docker is not installed or not in PATH"
    exit 1
}

# Test Docker Compose installation
try {
    $composeVersion = docker-compose --version
    Write-Host "`nDocker Compose Installation: SUCCESS" -ForegroundColor Green
    Write-Host $composeVersion
} catch {
    Write-Host "`nDocker Compose Installation: FAILED" -ForegroundColor Red
    Write-Host "Error: Docker Compose is not installed or not in PATH"
    exit 1
}

# Test Backend Dockerfile
Write-Host "`nTesting Backend Dockerfile..." -ForegroundColor Cyan
try {
    docker build -t plant-tracker-backend-test ./backend
    Write-Host "Backend Docker Build: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "Backend Docker Build: FAILED" -ForegroundColor Red
    Write-Host "Error: $_"
    exit 1
}

# Test Frontend Dockerfile
Write-Host "`nTesting Frontend Dockerfile..." -ForegroundColor Cyan
try {
    docker build -t plant-tracker-frontend-test ./frontend
    Write-Host "Frontend Docker Build: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "Frontend Docker Build: FAILED" -ForegroundColor Red
    Write-Host "Error: $_"
    exit 1
}

# Test docker-compose.yml
Write-Host "`nTesting docker-compose.yml..." -ForegroundColor Cyan
try {
    docker-compose config
    Write-Host "Docker Compose Configuration: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "Docker Compose Configuration: FAILED" -ForegroundColor Red
    Write-Host "Error: $_"
    exit 1
}

# Clean up test images
Write-Host "`nCleaning up test images..." -ForegroundColor Cyan
docker rmi plant-tracker-backend-test plant-tracker-frontend-test

Write-Host "`nAll Docker tests completed successfully!" -ForegroundColor Green
Write-Host "`nNext steps:" -ForegroundColor Yellow
Write-Host "1. Push your code to GitHub" -ForegroundColor Yellow
Write-Host "2. Go to your repository's Actions tab" -ForegroundColor Yellow
Write-Host "3. Run the 'Test Workflow' manually" -ForegroundColor Yellow
Write-Host "4. Check the workflow results for any issues" -ForegroundColor Yellow 