Write-Host "Configurando ambiente para testes..." -ForegroundColor Green
$env:PYTHONPATH = $PWD.Path
Write-Host "PYTHONPATH configurado para: $env:PYTHONPATH" -ForegroundColor Cyan
Write-Host ""
Write-Host "Executando testes..." -ForegroundColor Green
pytest -v
Write-Host ""
Write-Host "Pressione qualquer tecla para continuar..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown") 