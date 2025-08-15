# Instalar dependencias del panel central
Write-Host "Instalando dependencias del Panel Central..." -ForegroundColor Green
Set-Location "panel_central/backend"
pip install -r requirements.txt

# Volver al directorio raíz
Set-Location "../.."

# Instalar dependencias de las APIs existentes si no están instaladas
Write-Host "Verificando dependencias de las APIs existentes..." -ForegroundColor Green

# API Sergio
if (Test-Path "apis/sergio/requirements.txt") {
    Write-Host "Instalando dependencias de API Sergio..." -ForegroundColor Yellow
    Set-Location "apis/sergio"
    pip install -r requirements.txt
    Set-Location "../.."
} else {
    Write-Host "Instalando dependencias básicas para API Sergio..." -ForegroundColor Yellow
    pip install fastapi uvicorn sqlalchemy python-dotenv requests jinja2 python-multipart
}

# API Andrea  
if (Test-Path "apis/andrea/requirements.txt") {
    Write-Host "Instalando dependencias de API Andrea..." -ForegroundColor Yellow
    Set-Location "apis/andrea"
    pip install -r requirements.txt
    Set-Location "../.."
} else {
    Write-Host "Instalando dependencias básicas para API Andrea..." -ForegroundColor Yellow
    pip install fastapi uvicorn sqlalchemy python-dotenv requests
}

Write-Host "¡Instalación completada!" -ForegroundColor Green
Write-Host "Ejecuta 'start_all_apis.ps1' para iniciar todos los servicios." -ForegroundColor Cyan
