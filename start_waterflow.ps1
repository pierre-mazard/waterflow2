Write-Host "🚀 Waterflow 2 - Démarrage complet" -ForegroundColor Cyan

# Activer la venv
Write-Host "🐍 Activation de l'environnement Python (.venv310)..."
$venvPath = ".\.venv310\Scripts\Activate.ps1"
if (Test-Path $venvPath) { & $venvPath }

# Vérifier Docker
Write-Host "🔍 Vérification de Docker Desktop..."
$dockerStatus = docker info 2>$null
if (!$dockerStatus) { exit }

# 🔥 IMPORTANT : reconstruire la stack
Write-Host "🧹 Nettoyage des anciens conteneurs..."
docker compose down

Write-Host "🐳 Reconstruction et démarrage de la stack..."
docker compose up -d --build

Start-Sleep -Seconds 5

Write-Host "🌐 API FastAPI : http://localhost:8000/docs"
Write-Host "📊 Dashboard Expert : http://localhost:8501"
Write-Host "📚 MLflow UI : http://localhost:5000"
Write-Host "📈 Prometheus : http://localhost:9090"
Write-Host "📉 Grafana : http://localhost:3000"

Write-Host "🎉 Waterflow 2 est entièrement lancé !" -ForegroundColor Cyan
