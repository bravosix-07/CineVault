Write-Host "🚀 Starting CineVault with Docker..."

if (!(Test-Path ".env")) {
    Write-Host "⚠️  .env file not found. Creating from .env.example"
    Copy-Item ".env.example" ".env"
    Write-Host "👉 Edit .env with secure passwords before production use."
}

docker-compose up --build