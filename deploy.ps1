# Despliegue manual a GitHub Pages
# Este script empuja el contenido de la carpeta 'docs' a la rama 'gh-pages'

Write-Host "Iniciando despliegue a GitHub Pages..." -ForegroundColor Cyan

# 1. Verificar si hay cambios sin commitear
if (git status --porcelain) {
    Write-Host "Hay cambios sin guardar. Por favor haz commit primero." -ForegroundColor Yellow
    Write-Host "   Ejemplo: git add . ; git commit -m 'Update docs'"
    exit 1
}

# 2. Empujar carpeta docs
Write-Host "Empujando carpeta 'docs' a la rama 'gh-pages'..." -ForegroundColor Cyan
git subtree push --prefix docs origin gh-pages

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "Subida completada con exito!" -ForegroundColor Green
    Write-Host "--------------------------------------------------------"
    Write-Host "Pasos finales para activar tu sitio:" -ForegroundColor White
    Write-Host "1. Ve a la configuracion del repositorio:" -ForegroundColor White
    Write-Host "   https://github.com/270803ggiztheking-rgb/ms-graph-api-demo/settings/pages" -ForegroundColor Blue
    Write-Host "2. En 'Source', selecciona: Deploy from a branch" -ForegroundColor White
    Write-Host "3. En 'Branch', selecciona: gh-pages / (root)" -ForegroundColor White
    Write-Host "4. Guarda los cambios." -ForegroundColor White
    Write-Host "--------------------------------------------------------"
} else {
    Write-Host ""
    Write-Host "Error al desplegar. Revisa los mensajes de git arriba." -ForegroundColor Red
}
