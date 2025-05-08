# Test SSH connection
$SSH_KEY = "github-actions-deploy"
$SSH_HOST = Read-Host "Enter your server's IP or hostname"
$SSH_USER = Read-Host "Enter your server's username"

Write-Host "`nTesting SSH connection..."
Write-Host "Using key: $SSH_KEY"
Write-Host "Connecting to: $SSH_USER@$SSH_HOST"

# Test basic SSH connection
try {
    $result = ssh -i $SSH_KEY -o BatchMode=yes -o ConnectTimeout=5 $SSH_USER@$SSH_HOST "echo 'SSH connection successful!'"
    Write-Host "`nSSH Connection Test: SUCCESS" -ForegroundColor Green
    Write-Host $result
} catch {
    Write-Host "`nSSH Connection Test: FAILED" -ForegroundColor Red
    Write-Host "Error: $_"
    exit 1
}

# Test Docker access
Write-Host "`nTesting Docker access..."
try {
    $dockerTest = ssh -i $SSH_KEY $SSH_USER@$SSH_HOST "docker --version && docker-compose --version"
    Write-Host "`nDocker Access Test: SUCCESS" -ForegroundColor Green
    Write-Host $dockerTest
} catch {
    Write-Host "`nDocker Access Test: FAILED" -ForegroundColor Red
    Write-Host "Error: $_"
    exit 1
}

# Test directory permissions
Write-Host "`nTesting directory permissions..."
try {
    $dirTest = ssh -i $SSH_KEY $SSH_USER@$SSH_HOST "mkdir -p /opt/plant-tracker && touch /opt/plant-tracker/test.txt && rm /opt/plant-tracker/test.txt"
    Write-Host "`nDirectory Permissions Test: SUCCESS" -ForegroundColor Green
} catch {
    Write-Host "`nDirectory Permissions Test: FAILED" -ForegroundColor Red
    Write-Host "Error: $_"
    exit 1
}

Write-Host "`nAll tests completed successfully!" -ForegroundColor Green 