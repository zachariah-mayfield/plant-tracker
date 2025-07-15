# Create secrets directory if it doesn't exist
New-Item -ItemType Directory -Force -Path secrets

# Generate random secrets
$randomUser = -join ((65..90) + (97..122) | Get-Random -Count 12 | ForEach-Object {[char]$_})
$randomPassword = [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))
$randomDb = -join ((65..90) + (97..122) | Get-Random -Count 12 | ForEach-Object {[char]$_})
$randomJwt = [Convert]::ToBase64String([System.Security.Cryptography.RandomNumberGenerator]::GetBytes(32))

# Save secrets to files
$randomUser | Out-File -FilePath secrets/postgres_user.txt -NoNewline
$randomPassword | Out-File -FilePath secrets/postgres_password.txt -NoNewline
$randomDb | Out-File -FilePath secrets/postgres_db.txt -NoNewline
$randomJwt | Out-File -FilePath secrets/jwt_secret.txt -NoNewline

# Set proper permissions (Windows equivalent)
$acl = Get-Acl "secrets"
$accessRule = New-Object System.Security.AccessControl.FileSystemAccessRule("Everyone","FullControl","Deny")
$acl.SetAccessRule($accessRule)
Set-Acl "secrets" $acl

Write-Host "Secrets generated successfully!"
Write-Host "`nPlease add these secrets to your GitHub repository:"
Write-Host "POSTGRES_USER: $randomUser"
Write-Host "POSTGRES_PASSWORD: $randomPassword"
Write-Host "POSTGRES_DB: $randomDb"
Write-Host "JWT_SECRET: $randomJwt" 