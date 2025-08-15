# Script para iniciar todas las APIs simultáneamente
Write-Host "Iniciando Panel Central - Hub de APIs" -ForegroundColor Green
Write-Host "===============================================" -ForegroundColor Cyan

# Función para iniciar un proceso en segundo plano
function Start-APIProcess {
    param(
        [string]$WorkingDirectory,
        [string]$Command,
        [string]$APIName,
        [int]$Port
    )
    
    Write-Host "Iniciando $APIName en puerto $Port..." -ForegroundColor Yellow
    $process = Start-Process -FilePath "python" -ArgumentList $Command -WorkingDirectory $WorkingDirectory -WindowStyle Minimized -PassThru
    Write-Host "$APIName iniciada con PID: $($process.Id)" -ForegroundColor Green
    return $process
}

# Iniciar API Sergio (puerto 8001)
$sergioProcess = Start-APIProcess -WorkingDirectory "apis/sergio" -Command "-m uvicorn main:app --reload --port 8001" -APIName "API Sergio (Partidos)" -Port 8001
Start-Sleep -Seconds 3

# Iniciar API Andrea (puerto 8002)  
$andreaProcess = Start-APIProcess -WorkingDirectory "apis/andrea" -Command "-m uvicorn main:app --reload --port 8002" -APIName "API Andrea (Eventos)" -Port 8002
Start-Sleep -Seconds 3

# Iniciar Panel Central (puerto 8000)
$centralProcess = Start-APIProcess -WorkingDirectory "panel_central/backend" -Command "-m uvicorn main:app --reload --port 8000" -APIName "Panel Central" -Port 8000
Start-Sleep -Seconds 5

Write-Host "`n===============================================" -ForegroundColor Cyan
Write-Host "¡Todos los servicios están ejecutándose!" -ForegroundColor Green
Write-Host "`nURLs de acceso:" -ForegroundColor White
Write-Host "• Panel Central (Principal): http://localhost:8000" -ForegroundColor Cyan
Write-Host "• API Sergio (Partidos): http://localhost:8001" -ForegroundColor Yellow
Write-Host "• API Andrea (Eventos): http://localhost:8002" -ForegroundColor Yellow
Write-Host "`nDocumentación API:" -ForegroundColor White
Write-Host "• Panel Central Docs: http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host "• API Sergio Docs: http://localhost:8001/docs" -ForegroundColor Yellow
Write-Host "• API Andrea Docs: http://localhost:8002/docs" -ForegroundColor Yellow

Write-Host "`nPresiona Ctrl+C para detener todos los servicios" -ForegroundColor Red
Write-Host "===============================================" -ForegroundColor Cyan

# Mantener el script ejecutándose y manejar la interrupción
try {
    while ($true) {
        Start-Sleep -Seconds 10
        
        # Verificar si los procesos siguen ejecutándose
        if ($sergioProcess.HasExited) {
            Write-Host "API Sergio se ha detenido" -ForegroundColor Red
        }
        if ($andreaProcess.HasExited) {
            Write-Host "API Andrea se ha detenido" -ForegroundColor Red
        }
        if ($centralProcess.HasExited) {
            Write-Host "Panel Central se ha detenido" -ForegroundColor Red
        }
    }
}
catch {
    Write-Host "`nDeteniendo todos los servicios..." -ForegroundColor Yellow
    
    # Terminar procesos si siguen ejecutándose
    if (!$sergioProcess.HasExited) {
        $sergioProcess.Kill()
        Write-Host "API Sergio detenida" -ForegroundColor Green
    }
    if (!$andreaProcess.HasExited) {
        $andreaProcess.Kill()
        Write-Host "API Andrea detenida" -ForegroundColor Green
    }
    if (!$centralProcess.HasExited) {
        $centralProcess.Kill()
        Write-Host "Panel Central detenido" -ForegroundColor Green
    }
    
    Write-Host "Todos los servicios han sido detenidos." -ForegroundColor Green
}
