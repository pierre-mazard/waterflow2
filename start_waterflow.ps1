Write-Host "🚀 Waterflow 2 - Démarrage complet" -ForegroundColor Cyan

# Vérifier Docker Desktop
Write-Host "🔍 Vérification de Docker Desktop..."
$dockerStatus = docker info 2>$null

if (!$dockerStatus) {
    Write-Host "❌ Docker Desktop n'est pas lancé." -ForegroundColor Red
    Write-Host "➡️ Lance Docker Desktop puis relance ce script." -ForegroundColor Yellow
    exit
}

Write-Host "✔ Docker Desktop est actif." -ForegroundColor Green

# Démarrer toute la stack Docker
Write-Host "🐳 Démarrage des services Docker (DB, API, Web, Monitoring)..."
docker compose up -d

Start-Sleep -Seconds 5

Write-Host "✔ Services Docker démarrés." -ForegroundColor Green

Write-Host "🌐 API disponible sur : http://localhost:8000/docs"
Write-Host "📊 Dashboard Expert : http://localhost:8501"
Write-Host "📈 Prometheus : http://localhost:9090"
Write-Host "📉 Grafana : http://localhost:3000"

Write-Host "🎉 Waterflow 2 est entièrement lancé !" -ForegroundColor Cyan
