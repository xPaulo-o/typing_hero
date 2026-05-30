$ErrorActionPreference = "Stop"

$appName = "TypingHero"
$entryPoint = "main.py"

Write-Host "Checking Python dependencies..."
python -m pip install -r requirements.txt

Write-Host "Checking PyInstaller..."
python -m pip install pyinstaller

Write-Host "Cleaning previous build output..."
if (Test-Path "build") {
    Remove-Item "build" -Recurse -Force
}
if (Test-Path "dist") {
    try {
        Remove-Item "dist" -Recurse -Force
    }
    catch {
        Write-Host ""
        Write-Host "Could not remove dist. Close dist\$appName.exe if it is open, then run this script again."
        throw
    }
}
if (Test-Path "$appName.spec") {
    Remove-Item "$appName.spec" -Force
}

Write-Host "Building $appName.exe..."
python -m PyInstaller `
    --onefile `
    --windowed `
    --name $appName `
    --paths "Components" `
    --hidden-import "typing_hero" `
    --hidden-import "settings" `
    --hidden-import "fases" `
    --hidden-import "gamedata" `
    --hidden-import "performance" `
    --add-data "img;img" `
    --add-data "sounds;sounds" `
    --add-data "videos;videos" `
    --add-data "data;data" `
    $entryPoint

Write-Host ""
Write-Host "Build finished: dist\$appName.exe"
