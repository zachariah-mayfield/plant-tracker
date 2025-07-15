#!/bin/bash

# Create secrets directory if it doesn't exist
mkdir -p secrets

# Generate random secrets
openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c 12 > secrets/postgres_user.txt
openssl rand -base64 32 > secrets/postgres_password.txt
openssl rand -base64 16 | tr -dc 'a-zA-Z0-9' | head -c 12 > secrets/postgres_db.txt
openssl rand -base64 32 > secrets/jwt_secret.txt

# Set proper permissions
chmod 600 secrets/*.txt

echo "Secrets generated successfully!" 