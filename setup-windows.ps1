<#
setup-windows.ps1

Creates a Python virtual environment, installs backend requirements, copies .env.example -> .env,
installs frontend dependencies, and optionally opens two PowerShell windows to run backend and frontend.

Usage:
  .\setup-windows.ps1          # run setup and start servers in new windows
  .\setup-windows.ps1 -SkipStart  # run setup only
#>

[CmdletBinding()]
param(
    [switch]$SkipStart
)

Set-StrictMode -Version Latest

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Write-Host "Working in project: $scriptDir"
Set-Location $scriptDir

# 1) Create venv if not exists
if (-not (Test-Path -Path .venv)) {
    Write-Host "Creating virtual environment (.venv)..."
    python -m venv .venv
} else {
    Write-Host ".venv already exists - skipping creation"
}

$py = Join-Path $scriptDir ".venv\Scripts\python.exe"
if (-not (Test-Path $py)) {
    Write-Host "ERROR: Python executable not found in .venv. Ensure Python 3.11 is installed and on PATH." -ForegroundColor Red
    exit 1
}

Write-Host "Upgrading pip and installing backend requirements..."
Start-Process -FilePath $py -ArgumentList '-m','pip','install','--upgrade','pip' -Wait
Start-Process -FilePath $py -ArgumentList '-m','pip','install','-r','backend/requirements.txt' -Wait

# 2) Create .env from example if missing
if (-not (Test-Path -Path .env)) {
    if (Test-Path -Path .env.example) {
        Copy-Item -Path .env.example -Destination .env
        Write-Host "Created .env from .env.example — please edit it to add secrets (OPENWEATHER_API_KEY)."
    } else {
        Write-Host "No .env.example found. Create a .env file with required env vars." -ForegroundColor Yellow
    }
} else {
    Write-Host ".env already exists - not overwriting."
}

# 3) Install frontend deps
if (Test-Path -Path "front_end/package.json") {
    Push-Location front_end
    Write-Host "Installing frontend dependencies (npm ci)..."
    npm ci
    Pop-Location
} else {
    Write-Host "No frontend detected at front_end/ — skipping npm install." -ForegroundColor Yellow
}

Write-Host "Setup complete."

if ($SkipStart) {
    Write-Host "Skipping server start as requested. To start servers run the commands in README.md or run this script without -SkipStart."
    exit 0
}

# 4) Start backend and frontend each in a new PowerShell window
Write-Host "Starting backend and frontend in two new PowerShell windows..."

$backendCmd = "cd `"$scriptDir\backend`"; .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
$frontendCmd = "cd `"$scriptDir\front_end`"; $env:PORT=3000; npm run dev"

# Start backend window
Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command","$backendCmd"

# Start frontend window (if exists)
if (Test-Path -Path "front_end/package.json") {
    Start-Process -FilePath powershell -ArgumentList "-NoExit","-Command","$frontendCmd"
} else {
    Write-Host "Frontend not found — not starting frontend." -ForegroundColor Yellow
}

Write-Host "Done. Backend: http://localhost:8000   Frontend: URL printed by Vite (http://localhost:3000 if used)."
